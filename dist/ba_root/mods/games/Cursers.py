
# By itsre3 (:
# Just testing my abilities
# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING
import ba
import _ba
import random
from bastd.actor.spazfactory import SpazFactory
from bastd.gameutils import SharedObjects
from bastd.actor.playerspaz import PlayerSpaz
from bastd.actor.scoreboard import Scoreboard

if TYPE_CHECKING:
    from typing import Any, Union, Sequence, Optional


class WwFactory(object):
    def __init__(self):
        self.last_shoot_time = 0
        shared = SharedObjects.get()
        self.ball_material = ba.Material()
        self.ball_material.add_actions(conditions = ((("we_are_younger_than", 5), "or", ("they_are_younger_than", 50)), "and", ("they_have_material", shared.object_material)), actions = ("modify_node_collision", 'collide', False))
        self.ball_material.add_actions(
            conditions=('they_have_material', shared.pickup_material),
            actions=('modify_part_collision', 'use_node_collide', False),
            )
        self.ball_material.add_actions(
            actions = ("modify_part_collision", "friction", 0)
            )
        self.ball_material.add_actions(
            conditions = ("they_have_material", shared.player_material),
            actions = (("modify_part_collision", "physical", False),
            ('message', 'our_node', 'at_connect', TouchedSpaz())),
            )
        self.ball_material.add_actions(
            conditions = (("they_dont_have_material", shared.player_material), 'and',
            ("they_have_material", shared.object_material)),
            actions = ('message', 'our_node', 'at_connect', TouchedObject()),
            )
        self.ball_material.add_actions(
            conditions = (("they_dont_have_material", shared.player_material), 'and',
            ("they_have_material", shared.footing_material)),
            actions = ('message', 'our_node', 'at_connect', TouchedFootingMaterial()),
            )
    
    def give_orb_ball(self, spaz: ba.Actor) -> None:
        spaz.punch_callback = self.shoot_orb_ball
        self.last_shoot_time = ba.time(timetype=ba.TimeType.BASE, timeformat=ba.TimeFormat.MILLISECONDS)
    
    def shoot_orb_ball(self, spaz: ba.Actor) -> None:
        shoot_time = ba.time(timetype=ba.TimeType.BASE, timeformat=ba.TimeFormat.MILLISECONDS)
        if shoot_time - self.last_shoot_time > 800:
            
            position1 = spaz.node.position_center
            position2 = spaz.node.position_forward
            ball_direction = (position1[0] - position2[0], 0.0, position1[2] - position2[2])
            magnitude = 10.0 / ba.Vec3(*ball_direction).length()
            velocity = [v * magnitude for v in ball_direction]
            OrbBall(position = spaz.node.position, velocity = (velocity[0]*2, velocity[1]*2, velocity[2]*2), owner = spaz.getplayer(playertype = ba.Player), source_player = spaz.getplayer(playertype = ba.Player)).autoretain()

class TouchedSpaz(object):
    pass

class TouchedObject(object):
    pass

class TouchedFootingMaterial(object):
    pass

class OrbBall(ba.Actor):
    def __init__(self, position = (0, 1, 0), velocity = (0, 0, 0), owner = None, source_player = None, sessiontype = type(ba.Session)) -> None:
        ba.Actor.__init__(self)
        factory = self.get_factory()
        self.source_player = source_player
        shared = SharedObjects.get()
        self.node = ba.newnode("prop",
                            attrs = {
                            'position': position,
                            'velocity': velocity,
                            'model': ba.getmodel("shield"),
                            'body': 'sphere',
                            'color_texture': ba.gettexture("powerupCurse"),
                            'model_scale': 0.5,
                            'is_area_of_interest': True,
                            'body_scale': 1.3,
                            'reflection': 'soft',
                            'reflection_scale': [1.0],
                            'materials': [shared.object_material, factory.ball_material]
                            },
                            delegate = self)
        self.owner = owner
        self.source_player = source_player
        self.light = ba.newnode("light", attrs = {"color": (0.8, 0.4, 0.2), "height_attenuated": False, "radius": 0.1})
        self.node.connectattr("position", self.light, "position")
        ba.animate(self.light, "intensity", {0: 1.3, 250: 1.8, 500: 1.3}, loop = True, timetype = ba.TimeType.SIM, timeformat=ba.TimeFormat.MILLISECONDS)
        self.orb_ball_life_timer = ba.Timer(1, ba.WeakCall(self.die))
    
    def die(self) -> None:
        self.light.delete()
        self.node.handlemessage(ba.DieMessage())
    
    @classmethod
    def get_factory(cls):
        activity = ba.getactivity()
        if activity is None:
            raise Exception("no current activity found!")
        try:
            return activity._orbBallFactory
        except:
            f = activity._orbBallFactory = WwFactory()
            return f

    def handlemessage(self, msg):
        super(self.__class__, self).handlemessage(msg)
        if isinstance(msg, TouchedObject):
            node = ba.getcollision().opposingnode
            if node and node.exists():
                v = self.node.velocity
                m = ba.Vec3(*v).length() * 40
                node.handlemessage(
                    ba.HitMessage(pos = self.node.position,
                    velocity = v,
                    magnitude = m,
                    velocity_magnitude = m,
                    radius = 0,
                    srcnode = self.node,
                    source_player = self.source_player,
                    force_direction = self.node.velocity)
                    )
            self.node.handlemessage(ba.DieMessage())
        
        elif isinstance(msg, ba.DieMessage):
            
            if self.node.exists():
                velocity = self.node.velocity
                explosion = ba.newnode("explosion",
                attrs = {'position': self.node.position,
                'velocity': (velocity[0], max(-1.0, velocity[1]), velocity[2]),
                'radius': 2,
                'big': False
                })
                ba.playsound(sound = ba.getsound(random.choice(['impactHard', 'impactHard2', 'impactHard3'])), position = self.node.position)
                self.node.delete()
                self.emit_timer = None
        
        elif isinstance(msg, ba.OutOfBoundsMessage):
            self.node.handlemessage(ba.DieMessage())
        
        elif isinstance(msg, ba.HitMessage):
            self.node.handlemessage("impulse",
            msg.pos[0], msg.pos[1], msg.pos[2],
            msg.velocity[0], msg.velocity[1], msg.velocity[2],
            1.0*msg.magnitude, 1.0*msg.velocity_magnitude, msg.radius, 0,
            msg.force_direction[0], msg.force_direction[1], msg.force_direction[2]
            )

        elif isinstance(msg, TouchedSpaz):
            node = ba.getcollision().opposingnode
            if node and node.exists():
                node.handlemessage(
                    ba.PowerupMessage('curse'))
                node.handlemessage('knockout', 250)
                ba.playsound(sound = ba.getsound('impactHard2'))
                

            self.node.handlemessage(ba.DieMessage())
        
        elif isinstance(msg, TouchedFootingMaterial):
            ba.playsound(sound = ba.getsound("blip"), position = self.node.position)


class Player(ba.Player['Team']):
    """Our player type for this game."""


class Team(ba.Team[Player]):
    """Our team type for this game."""

    def __init__(self) -> None:
        self.score = 0


# ba_meta export game
class CursersGame(ba.TeamGameActivity[Player, Team]):
    """A game type based on acquiring kills."""

    name = 'Curser\'s'
    description = 'Teach enemies lesson\nPress punch to summon curse'

    # Print messages when players die since it matters here.
    announce_player_deaths = True

    @classmethod
    def get_available_settings(
            cls, sessiontype: type[ba.Session]) -> list[ba.Setting]:
        settings = [
            ba.IntSetting(
                'Kills to Win Per Player',
                min_value=1,
                default=5,
                increment=1,
            ),
            ba.IntChoiceSetting(
                'Time Limit',
                choices=[
                    ('None', 0),
                    ('1 Minute', 60),
                    ('2 Minutes', 120),
                    ('5 Minutes', 300),
                    ('10 Minutes', 600),
                    ('20 Minutes', 1200),
                ],
                default=0,
            ),
            ba.FloatChoiceSetting(
                'Respawn Times',
                choices=[
                    ('Shorter', 0.25),
                    ('Short', 0.5),
                    ('Normal', 1.0),
                    ('Long', 2.0),
                    ('Longer', 4.0),
                ],
                default=1.0,
            ),
            ba.BoolSetting('Epic Mode', default=False),
            ba.BoolSetting('Credits', default=True)
        ]

        # In teams mode, a suicide gives a point to the other team, but in
        # free-for-all it subtracts from your own score. By default we clamp
        # this at zero to benefit new players, but pro players might like to
        # be able to go negative. (to avoid a strategy of just
        # suiciding until you get a good drop)
        if issubclass(sessiontype, ba.FreeForAllSession):
            settings.append(
                ba.BoolSetting('Allow Negative Scores', default=False))

        return settings

    @classmethod
    def supports_session_type(cls, sessiontype: type[ba.Session]) -> bool:
        return (issubclass(sessiontype, ba.DualTeamSession)
                or issubclass(sessiontype, ba.FreeForAllSession))

    @classmethod
    def get_supported_maps(cls, sessiontype: type[ba.Session]) -> list[str]:
        return ba.getmaps('melee')

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._scoreboard = Scoreboard()
        self._score_to_win: Optional[int] = None
        self._cd_text: Optional[ba.Actor] = None
        self._dingsound = ba.getsound('dingSmall')
        self._epic_mode = bool(settings['Epic Mode'])
        self._kills_to_win_per_player = int(
            settings['Kills to Win Per Player'])
        self._time_limit = float(settings['Time Limit'])
        self._allow_negative_scores = bool(
            settings.get('Allow Negative Scores', False))
        self._credits = bool(settings['Credits'])

        # Base class overrides.
        self.slow_motion = self._epic_mode
        self.default_music = (ba.MusicType.EPIC if self._epic_mode else
                              ba.MusicType.TO_THE_DEATH)

    def get_instance_description(self) -> Union[str, Sequence]:
        return 'Curse ${ARG1} of your enemies.', self._score_to_win

    def get_instance_description_short(self) -> Union[str, Sequence]:
        return 'Curse ${ARG1} enemies', self._score_to_win

    def on_team_join(self, team: Team) -> None:
        if self.has_begun():
            self._update_scoreboard()

    def on_begin(self) -> None:
        super().on_begin()
        self.setup_standard_time_limit(self._time_limit)
        if self._credits:
            self._cd_text = ba.NodeActor(
                ba.newnode('text',
                           attrs={
                               'position': (0, 0),
                               'h_attach': 'center',
                               'h_align': 'center',
                               'maxwidth': 200,
                               'shadow': 0.5,
                               'vr_depth': 390,
                               'scale': 0.8,
                               'v_attach': 'bottom',
                               'color': (1, 1, 1),
                               'text': 'By itsre3'
                           }))


        # Base kills needed to win on the size of the largest team.
        self._score_to_win = (self._kills_to_win_per_player *
                              max(1, max(len(t.players) for t in self.teams)))
        self._update_scoreboard()

    def spawn_player(self, player: Player) -> ba.Actor:
        spaz = self.spawn_player_spaz(player)
        WwFactory().give_orb_ball(spaz)
        spaz.connect_controls_to_player(enable_punch=True,
                                        enable_bomb=False,
                                        enable_pickup=True)
# This below overwrites default character. Vishuuuuuuuuuu lol
        spaz.node.color_mask_texture = ba.gettexture('wizardColorMask')
        spaz.node.color_texture = ba.gettexture('powerupCurse')
        spaz.node.head_model = ba.getmodel('wizardHead')
        spaz.node.hand_model = ba.getmodel('wizardHand')
        spaz.node.torso_model = ba.getmodel('wizardTorso')
        spaz.node.pelvis_model = ba.getmodel('wizardPelvis')
        spaz.node.upper_arm_model = ba.getmodel('wizardUpperArm')
        spaz.node.forearm_model = ba.getmodel('wizardForeArm')
        spaz.node.upper_leg_model = ba.getmodel('wizardUpperLeg')
        spaz.node.lower_leg_model = ba.getmodel('wizardLowerLeg')
        spaz.node.toes_model = ba.getmodel('wizardToes')
        wizard_sounds = [ba.getsound('wizard1'), ba.getsound('wizard2'), ba.getsound('wizard3'),ba.getsound('wizard4')]
        spaz.node.jump_sounds = wizard_sounds
        spaz.node.attack_sounds = wizard_sounds
        spaz.node.impact_sounds = wizard_sounds
        spaz.node.pickup_sounds = wizard_sounds
        spaz.node.death_sounds = [ba.getsound('wizardDeath')]
        spaz.node.fall_sounds = [ba.getsound('wizardFall')]
        
        return spaz

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.PlayerDiedMessage):
            # Augment standard behavior.
            super().handlemessage(msg)
            player = msg.getplayer(Player)
            self.respawn_player(player)
            killer = msg.getkillerplayer(Player)
            if killer is None:
                return None
            # Handle team-kills.
            if killer.team is player.team:
                # In free-for-all, killing yourself loses you a point.
                if isinstance(self.session, ba.FreeForAllSession):
                    new_score = player.team.score - 1
                    if not self._allow_negative_scores:
                        new_score = max(0, new_score)
                    player.team.score = new_score
                # In teams-mode it gives a point to the other team.
                else:
                    ba.playsound(self._dingsound)
                    for team in self.teams:
                        if team is not killer.team:
                            team.score += 1
            # Killing someone on another team nets a kill.
            else:
                killer.team.score += 1
                ba.playsound(self._dingsound)
                # In FFA show scores since its hard to find on the scoreboard.
                if isinstance(killer.actor, PlayerSpaz) and killer.actor:
                    killer.actor.set_score_text(str(killer.team.score) + '/' +
                                                str(self._score_to_win),
                                                color=killer.team.color,
                                                flash=True)

            self._update_scoreboard()

            # If someone has won, set a timer to end shortly.
            # (allows the dust to clear and draws to occur if deaths are
            # close enough)
            assert self._score_to_win is not None
            if any(team.score >= self._score_to_win for team in self.teams):
                ba.timer(0.5, self.end_game)

        else:
            return super().handlemessage(msg)
        return None

    def _update_scoreboard(self) -> None:
        for team in self.teams:
            self._scoreboard.set_team_value(team, team.score,
                                            self._score_to_win)

    def end_game(self) -> None:
        results = ba.GameResults()
        for team in self.teams:
            results.set_team_score(team, team.score)
        self.end(results=results)
