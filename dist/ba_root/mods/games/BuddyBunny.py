# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations
from typing import TYPE_CHECKING

import ba
import _ba
import random
import weakref
from ba import internal
from bastd.actor import powerupbox
from bastd.actor.powerupbox import (_TouchedMessage, PowerupBoxFactory,
                                    DEFAULT_POWERUP_INTERVAL)
from bastd.gameutils import SharedObjects
from bastd.actor.spazbot import SpazBot, SpazBotSet
from bastd.actor.playerspaz import PlayerSpaz
from bastd.actor.spaz import Spaz
from ba._gameactivity import GameActivity
from ba._coopsession import CoopSession
from bastd.game.onslaught import OnslaughtGame
from bastd.game.football import FootballCoopGame
from bastd.game.runaround import RunaroundGame
from bastd.game.thelaststand import TheLastStandGame

if TYPE_CHECKING:
    from typing import List, Any, Optional, Sequence


class BunnyBuddyBot(SpazBot):
    color = (1.0, 1.0, 1.0)
    highlight = (1.0, 0.5, 0.5)
    character = 'Easter Bunny'
    punchiness = 1.0
    run = False
    bouncy = False
    default_boxing_gloves = True
    charge_dist_min = 1.0
    charge_dist_max = 9999.0
    charge_speed_min = 1.0
    charge_speed_max = 1.0
    throw_dist_min = 3
    throw_dist_max = 6
    points_mult = 2

    def __init__(self, player) -> None:
        """Instantiate a spaz-bot."""
        self.color = player.color
        self.highlight = player.highlight
        Spaz.__init__(self,
                      color=self.color,
                      highlight=self.highlight,
                      character=self.character,
                      source_player=None,
                      start_invincible=False,
                      can_accept_powerups=False)

        # If you need to add custom behavior to a bot, set this to a callable
        # which takes one arg (the bot) and returns False if the bot's normal
        # update should be run and True if not.
        self.update_callback: Optional[Callable[[SpazBot], Any]] = None
        activity = self.activity
        assert isinstance(activity, ba.GameActivity)
        self._map = weakref.ref(activity.map)
        self.last_player_attacked_by: Optional[ba.Player] = None
        self.last_attacked_time = 0.0
        self.last_attacked_type: Optional[Tuple[str, str]] = None
        self.target_point_default: Optional[ba.Vec3] = None
        self.held_count = 0
        self.last_player_held_by: Optional[ba.Player] = None
        self.target_flag: Optional[Flag] = None
        self._charge_speed = 0.5 * (self.charge_speed_min +
                                    self.charge_speed_max)
        self._lead_amount = 0.5
        self._mode = 'wait'
        self._charge_closing_in = False
        self._last_charge_dist = 0.0
        self._running = False
        self._last_jump_time = 0.0

    def handlemessage(self, msg: Any) -> Any:
        # pylint: disable=too-many-branches
        assert not self.expired

        # Keep track of if we're being held and by who most recently.
        if isinstance(msg, ba.DieMessage):
            wasdead = self._dead
            self._dead = True
            self.hitpoints = 0
            if msg.immediate:
                if self.node:
                    self.node.delete()
            elif self.node:
                self.node.hurt = 1.0
                if self.play_big_death_sound and not wasdead:
                    ba.playsound(SpazFactory.get().single_player_death_sound)
                self.node.dead = True
                ba.timer(2.0, self.node.delete)
        else:
            return super().handlemessage(msg)

class BunnyBotSet(SpazBotSet):

    def __init__(self,
                 source_player: ba.Player = None) -> None:
        """Create a bot-set."""

        # We spread our bots out over a few lists so we can update
        # them in a staggered fashion.
        self._bot_list_count = 5
        self._bot_add_list = 0
        self._bot_update_list = 0
        self._bot_lists: List[List[SpazBot]] = [
            [] for _ in range(self._bot_list_count)
        ]
        self._spawn_sound = ba.getsound('spawn')
        self._spawning_count = 0
        self._bot_update_timer: Optional[ba.Timer] = None
        self.start_moving_bunnies()
        self.source_player = source_player
        session = _ba.get_foreground_host_session()
        if (isinstance(session, ba.DualTeamSession)):
            self.team = self.source_player.team

    def do_bunny(self) -> None:
        self.spawn_bot(BunnyBuddyBot,
                       self.source_player.actor.node.position,
                       2.0, self.setup_bunny)

    def start_moving_bunnies(self) -> None:
        self._bot_update_timer = ba.Timer(0.05,
                                          ba.WeakCall(self._bupdate),
                                          repeat=True)

    def _spawn_bot(self, bot_type: Type[SpazBot], pos: Sequence[float],
                   on_spawn_call: Optional[Callable[[SpazBot], Any]]) -> None:
        spaz = bot_type(self.source_player)
        ba.playsound(self._spawn_sound, position=pos)
        assert spaz.node
        spaz.node.handlemessage('flash')
        spaz.node.is_area_of_interest = False
        spaz.handlemessage(ba.StandMessage(pos, random.uniform(0, 360)))
        self.add_bot(spaz)
        self._spawning_count -= 1
        if on_spawn_call is not None:
            on_spawn_call(spaz)

    def _bupdate(self) -> None:

        # Update one of our bot lists each time through.
        # First off, remove no-longer-existing bots from the list.
        try:
            bot_list = self._bot_lists[self._bot_update_list] = ([
                b for b in self._bot_lists[self._bot_update_list] if b
            ])
        except Exception:
            bot_list = []
            ba.print_exception('Error updating bot list: ' +
                               str(self._bot_lists[self._bot_update_list]))
        self._bot_update_list = (self._bot_update_list +
                                 1) % self._bot_list_count

        # Update our list of player points for the bots to use.
        player_pts = []

        try:
            for n in ba.getnodes():
                if n.getnodetype() == 'spaz':
                    s = n.getdelegate(object)
                    session = _ba.get_foreground_host_session()
                    if isinstance(s, SpazBot):
                        if not s in self.get_living_bots():
                            if hasattr(s, 'source_player'):
                                if not s.source_player is self.source_player:
                                    if (isinstance(
                                            session, ba.DualTeamSession)):
                                        if not s.source_player.team is (
                                                self.team):
                                            player_pts.append((
                                                ba.Vec3(n.position),
                                                ba.Vec3(n.velocity)))
                                    else:
                                        player_pts.append((
                                            ba.Vec3(n.position),
                                            ba.Vec3(n.velocity)))
                            else:
                                player_pts.append((
                                    ba.Vec3(n.position),
                                    ba.Vec3(n.velocity)))
                    elif isinstance(s, PlayerSpaz):
                        player = s.getplayer(ba.Player, True)
                        if (isinstance(session, ba.DualTeamSession)):
                            if not player is self.source_player:
                                if not player.team is self.team:
                                    player_pts.append((
                                        ba.Vec3(n.position),
                                        ba.Vec3(n.velocity)))
                        else:
                            if not player is self.source_player:
                                player_pts.append((
                                    ba.Vec3(n.position),
                                    ba.Vec3(n.velocity)))

        except Exception:
            ba.print_exception('Error on bot-set _update.')

        for bot in bot_list:
            bot.set_player_points(player_pts)
            bot.update_ai()

    def setup_bunny(self, spaz) -> None:
        spaz.source_player = self.source_player
        spaz.color = self.source_player.color
        spaz.highlight = self.source_player.highlight
        self.set_bunny_text(spaz)

    def set_bunny_text(self, spaz) -> None:
        m = ba.newnode('math',
                       owner=spaz.node,
                       attrs={'input1': (0, 0.7, 0),
                              'operation': 'add'})
        spaz.node.connectattr('position', m, 'input2')
        spaz._bunny_text = ba.newnode(
            'text',
            owner=spaz.node,
            attrs={'text': self.source_player.getname(),
                   'in_world': True,
                   'shadow': 1.0,
                   'flatness': 1.0,
                   'color': self.source_player.color,
                   'scale': 0.0,
                   'h_align': 'center'})
        m.connectattr('output', spaz._bunny_text, 'position')
        ba.animate(spaz._bunny_text, 'scale', {0: 0.0, 1.0: 0.01})

class NewPowerupBox(ba.Actor):
    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 poweruptype: str = 'triple_bombs',
                 expire: bool = True):
        super().__init__()
        shared = SharedObjects.get()
        factory = PowerupBoxFactory.get()
        self.poweruptype = poweruptype
        self._powersgiven = False
        bunny = False

        if poweruptype == 'triple_bombs':
            tex = factory.tex_bomb
        elif poweruptype == 'punch':
            tex = factory.tex_punch
        elif poweruptype == 'ice_bombs':
            tex = factory.tex_ice_bombs
        elif poweruptype == 'impact_bombs':
            tex = factory.tex_impact_bombs
        elif poweruptype == 'land_mines':
            tex = factory.tex_land_mines
        elif poweruptype == 'sticky_bombs':
            tex = factory.tex_sticky_bombs
        elif poweruptype == 'shield':
            tex = factory.tex_shield
        elif poweruptype == 'health':
            tex = factory.tex_health
        elif poweruptype == 'curse':
            tex = factory.tex_curse
        elif poweruptype == 'bunny':
            bunny = True
            tex = ba.gettexture('eggTex1')
        else:
            raise ValueError('invalid poweruptype: ' + str(poweruptype))

        if len(position) != 3:
            raise ValueError('expected 3 floats for position')

        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'body': 'capsule' if bunny else 'box',
                'body_scale': 0.85 if bunny else 1.0,
                'position': position,
                'model': ba.getmodel('egg') if bunny else factory.model,
                'light_model': None if bunny else factory.model_simple,
                'shadow_size': 0.3 if bunny else 0.5,
                'color_texture': tex,
                'reflection': 'powerup',
                'reflection_scale': [1.5] if bunny else [1.0],
                'materials': (factory.powerup_material,
                              shared.object_material)
            })  # yapf: disable

        # Animate in.
        curve = ba.animate(self.node, 'model_scale',
            {0: 0, 0.14: 0.9, 0.2: 0.7} if bunny
            else {0: 0, 0.14: 1.6, 0.2: 1})

        ba.timer(0.2, curve.delete)

        if expire:
            ba.timer(DEFAULT_POWERUP_INTERVAL - 2.5,
                     ba.WeakCall(self._start_flashing))
            ba.timer(DEFAULT_POWERUP_INTERVAL - 1.0,
                     ba.WeakCall(self.handlemessage, ba.DieMessage()))

    def _start_flashing(self) -> None:
        if self.node:
            self.node.flashing = True

    def handlemessage(self, msg: Any) -> Any:
        assert not self.expired

        if isinstance(msg, ba.PowerupAcceptMessage):
            factory = PowerupBoxFactory.get()
            assert self.node
            if self.poweruptype == 'health':
                ba.playsound(factory.health_powerup_sound,
                             3,
                             position=self.node.position)
            ba.playsound(factory.powerup_sound, 3, position=self.node.position)
            self._powersgiven = True
            self.handlemessage(ba.DieMessage())

        elif isinstance(msg, _TouchedMessage):
            if not self._powersgiven:
                node = ba.getcollision().opposingnode
                if node is not None and node:
                    if self.poweruptype == 'bunny':
                        p = node.getdelegate(
                            PlayerSpaz, True).getplayer(ba.Player, True)
                        if 'bunnies' not in p.customdata:
                            p.customdata['bunnies'] = BunnyBotSet(p)
                        p.customdata['bunnies'].do_bunny()
                        self._powersgiven = True
                        self.handlemessage(ba.DieMessage())
                    else:
                        node.handlemessage(
                            ba.PowerupMessage(self.poweruptype,
                                              sourcenode=self.node))

        elif isinstance(msg, ba.DieMessage):
            if self.node:
                if msg.immediate:
                    self.node.delete()
                else:
                    ba.animate(self.node, 'model_scale', {0: 1, 0.1: 0})
                    ba.timer(0.1, self.node.delete)

        elif isinstance(msg, ba.OutOfBoundsMessage):
            self.handlemessage(ba.DieMessage())

        elif isinstance(msg, ba.HitMessage):
            # Don't die on punches (that's annoying).
            if msg.hit_type != 'punch':
                self.handlemessage(ba.DieMessage())
        else:
            return super().handlemessage(msg)
        return None

def new_powerup_distribution() -> Sequence[Tuple[str, int]]:
    """Standard set of powerups."""
    return (('triple_bombs', 3), ('ice_bombs', 3), ('punch', 3),
            ('impact_bombs', 3), ('land_mines', 2), ('sticky_bombs', 3),
            ('shield', 2), ('health', 1), ('curse', 1), ('bunny', 30))

def _standard_drop_powerup(self, index: int, expire: bool = True) -> None:
    # pylint: disable=cyclic-import
    from bastd.actor.powerupbox import PowerupBox, PowerupBoxFactory
    NewPowerupBox(
        position=self.map.powerup_spawn_points[index],
        poweruptype=PowerupBoxFactory.get().get_random_powerup_type(),
        expire=expire).autoretain()

def _drop_powerup(self, index: int, poweruptype: str = None) -> None:
    poweruptype = (PowerupBoxFactory.get().get_random_powerup_type(
        forcetype=poweruptype, excludetypes=self._excluded_powerups))
    NewPowerupBox(position=self.map.powerup_spawn_points[index],
               poweruptype=poweruptype).autoretain()

def _drop_powerup2(self, index: int, poweruptype: str = None) -> None:
    if poweruptype is None:
        poweruptype = (PowerupBoxFactory.get().get_random_powerup_type(
            excludetypes=self._exclude_powerups))
    NewPowerupBox(position=self.map.powerup_spawn_points[index],
               poweruptype=poweruptype).autoretain()

def _drop_powerup3(self, index: int, poweruptype: str = None) -> None:
    if poweruptype is None:
        poweruptype = (PowerupBoxFactory.get().get_random_powerup_type(
            excludetypes=self._excludepowerups))
    NewPowerupBox(position=self.map.powerup_spawn_points[index],
               poweruptype=poweruptype).autoretain()

def _drop_powerups(self,
                   standard_points: bool = False,
                   poweruptype: str = None) -> None:
    """Generic powerup drop."""
    if standard_points:
        points = self.map.powerup_spawn_points
        for i in range(len(points)):
            ba.timer(
                1.0 + i * 0.5,
                ba.WeakCall(self._drop_powerup, i,
                            poweruptype if i == 0 else None))
    else:
        point = (self._powerup_center[0] + random.uniform(
            -1.0 * self._powerup_spread[0], 1.0 * self._powerup_spread[0]),
                 self._powerup_center[1],
                 self._powerup_center[2] + random.uniform(
                     -self._powerup_spread[1], self._powerup_spread[1]))

        # Drop one random one somewhere.
        NewPowerupBox(
            position=point,
            poweruptype=PowerupBoxFactory.get().get_random_powerup_type(
                excludetypes=self._excluded_powerups)).autoretain()

def _drop_powerups2(self,
                   standard_points: bool = False,
                   poweruptype: str = None) -> None:
    """Generic powerup drop."""
    if standard_points:
        spawnpoints = self.map.powerup_spawn_points
        for i, _point in enumerate(spawnpoints):
            ba.timer(1.0 + i * 0.5,
                     ba.Call(self._drop_powerup, i, poweruptype))
    else:
        point = (self._powerup_center[0] + random.uniform(
            -1.0 * self._powerup_spread[0], 1.0 * self._powerup_spread[0]),
                 self._powerup_center[1],
                 self._powerup_center[2] + random.uniform(
                     -self._powerup_spread[1], self._powerup_spread[1]))

        # Drop one random one somewhere.
        NewPowerupBox(
            position=point,
            poweruptype=PowerupBoxFactory.get().get_random_powerup_type(
                excludetypes=self._exclude_powerups)).autoretain()

def _drop_powerups3(self,
                   standard_points: bool = False,
                   force_first: str = None) -> None:
    """Generic powerup drop."""
    from bastd.actor import powerupbox
    if standard_points:
        pts = self.map.powerup_spawn_points
        for i in range(len(pts)):
            ba.timer(
                1.0 + i * 0.5,
                ba.WeakCall(self._drop_powerup, i,
                            force_first if i == 0 else None))
    else:
        drop_pt = (self._powerup_center[0] + random.uniform(
            -1.0 * self._powerup_spread[0], 1.0 * self._powerup_spread[0]),
                   self._powerup_center[1],
                   self._powerup_center[2] + random.uniform(
                       -self._powerup_spread[1], self._powerup_spread[1]))

        # Drop one random one somewhere.
        NewPowerupBox(
            position=drop_pt,
            poweruptype=PowerupBoxFactory.get().get_random_powerup_type(
                excludetypes=self._excludepowerups)).autoretain()

# ba_meta export plugin
class BuddyBunnyPlugin(ba.Plugin):

    internal.get_default_powerup_distribution = new_powerup_distribution
    ba._powerup.get_default_powerup_distribution = new_powerup_distribution
    powerupbox.PowerupBox = NewPowerupBox
    GameActivity._standard_drop_powerup = _standard_drop_powerup
    OnslaughtGame._drop_powerup = _drop_powerup
    OnslaughtGame._drop_powerups = _drop_powerups
    FootballCoopGame._drop_powerup = _drop_powerup2
    FootballCoopGame._drop_powerups = _drop_powerups2
    RunaroundGame._drop_powerup = _drop_powerup2
    RunaroundGame._drop_powerups = _drop_powerups2
    TheLastStandGame._drop_powerup = _drop_powerup3
    TheLastStandGame._drop_powerups = _drop_powerups3
