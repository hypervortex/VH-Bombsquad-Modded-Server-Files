# -*- coding: utf-8 -*-
# Released under the MIT License. See LICENSE for details.

import ba, _ba, setting
import ba.internal
from stats.mystats import damage_data
import random
from bastd.actor.popuptext import PopupText

our_settings = setting.get_settings_data()


def handle_hit(mag, pos):
    if not mag:
        return
    
    # Send Screen Texts if enabled
    if our_settings['enableHitTexts']:
        try:
            hit_messages = {
                (200, float('inf')): ("#PRO !", "spark"),
                (130, 150): ("GOOD ONE!", "slime"),
                (90, 130): ("OH! YEAH", "ice"),
                (70, 90): ("WTF!", "metal"),
                (50, 70): ("!!!", "spark"),
                (30, 50): ("IMPRESSIVE!", "slime"),
                (15, 30): ("INSANE!", "ice"),
                (0, 15): ("UNBELIEVABLE!", "metal"),
            }

            for (lower, upper), (text, chunk_type) in hit_messages.items():
                if lower <= mag < upper:
                    PopupText(text, color=(random.random(), random.random(), random.random()), scale=1.6, position=pos).autoretain()

                    # Emit spark effect for each hit message
                    ba.emitfx(position=pos, velocity=(0, 1, 0), count=random.randint(5, 10), scale=0.5,
                              spread=0.2, chunk_type=chunk_type)
        except Exception as e:
            print(f"Error in handle_hit: {e}")

    return


class hit_message(ba.HitMessage):
    def __init__(self, *args, **kwargs):
        hit_type = kwargs["hit_type"]
        if hit_type == "punch":
            handle_hit(kwargs['magnitude'], kwargs['pos'])
        super().__init__(*args, **kwargs)
ba.HitMessage = hit_message
