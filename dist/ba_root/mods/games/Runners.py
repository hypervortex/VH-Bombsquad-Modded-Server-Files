# Made by: Froshlee14
# Ported by: Freaku / @[Just] Freak#4999





from __future__ import annotations
from typing import TYPE_CHECKING
import ba, random
from bastd.actor import bomb, spazbot, powerupbox, bomb
from bastd.gameutils import SharedObjects
from bastd.actor.onscreentimer import OnScreenTimer
if TYPE_CHECKING:
    from typing import Any, Sequence, Union, Optional, List, Dict, Type, Literal



## MoreMinigames.py support ##
def ba_get_api_version():
    return 6
def ba_get_levels():
    return [ba._level.Level('Runners',gametype=RunnersGame, settings={}, preview_texture_name = 'achievementGotTheMoves')]
## MoreMinigames.py support ##



class SpookyBot(spazbot.BrawlerBot):
    character = 'Bones'
    color = (1,1,1)

class Player(ba.Player['Team']):
    """Our player type for this game."""
    def __init__(self) -> None:
        super().__init__()
        self.death_time: Optional[float] = None
class Team(ba.Team[Player]):
    """Our team type for this game."""


# ba_meta require api 7
# ba_meta export game
class RunnersGame(ba.TeamGameActivity[Player, Team]):
    name = 'Runners'
    description = 'Run for your Life!'
    available_settings = [ba.BoolSetting('Epic Mode', default=False)]
    scoreconfig = ba.ScoreConfig(label='Survived',
                                 scoretype=ba.ScoreType.MILLISECONDS,
                                 version='B')

    # Print messages when players die (since its meaningful in this game).
    announce_player_deaths = True

    # we're currently hard-coded for one map..
    @classmethod
    def get_supported_maps(cls, sessiontype: Type[ba.Session]) -> List[str]:
        return ['Dak']

    # We support teams, free-for-all, and co-op sessions.
    @classmethod
    def supports_session_type(cls, sessiontype: Type[ba.Session]) -> bool:
        return (issubclass(sessiontype, ba.DualTeamSession)
                or issubclass(sessiontype, ba.FreeForAllSession)
                or issubclass(sessiontype, ba.CoopSession))

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._epic_mode = settings.get('Epic Mode', False)
        self._last_player_death_time: Optional[float] = None
        self._timer: Optional[OnScreenTimer] = None
        self._time2Object = 1 if self._epic_mode else 1.5

        # Some base class overrides:
        self.default_music = (ba.MusicType.EPIC
                              if self._epic_mode else ba.MusicType.SURVIVAL)
        if self._epic_mode:
            self.slow_motion = True


    def on_begin(self) -> None:
        super().on_begin()

        self._timer = OnScreenTimer()
        self._timer.start()

        # Check for immediate end (if we've only got 1 player, etc).
        ba.timer(5.0, self._check_end_game)
        self._bots = spazbot.SpazBotSet()
        for i in range(6+len(self.players)):
            self.addBot()

        self.obstacleTime = 5
        ba.timer(3,self.start)

    def start(self):
        self._obsTimer = ba.timer(self._time2Object,self.doObstacle,repeat=True)
        self._move = ba.timer(0.8,ba.WeakCall(self.movePlayers),repeat=True)
        self._fast = ba.timer(5,ba.WeakCall(self.faster),repeat=True)

    def faster(self):
        if self.obstacleTime > 1:
            self.obstacleTime -= 0.1

    def addBot(self):
        ba.timer(1, ba.Call(self._bots.spawn_bot, SpookyBot, pos=(random.randint(-4,4),5,-7.3), spawn_time=0))

    def doObstacle(self):
        for i in range(random.randrange(4,8)):
            type = random.choice(['tnt','land_mine','land_mine','land_mine','powerup','land_mine','land_mine','land_mine','tnt','tnt','land_mine'])
            pos = (random.randrange(-5,5),4.8 if type != 'land_mine' else 4.6,8)
            if type == 'powerup':
                b = powerupbox.PowerupBox(position=pos,poweruptype=random.choice(['health','shield'])).autoretain()
                b.node.model_scale = 0.6
            else:
                b = bomb.Bomb(position=pos,velocity=(0,0,0),bomb_type = type, bomb_scale = 0.6).autoretain()
                if type == 'land_mine': b.arm()
            pos = b.node.position
            ba.animate_array(b.node,'position',3,{0:b.node.position,self.obstacleTime:(pos[0],pos[1],pos[2]-16)})

    def movePlayers(self):
        for p in self.players:
            if p.is_alive():
                p.actor.node.move_up_down = -10

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
        spaz = self.spawn_player_spaz(player, self.map.defs.points['spawn'])

        # Let's reconnect this player's controls to this
        # spaz but *without* the ability to attack or pick stuff up.
        spaz.connect_controls_to_player(enable_punch=False,
                                        enable_bomb=False,
                                        enable_pickup=False)

        # Also lets have them make some noise when they die.
        spaz.play_big_death_sound = True
        return spaz

    # Various high-level game events come through this method.
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
        elif isinstance(msg, spazbot.SpazBotDiedMessage):
            self.addBot()
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





class dakDefs():
    points = {}
    boxes = {}
    points['spawn'] = (0,5,0) + (0, 0, 0) + (10,0,0.5)
    boxes['area_of_interest_bounds'] = (0,-1,-5) + (0, 0, 0) + (0, 0, 0)
    boxes['map_bounds'] = (0,5,0) + (0, 0, 0) + (10,10,16)

class dakMap(ba.Map):
    defs = dakDefs()
    name = 'Dak'

    @classmethod
    def get_play_types(cls) -> List[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'achievementGotTheMoves'

    @classmethod
    def on_preload(cls) -> Any:
        data: Dict[str, Any] = {
            'tex': ba.gettexture('white'),
            'bgmodel': ba.getmodel('thePadBG')
        }
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self._playMaterial = ba.Material()
        self._playMaterial.add_actions(
            conditions=("they_have_material",shared.player_material),
            actions=(("modify_part_collision","collide",True),("modify_part_collision","physical",True)))
        self._bombMaterial = ba.Material()
        self._bombMaterial.add_actions(
            conditions=("they_have_material",bomb.BombFactory.get().bomb_material),
            actions=(("modify_part_collision","collide",True),("modify_part_collision","physical",True)))
        self.ground = ba.newnode('region', attrs={'position':(0,4,0),'scale':(10,1,20),'type': 'box',
                                              'materials':(self._playMaterial,self._bombMaterial,shared.footing_material)})
        self.playWall = ba.newnode('region', attrs={'position':(0,4,1.5),'scale':(10,10,0.5),'type': 'box',
                                              'materials':(self._playMaterial,shared.footing_material)})
        self.botWall = ba.newnode('region', attrs={'position':(0,4,-1),'scale':(10,10,0.25),'type': 'box',
                                              'materials':(self._playMaterial,shared.footing_material)})
        self.rightWall = ba.newnode('region', attrs={'position':(4,4,0),'scale':(0.5,10,10),'type': 'box',
                                              'materials':(self._playMaterial,shared.footing_material)})
        self.leftWall = ba.newnode('region', attrs={'position':(-4,4,0),'scale':(0.5,10,10),'type': 'box',
                                              'materials':(self._playMaterial,shared.footing_material)})
        self.bg = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['tex']
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.3, 1.2, 1.0)
        gnode.ambient_color = (1.3, 1.2, 1.0)
        gnode.vignette_outer = (0.57, 0.57, 0.57)
        gnode.vignette_inner = (0.9, 0.9, 0.9)
        gnode.vr_camera_offset = (0, -0.8, -1.1)
        gnode.vr_near_clip = 0.5







ba._map.register_map(dakMap)