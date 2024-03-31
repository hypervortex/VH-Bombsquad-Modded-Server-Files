"""Avalancha Game."""

# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import random
from bastd.actor.onscreentimer import OnScreenTimer
from bastd.actor.spazbot import BrawlerBot, SpazBotSet

if TYPE_CHECKING:
    from typing import Any, Sequence, Optional, List, Dict, Type, Type


def ba_get_api_version():
    return 6

def ba_get_levels():
	return [ba._level.Level(
            '${GAME}',
			gametype=AvalanchaGame,
			settings={},
			preview_texture_name='snowRampMapPreview')]

class InmortalBot(BrawlerBot):
    character = 'Agent Johnson'
    color = (0.1,0.35,0.1)
    highlight = (1,0.15,0.15)
    default_boxing_gloves = True
    charge_speed_min = 0.3
    charge_speed_max = 0.5

    def __init__(self) -> None:
        super().__init__()
        self.hitpoints = -1

    def _do_teleport(self) -> None:
        self.handlemessage(
            ba.StandMessage(position=(-0.1, 6.4, 1.8)))
        ba.playsound(ba.getsound('shieldHit'))

    def handlemessage(self, msg: Any) -> Any:
        # pylint: disable=too-many-branches
        assert not self.expired
        if isinstance(msg, ba.OutOfBoundsMessage):
            self._do_teleport()
        else:
            return super().handlemessage(msg)

class Snow(ba.Actor):
    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 velocity: Sequence[float] = (0.0, 0.0, 0.0),
                 snow_type: str = 'normal'):
        super().__init__()
        self.bomb_type = snow_type
        if self.bomb_type == 'snow':
            self.node = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'body': 'sphere',
                                       'body_scale': 2.0,
                                       'model': ba.getmodel('snow'),
                                       'shadow_size': 0.2,
                                       'color_texture':
                                            ba.gettexture('powerupIceBombs'),
                                       'reflection': 'soft',
                                       'reflection_scale': [1.0]
                                   })
        elif self.bomb_type == 'snow_big':
            self.node = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'body': 'sphere',
                                       'body_scale': 3.5,
                                       'model': ba.getmodel('snow'),
                                       'shadow_size': 0.2,
                                       'color_texture':
                                            ba.gettexture('powerupIceBombs'),
                                       'reflection': 'soft',
                                       'reflection_scale': [1.0]
                                   })
        ba.animate(self.node, 'model_scale',
            {0:0, 0.2:1.4, 0.26:1.2} if self.bomb_type == 'snow'
            else {0:0, 0.2:3.2, 0.26:3})

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.OutOfBoundsMessage):
            self.node.delete()

class Player(ba.Player['Team']):
    """Our player type for this game."""

    def __init__(self) -> None:
        super().__init__()
        self.death_time: Optional[float] = None

class Team(ba.Team[Player]):
    """Our team type for this game."""

# ba_meta export game
class AvalanchaGame(ba.TeamGameActivity[Player, Team]):
    """A game type based on acquiring kills."""

    name = 'Avalancha'
    description = 'Dodge the falling bombs.'

    # Print messages when players die since it matters here.
    announce_player_deaths = True

    @classmethod
    def get_available_settings(
            cls, sessiontype: Type[ba.Session]) -> List[ba.Setting]:
        settings = [
            ba.BoolSetting('Epic Mode', default=False),
        ]
        return settings

    @classmethod
    def supports_session_type(cls, sessiontype: Type[ba.Session]) -> bool:
        return (issubclass(sessiontype, ba.DualTeamSession)
                or issubclass(sessiontype, ba.FreeForAllSession)
                or issubclass(sessiontype, ba.CoopSession))

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[ba.Session]) -> List[str]:
        return ['Rampa de Nieve']

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._epic_mode = bool(settings['Epic Mode'])
        self._last_player_death_time: Optional[float] = None
        self._snow_time = 2.0
        self._timer: Optional[OnScreenTimer] = None

        # Base class overrides.
        self.slow_motion = self._epic_mode
        self.default_music = (ba.MusicType.EPIC if self._epic_mode else
                              ba.MusicType.SURVIVAL)

    def on_begin(self) -> None:
        super().on_begin()
        self._prop_player()

        delay = 5.0 if len(self.players) > 2 else 2.5
        if self._epic_mode:
            delay *= 0.25
        ba.timer(delay, self._decrement_snow_time, repeat=True)

        # Kick off the first wave in a few seconds.
        delay = 3.0
        if self._epic_mode:
            delay *= 0.25
        ba.timer(delay, self._set_snow_timer)

        self._timer = OnScreenTimer()
        self._timer.start()

        # Check for immediate end (if we've only got 1 player, etc).
        ba.timer(5.0, self._check_end_game)

        self._bots = SpazBotSet()

        ba.timer(2.0, ba.Call(self._bots.spawn_bot,
            InmortalBot, pos=(-0.14, 6.45, 1.78), spawn_time=3.0))
        ba.timer(50.0, ba.Call(self._bots.spawn_bot,
            InmortalBot, pos=(-5.14, 6.45, 1.78), spawn_time=3.0))
        ba.timer(50.0, ba.Call(self._bots.spawn_bot,
            InmortalBot, pos=(5.14, 6.45, 1.78), spawn_time=3.0))

    def _prop_player(self) -> None:
        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'position': (-0.14, 10.45, -10.78),
                'model': ba.getmodel('none'),
                'model_scale': 0.0,
                'body': 'sphere',
                'body_scale': 0.0,
                'density': 999999999999999999999,
                'damping': 999999999999999999999,
                'gravity_scale': 0,
                'is_area_of_interest': True,
                'color_texture': ba.gettexture('black')
            })

    def on_player_join(self, player: Player) -> None:
        # Don't allow joining after we start
        # (would enable leave/rejoin tomfoolery).
        if self.has_begun():
            ba.screenmessage(
                ba.Lstr(resource='playerDelayedJoinText',
                        subs=[('${PLAYER}', player.getname(full=True))]),
                color=(0, 1, 0),
            )
            # For score purposes, mark them as having died right as the
            # game started.
            assert self._timer is not None
            player.death_time = self._timer.getstarttime()
            return
        self.spawn_player(player)

    def on_player_leave(self, player: Player) -> None:
        # Augment default behavior.
        super().on_player_leave(player)

        # A departing player may trigger game-over.
        self._check_end_game()

    def spawn_player(self, player: Player) -> ba.Actor:
        spaz = self.spawn_player_spaz(player)

        # Let's reconnect this player's controls to this
        # spaz but *without* the ability to attack or pick stuff up.
        spaz.connect_controls_to_player(enable_punch=False,
                                        enable_bomb=False,
                                        enable_pickup=False)

        mat = self.map.preloaddata['collide_with_wall_material']
        assert isinstance(spaz.node.materials, tuple)
        assert isinstance(spaz.node.roller_materials, tuple)
        spaz.node.materials += (mat, )
        spaz.node.roller_materials += (mat, )

        # Also lets have them make some noise when they die.
        spaz.play_big_death_sound = True
        return spaz

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.PlayerDiedMessage):

            # Augment standard behavior.
            super().handlemessage(msg)

            curtime = ba.time()

            # Record the player's moment of death.
            # assert isinstance(msg.spaz.player
            msg.getplayer(Player).death_time = curtime

            # In co-op mode, end the game the instant everyone dies
            # (more accurate looking).
            # In teams/ffa, allow a one-second fudge-factor so we can
            # get more draws if players die basically at the same time.
            if isinstance(self.session, ba.CoopSession):
                # Teams will still show up if we check now.. check in
                # the next cycle.
                ba.pushcall(self._check_end_game)

                # Also record this for a final setting of the clock.
                self._last_player_death_time = curtime
            else:
                ba.timer(1.0, self._check_end_game)

        else:
            # Default handler:
            return super().handlemessage(msg)
        return None

    def _check_end_game(self) -> None:
        living_team_count = 0
        for team in self.teams:
            for player in team.players:
                if player.is_alive():
                    living_team_count += 1
                    break

        # In co-op, we go till everyone is dead.. otherwise we go
        # until one team remains.
        if isinstance(self.session, ba.CoopSession):
            if living_team_count <= 0:
                self.end_game()
        else:
            if living_team_count <= 1:
                self.end_game()

    def _set_snow_timer(self) -> None:
        ba.timer((1.0 + 0.2 * random.random()) * self._snow_time,
                 self._drop_snow_cluster)

    def _drop_snow_cluster(self) -> None:

        # Random note: code like this is a handy way to plot out extents
        # and debug things.
        loc_test = False
        if loc_test:
            ba.newnode('locator', attrs={'position': (0.0, 20.0, -20.0)})

        # Drop several bombs in series.
        delay = 0.0
        for _i in range(random.randrange(1, 3)):
            # Drop them somewhere within our bounds with velocity pointing
            # toward the opposite side.
            pos = (-2.3 + 5.3 * random.random(), 21,
                   -15.5 + 2.1 * random.random())
            dropdir = (-1.0 if pos[0] > 0 else 1.0)
            vel = ((-5.0 + random.random() * 30.0) * dropdir, -4.0, 0)
            st = random.choice(['snow', 'snow', 'snow', 'snow_big'])
            ba.timer(delay, ba.Call(self._drop_snow, pos, vel, st))
            delay += 0.1
        self._set_snow_timer()

    def _drop_snow(self, position: Sequence[float],
                   velocity: Sequence[float],
                   snow_type: str) -> None:
        Snow(position=position,
             velocity=velocity,
             snow_type=snow_type).autoretain()

    def _decrement_snow_time(self) -> None:
        self._snow_time = max(0.01, self._snow_time * 0.9)

    def end_game(self) -> None:
        cur_time = ba.time()
        assert self._timer is not None
        start_time = self._timer.getstarttime()

        # Mark death-time as now for any still-living players
        # and award players points for how long they lasted.
        # (these per-player scores are only meaningful in team-games)
        for team in self.teams:
            for player in team.players:
                survived = False

                # Throw an extra fudge factor in so teams that
                # didn't die come out ahead of teams that did.
                if player.death_time is None:
                    survived = True
                    player.death_time = cur_time + 1

                # Award a per-player score depending on how many seconds
                # they lasted (per-player scores only affect teams mode;
                # everywhere else just looks at the per-team score).
                score = int(player.death_time - self._timer.getstarttime())
                if survived:
                    score += 50  # A bit extra for survivors.
                self.stats.player_scored(player, score, screenmessage=False)

        # Stop updating our time text, and set the final time to match
        # exactly when our last guy died.
        self._timer.stop(endtime=self._last_player_death_time)

        # Ok now calc game results: set a score for each team and then tell
        # the game to end.
        results = ba.GameResults()

        # Remember that 'free-for-all' mode is simply a special form
        # of 'teams' mode where each player gets their own team, so we can
        # just always deal in teams and have all cases covered.
        for team in self.teams:

            # Set the team score to the max time survived by any player on
            # that team.
            longest_life = 0.0
            for player in team.players:
                assert player.death_time is not None
                longest_life = max(longest_life,
                                   player.death_time - start_time)

            # Submit the score value in milliseconds.
            results.set_team_score(team, int(1000.0 * longest_life))

        self.end(results=results)
