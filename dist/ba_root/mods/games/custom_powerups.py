# ba_meta require api 7

"""
    Custom Powerups by EmperorR(NULL)
"""

from __future__ import annotations
from typing import TYPE_CHECKING

import ba
import bastd
from random import choice, random, randrange
from bastd.actor.bomb import (Blast,
       ExplodeMessage, ArmMessage, BombFactory,
       WarnMessage, ImpactMessage, ExplodeHitMessage,
       )
from bastd.actor.popuptext import PopupText
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import NoReturn, Sequence, Any, Callable 

def get_custom_powerups() -> dict[str, int]:
    """ custom powerups """
    powerups = {
       'random': 1,
       'fake': 1,
       'ice_impact_bombs': 2,
       'ice_mines': 2,
       'invisible': 2,
    }
    return powerups

# ba_meta export plugin
class Plugin(ba.Plugin): 
     
    # Here we use the decorators to add extra code in original fuction
    def pbx_factory_new_init(func):
        def wrapper(*args):
            # Original code.
            func(*args)
            
            custom_powerups: dict[str, int] = get_custom_powerups()
            
            # in original code all power randomly picked up from self._powerupdist list attribute
            # so we just need to add our custom power in "self._powerupdist" list
            for powerup in custom_powerups:
                 for _ in range(int(custom_powerups[powerup])):
                     args[0]._powerupdist.append(powerup)
            
        return wrapper
    
    # replace orignal one to custom one
    bastd.actor.powerupbox.PowerupBoxFactory.__init__ = pbx_factory_new_init(bastd.actor.powerupbox.PowerupBoxFactory.__init__)
    
    # Here we make our boxes for our custom powerups.
    # With help of decorators.
    def pbx_new_init(func):
        def wrapper(*args, **kwargs):
            
            new_powerup: str | None = None
            # Checking if poweruptype is a custom to avoid error from original code
            # Need to check that because for original code our powerup is invalid 
            if kwargs['poweruptype'] in get_custom_powerups():
                
                new_powerup = kwargs['poweruptype']
                # Changing the value of custom to default to avoid error from else statement in original code
                kwargs['poweruptype'] = 'triple_bombs'
            
            # Orignal code
            # this orignal code create box for as 
            func(*args, **kwargs)
            
            if new_powerup is not None:
                # Replace default to custom 
                args[0].poweruptype  =  new_powerup
               
                # texturing default powerupbox to custom
                if args[0].poweruptype == 'random':
                    args[0].node.color_texture = ba.gettexture('achievementEmpty')
                    
                elif args[0].poweruptype == 'ice_impact_bombs':
                    args[0].node.color_texture = ba.gettexture('bombColorIce')
                
                elif args[0].poweruptype == 'ice_mines':
                    args[0].node.color_texture = ba.gettexture('achievementMine')
                    
                elif args[0].poweruptype == 'invisible':
                    args[0].node.color_texture = ba.gettexture('empty')
                    
                elif args[0].poweruptype == 'fake':
                    fake_tex = (
                        'powerupBomb',
                        'powerupPunch',
                        'powerupShield',
                        'powerupStickyBombs',
                        'powerupImpactBombs',
                        'powerupIceBombs',
                        'powerupHealth',
                        'powerupLandMines',
                        'bombColorIce',
                        'achievementMine',
                    )
                    args[0].node.color_texture = ba.gettexture(choice(fake_tex))
            
            # if powertype is default we do Nothing 
        return wrapper

    # replace original one to custom one
    bastd.actor.powerupbox.PowerupBox.__init__ = pbx_new_init(bastd.actor.powerupbox.PowerupBox.__init__)
    
    # adding some attributes in Spaz __init__ function that we need
    def spaz_new_init(func):
        def wrapper(*args, **kwargs):
        
            # original code
            func(*args, **kwargs)
            
            args[0].bomb_counter: int = 0
            args[0].last_bomb_count: int | None = None
            args[0].last_counter_tex: ba.Texture | None = None
            
            args[0].invisible_wear_off_flash_timer: ba.Timer | None = None
            args[0].invisible_wear_off_timer: ba.Timer | None = None
            args[0].invisible: bool = False
            
            
        return wrapper
    # replace original one to custome one
    bastd.actor.spaz.Spaz.__init__ = spaz_new_init(bastd.actor.spaz.Spaz.__init__)

    # Spaz 
    def spaz_new_handlemessage(func):
        def wrapper(*args, **kwargs):
            # only rect to ba.PowerupMessage
            if isinstance(args[1], ba.PowerupMessage):
                    
                    if args[1].poweruptype == 'random':
                        # Only Postive powerups
                        powerups = (
                            'health',
                            'ice_bombs',
                            'impact_bombs',
                            'sticky_bombs',
                            'punch',
                            'shield',
                            'ice_impact_bombs',
                            'ice_mine',
                            'invisible',
                        )
                        random_powerup = choice(powerups)
                        args[0].node.handlemessage(ba.PowerupMessage(random_powerup))
                        
                        # Let's add popuptext to know that which powerup we get 
                        PopupText(
                            text = random_powerup.upper(),
                            position = args[0].node.position,
                            random_offset = 0.0,
                            scale = 2.0,
                        ).autoretain()
                    # annoying powerup
                    elif args[1].poweruptype == 'fake':
                        
                        # if player have shields so our blast and freeze no longer work
                        if not args[0].shield:
                            danger = choice(['blast', 'freeze'])
                        
                            if danger == "blast":
                                Blast(
                                    position = args[0].node.position,
                                    velocity = args[0].node.velocity,
                                    blast_radius = 0.7,
                                    blast_type = 'land_mine',
                                ).autoretain()
                        
                                PopupText(
                                   text = "Boom!",
                                   position = args[0].node.position,
                                   random_offset = 0.0,
                                   scale = 2.0,
                                   color = (1.0, 0.0, 0.0)
                                ).autoretain()
                                
                            elif danger == 'freeze':
                                args[0].node.handlemessage(ba.FreezeMessage())
                            
                                PopupText(
                                    text = "So Cold!",
                                    position = args[0].node.position,
                                    random_offset = 0.0,
                                    scale = 2.0,
                                    color = (0.0, 0.5, 1.0)
                                ).autoretain()
                            
                                # emit some Cold chunk 
                                ba.emitfx(
                                   position = args[0].node.position,
                                   velocity = args[0].node.velocity,
                                   count =  10,
                                   scale = 0.6,
                                   spread = 0.4,
                                   chunk_type = 'ice',
                               )
                            # let's also provide shield to get hope
                            def shield_time() -> NoReturn:
                                args[0].node.handlemessage(ba.PowerupMessage('shield'))
                            # only run if player is alive 
                            if args[0].node:
                                # needd little bit delay cause our code run first 
                                ba.timer(0.1, shield_time)
                        # if player have shield with good hitpoint so we remove it
                        # shield max hitpoint = 575
                        elif args[0].shield_hitpoints > 575/2:
                            args[0].shield_hitpoints = -1
                            
                            PopupText(
                                    text = "i eat your shield!",
                                    position = args[0].node.position,
                                    random_offset = 0.0,
                                    scale = 2.0,
                                    color = (0.0, 0.5, 1.0)
                                ).autoretain()
                        # else player have low shield hitpoint so we knockout him
                        else:
                            args[0].node.handlemessage('knockout', 5000)
                            
                            PopupText(
                                    text = "GoodNight!",
                                    position = args[0].node.position,
                                    random_offset = 0.0,
                                    scale = 2.0,
                                    color = (0.0, 0.5, 1.0)
                                ).autoretain()
                    elif args[1].poweruptype == 'invisible':
                        # what if player model remove two times? 
                        if args[0].invisible == False:
                            tex = ba.gettexture('scrollWidgetGlow')
                            args[0]._flash_billboard(tex)
                            args[0].invisible = True
                            Plugin.remove_models(args[0])
                        
                            if args[0].powerups_expire:
                                args[0].node.mini_billboard_3_texture = tex
                                t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                                assert isinstance(t_ms, int)
                                args[0].node.mini_billboard_3_start_time = t_ms
                                args[0].node.mini_billboard_3_end_time = (
                                    t_ms + 15000
                                )
                                args[0].invisible_wear_off_flash_timer = ba.Timer(
                                    15000 - 2000,
                                    ba.Call(Plugin.invisible_wear_off_flash, args[0]),
                                    timeformat=ba.TimeFormat.MILLISECONDS,
                                 )
                                args[0].invisible_wear_off_timer = ba.Timer(
                                    15000,
                                     ba.Call(Plugin.invisible_wear_off, args[0]),
                                     timeformat=ba.TimeFormat.MILLISECONDS,
                                 )
                        # lets gives negative powerup
                        else:
                            args[0].node.handlemessage(ba.PowerupMessage('fake'))
                    elif args[1].poweruptype == 'ice_impact_bombs':
                        tex = ba.gettexture('bombColorIce')
                        Plugin.set_bomb_count(args[0], 3, 'ice_impact', tex)
                        
                        args[0].last_bomb_count = 'ice_impact'
                        args[0].last_counter_tex = tex
                        # need to reset our other counter
                        args[0].land_mine_count = 0
                        
                    elif args[1].poweruptype == 'ice_mines':
                        tex = ba.gettexture('achievementMine')
                        Plugin.set_bomb_count(args[0], 3, 'ice_mine', tex)
                        
                        args[0].last_bomb_count = 'ice_mine'
                        args[0].last_counter_tex = tex
                        # need to reset our other counter
                        args[0].land_mine_count = 0

                    elif args[1].poweruptype == 'land_mines':
                        # need to reset our other counter
                        args[0].bomb_counter = 0
                    # if invisible is active let's also hide Boxing gloves 
                    elif args[1].poweruptype == 'punch':
                        if args[0].invisible:
                            def glove_timer() -> NoReturn:
                                args[0].node.boxing_gloves = False
                            # need little bit delay cause our code run first 
                            ba.timer(0.1, glove_timer)
                        
            # orignal code
            func(*args, **kwargs)
            
        return wrapper
    
    # replace original one to custom one
    bastd.actor.spaz.Spaz.handlemessage = spaz_new_handlemessage(bastd.actor.spaz.Spaz.handlemessage)
    
    # new_bomb_drop for Our custom Bombs
    def new_bomb_drop(func):
        def wrapper(*args):
            
            from bastd.actor.spaz import BombDiedMessage
            # add custom non counter bomb string in this empty tuple
            custom_bomb = ()
            
            if args[0].bomb_counter > 0 or args[0].bomb_type in custom_bomb:
            
                if args[0].frozen or args[0].bomb_count <= 0:
                     return None

                assert args[0].node

                pos = args[0].node.position_forward
                vel = args[0].node.velocity

                if args[0].bomb_counter > 0:
                    bomb_type = Plugin.set_bomb_count(args[0], args[0].bomb_counter - 1, args[0].last_bomb_count, args[0].last_counter_tex)
                    dropping_bomb = False
                else:
                    dropping_bomb = True
                    bomb_type = args[0].bomb_type

                bomb = CustomBomb(
                    position = (pos[0], pos[1], pos[2]),
                    velocity = (vel[0], vel[1], vel[2]),
                    bomb_type = bomb_type,
                    blast_radius = args[0].blast_radius,
                    source_player = args[0].source_player,
                    owner = args[0].node,
                ).autoretain()
                
                assert bomb.node
                
                if dropping_bomb:
                    args[0].bomb_count -= 1
                    bomb.node.add_death_action(
                         ba.WeakCall(args[0].handlemessage, BombDiedMessage())
                    )
                
                args[0]._pick_up(bomb.node)
                
                return bomb
                
            else:
                # Original Code
                # only run when bomb type is default
                func(*args)
               
        return wrapper

    bastd.actor.spaz.Spaz.drop_bomb = new_bomb_drop(bastd.actor.spaz.Spaz.drop_bomb)
    
    # because of my laziness i replace whole function
    # but in future i most probably change it
    # this function is bot ai Updater 
    def _update(self) -> None:

        # Update one of our bot lists each time through.
        # First off, remove no-longer-existing bots from the list.
        try:
            bot_list = self._bot_lists[self._bot_update_list] = [
                b for b in self._bot_lists[self._bot_update_list] if b
            ]
        except Exception:
            bot_list = []
            ba.print_exception(
                'Error updating bot list: '
                + str(self._bot_lists[self._bot_update_list])
            )
        self._bot_update_list = (
            self._bot_update_list + 1
        ) % self._bot_list_count

        # Update our list of player points for the bots to use.
        player_pts = []
        for player in ba.getactivity().players:
            assert isinstance(player, ba.Player)
            try:
                # TODO: could use abstracted player.position here so we
                # don't have to assume their actor type, but we have no
                # abstracted velocity as of yet.
                if player.is_alive() and not player.actor.invisible:
                    assert isinstance(player.actor, Spaz)
                    assert player.actor.node
                    player_pts.append(
                        (
                            ba.Vec3(player.actor.node.position),
                            ba.Vec3(player.actor.node.velocity),
                        )
                    )
            except Exception:
                ba.print_exception('Error on bot-set _update.')

        for bot in bot_list:
            bot.set_player_points(player_pts)
            bot.update_ai()

    bastd.actor.spazbot.SpazBotSet._update = _update
    
    def remove_models(self) -> NoReturn:
        
        if self.node:
            self.head = self.node.head_model
            self.torso = self.node.torso_model
            self.pelvis = self.node.pelvis_model
            self.upper_arm = self.node.upper_arm_model
            self.upper_leg = self.node.upper_leg_model
            self.lower_leg = self.node.lower_leg_model
            self.forearm = self.node.forearm_model
            self.hand = self.node.hand_model
            self.toes = self.node.toes_model
            self.style = self.node.style
            self.name = self.node.name
            self.node.head_model = None
            self.node.torso_model = None
            self.node.pelvis_model = None
            self.node.upper_arm_model = None
            self.node.upper_leg_model = None
            self.node.lower_leg_model = None
            self.node.hand_model = None
            self.node.forearm_model = None
            self.node.toes_model = None
            self.node.style = 'ali'
            self.node.name = ''
            self.node.boxing_gloves = False

    def invisible_wear_off_flash(self) -> NoReturn:
        
        if self.node:
            self.node.billboard_texture = ba.gettexture('scrollWidgetGlow')
            self.node.billboard_opacity = 1.0
            self.node.billboard_cross_out = True

    def invisible_wear_off(self) -> NoReturn:
        
        if self.node:
            self.invisible = False
            self.node.billboard_opacity = 0.0
            self.node.head_model = self.head
            self.node.torso_model = self.torso
            self.node.pelvis_model = self.pelvis
            self.node.upper_arm_model = self.upper_arm
            self.node.upper_leg_model = self.upper_leg
            self.node.lower_leg_model = self.lower_leg
            self.node.hand_model = self.hand
            self.node.forearm_model = self.forearm
            self.node.toes_model = self.toes
            self.node.style = self.style
            self.node.name = self.name

    def set_bomb_count(self, count: int, bomb_type: str, tex: ba.Texture) -> bomb_type:
        """ bomb text counter """
 
        self.bomb_counter = count

        if self.node:
            if self.bomb_counter > 0:
                self.node.counter_text = 'x' + str(self.bomb_counter)
                self.node.counter_texture = (tex)
            else:
                self.node.counter_text = ''
                
        return bomb_type
    
    # adding attribute in bomb factory that we need
    def bomb_factory_new_init(func):
       def wrapper(*args):
        
            func(*args)
            
            args[0].ice_mine_tex = ba.gettexture('egg2')
            args[0].ice_impact_tex = ba.gettexture('bunnyColor')
            
       return wrapper
    # replacing....
    bastd.actor.bomb.BombFactory.__init__ = bomb_factory_new_init(bastd.actor.bomb.BombFactory.__init__)
#————————————————————————————————————————————————

# i make new bomb and blast by using decorators
# but its also required to edit function of Bomb and Blast
# and after edit function we won't get new Bomb and Blast according to our requirements
# so, I make Whole new Class for Our Custom Bombs and blast
# nothing much difference between original and custom code
# cause most of code i copy from original code
# but now atleast we can create our own custom bomb and blast
# according to our requirements

class CustomBlast(ba.Actor):
    """ Poor Blasts """
    def __init__(self,
        position: Sequence[float],
        velocity: Sequence[float],
        blast_radius: float = 1.0,
        blast_type: str = 'ice_impact',
        hit_type: str = 'explosion',
        hit_subtype: str = 'ice_impact',
        source_player: ba.Player | None = None,
    ): # <-- sad
        
        super().__init__()
        
        shared = SharedObjects.get()
        factory = BombFactory.get()

        self.blast_type = blast_type
        self._source_player = source_player
        self.hit_type = hit_type
        self.hit_subtype = hit_subtype
        self.radius = blast_radius

        # Set our position a bit lower so we throw more things upward.
        rmats = (factory.blast_material, shared.attack_material)
        self.node = ba.newnode(
            'region',
            delegate=self,
            attrs={
                'position': (position[0], position[1] - 0.1, position[2]),
                'scale': (self.radius, self.radius, self.radius),
                'type': 'sphere',
                'materials': rmats,
            },
        )

        ba.timer(0.05, self.node.delete)

        # Throw in an explosion and flash.
        evel = (velocity[0], max(-1.0, velocity[1]), velocity[2])
        explosion = ba.newnode(
            'explosion',
            attrs={
                'position': position,
                'velocity': evel,
                'radius': self.radius,
                'big': (self.blast_type == 'ice_mine'),
            },
        )
        if self.blast_type in ('ice_impact', 'ice_mine'):
            explosion.color = (0.0, 0.5, 0.5)
            
        ba.timer(0.15, explosion.delete)
        
        # blast emits
        ba.emitfx(
            position = position,
            velocity = velocity,
            count = int(4.0 + random() * 4),
            emit_type = 'tendrils',
            tendril_type='ice' if self.blast_type in ('ice_impact', 'ice_mine') else 'smoke',
        )
        ba.emitfx(
            position = position,
            emit_type = 'distortion',
            spread = 2.0,
        )
        
        if self.blast_type == 'ice_impact':
            
            def emit() -> None:
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=20,
                    spread=2.0,
                    scale=0.4,
                    chunk_type='ice',
                    emit_type='stickers',
                )
                
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=randrange(10, 20),
                    spread=0.4,
                    scale=0.3,
                    chunk_type='ice',
                )

            # It looks better if we delay a bit.
            ba.timer(0.05, emit)

        elif self.blast_type == 'ice_mine':
        
            def emit() -> None:
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=randrange(10, 20),
                    spread=2.0,
                    scale=0.4,
                    chunk_type='ice',
                    emit_type='stickers',
                )
                
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=randrange(3, 8),
                    spread=0.3,
                    scale=0.8,
                    chunk_type='ice',
                )
                
            # It looks better if we delay a bit.
            ba.timer(0.05, emit)
        
        # blast lights 
        light_radius = self.radius
       
        if self.blast_type in ('ice_mine', 'ice_impact'):
            
            light = ba.newnode(
                'light',
                attrs={
                    'position': position,
                    'volume_intensity_scale': 10.0,
                    'color': (0.5, 1.0, 1.0),
                },
            )
        
        ba.animate(
            light,
            'intensity',
            {
                0: 2.0,
                0.02: 0.1,
                0.025: 0.2,
                0.05: 0.5,
                0.06: 1.0,
                0.08: 2.0,
                0.2: 1.0,
                2.0: 0.5,
                3.0: 0.0,
            }
        )
        
        ba.animate(
            light,
            'radius',
            {
                0: light_radius * 0.2,
                0.05: light_radius * 0.55,
                0.1: light_radius * 0.3,
                0.3: light_radius * 0.15,
                1.0: light_radius * 0.05,
            }
        )
        
        ba.timer(0.05, light.delete)
        
        # blast scorchs
        scorch_radius = self.radius
        
        scorch = ba.newnode(
            'scorch',
            attrs={
                'position': position,
                'size': scorch_radius * 0.5,
                'big': (self.blast_type == 'ice_mine'),
            },
        )
        
        if self.blast_type in ('ice_impact', 'ice_mine'):
            scorch.color = (0.5, 1.0, 1.0)

        ba.animate(scorch, 'presence', {3.000: 1, 13.000: 0})
        ba.timer(13.0, scorch.delete)
        
        # blast sounds
        if self.blast_type == ('ice_impact'):
            ba.playsound(factory.hiss_sound, position=light.position)
        
        lpos = light.position
        ba.playsound(factory.random_explode_sound(), position=lpos)
        ba.playsound(factory.debris_fall_sound, position=lpos)
        
        # camera shakes
        ba.camerashake(intensity=1.0)
            
    def handlemessage(self, msg: Any) -> Any:
        assert not self.expired

        if isinstance(msg, ba.DieMessage):
            if self.node:
                self.node.delete()

        elif isinstance(msg, ExplodeHitMessage):
            node = ba.getcollision().opposingnode
            assert self.node
            nodepos = self.node.position
            mag = 2000.0
            
            # blast magnitude
            if self.blast_type == 'ice_impact':
                mag *= 0.5
            elif self.blast_type == 'ice_mine':
                mag *= 1.5
            
            node.handlemessage(
                ba.HitMessage(
                    pos=nodepos,
                    velocity=(0, 0, 0),
                    magnitude=mag,
                    hit_type=self.hit_type,
                    hit_subtype=self.hit_subtype,
                    radius=self.radius,
                    source_player=ba.existing(self._source_player),
                )
            )
            
            # Freezing bombs and their sounds
            if self.blast_type in ('ice_mine', 'ice_impact'):
                ba.playsound(
                    BombFactory.get().freeze_sound, 10, position=nodepos
                )
                node.handlemessage(ba.FreezeMessage())

        else:
            return super().handlemessage(msg)
        return None


class CustomBomb(ba.Actor):
    """ Poor bombs """
    def __init__(self,
        position: Sequence[float],
        velocity: Sequence[float],
        bomb_type: str = 'ice_impact',
        blast_radius: float = 1.0,
        bomb_scale: float = 1.0,
        gravity_scale: float = 1.0,
        density: float = 1.0,
        source_player: ba.Player | None = None,
        owner: ba.Node | None = None,
    ): # <-- sad 
        
        if bomb_type not in (
            'ice_mine',
            'ice_impact',
        ): 
            raise ValueError('invalid bomb type: ' + bomb_type)
        
        super().__init__()
        
        factory = BombFactory.get()
        shared = SharedObjects.get()
        
        self.bomb_type = bomb_type
        self.blast_radius = blast_radius
        self.scale = bomb_scale
        
        self._explode_callbacks: list[Callable[[CustomBomb, CustomBlast], Any]] = []
        self._source_player = source_player

        self.hit_type = 'explosion'
        self.hit_subtype = self.bomb_type

        self.owner = owner
        
        self.texture_sequence: ba.Node | None = None
        self._exploded = False

        if self.bomb_type == 'ice_impact':
            self.blast_radius *= 0.5
        elif self.bomb_type == 'ice_mine':
            self.blast_radius *= 0.6
            
        materials = (factory.bomb_material, shared.object_material)
        
        self.trigger_bombs = ('ice_impact')
        
        if self.bomb_type in self.trigger_bombs:
            materials += (factory.impact_blast_material,)
        elif self.bomb_type == 'ice_mine':
            materials += (factory.land_mine_no_explode_material,)

        if self.bomb_type == 'ice_mine':
            fuse_time = None
            self.node = ba.newnode(
                'prop',
                delegate=self,
                attrs={
                    'position': position,
                    'velocity': velocity,
                    'model': factory.land_mine_model,
                    'light_model': factory.land_mine_model,
                    'body': 'landMine',
                    'body_scale': self.scale,
                    'shadow_size': 0.44,
                    'color_texture': factory.ice_mine_tex,
                    'reflection': 'powerup',
                    'reflection_scale': [1.0],
                    'gravity_scale': gravity_scale,
                    'density': density,
                    'materials': materials,
                },
            )

        elif self.bomb_type == 'ice_impact':
            fuse_time = 10.0
            self.node = ba.newnode(
                'prop',
                delegate=self,
                attrs={
                    'position': position,
                    'velocity': velocity,
                    'body': 'sphere',
                    'body_scale': self.scale,
                    'model': factory.impact_bomb_model,
                    'shadow_size': 0.3,
                    'color_texture': factory.ice_impact_tex,
                    'reflection': 'powerup',
                    'reflection_scale': [1.5],
                    'gravity_scale': gravity_scale,
                    'density': density,
                    'materials': materials,
                },
            )
            
            self.warn_timer = ba.Timer(
                fuse_time - 1.7, ba.WeakCall(self.handlemessage, WarnMessage())
            )
            
        # Light the fuse!!!
        if self.bomb_type not in ('ice_mine'):
            assert fuse_time is not None
            ba.timer(
                fuse_time, ba.WeakCall(self.handlemessage, ExplodeMessage())
            )

        ba.animate(
            self.node,
            'model_scale',
            {0: 0, 0.2: 1.3 * self.scale, 0.26: self.scale},
        )
    
    def on_expire(self) -> NoReturn:
        super().on_expire()

        # Release callbacks/refs so we don't wind up with dependency loops.
        self._explode_callbacks = []
    
    def _handle_die(self) -> NoReturn:
        if self.node:
            self.node.delete()

    def _handle_oob(self) -> NoReturn:
        self.handlemessage(ba.DieMessage())

    def _handle_impact(self) -> NoReturn:
        node = ba.getcollision().opposingnode
        
        node_delegate = node.getdelegate(object)
        if node:
            if self.bomb_type in self.trigger_bombs and (
                node is self.owner
                or (
                    isinstance(node_delegate, CustomBomb)
                    and node_delegate.bomb_type in self.trigger_bombs
                    and node_delegate.owner is self.owner
                )
            ):
                return
            self.handlemessage(ExplodeMessage())
            
    def add_explode_callback(self, call: Callable[[CustomBomb, CustomBlast], Any]) -> NoReturn:
        """
        Add a call to be run when the bomb has exploded.

        The bomb and the new blast object are passed as arguments.
        """
        self._explode_callbacks.append(call)

    def explode(self) -> None:
        """Blows up the bomb if it has not yet done so."""
        if self._exploded:
            return
        self._exploded = True
        if self.node:
            blast = CustomBlast(
                position=self.node.position,
                velocity=self.node.velocity,
                blast_radius=self.blast_radius,
                blast_type=self.bomb_type,
                source_player=ba.existing(self._source_player),
                hit_type=self.hit_type,
                hit_subtype=self.hit_subtype,
            ).autoretain()
            for callback in self._explode_callbacks:
                callback(self, blast)

        # We blew up so we need to go away.
        # NOTE TO SELF: do we actually need this delay?
        # If you are curious to know, just remove timer and see the magic
        ba.timer(0.001, ba.WeakCall(self.handlemessage, ba.DieMessage()))

    def _handle_dropped(self) -> NoReturn:
    
        if self.bomb_type == 'ice_mine':
            self.arm_timer = ba.Timer(
                1.25, ba.WeakCall(self.handlemessage, ArmMessage())
            )

    def warn(self) -> NoReturn:
        if self.texture_sequence and self.node:
            self.texture_sequence.rate = 30
            ba.playsound(
                BombFactory.get().warn_sound, 0.5, position=self.node.position
            )
    
    def _add_material(self, material: ba.Material) -> NoReturn:
        if not self.node:
            return
        materials = self.node.materials
        if material not in materials:
            assert isinstance(materials, tuple)
            self.node.materials = materials + (material,)
            
    def arm(self) -> NoReturn:
        """
         Arm the bomb (for ice-mines).

        These types of bombs will not explode until they have been armed.
        """
        if not self.node:
            return
        
        factory = BombFactory.get()
        intex: Sequence[ba.Texture]
        
        if self.bomb_type == 'ice_mine':
            intex = (factory.land_mine_lit_tex, factory.ice_mine_tex)
            self.texture_sequence = ba.newnode(
                'texture_sequence',
                owner=self.node,
                attrs={'rate': 30, 'input_textures': intex},
            )
            ba.timer(0.5, self.texture_sequence.delete)

            # We now make it explodable.
            ba.timer(
                0.25,
                ba.WeakCall(
                    self._add_material, factory.land_mine_blast_material
                ),
            )
        else:
            raise Exception('arm() should only be called on ice_mine')
            
        self.texture_sequence.connectattr(
            'output_texture', self.node, 'color_texture'
        )
        ba.playsound(factory.activate_sound, 0.5, position=self.node.position)
        
    def _handle_hit(self, msg: ba.HitMessage) -> NoReturn:
        ispunched = msg.srcnode and msg.srcnode.getnodetype() == 'spaz'

        if not self._exploded and (
            not ispunched or self.bomb_type in ['ice_impact', 'ice_mine']
        ):

            source_player = msg.get_source_player(ba.Player)
            if source_player is not None:
                self._source_player = source_player

            ba.timer(
                0.1 + random() * 0.1,
                ba.WeakCall(self.handlemessage, ExplodeMessage()),
            )
        assert self.node
        self.node.handlemessage(
            'impulse',
            msg.pos[0],
            msg.pos[1],
            msg.pos[2],
            msg.velocity[0],
            msg.velocity[1],
            msg.velocity[2],
            msg.magnitude,
            msg.velocity_magnitude,
            msg.radius,
            0,
            msg.velocity[0],
            msg.velocity[1],
            msg.velocity[2],
        )

        if msg.srcnode:
            pass

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ExplodeMessage):
            self.explode()
        elif isinstance(msg, ImpactMessage):
            self._handle_impact()
        elif isinstance(msg, ba.DroppedMessage):
            self._handle_dropped()
        elif isinstance(msg, ba.HitMessage):
            self._handle_hit(msg)
        elif isinstance(msg, ba.DieMessage):
            self._handle_die()
        elif isinstance(msg, ba.OutOfBoundsMessage):
            self._handle_oob()
        elif isinstance(msg, ArmMessage):
            self.arm()
        elif isinstance(msg, WarnMessage):
            self.warn()
        else:
            super().handlemessage(msg)
        