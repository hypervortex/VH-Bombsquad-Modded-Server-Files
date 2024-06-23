import time
import ba
import _ba
from bastd.actor import playerspaz

print("Custom PlayerSpaz script loaded.")

class PlayerSpaz(playerspaz.PlayerSpaz):
    def __init__(self, color=(1, 1, 1), highlight=(0.5, 0.5, 0.5), 
                 character="Spaz", player=None, powerups_expire=True):
        super().__init__(color=color, highlight=highlight,
                         character=character, player=player, powerups_expire=False)
        self._fly_mode = False
        self._fly_speed = self._fly_speed_normal = 2.0

    def delete_hold_node(self):
        for attr in ['_c', 'hold_node']:
            node = getattr(self, attr, None)
            if node is not None and node.exists():
                node.delete()
        self._fly_timer = None

    def spawn_hold_node(self):
        if self.node is None or not self.node.exists():
            return
        self.delete_hold_node()
        t = self.node.position
        t = (t[0], t[1] + 1, t[2])
        self.hold_node = ba.newnode('prop', owner=self.node,
                                    delegate=self, attrs={
                                        'position': t,
                                        'body': 'box',
                                        'body_scale': 0.000001,
                                        'model': None,
                                        'model_scale': 0.000001,
                                        'color_texture': None,
                                        'max_speed': 0,
                                        'sticky': True,
                                        'stick_to_owner': True,
                                        'owner': self.node,
                                        'materials': []})
        self._c = c = ba.newnode('combine', owner=self.hold_node, attrs={'size': 3})
        self._c_move = [0, 0, 0]
        c.input0, c.input1, c.input2 = t
        self._c.connectattr('output', self.hold_node, 'position')
        self._fly_timer = ba.Timer(0.1, ba.WeakCall(self.move_hold_node, 'all'), repeat=True)

    def move_hold_node(self, v='height'):
        if getattr(self, '_c', None) is not None and self._c.exists():
            l = [0, 1, 2] if v == 'all' else [1] if v == 'height' else [0, 2]
            for c in l:
                val = getattr(self._c, 'input' + str(c))
                ba.animate(self._c, 'input' + str(c), {0: val, 0.5: val + self._c_move[c]})

    def hold_node_alive(self):
        for attr in ['_c', 'hold_node']:
            node = getattr(self, attr, None)
            if node is None or not node.exists():
                return False
        return True

    def set_fly_mode(self, val):
        self._fly_mode = val
        if self._fly_mode:
            super().on_move_up_down(0)
            super().on_move_left_right(0)
            self.spawn_hold_node()
            node = getattr(self, 'hold_node', None)
            if node is None or not node.exists():
                node = ba.Node(None)
            self.node.hold_body = 0
            self.node.hold_node = node
            print("Fly mode enabled")
        else:
            self.node.hold_body = 0
            self.node.hold_node = ba.Node(None)
            self.delete_hold_node()
            super().on_move_up_down(0)
            super().on_move_left_right(0)
            print("Fly mode disabled")

    def on_punch_press(self):
        if self.node is None or not self.node.exists():
            return
        if not self._fly_mode:
            super().on_punch_press()
        elif self.hold_node_alive():
            t = self.node.position
            self._c.input0, self._c.input1, self._c.input2 = (t[0], t[1] + 1, t[2])

    def on_punch_release(self):
        if not self._fly_mode:
            super().on_punch_release()
        else:
            player = self.getplayer('some_playertype')  # Provide the required playertype
            if player is not None and player.exists() and not player.is_alive():
                activity = self.getactivity()
                if activity is not None and hasattr(activity, 'spawn_player'):
                    player.gamedata['respawn_timer'] = player.gamedata['respawn_icon'] = None
                    with ba.Context(activity):
                        activity.spawn_player(player=player)

    def on_bomb_press(self):
        if not self._fly_mode:
            super().on_bomb_press()
        else:
            self._fly_speed *= 2.5

    def on_bomb_release(self):
        if not self._fly_mode:
            super().on_bomb_release()
        else:
            self._fly_speed = self._fly_speed_normal

    def on_jump_release(self):
        if not self._fly_mode:
            super().on_jump_release()
        else:
            self._c_move[1] = 0

    def on_pickup_release(self):
        if not self._fly_mode:
            super().on_pickup_release()
        else:
            self._c_move[1] = 0

    def on_jump_press(self):
        if self.node is None or not self.node.exists():
            return
        now = time.time()
        if float(now - getattr(self, 'last_jump_press_time', 0)) <= 0.28:
            self.set_fly_mode(not self._fly_mode)
        else:
            self.last_jump_press_time = now
            if not self._fly_mode:
                super().on_jump_press()
            else:
                self._c_move[1] = 0.5 * self._fly_speed
                self.move_hold_node()

    def on_pickup_press(self):
        if not self._fly_mode:
            super().on_pickup_press()
        elif self.node is not None and self.node.exists():
            self._c_move[1] = -0.5 * self._fly_speed
            self.move_hold_node()

    def on_move_up_down(self, value):
        if self.node is None or not self.node.exists():
            return
        if not self._fly_mode:
            super().on_move_up_down(value)
        else:
            self._c_move[2] = -value * self._fly_speed

    def on_move_left_right(self, value):
        if self.node is None or not self.node.exists():
            return
        if not self._fly_mode:
            super().on_move_left_right(value)
        else:
            self._c_move[0] = value * self._fly_speed

    def handlemessage(self, msg):
        if isinstance(msg, ba.DieMessage) or isinstance(msg, ba.OutOfBoundsMessage):
            n = getattr(self, 'hold_node', None)
            if n is not None and n.exists():
                n.delete()
        elif isinstance(msg, ba.HitMessage) and self._fly_mode:
            return
        super().handlemessage(msg)

# Overriding the PlayerSpaz with the custom one
playerspaz.PlayerSpaz = PlayerSpaz