"""Super Duel / Created by: byANG3L"""

# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
import json
import random
from bastd.actor.playerspaz import PlayerSpaz
from bastd.actor.scoreboard import Scoreboard
from bastd.game.elimination import Icon
from bastd.actor.powerupbox import PowerupBox, PowerupBoxFactory
from bastd.actor.bomb import Bomb, BombFactory

if TYPE_CHECKING:
    from typing import Any, Type, List, Dict, Tuple, Union, Sequence, Optional


lang = ba.app.lang.language
if lang == 'Spanish':
    enable_powerups = 'Habilitar Potenciadores'
    night_mode = 'Modo Noche'
    fight_delay = 'Tiempo entre Pelea'
    very_fast = 'Muy Rápido'
    fast = 'Rápido'
    normal = 'Normal'
    slow = 'Lento'
    very_slow = 'Muy Lento'
    none = 'Ninguno'
    super_punch = 'Super Golpe'
    super_speed = 'Super Velocidad'
    box_mode = 'Modo Caja'
    boxing_gloves = 'Guantes de Boxeo'
    shield = 'Electro-Escudo'
    reset_position = 'Reiniciar Posición'
    spawn_particles = 'Efectos al Aparecer'
    hitpoints = 'Vida'
    jump = 'Saltar'
    punch = 'Golpear'
    pickup = 'Agarrar'
    bomb = 'Bomba'
    run = 'Correr'
    same_powerups = 'Potenciadores Iguales'
    clear_objects = 'Eliminar Objetos cada Ronda'
    meteor_shower = 'Lluvia de Meteoritos'
else:
    enable_powerups = 'Enable Powerups'
    night_mode = 'Night Mode'
    fight_delay = 'Fight Delay'
    very_fast = 'Very Fast'
    fast = 'Fast'
    normal = 'Normal'
    slow = 'Slow'
    very_slow = 'Very Slow'
    none = 'None'
    super_punch = 'Super Punch'
    super_speed = 'Super Speed'
    box_mode = 'Box Mode'
    boxing_gloves = 'Boxing Gloves'
    shield = 'Shield'
    reset_position = 'Reset Position'
    spawn_particles = 'Effects on Spawn'
    hitpoints = 'Hitpoints'
    jump = 'Jump'
    punch = 'Punch'
    pickup = 'Pickup'
    bomb = 'Bomb'
    run = 'Run'
    same_powerups = 'Same Powerups'
    clear_objects = 'Eliminate Objects every Round'
    meteor_shower = 'Meteor Shower'


class SuperSpaz(PlayerSpaz):

    def __init__(self,
                 player: ba.Player,
                 color: Sequence[float] = (1.0, 1.0, 1.0),
                 highlight: Sequence[float] = (0.5, 0.5, 0.5),
                 character: str = 'Spaz',
                 super_punch: bool = False,
                 powerups_expire: bool = True):
        super().__init__(player=player,
                         color=color,
                         highlight=highlight,
                         character=character,
                         powerups_expire=powerups_expire)
        self._super_punch = super_punch

    def handlemessage(self, msg: Any) -> Any:
        from bastd.actor.spaz import PunchHitMessage
        from bastd.actor.bomb import Blast
        if isinstance(msg, PunchHitMessage):
            super().handlemessage(msg)
            node = ba.getcollision().opposingnode
            if self._super_punch:
                if node.getnodetype() == 'spaz':
                    if not node.frozen:
                        node.frozen = True
                        node.handlemessage(ba.FreezeMessage())
                        ba.playsound(ba.getsound('freeze'))
                    ba.playsound(ba.getsound('superPunch'))
                    ba.playsound(ba.getsound('punchStrong02'))
                    Blast(position=node.position,
                          velocity=node.velocity,
                          blast_radius=0.0,
                          blast_type='normal').autoretain()
        else:
            return super().handlemessage(msg)
        return None


class Player(ba.Player['Team']):
    """Our player type for this game."""
    def __init__(self) -> None:
        self.icons: List[Icon] = []
        self.in_game: bool = False
        self.playervs1: bool = False
        self.playervs2: bool = False
        self.light: bool = False
        self.crown: bool = False
        self.crown_node: ba.Node = None


class Team(ba.Team[Player]):
    """Our team type for this game."""

    def __init__(self) -> None:
        self.score = 0


# ba_meta export game
class NewDuelGame(ba.TeamGameActivity[Player, Team]):
    """A game type based on acquiring kills."""

    name = 'Super Duel'
    description = 'Kill a set number of enemies to win.'

    # Print messages when players die since it matters here.
    announce_player_deaths = True

    @classmethod
    def get_available_settings(
            cls, sessiontype: Type[ba.Session]) -> List[ba.Setting]:
        settings = [
            ba.IntSetting(
                'Kills to Win Per Player',
                min_value=1,
                default=5,
                increment=1,
            ),
            ba.IntChoiceSetting(
                fight_delay,
                choices=[
                    (none, 0.0),
                    (very_fast, 0.3),
                    (fast, 0.6),
                    (normal, 1.0),
                    (slow, 1.4),
                    (very_slow, 1.7),
                ],
                default=1.0,
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
            ba.IntChoiceSetting(
                '\ue043',
                choices=[
                    ('\ue043', 0),
                ],
                default=0,
            ),
            ba.IntSetting(
                hitpoints,
                min_value=100,
                default=1000,
                increment=100,
            ),
            ba.BoolSetting(boxing_gloves, default=False),
            ba.BoolSetting(shield, default=False),
            ba.BoolSetting(super_punch, default=False),
            ba.BoolSetting(super_speed, default=False),
            ba.BoolSetting(box_mode, default=False),
            ba.BoolSetting(reset_position, default=False),
            ba.BoolSetting(spawn_particles, default=False),
            ba.BoolSetting(jump, default=True),
            ba.BoolSetting(punch, default=True),
            ba.BoolSetting(pickup, default=True),
            ba.BoolSetting(bomb, default=True),
            ba.BoolSetting(run, default=True),
            ba.IntChoiceSetting(
                '\ue043',
                choices=[
                    ('\ue043', 0),
                ],
                default=0,
            ),
            ba.BoolSetting(meteor_shower, default=True),
            ba.BoolSetting(enable_powerups, default=True),
            ba.BoolSetting(same_powerups, default=False),
            ba.BoolSetting(clear_objects, default=False),
            ba.BoolSetting(night_mode, default=False),
            ba.BoolSetting('Epic Mode', default=False),
            ba.BoolSetting('Allow Negative Scores', default=False),
        ]
        return settings

    @classmethod
    def supports_session_type(cls, sessiontype: type[ba.Session]) -> bool:
        return (issubclass(sessiontype, ba.DualTeamSession)
                or issubclass(sessiontype, ba.FreeForAllSession))

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[ba.Session]) -> List[str]:
        return ba.getmaps('melee')

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._scoreboard = Scoreboard()
        self._score_to_win: Optional[int] = None
        self._dingsound = ba.getsound('dingSmall')
        self._epic_mode = bool(settings['Epic Mode'])
        self._kills_to_win_per_player = int(
            settings['Kills to Win Per Player'])
        self._enable_powerups = bool(settings[enable_powerups])
        self._night_mode = bool(settings[night_mode])
        self._fight_delay = float(settings[fight_delay])
        self._time_limit = float(settings['Time Limit'])
        self._allow_negative_scores = bool(
            settings.get('Allow Negative Scores', False))
        self._super_punch = bool(settings[super_punch])
        self._super_speed = bool(settings[super_speed])
        self._box_mode = bool(settings[box_mode])
        self._boxing_gloves = bool(settings[boxing_gloves])
        self._shield = bool(settings[shield])
        self._vs_text: Optional[ba.Actor] = None
        self.spawn_order: List[Player] = []
        self._players_vs_1: bool = False
        self._players_vs_2: bool = False
        self._count_1 = ba.getsound('announceOne')
        self._count_2 = ba.getsound('announceTwo')
        self._count_3 = ba.getsound('announceThree')
        self._boxing_bell = ba.getsound('boxingBell')
        self._reset_position = bool(settings[reset_position])
        self._spawn_particles = bool(settings[spawn_particles])
        self._player_hitpoints = int(settings[hitpoints])
        self._enable_jump = bool(settings[jump])
        self._enable_punch = bool(settings[punch])
        self._enable_pickup = bool(settings[pickup])
        self._enable_bomb = bool(settings[bomb])
        self._enable_run = bool(settings[run])
        self._same_powerups = bool(settings[same_powerups])
        self._clear_objects = bool(settings[clear_objects])
        self._meteor_shower = bool(settings[meteor_shower])

        self._bomb_time = 2.0

        # Base class overrides.
        self.slow_motion = self._epic_mode
        self.default_music = (ba.MusicType.EPIC if self._epic_mode else
                              ba.MusicType.TO_THE_DEATH)

    def get_instance_description(self) -> Union[str, Sequence]:
        return 'Crush ${ARG1} of your enemies.', self._score_to_win

    def get_instance_description_short(self) -> Union[str, Sequence]:
        return 'kill ${ARG1} enemies', self._score_to_win

    def on_player_join(self, player: Player) -> None:
        self.spawn_order.append(player)
        self._update_order()

    def on_player_leave(self, player: Player) -> None:
        super().on_player_leave(player)
        player.icons = []
        if player.playervs1:
            player.playervs1 = False
            self._players_vs_1 = False
            player.in_game = False
        elif player.playervs2:
            player.playervs2 = False
            self._players_vs_2 = False
            player.in_game = False
        if player in self.spawn_order:
            self.spawn_order.remove(player)
        self._update_order()

    def on_transition_in(self) -> None:
        super().on_transition_in()
        if self._night_mode:
            gnode = ba.getactivity().globalsnode
            gnode.tint = (0.3, 0.3, 0.3)
        if self._super_speed:
            if self.map.getname() in ['Hockey Stadium', 'Lake Frigid']:
                new_material = ba.Material()
                new_material.add_actions(
                    actions=('modify_part_collision', 'friction', 500.01))
                oldm = self.map.node.materials
                print(oldm)
                oldm = oldm + (new_material, )
                self.map.node.materials = oldm

    def on_team_join(self, team: Team) -> None:
        if self.has_begun():
            self._update_scoreboard()

    def on_begin(self) -> None:
        super().on_begin()
        self.setup_standard_time_limit(self._time_limit)
        self._vs_text = ba.NodeActor(
        ba.newnode('text',
                   attrs={
                       'position': (0, 105),
                       'h_attach': 'center',
                       'h_align': 'center',
                       'maxwidth': 200,
                       'shadow': 0.5,
                       'vr_depth': 390,
                       'scale': 0.6,
                       'v_attach': 'bottom',
                       'color': (0.8, 0.8, 0.3, 1.0),
                       'text': ba.Lstr(resource='vsText')
                   }))

        # Base kills needed to win on the size of the largest team.
        self._score_to_win = (self._kills_to_win_per_player *
                              max(1, max(len(t.players) for t in self.teams)))
        self._update_scoreboard()
        self._do_environment()

    def _do_environment(self) -> None:
        if self._meteor_shower:
            delay = 3.5
            ba.timer(delay, self._decrement_bomb_time, repeat=True)

            # Kick off the first wave in a few seconds.
            delay = 3.0
            ba.timer(delay, self._set_bomb_timer)

    def _set_bomb_timer(self) -> None:
        ba.timer((1.0 + 0.2 * random.random()) * self._bomb_time,
                 self._drop_bomb_cluster)

    def _drop_bomb_cluster(self) -> None:

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

            if self.map.getname() == 'Hockey Stadium':
                pos = (random.randrange(-11, 12), 6, random.randrange(-4, 5))
            elif self.map.getname() == 'Football Stadium':
                pos = (random.randrange(-10, 11), 6, random.randrange(-5, 6))
            elif self.map.getname() == 'Bridgit':
                pos = (random.randrange(-5, 6), 9, random.randrange(0, 4))
            elif self.map.getname() == 'Big G':
                pos = (random.randrange(-7, 8), 8, random.randrange(-7, 7))
            elif self.map.getname() == 'Roundabout':
                pos = (random.randrange(-4, 1), 9, random.randrange(-6, 0))
            elif self.map.getname() == 'Monkey Face':
                pos = (random.randrange(-8, 5), 9, random.randrange(-6, 3))
            elif self.map.getname() == 'Zigzag':
                pos = (random.randrange(-9, 7), 10, random.randrange(-4, 1))
            elif self.map.getname() == 'The Pad':
                pos = (random.randrange(-3, 4), 10, random.randrange(-8, 4))
            elif self.map.getname() == 'Doom Shroom':
                pos = (random.randrange(-7, 8), 8, random.randrange(-7, 1))
            elif self.map.getname() == 'Lake Frigid':
                pos = (random.randrange(-7, 8), 8, random.randrange(-7, 3))
            elif self.map.getname() == 'Tip Top':
                pos = (random.randrange(-7, 8), 14, random.randrange(-5, 2))
            elif self.map.getname() == 'Crag Castle':
                pos = (random.randrange(-5, 4), 13, random.randrange(-6, 1))
            elif self.map.getname() == 'Tower D':
                pos = (random.randrange(-7, 8), 8, random.randrange(-5, 5))
            elif self.map.getname() == 'Happy Thoughts':
                pos = (random.randrange(-10, 11), 21, -5.4)
            elif self.map.getname() == 'Step Right Up':
                pos = (random.randrange(-7, 8), 10, random.randrange(-8, 3))
            elif self.map.getname() == 'Courtyard':
                pos = (random.randrange(-7, 8), 10, random.randrange(-6, 4))
            elif self.map.getname() == 'Rampage':
                pos = (random.randrange(-7, 8), 11, random.randrange(-5, -2))
            else:
                pos = (random.randrange(-7, 8), 6, random.randrange(-5, 6))

            dropdir = (-1.0 if pos[0] > 0 else 1.0)
            vel = ((-5.0 + random.random() * 30.0) * dropdir, -4.0, 0)
            ba.timer(delay, ba.Call(self._drop_bomb, pos, vel))
            delay += 0.1
        self._set_bomb_timer()

    def _drop_bomb(self, position: Sequence[float],
                   velocity: Sequence[float]) -> None:
        Bomb(position=position,
             velocity=velocity).autoretain()

    def _decrement_bomb_time(self) -> None:
        self._bomb_time = max(2.0, self._bomb_time * 0.9)

    def _drop_custom_powerups(self) -> None:
        if self._enable_powerups:
            last_pwp = None
            powerup = PowerupBoxFactory.get().get_random_powerup_type()
            points = self.map.powerup_spawn_points
            for i in range(len(points)):
                pwp = PowerupBoxFactory.get().get_random_powerup_type()
                if not self._same_powerups:
                    powerup = pwp
                    if pwp == last_pwp:
                        powerup = PowerupBoxFactory.get().get_random_powerup_type()
                PowerupBox(
                    position=self.map.powerup_spawn_points[i],
                    poweruptype=powerup,
                    expire=False).autoretain()
                last_pwp = pwp
            self._tnt_spawners = {}
            self._setup_standard_tnt_drops()

    def _clear_all_objects(self) -> None:
        factory = BombFactory.get()
        pwfactory = PowerupBoxFactory.get()
        if self._clear_objects:
            conditions = (('they_have_material', factory.bomb_material),
                         'or',
                         ('they_have_material',
                         pwfactory.powerup_material))
        else:
            conditions = ('they_have_material', pwfactory.powerup_material)
        for player in self.players:
            if player.playervs1 or player.playervs2:
                self._die_material = ba.Material()
                self._die_material.add_actions(
                    conditions=conditions,
                    actions=(('modify_part_collision', 'physical', False),
                             ('modify_part_collision', 'collide', True),
                             ('message', 'their_node', 'at_connect',
                              ba.DieMessage())))
                new_region = ba.newnode(
                    'region',
                    attrs={
                        'position': player.node.position,
                        'scale': (20, 20, 20),
                        'type': 'sphere',
                        'materials': [self._die_material]
                    })
                ba.timer(0.05, new_region.delete)

    def _update_crown(self) -> None:
        score_players = []
        crown_players = []
        for player in self.players:
            if player.team.score > 0:
                pscore = player.team.score
                score_players.append(pscore)
        score_players.sort()
        if not score_players:
            return
        for player in self.players:
            if player.team.score != score_players[-1]:
                player.crown = False
                player.crown_node = None
            else:
                if player.is_alive():
                    player.crown = True
                    spaz = player.actor
                    if player.crown_node:
                        ba.animate(player.crown_node, 'scale', {
                            0: 0.02,
                            0.2: 0.026,
                            0.4: 0.02})
                    else:
                        crown_text = ba.newnode(
                            'math',
                            owner=spaz.node,
                            attrs={'input1': (0, 0.85, -0.2),
                                   'operation': 'add'})
                        spaz.node.connectattr(
                            'torso_position', crown_text, 'input2')
                        player.crown_node = cnode = ba.newnode('text',
                                             owner=spaz.node,
                                             attrs={
                                                'text': '\ue043',
                                                'in_world': True,
                                                'shadow': 0.5,
                                                'flatness': 1.0,
                                                'scale': 0.02,
                                                'h_align': 'center',
                                             })
                        crown_text.connectattr(
                            'output', cnode, 'position')
                        ba.animate(cnode, 'scale', {
                            0: 0,
                            0.2: 0,
                            0.6: 0.024,
                            0.8: 0.02})

    def spawn_player(self, player: PlayerType) -> ba.Actor:
        # pylint: disable=too-many-locals
        # pylint: disable=cyclic-import
        from ba import _math
        from ba._coopsession import CoopSession
        from bastd.actor.spazfactory import SpazFactory
        factory = SpazFactory.get()
        name = player.getname()
        color = player.color
        highlight = player.highlight

        light_color = _math.normalized_color(color)
        display_color = ba.safecolor(color, target_intensity=0.75)
        spaz = SuperSpaz(color=color,
                         highlight=highlight,
                         character=player.character,
                         player=player,
                         super_punch=True if self._super_punch else False)

        player.actor = spaz
        assert spaz.node

        # If this is co-op and we're on Courtyard or Runaround, add the
        # material that allows us to collide with the player-walls.
        # FIXME: Need to generalize this.
        if isinstance(self.session, CoopSession) and self.map.getname() in [
                'Courtyard', 'Tower D'
        ]:
            mat = self.map.preloaddata['collide_with_wall_material']
            assert isinstance(spaz.node.materials, tuple)
            assert isinstance(spaz.node.roller_materials, tuple)
            spaz.node.materials += (mat, )
            spaz.node.roller_materials += (mat, )

        spaz.node.name = name
        spaz.node.name_color = display_color
        self._connect_controls(player)

        spaz.handlemessage(ba.StandMessage(self._get_spawn_point(player)))

        ba.playsound(self._spawn_sound, 1, position=spaz.node.position)
        light = ba.newnode('light', attrs={'color': light_color})
        spaz.node.connectattr('position', light, 'position')
        ba.animate(light, 'intensity', {0: 0, 0.25: 1, 0.5: 0})
        ba.timer(0.5, light.delete)

        if self._super_punch:
            spaz._punch_power_scale = factory.punch_power_scale_gloves = 6
            spaz.equip_boxing_gloves()
            lfx = ba.newnode(
                'light',
                attrs={
                    'color': color,
                    'radius': 0.3,
                    'intensity': 0.3})
            def sp_fx():
                if not spaz.node:
                    lfx.delete()
                    return
                ba.emitfx(position=spaz.node.position,
                          velocity=spaz.node.velocity,
                          count=5,
                          scale=0.5,
                          spread=0.5,
                          chunk_type='spark')
                ba.emitfx(position=spaz.node.position,
                          velocity=spaz.node.velocity,
                          count=2,
                          scale=0.8,
                          spread=0.3,
                          chunk_type='spark')
                if lfx:
                    spaz.node.connectattr('position', lfx, 'position')
            ba.timer(0.1, sp_fx, repeat=True)

        if self._box_mode:
            spaz.node.color_texture = ba.gettexture('tnt')
            spaz.node.color_mask_texture = ba.gettexture('tnt')
            spaz.node.color = (1, 1, 1)
            spaz.node.highlight = (1, 1, 1)
            spaz.node.head_model = None
            spaz.node.torso_model = ba.getmodel('tnt')
            spaz.node.style = 'cyborg'

        if self._boxing_gloves:
            spaz.equip_boxing_gloves()

        if self._shield:
            spaz.equip_shields()

        if self._spawn_particles:
            ba.emitfx(position=spaz.node.position,
                      velocity=(0,0,0),
                      count=16,
                      scale=0.8,
                      spread=1.5,
                      chunk_type='spark')

        spaz.hitpoints = spaz.hitpoints_max = self._player_hitpoints

        if self._super_speed:
            spaz.node.hockey = True

        ba.timer(0.05, self._update_crown)

        return spaz

    def _update_spawn(self, player: Player) -> None:
        if self._players_vs_1 and self._players_vs_2:
            if not player.is_alive():
                self.spawn_player(player)
                self._set_night_light(player)
            for player in self.players:
                if player.is_alive():
                    player.actor.disconnect_controls_from_player()
                    if self._reset_position:
                        self._set_start_position(player)
            self._countdown()
            self._clear_all_objects()
            ba.timer(0.1, self._drop_custom_powerups)
        else:
            if not player.is_alive():
                self.spawn_player(player)
                self._set_start_position(player)
                self._set_night_light(player)

    def _set_start_position(self, player: Player) -> None:
        pos1 = [self.map.get_start_position(0), 90]
        pos2 = [self.map.get_start_position(1), 270]
        player.actor.handlemessage(
            ba.StandMessage(
                pos1[0] if player.playervs1 else pos2[0],
                pos1[1] if player.playervs1 else pos2[1]))

    def _get_spawn_point(self, player: Player) -> Optional[ba.Vec3]:
        living_player = None
        living_player_pos = None
        if player.playervs1:
            main_player = 'pvs1'
        elif player.playervs2:
            main_player = 'pvs2'

        for team in self.teams:
            for tplayer in team.players:
                if self._players_vs_1 and self._players_vs_2:
                    if main_player == 'pvs1':
                        if tplayer.is_alive() and tplayer.playervs2:
                            assert tplayer.node
                            ppos = tplayer.node.position
                            living_player = tplayer
                            living_player_pos = ppos
                            break
                    elif main_player == 'pvs2':
                        if tplayer.is_alive() and tplayer.playervs1:
                            assert tplayer.node
                            ppos = tplayer.node.position
                            living_player = tplayer
                            living_player_pos = ppos
                            break
                else:
                    if tplayer.is_alive():
                        assert tplayer.node
                        ppos = tplayer.node.position
                        living_player = tplayer
                        living_player_pos = ppos
                        break

        if living_player:
            assert living_player_pos is not None
            player_pos = ba.Vec3(living_player_pos)
            points: list[tuple[float, ba.Vec3]] = []
            for team in self.teams:
                start_pos = ba.Vec3(self.map.get_start_position(team.id))
                points.append(
                    ((start_pos - player_pos).length(), start_pos))
            # Hmm.. we need to sorting vectors too?
            points.sort(key=lambda x: x[0])
            return points[-1][1]
        return None

    def _connect_controls(self, player: Player) -> None:
        player.actor.connect_controls_to_player(
            enable_jump=self._enable_jump,
            enable_punch=self._enable_punch,
            enable_pickup=self._enable_pickup,
            enable_bomb=self._enable_bomb,
            enable_run=self._enable_run)

    def _set_night_light(self, player: Player) -> None:
        if self._night_mode:
            if not player.light:
                player.light = True
                light = ba.newnode(
                    'light',
                    owner=player.node,
                    attrs={
                        'radius': 0.3,
                        'intensity': 0.6,
                        'height_attenuated': False,
                        'color': player.color
                    })
                player.node.connectattr(
                    'position', light, 'position')

    def _countdown(self) -> None:
        if self._fight_delay == 0:
            for player in self.players:
                if player.playervs1 or player.playervs2:
                    if player.is_alive():
                        self._connect_controls(player)
        else:
            ba.timer(self._fight_delay + 0.5, self.count3)

    def start(self) -> None:
        self._count_text('FIGHT')
        ba.playsound(self._boxing_bell)
        for player in self.players:
            if player.playervs1 or player.playervs2:
                if not player.is_alive():
                    return
                else:
                    self._connect_controls(player)

    def count(self) -> None:
        self._count_text('1')
        ba.playsound(self._count_1)
        ba.timer(self._fight_delay, self.start)

    def count2(self) -> None:
        self._count_text('2')
        ba.playsound(self._count_2)
        ba.timer(self._fight_delay, self.count)

    def count3(self) -> None:
        self._count_text('3')
        ba.playsound(self._count_3)
        ba.timer(self._fight_delay, self.count2)

    def _count_text(self, num: str) -> None:
        self.node = ba.newnode('text',
                               attrs={
                                   'v_attach': 'center',
                                   'h_attach': 'center',
                                   'h_align': 'center',
                                   'color': (1, 1, 0.5, 1),
                                   'flatness': 0.5,
                                   'shadow': 0.5,
                                   'position': (0, 18),
                                   'text': num
                               })
        if self._fight_delay == 0.7:
            ba.animate(self.node, 'scale',
                      {0: 0, 0.1: 3.9, 0.64: 4.3, 0.68: 0})
        elif self._fight_delay == 0.4:
            ba.animate(self.node, 'scale',
                      {0: 0, 0.1: 3.9, 0.34: 4.3, 0.38: 0})
        else:
            ba.animate(self.node, 'scale',
                      {0: 0, 0.1: 3.9, 0.92: 4.3, 0.96: 0})
        cmb = ba.newnode('combine', owner=self.node, attrs={'size': 4})
        cmb.connectattr('output', self.node, 'color')
        ba.animate(cmb, 'input0', {0: 1.0, 0.15: 1.0}, loop=True)
        ba.animate(cmb, 'input1', {0: 1.0, 0.15: 0.5}, loop=True)
        ba.animate(cmb, 'input2', {0: 0.1, 0.15: 0.0}, loop=True)
        cmb.input3 = 1.0
        ba.timer(self._fight_delay, self.node.delete)

    def _update_order(self) -> None:
        for player in self.spawn_order:
            assert isinstance(player, Player)
            if not player.is_alive():
                if not self._players_vs_1:
                    self._players_vs_1 = True
                    player.playervs1 = True
                    player.in_game = True
                    self.spawn_order.remove(player)
                    self._update_spawn(player)
                elif not self._players_vs_2:
                    self._players_vs_2 = True
                    player.playervs2 = True
                    player.in_game = True
                    self.spawn_order.remove(player)
                    self._update_spawn(player)
                self._update_icons()

    def _update_icons(self) -> None:
        # pylint: disable=too-many-branches

        for player in self.players:
            player.icons = []

            if player.in_game:
                if player.playervs1:
                    xval = -60
                    x_offs = -78
                elif player.playervs2:
                    xval = 60
                    x_offs = 78
                player.icons.append(
                    Icon(player,
                         position=(xval, 40),
                         scale=1.0,
                         name_maxwidth=130,
                         name_scale=0.8,
                         flatness=0.0,
                         shadow=0.5,
                         show_death=True,
                         show_lives=False))
            else:
                xval = 125
                xval2 = -125
                x_offs = 78
                for player in self.spawn_order:
                    player.icons.append(
                        Icon(player,
                             position=(xval, 25),
                             scale=0.5,
                             name_maxwidth=75,
                             name_scale=1.0,
                             flatness=1.0,
                             shadow=1.0,
                             show_death=False,
                             show_lives=False))
                    xval += x_offs * 0.56
                    player.icons.append(
                        Icon(player,
                             position=(xval2, 25),
                             scale=0.5,
                             name_maxwidth=75,
                             name_scale=1.0,
                             flatness=1.0,
                             shadow=1.0,
                             show_death=False,
                             show_lives=False))
                    xval2 -= x_offs * 0.56

    def handlemessage(self, msg: Any) -> Any:

        if isinstance(msg, ba.PlayerDiedMessage):

            # Augment standard behavior.
            super().handlemessage(msg)

            player = msg.getplayer(Player)

            if player.playervs1:
                player.playervs1 = False
                self._players_vs_1 = False
                player.in_game = False
                self.spawn_order.append(player)
            elif player.playervs2:
                player.playervs2 = False
                self._players_vs_2 = False
                player.in_game = False
                self.spawn_order.append(player)
            ba.timer(0.1, self._update_order)

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

            player.crown_node = None
            ba.timer(0.05, self._update_crown)

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
