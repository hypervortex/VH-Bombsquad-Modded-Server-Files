# ba_meta require api 7


#==============================================================================#             
#     
#     version v1.0 (test, 2bugs)
#     Create by Unknown_#7004 
#     Github https://github.com/uwu-user
#
#==============================================================================#             


from __future__ import annotations
from typing import TYPE_CHECKING, cast

import ba
import _ba
import math
import random
from bastd.actor.bomb import Bomb
from bastd.actor.onscreentimer import OnScreenTimer
from bastd.actor.powerupbox import PowerupBox, PowerupBoxFactory

if TYPE_CHECKING:
    from typing import Any, Sequence, Callable, List, Dict, Tuple, Optional, Union

#==============================================================================#             

_version = "1.0"
_by = "Unknown_#7004"

#==============================================================================#             

# custom end time
custom_time = 10 # 10s

# custom powerup drop time
custom_speed = 1.0

#==============================================================================#             


class Player(ba.Player['Team']):
    """Our player type for this game."""

    def __init__(self) -> None:
        super().__init__()
        self.death_time: Optional[float] = None


class Team(ba.Team[Player]):
    """Our team type for this game."""


#==============================================================================#             


# ba_meta export game
class PowerUpShowerGame(ba.TeamGameActivity[Player, Team]):
    """Minigame involving dodging falling bombs."""

    name = 'PowerUp Shower'
    description = 'Becareful with the curse powerups.'
    scoreconfig = ba.ScoreConfig(label='Survived',
                                 scoretype=ba.ScoreType.MILLISECONDS,
                                 version='B')

    # Print messages when players die (since its meaningful in this game).
    announce_player_deaths = True

    @classmethod
    def get_available_settings(
            cls, sessiontype: Type[ba.Session]) -> List[ba.Setting]:
        settings = [
            ba.IntChoiceSetting(
                'Time Limit',
                choices=[ # memes
                    ('No timer', 0),
                    ('1 Minute', 60),
                    ('2 Minutes', 120),
                    ('5 Minutes', 300),
                    ('10 Minutes', 600),
                    ('15 Minutes', 900),
                    ('30 Minutes', 1800),
                    ('60 Minutes', 3600),
                    ('2 Hours', 7200),
                    ('3 Hours', 10800),
                    ('4 Hours', 14400),
                    ('5 Hours', 18000),
                    ('6 Hours', 21600),
                    ('7 Hours', 25200),
                    ('8 Hours', 28800),
                    ('9 Hours', 32400),
                    ('10 Hours', 36000),
                    ('11 Hours', 39600),
                    ('12 Hours', 43200),
                    ('13 Hours', 46800),
                    ('14 Hours', 50400),
                    ('15 Hours', 54000),
                    ('16 Hours', 57600),
                    ('17 Hours', 61200),
                    ('18 Hours', 64800),
                    ('19 Hours', 68400),
                    ('20 Hours', 72000),
                    ('21 Hours', 75600),
                    ('22 Hours', 79200),
                    ('23 Hours', 82800),
                    ('1 days', 86400),
                    ('2 days', 172800),
                    ('3 days', 259200),
                    ('4 days', 345600),
                    ('5 days', 432000),
                    ('6 days', 518400),
                    ('7 days', 604800),
                    ('8 days', 691200),
                    ('9 days', 777600),
                    ('10 days', 864000),
                    ('11 days', 950400),
                    ('custom', custom_time)
                ],
                default=300,
            ),
            ba.FloatChoiceSetting(
                'Respawn Times',
                choices=[
                    ('very fast', 0.001),
                    ('Shorter', 0.25),
                    ('Short', 0.5),
                    ('Normal', 1.0),
                    ('Long', 2.0),
                    ('Longer', 4.0)
                ],
                default=1.0,
            ),
            ba.FloatChoiceSetting(
                'Respawn PowerUp Times',
                choices=[
                    ('Fast', 0.10),
                    ('Normal', 0.35),
                    ('Long', 0.7),
                    ('Longer', 1.0),
                    ('custom', custom_speed)
                ],
                default=0.3
            ),
            ba.BoolSetting('Timer on Screen', default=False),
            ba.BoolSetting('PowerUp Expire', default=False),
            ba.BoolSetting('Epic Mode', default=False),
            ba.BoolSetting('spaz » enable punch', default=False),
            ba.BoolSetting('spaz » enable bomb', default=False),
            ba.BoolSetting('spaz » enable pickup', default=False),
            ba.BoolSetting('PowerUp » shield', default=False),
            ba.BoolSetting('PowerUp » health', default=False),
            ba.BoolSetting('PowerUp » curse', default=False),
            ba.BoolSetting('PowerUp » Triple bombs', default=False),
            ba.BoolSetting('PowerUp » ice bombs', default=False),
            ba.BoolSetting('PowerUp » impact bombs', default=False),
            ba.BoolSetting('PowerUp » land mines', default=False),
            ba.BoolSetting('PowerUp » sticky bombs', default=False),
            ba.BoolSetting('PowerUp » random', default=True)
        ]
        return settings
        
    # We support teams, free-for-all, and co-op sessions.
    @classmethod
    def supports_session_type(cls, sessiontype: Type[ba.Session]) -> bool:
        return (issubclass(sessiontype, ba.DualTeamSession)
                or issubclass(sessiontype, ba.FreeForAllSession)
                or issubclass(sessiontype, ba.CoopSession))

    def __init__(self, settings: dict):
        super().__init__(settings)

        self._epic_mode = settings.get('Epic Mode', False)
        self._punch_mode = settings.get('spaz » enable punch', False)
        self._bomb_mode = settings.get('spaz » enable bomb', False)
        self._pickup_mode = settings.get('spaz » enable pickup', False)
        self._powerup_timer = settings.get('Respawn PowerUp Times', False)
        self.expire_type = settings.get('PowerUp Expire', True)
        self._time_limit = float(settings['Time Limit'])
        self._timer_type = float(settings['Timer on Screen'])
        self._powerup_shield = settings.get('PowerUp » shield', False)
        self._powerup_health = settings.get('PowerUp » health', False)
        self._powerup_curse = settings.get('PowerUp » curse', False)
        self._powerup_triple_bombs = settings.get('PowerUp » Triple bombs', False)
        self._powerup_ice_bombs = settings.get('PowerUp » ice bombs', False)
        self._powerup_impact_bombs = settings.get('PowerUp » impact bombs', False)
        self._powerup_land_mines = settings.get('PowerUp » land mines', False)
        self._powerup_sticky_bombs = settings.get('PowerUp » sticky bombs', False)
        self._powerup_random = settings.get('PowerUp » random', True)
     
        self._last_player_death_time: Optional[float] = None
        self._meteor_time = 2.0
        self._timer: Optional[OnScreenTimer] = None
        
        # Some base class overrides:
        self.default_music = (ba.MusicType.EPIC
                              if self._epic_mode else ba.MusicType.SURVIVAL)
        if self._epic_mode:
            self.slow_motion = True

    def on_begin(self) -> None:
        super().on_begin()
        self.setup_standard_time_limit(self._time_limit)
        
        # Drop a wave every few seconds.. and every so often drop the time
        # between waves ..lets have things increase faster if we have fewer
        # players.
        delay = 5.0 if len(self.players) > 2 else 2.5
        if self._epic_mode:
            delay *= 0.25
        ba.timer(delay, self._decrement_meteor_time, repeat=True)

        # Kick off the first wave in a few seconds.
        delay = 3.0
        if self._epic_mode:
            delay *= 0.25
        ba.timer(delay, self._set_meteor_timer)

        if self._timer_type: 
           self._timer = OnScreenTimer()
           self._timer.start()
        else:
           self._timer = None
          
        if not self._time_limit == 0:
           ba.timer(self._time_limit, self._check_end_game)
        else: pass

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

    # overriding the default character spawning..
    def spawn_player(self, player: Player) -> ba.Actor:
        spaz = self.spawn_player_spaz(player)

        # Let's reconnect this player's controls to this
        # spaz but *without* the ability to attack or pick stuff up.
        spaz.connect_controls_to_player(enable_punch=self._punch_mode,
                                        enable_bomb=self._bomb_mode,
                                        enable_pickup=self._pickup_mode)

        # Also lets have them make some noise when they die.
        spaz.play_big_death_sound = True
        return spaz

    # Various high-level game events come through this method.
    def handlemessage(self, msg: Any) -> Any: # Respawn
        if isinstance(msg, ba.PlayerDiedMessage):
            super().handlemessage(msg)

            player = msg.getplayer(Player)
            self.respawn_player(player)
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

    def _set_meteor_timer(self) -> None:
        ba.timer(self._powerup_timer, self._drop_powerup_cluster)

    def _drop_powerup_cluster(self) -> None:

        # Random note: code like this is a handy way to plot out extents
        # and debug things.
        loc_test = False
        if loc_test:
            ba.newnode('locator', attrs={'position': (8, 6, -5.5)})
            ba.newnode('locator', attrs={'position': (8, 6, -2.3)})
            ba.newnode('locator', attrs={'position': (-7.3, 6, -5.5)})
            ba.newnode('locator', attrs={'position': (-7.3, 6, -2.3)})

        # Drop several bombs in series.
        delay = 0.0
        for _i in range(random.randrange(1, 3)):
            # Drop them somewhere within our bounds with velocity pointing
            # toward the opposite side.
            pos = (-7.3 + 15.3 * random.random(), 11, -5.5 + 2.1 * random.random()*2)
            dropdir = (-1.0 if pos[0] > 0 else 1.0)
            vel = ((-5.0 + random.random() * 30.0) * dropdir, -4.0, 0)
            if self._powerup_shield or self._powerup_health or self._powerup_curse or self._powerup_triple_bombs or self._powerup_ice_bombs or self._powerup_impact_bombs or self._powerup_land_mines or self._powerup_sticky_bombs or self._powerup_random:
               if not self._powerup_random:
                   if self._powerup_shield: ba.timer(delay /random.random(), ba.Call(self._drop_powerup, pos, vel, "shield"))
                   if self._powerup_health: ba.timer(delay / random.random(), ba.Call(self._drop_powerup, pos, vel, "health"))
                   if self._powerup_curse: ba.timer(delay / random.random(), ba.Call(self._drop_powerup, pos, vel, "curse"))
                   if self._powerup_triple_bombs: ba.timer(delay / random.random(), ba.Call(self._drop_powerup, pos, vel, "triple_bombs"))
                   if self._powerup_ice_bombs: ba.timer(delay /  random.random(), ba.Call(self._drop_powerup, pos, vel, "ice_bombs"))
                   if self._powerup_impact_bombs: ba.timer(delay / random.random(), ba.Call(self._drop_powerup, pos, vel, "impact_bombs"))
                   if self._powerup_land_mines: ba.timer(delay / random.random(), ba.Call(self._drop_powerup, pos, vel, "land_mines"))
                   if self._powerup_sticky_bombs: ba.timer(delay / random.random(), ba.Call(self._drop_powerup, pos, vel, "sticky_bombs"))
               else:
                   ba.timer(delay, ba.Call(self._drop_powerup, pos, vel, PowerupBoxFactory().get_random_powerup_type()))
            else: pass
 
            delay += 0.5
        self._set_meteor_timer()

    def _drop_powerup(self, position: Sequence[float], velocity: Sequence[float], PowerupType) -> None:    
        PowerupBox(position=position,poweruptype=PowerupType,expire=self.expire_type).autoretain()
        
    def _decrement_meteor_time(self) -> None:
        self._meteor_time = max(0.01, self._meteor_time * 0.9)

    def end_game(self) -> None:
        cur_time = 0
        assert self._timer is not None
        start_time = self._timer.getstarttime()

        # Mark death-time as now for any still-living players
        # and award players points for how long they lasted.
        # (these per-player scores are only meaningful in team-games)
        for team in self.teams:
            for player in team.players:
                survived = True

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
                    score += 69  # A bit extra for survivors. :p
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
