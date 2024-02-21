from bastd.actor.playerspaz import *
import ba
import bastd
from bastd.actor.spazfactory import SpazFactory
import functools
import random
from typing import List, Sequence, Optional, Dict, Any
import setting
from playersData import pdata
from stats import mystats
_settings = setting.get_settings_data()

RANK_EFFECT_MAP = {
    1: ["fairydust"],
    2: ["sweat"],
    3: ["metal"],
    4: ["iceground"],
}
def effect(repeat_interval=0):
    def _activator(method):
        @functools.wraps(method)
        def _inner_activator(self, *args, **kwargs):
            def _caller():
                try:
                    method(self, *args, **kwargs)
                except:
                    if self is None or not self.is_alive() or not self.node.exists():
                        self._activations = []
                    else:
                        raise
            effect_activation = ba.Timer(repeat_interval, ba.Call(_caller), repeat=repeat_interval > 0)
            self._activations.append(effect_activation)
        return _inner_activator
    return _activator


def node(check_interval=0):
    def _activator(method):
        @functools.wraps(method)
        def _inner_activator(self):
            node = method(self)
            def _caller():
                if self is None or not self.is_alive() or not self.node.exists():
                    node.delete()
                    self._activations = []
            node_activation = ba.Timer(check_interval, ba.Call(_caller), repeat=check_interval > 0)
            try:
                self._activations.append(node_activation)
            except AttributeError:
                pass
        return _inner_activator
    return _activator


class NewPlayerSpaz(PlayerSpaz):
    def __init__(self,
                 player: ba.Player,
                 color: Sequence[float],
                 highlight: Sequence[float],
                 character: str,
                 powerups_expire: bool = True,
                 *args,
                 **kwargs):

        super().__init__(player=player,
                         color=color,
                         highlight=highlight,
                         character=character,
                         powerups_expire=powerups_expire,
                         *args,
                         **kwargs)
        self._activations = []
        self.effects = []

        ba._asyncio._asyncio_event_loop.create_task(self.set_effects())

    async def set_effects(self):
        account_id = self._player._sessionplayer.get_v1_account_id()
        custom_effects = pdata.get_custom()['customeffects']
        paid_effects = pdata.get_custom()['paideffects']

        if account_id in paid_effects:
            self.effects = [paid_effects[account_id]['effect']] if type(paid_effects[account_id]['effect']) is str else paid_effects[account_id]['effect']
        elif account_id  in custom_effects:      
            self.effects = [custom_effects[account_id]] if type(custom_effects[account_id]) is str else custom_effects[account_id]
        else:
            #  check if we have any effect for his rank.
            if _settings['enablestats']:
                stats = mystats.get_cached_stats()
                if account_id in stats and _settings['enableTop5effects']:
                    rank = stats[account_id]["rank"]
                    self.effects = RANK_EFFECT_MAP[rank] if rank in RANK_EFFECT_MAP else []



        if len(self.effects) == 0:
            return

        self._effect_mappings = {
            "spark": self._add_spark,
            "sparkground": self._add_sparkground,
            "sweat": self._add_sweat,
            "sweatground": self._add_sweatground,
            "distortion": self._add_distortion,
            "glow": self._add_glow,
            "shine": self._add_shine,
            "highlightshine": self._add_highlightshine,
            "scorch": self._add_scorch,
            "ice": self._add_ice,
            "iceground": self._add_iceground,
            "slime": self._add_slime,
            "metal": self._add_metal,
            "splinter": self._add_splinter,
            "rainbow": self._add_rainbow,
            "fairydust": self._add_fairydust,
            "noeffect": lambda: None,
            "fire":self._add_fire,
            "stars":self._add_stars,
            "new_rainbow":self._add_new_rainbow,
            "footprint": self._add_footprint,
            "chispitas": self._add_chispitas,
            "darkmagic": self._add_darkmagic,
            "colourfullspark": self._add_colorful_spark,
            "ring": self._add_aure,
            "brust": self._add_galactic_burst
        }

        for effect in self.effects:
            trigger = self._effect_mappings[effect] if effect in self._effect_mappings else lambda: None
            activity = self._activity()
            if activity:
                with ba.Context(self._activity()):
                    trigger()

    @effect(repeat_interval=0.1)
    def _add_spark(self):
        ba.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 10),
            scale=0.5,
            spread=0.2,
            chunk_type="spark",
        )

    @effect(repeat_interval= 1.0)   
    def _add_colorful_spark(self) -> None:
        ba.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 10),
            scale=0.8,
            spread=0.2,
            chunk_type="spark",
        )
        ba.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 7),
            scale=0.4,
            spread=0.2,
            chunk_type="sweat",
            emit_type="stickers",
        )
        keys = {
             0.0: (2.0, 0.0, 0.0),
             0.2: (2.0, 1.5, 0.5),
             0.4: (2.0, 2.0, 0.0),
             0.6: (0.0, 2.0, 0.0),
             0.8: (0.0, 2.0, 2.0),
             1.0: (0.0, 0.0, 2.0),
            }.items()

        def _changecolor(color: Sequence[float]) -> None:
            if self.node.exists():
                self.node.color = color

        for time, color in keys:
            ba.timer(time, ba.Call(_changecolor, color))
  
    @effect(repeat_interval=0.1)
    def _add_sparkground(self):
        ba.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 5),
            scale=0.2,
            spread=0.1,
            chunk_type="spark",
            emit_type="stickers",
        )

    @effect(repeat_interval=0.04)
    def _add_sweat(self):
        velocity = 4.0
        calculate_position = lambda torso_position: torso_position - 0.25 + random.uniform(0, 0.5)
        calculate_velocity = lambda node_velocity, multiplier: random.uniform(-velocity, velocity) + node_velocity * multiplier
        position = tuple(calculate_position(coordinate)
                         for coordinate in self.node.torso_position)
        velocity = (
            calculate_velocity(self.node.velocity[0], 2),
            calculate_velocity(self.node.velocity[1], 4),
            calculate_velocity(self.node.velocity[2], 2),
        )
        ba.emitfx(
            position=position,
            velocity=velocity,
            count=10,
            scale=random.uniform(0.3, 1.4),
            spread=0.2,
            chunk_type="sweat",
        )

    @effect(repeat_interval=0.04)
    def _add_sweatground(self):
        velocity = 1.2
        calculate_position = lambda torso_position: torso_position - 0.25 + random.uniform(0, 0.5)
        calculate_velocity = lambda node_velocity, multiplier: random.uniform(-velocity, velocity) + node_velocity * multiplier
        position = tuple(calculate_position(coordinate)
                         for coordinate in self.node.torso_position)
        velocity = (
            calculate_velocity(self.node.velocity[0], 2),
            calculate_velocity(self.node.velocity[1], 4),
            calculate_velocity(self.node.velocity[2], 2),
        )
        ba.emitfx(
            position=position,
            velocity=velocity,
            count=10,
            scale=random.uniform(0.1, 1.2),
            spread=0.1,
            chunk_type="sweat",
            emit_type="stickers",
        )

    @effect(repeat_interval=1.0)
    def _add_distortion(self):
        ba.emitfx(
            position=self.node.position,
            spread=1.0,
            emit_type="distortion"
        )
        ba.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 5),
            emit_type="tendrils",
            tendril_type="smoke",
        )

    @effect(repeat_interval=3.0)
    def _add_shine(self):
        shine_factor = 1.2
        dim_factor = 0.90

        default_color = self.node.color
        shiny_color = tuple(channel * shine_factor for channel in default_color)
        dimmy_color = tuple(channel * dim_factor for channel in default_color)
        animation = {
            0: default_color,
            1: dimmy_color,
            2: shiny_color,
            3: default_color,
        }
        ba.animate_array(self.node, "color", 3, animation)

    @effect(repeat_interval=9.0)
    def _add_highlightshine(self):
        shine_factor = 1.2
        dim_factor = 0.90

        default_highlight = self.node.highlight
        shiny_highlight = tuple(channel * shine_factor for channel in default_highlight)
        dimmy_highlight = tuple(channel * dim_factor for channel in default_highlight)
        animation = {
            0: default_highlight,
            3: dimmy_highlight,
            6: shiny_highlight,
            9: default_highlight,
        }
        ba.animate_array(self.node, "highlight", 3, animation)

    @effect(repeat_interval=0.05)
    def _add_rainbow(self):
    # Increase intensity by multiplying each component by a factor
        intensity_factor = 8.0
        highlight = tuple(component * intensity_factor for component in (random.random() for _ in range(3)))
    
    # Ensure the values are within the valid color range
        highlight = ba.safecolor(highlight)

        animation = {
            0: self.node.highlight,
            2: highlight,
        }
        ba.animate_array(self.node, "highlight", 3, animation)



    @node(check_interval=0.5)
    def _add_glow(self):
        glowing_light = ba.newnode(
            "light",
            attrs={
                "color": (1.0, 0.4, 0.5),
                "height_attenuated": False,
                "radius": 0.4}
            )
        self.node.connectattr("position", glowing_light, "position")
        ba.animate(
            glowing_light,
            "intensity",
            {0: 0.0, 1: 0.2, 2: 0.0},
            loop=True)
        return glowing_light

    @node(check_interval=0.5)
    def _add_scorch(self):
        scorcher = ba.newnode(
            "scorch",
            attrs={
                "position": self.node.position,
                "size": 1.00,
                "big": True}
            )
        self.node.connectattr("position", scorcher, "position")
        animation = {
            0: (1,0,0),
            1: (0,1,0),
            2: (1,0,1),
            3: (0,1,1),
            4: (1,0,0),
        }
        ba.animate_array(scorcher, "color", 3, animation, loop=True)
        return scorcher

    @effect(repeat_interval=0.5)
    def _add_ice(self):
        ba.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(2, 8),
            scale=0.4,
            spread=0.2,
            chunk_type="ice",
        )

    @effect(repeat_interval=0.05)
    def _add_iceground(self):
        ba.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 2),
            scale=random.uniform(0, 0.5),
            spread=1.0,
            chunk_type="ice",
            emit_type="stickers",
        )

    @effect(repeat_interval=0.25)
    def _add_slime(self):
        ba.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 10),
            scale=0.4,
            spread=0.2,
            chunk_type="slime",
        )

    @effect(repeat_interval=0.25)
    def _add_metal(self):
        ba.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 4),
            scale=0.4,
            spread=1,
            chunk_type="metal",
        )

    @effect(repeat_interval=0.75)
    def _add_splinter(self):
        ba.emitfx(
            position=self.node.position,
            velocity=self.node.velocity,
            count=random.randint(1, 5),
            scale=0.5,
            spread=0.2,
            chunk_type="splinter",
        )

    @effect(repeat_interval=0.001)
    def _add_fairydust(self):
        velocity = 2
        calculate_position = lambda torso_position: torso_position - 0.25 + random.uniform(0, 0.5)
        calculate_velocity = lambda node_velocity, multiplier: random.uniform(-velocity, velocity) + node_velocity * multiplier
        position = tuple(calculate_position(coordinate) for coordinate in self.node.torso_position)
        velocity = (
                    calculate_velocity(self.node.velocity[0], 6),
                    calculate_velocity(self.node.velocity[1], 8),
                    calculate_velocity(self.node.velocity[2], 8),
    )
        ba.emitfx(
                position=position,
                velocity=velocity,
                count=random.randint(100,200),
                spread=8.5,
                emit_type="fairydust",
    )
    
    
    @effect(repeat_interval=0.1)
    def _add_fire(self) -> None:
        if not self.node.exists():
            self._cm_effect_timer = None
        else:
            ba.emitfx(position=self.node.position,
            scale=3,count=50*2,spread=0.3,
            chunk_type='sweat')

    @effect(repeat_interval=0.1)
    def _add_stars(self) -> None:
        def die(node: ba.Node) -> None:
            if node:
                m = node.model_scale
                ba.animate(node, 'model_scale', {0: m, 0.1: 0})
                ba.timer(0.1, node.delete)

        if not self.node.exists() or self._dead:
            self._cm_effect_timer = None
        else:
            c = 0.3
            pos_list = [
                (c, 0, 0), (0, 0, c),
                (-c, 0, 0), (0, 0, -c)]
            
            for p in pos_list:
                m= 1.5
                np = self.node.position
                pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
                vel = (random.uniform(-m, m), random.uniform(2, 7), random.uniform(-m, m))

                texs = ['bombStickyColor', 'aliColor', 'aliColorMask', 'eggTex3']
                tex = ba.gettexture(random.choice(texs))
                mesh = ba.getmodel('flash')
                factory = SpazFactory.get()

                mat = ba.Material()
                mat.add_actions(
                    conditions=('they_have_material', factory.punch_material),
                    actions=(
                        ('modify_part_collision', 'collide', False),
                        ('modify_part_collision', 'physical', False),
                    ))
                node = ba.newnode('prop',
                                owner=self.node,
                                attrs={'body': 'sphere',
                                       'position': pos,
                                        'velocity': vel,
                                        'model': mesh,
                                        'model_scale': 0.1,
                                        'body_scale': 0.0,
                                        'shadow_size': 0.0,
                                        'gravity_scale': 0.5,
                                        'color_texture': tex,
                                        'reflection': 'soft',
                                        'reflection_scale': [1.5],
                                        'materials': [mat]})
                light = ba.newnode('light',
                                   owner=node,
                                   attrs={
                                       'intensity': 0.3,
                                       'volume_intensity_scale': 0.5,
                                       'color': (random.uniform(0.5, 1.5),
                                                 random.uniform(0.5, 1.5),
                                                 random.uniform(0.5, 1.5)),
                                        'radius': 0.035})
                node.connectattr('position', light, 'position')
                ba.timer(0.25, ba.Call(die, node))

    @effect(repeat_interval= 1.0)   
    def _add_new_rainbow(self) -> None:
        keys = {
             0.0: (2.0, 0.0, 0.0),
             0.2: (2.0, 1.5, 0.5),
             0.4: (2.0, 2.0, 0.0),
             0.6: (0.0, 2.0, 0.0),
             0.8: (0.0, 2.0, 2.0),
             1.0: (0.0, 0.0, 2.0),
            }.items()

        def _changecolor(color: Sequence[float]) -> None:
            if self.node.exists():
                self.node.color = color

        for time, color in keys:
            ba.timer(time, ba.Call(_changecolor, color))
   
    @effect(repeat_interval=0.5) 
    def _add_footprint(self) -> None:
        if not self.node.exists():
            self._cm_effect_timer = None
        else:
            loc = ba.newnode('locator', owner=self.node,
              attrs={
                     'position': self.node.position,
                     'shape': 'circle',
                     'color': self.node.color,
                     'size': [0.2],
                     'draw_beauty': False,
                     'additive': False})
            ba.animate(loc, 'opacity', {0: 1.0, 1.9: 0.0})
            ba.timer(2.0, loc.delete)
            
    @effect(repeat_interval=0.2)
    def _add_chispitas(self) -> None:
        def die(node: ba.Node) -> None:
            if node:
                m = node.model_scale
                ba.animate(node, 'model_scale', {0: m, 0.1: 0})
                ba.timer(0.1, node.delete)

        if not self.node.exists() or self._dead:
            self._cm_effect_timer = None
        else:
            c = 0.3
            pos_list = [
                (c, 0, 0), (0, 0, c),
                (-c, 0, 0), (0, 0, -c)]
            
            for p in pos_list:
                m= 1.5
                np = self.node.position
                pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
                vel = (random.uniform(-m, m), random.uniform(2, 7), random.uniform(-m, m))

                tex = ba.gettexture('null')
                mesh = None
                factory = SpazFactory.get()

                mat = ba.Material()
                mat.add_actions(
                    conditions=('they_have_material', factory.punch_material),
                    actions=(
                        ('modify_part_collision', 'collide', False),
                        ('modify_part_collision', 'physical', False),
                    ))
                node = ba.newnode('bomb',
                                owner=self.node,
                                attrs={'body': 'sphere',
                                       'position': pos,
                                        'velocity': vel,
                                        'model': mesh,
                                        'model_scale': 0.1,
                                        'body_scale': 0.0,
                                        'color_texture': tex,
                                        'fuse_length': 0.1,
                                        'materials': [mat]})
                light = ba.newnode('light',
                                   owner=node,
                                   attrs={
                                       'intensity': 0.3,
                                       'volume_intensity_scale': 0.5,
                                       'color': (random.uniform(0.5, 1.5),
                                                 random.uniform(0.5, 1.5),
                                                 random.uniform(0.5, 1.5)),
                                        'radius': 0.035})
                node.connectattr('position', light, 'position')
                ba.timer(0.25, ba.Call(die, node)) 



    @effect(repeat_interval=0.1)
    def _add_darkmagic(self) -> None:
        def die(node: ba.Node) -> None:
            if node:
                m = node.model_scale
                ba.animate(node, 'model_scale', {0: m, 0.1: 0})
                ba.timer(0.1, node.delete)

        if not self.node.exists() or self._dead:
            self._cm_effect_timer = None
        else:
            c = 0.3
            pos_list = [
                (c, 0, 0), (0, 0, c),
                (-c, 0, 0), (0, 0, -c)]
            
            for p in pos_list:
                m= 1.5
                np = self.node.position
                pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
                vel = (random.uniform(-m, m), 30.0, random.uniform(-m, m))

                tex = ba.gettexture('impactBombColor')
                mesh = ba.getmodel('impactBomb')
                factory = SpazFactory.get()

                mat = ba.Material()
                mat.add_actions(
                    conditions=('they_have_material', factory.punch_material),
                    actions=(
                        ('modify_part_collision', 'collide', False),
                        ('modify_part_collision', 'physical', False),
                    ))
                node = ba.newnode('prop',
                                owner=self.node,
                                attrs={'body': 'sphere',
                                       'position': pos,
                                        'velocity': vel,
                                        'model': mesh,
                                        'model_scale': 0.4,
                                        'body_scale': 0.0,
                                        'shadow_size': 0.0,
                                        'gravity_scale': 0.5,
                                        'color_texture': tex,
                                        'reflection': 'soft',
                                        'reflection_scale': [0.0],
                                        'materials': [mat]})
                light = ba.newnode('light',
                                   owner=node,
                                   attrs={
                                       'intensity': 3.1,
                                       'volume_intensity_scale': 1.3,
                                       'color': (0.5, 0.0, 1.0),
                                       'radius': 0.035})
                node.connectattr('position', light, 'position')
                ba.timer(0.25, ba.Call(die, node)) 

    @effect(repeat_interval=0.3)
    def _add_aure(self) -> None:
        def anim(node: ba.Node) -> None:
            ba.animate_array(node, 'color', 3,
                {0: (1,1,0), 0.1: (0,1,0),
                 0.2: (1,0,0), 0.3: (0,0.5,1),
                 0.4: (1,0,1)}, loop=True)
            ba.animate_array(node, 'size', 1,
                {0: [1.0], 0.2: [1.5], 0.3: [1.0]}, loop=True)

        attrs = ['torso_position', 'position_center', 'position']
        for i, pos in enumerate(attrs):
            loc = ba.newnode('locator', owner=self.node,
                  attrs={'shape': 'circleOutline',
                         'color': self.node.color,
                         'opacity': 1.0,
                         'draw_beauty': True,
                         'additive': False})
            self.node.connectattr(pos, loc, 'position')
            ba.timer(0.1 * i, ba.Call(anim, loc))
       

    @effect(repeat_interval=1.5)
    def _add_galactic_burst(self) -> None:
        def die(node: ba.Node) -> None:
            if node:
                m = node.model_scale
                ba.animate(node, 'model_scale', {0: m, 0.1: 0})
                ba.timer(0.1, node.delete)

        if not self.node.exists() or self._dead:
            self._cm_effect_timer = None
        else:
            c = 0.3
            pos_list = [
                (c, 0, 0), (0, 0, c),
                (-c, 0, 0), (0, 0, -c)]

            for p in pos_list:
                m = 1.5
                np = self.node.position
                pos = (np[0] + p[0], np[1] + p[1] + 0.0, np[2] + p[2])
                vel = (random.uniform(-m, m), random.uniform(2, 7), random.uniform(-m, m))

                tex = ba.gettexture('bombStickyColor')
                mesh = ba.getmodel('flash')
                factory = SpazFactory.get()

                mat = ba.Material()
                mat.add_actions(
                    conditions=('they_have_material', factory.punch_material),
                    actions=(
                        ('modify_part_collision', 'collide', False),
                        ('modify_part_collision', 'physical', False),
                    ))
                node = ba.newnode('prop',
                                  owner=self.node,
                                  attrs={'body': 'sphere',
                                         'position': pos,
                                         'velocity': vel,
                                         'model': mesh,
                                         'model_scale': 0.1,
                                         'body_scale': 0.0,
                                         'shadow_size': 0.0,
                                         'gravity_scale': 0.5,
                                         'color_texture': tex,
                                         'reflection': 'soft',
                                         'reflection_scale': [1.5],
                                         'materials': [mat]})
                light = ba.newnode('light',
                                   owner=node,
                                   attrs={
                                       'intensity': 0.3,
                                       'volume_intensity_scale': 0.5,
                                       'color': (random.uniform(0.5, 1.5),
                                                 random.uniform(0.5, 1.5),
                                                 random.uniform(0.5, 1.5)),
                                       'radius': 0.035})
                node.connectattr('position', light, 'position')
                ba.timer(0.25, ba.Call(die, node))

            keys = {
                0.0: (2.0, 0.0, 0.0),
                0.2: (2.0, 1.5, 0.5),
                0.4: (2.0, 2.0, 0.0),
                0.6: (0.0, 2.0, 0.0),
                0.8: (0.0, 2.0, 2.0),
                1.0: (0.0, 0.0, 2.0),
            }.items()

            def _changecolor(color: Sequence[float]) -> None:
                if self.node.exists():
                    self.node.color = color

            for time, color in keys:
                ba.timer(time, ba.Call(_changecolor, color))


def apply() -> None:
    bastd.actor.playerspaz.PlayerSpaz = NewPlayerSpaz
