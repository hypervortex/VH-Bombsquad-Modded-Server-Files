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
    if our_settings['enableOldHitTexts']:
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
                    PopupText(text, color=(random.random(), random.random(), random.random()), scale=0.8, position=pos).autoretain()

                    # Emit spark effect for each hit message
                    ba.emitfx(position=pos, velocity=(0, 1, 0), count=random.randint(5, 10), scale=0.2,
                              spread=0.1, chunk_type=chunk_type)
        except Exception as e:
            print(f"Error in handle_hit: {e}")

    return


def new_message(damage, pos):
    if not damage:
        return
    if our_settings['enableNewHitTexts']:
        try:
            if damage > 2000:
                PopupText(u"\ue043K.\ue046.O\ue043", color=(3, 0, 0), scale=2.0, position=pos).autoretain()
                ba.emitfx(position=(pos[0], pos[1] + 4, pos[2]), velocity=(0, 0, 0), scale=1.5, count=400, spread=0.6, chunk_type='metal')
                def light():
                    light = ba.newnode('light',
                                        attrs={'position': (0, 10, 0),
                                               'color': (0.2, 0.2, 0.4),
                                               'volumeIntensityScale': 1.0,
                                               'radius': 10})
                    ba.animate(light, "intensity", {0: 1, 10: 10, 250: 5, 450: 0, 550: 10, 700: 5, 1000: 10, 1250: 0})
                light()
                def dark(val):
                    if val == 1:
                        activity = _ba.get_foreground_host_activity()
                        activity.globalsnode.tint = (0.7, 0.6, 1)
                    else:
                        activity.globalsnode.tint = (1, 1, 1)
                    activity.globalsnode.slow_motion = not activity.globalsnode.slow_motion
                dark(1)
                ba.playsound(ba.getsound("orchestraHitBig2"))
                ba.Timer(30, ba.Call(dark, 2))

            elif 350 < damage < 400:
                PopupText(u"\ue049PATTA SE HEADSHOT\ue049", color=(0.3, 1, 0), scale=1.8, position=pos).autoretain()
                ba.emitfx(position=(pos[0], pos[1] + 4, pos[2]), velocity=(0, 0, 0), scale=1, count=100, spread=0.4, chunk_type='metal')

            elif 300 < damage < 350:
                PopupText(u"\ue048IMPRESSIVE\ue048", color=(0, 1, 3), scale=1.3, position=pos).autoretain()
               

            elif 250 < damage < 300:
                PopupText(u"\ue042WTF\ue042", color=(0, 0, 1), scale=1.3, position=pos).autoretain()

            elif 200 < damage < 250:
                PopupText(u"\ue04fBOOM!\ue04f", color=(2, 2, 0), scale=1.3, position=pos).autoretain()
                
         
        except Exception as e:
            print(f"Error in new_message: {e}")

    return


class hit_message(ba.HitMessage):
    def __init__(self, *args, **kwargs):
        hit_type = kwargs["hit_type"]
        if hit_type == "punch":
            handle_hit(kwargs['magnitude'], kwargs['pos'])
            new_message(kwargs['magnitude'], kwargs['pos'])
        super().__init__(*args, **kwargs)
ba.HitMessage = hit_message
