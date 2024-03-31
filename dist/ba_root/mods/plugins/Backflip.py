# ba_meta require api 7
#backflip by SARA

import ba, _ba
from bastd.actor import spaz
import setting 
import random

settings = setting.get_settings_data()
backflip = settings['backflip']['enable']
turn = backflip  # Set turn based on the value fetched from settings

def myOnJumpPress(Slade):
    def wrapper(self):
        is_moving = abs(self.node.move_up_down) >= 0.75 or abs(self.node.move_left_right) >= 0.75
        if not self.node.exists():
            return

        t = ba.time(timetype=ba.TimeType.REAL, timeformat=ba.TimeFormat.SECONDS)
        self.last_jump_time_ms = -9999

        if t - self.last_jump_time_ms >= self._jump_cooldown:
            self.node.jump_pressed = True

            if turn and t - self.last_punch_time_ms <= 95 and is_moving and self.node.jump_pressed and self.node.punch_pressed:
                # Apply impulses for a backflip with reduced flip strength for bomb jumping
                flip_strength = 160  # Adjust this value for the desired flip strength
                self.node.handlemessage("impulse", self.node.position[0], self.node.position[1] + 3.5, self.node.position[2],
                                        self.node.velocity[0], self.node.velocity[1], self.node.velocity[2],
                                        -flip_strength * self.node.run, 15 * self.node.run, 0, 0, self.node.velocity[0],
                                        self.node.velocity[1], self.node.velocity[2])

                self.node.handlemessage("impulse", self.node.position[0], self.node.position[1] + 3.6, self.node.position[2],
                                        self.node.velocity[0], self.node.velocity[1], self.node.velocity[2],
                                        -flip_strength * self.node.run, 15 * self.node.run, 0, 0, self.node.velocity[0],
                                        self.node.velocity[1], self.node.velocity[2])

                self.node.handlemessage('impulse', self.node.position[0], self.node.position[1] + 0.001,
                                        self.node.position[2], 0, 0.2, 0, 200, 200, 0, 0, 0, 5, 0)

                # Emit sparks with a random chunk type during the backflip
                chunk_types = ["spark", "slime", "ice", "metal"]  # Add more chunk types if needed
                random_chunk_type = random.choice(chunk_types)
                ba.emitfx(
                    position=self.node.position,
                    velocity=self.node.velocity,
                    count=random.randint(1, 10),
                    scale=0.5,
                    spread=0.2,
                    chunk_type=random_chunk_type
                )

            self.last_jump_time_ms = t

        self._turbo_filter_add_press('jump')

    return wrapper

# ba_meta export plugin
class Sara(ba.Plugin):
    def __init__(self):
        spaz.Spaz.on_jump_press = myOnJumpPress(spaz.Spaz.on_jump_press)
