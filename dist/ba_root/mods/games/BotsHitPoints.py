# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import ba
from bastd.actor.spazbot import SpazBot
from bastd.ui.popup import PopupWindow

if TYPE_CHECKING:
    pass


lang = ba.app.lang.language
if lang == 'Spanish':
    title_text = 'Puntos de vida para Bots'
    default_text = 'por defecto: 1000'
    empty_text = '¡No puede quedar vacío!'
    only_numbers = 'Error: Solo números'
    minimum_number = 'El valor mínimo es 1'
else:
    title_text = 'Bots Hit Points'
    default_text = 'default: 1000'
    empty_text = 'It can\'t be empty!'
    only_numbers = 'Error: Only numbers'
    minimum_number = 'The minimum value is 1'


SpazBot._old_init = SpazBot.__init__
def __init__(self) -> None:
    self._old_init()
    self.hitpoints = self.hitpoints_max = ba.app.config['Bots Hit Points']


class BotsHitPointPopup(PopupWindow):

    def __init__(self):
        uiscale = ba.app.ui.uiscale
        self._transitioning_out = False
        self._width = 400
        self._height = 220
        bg_color = (0.5, 0.4, 0.6)
        scale = (2.2 if uiscale is ba.UIScale.SMALL
            else 1.4 if uiscale is ba.UIScale.MEDIUM else 1.0)

        # creates our _root_widget
        PopupWindow.__init__(self,
                             position=(0.0, 0.0),
                             size=(self._width, self._height),
                             scale=scale,
                             bg_color=bg_color)

        cancel_button = ba.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.11, self._height * 0.06),
            scale=0.8,
            size=(175, 60),
            autoselect=True,
            label=ba.Lstr(resource='cancelText'),
            text_scale=1.2,
            color=(0.7, 0.4, 0.34),
            textcolor=(0.9, 0.9, 1.0),
            on_activate_call=self.cancel
        )
        save_button = btn = ba.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height * 0.06),
            scale=0.8,
            size=(190, 60),
            autoselect=True,
            left_widget=cancel_button,
            label=ba.Lstr(resource='saveText'),
            text_scale=1.2,
            color=(0.2, 0.8, 0.55),
            on_activate_call=self.save
        )
        ba.containerwidget(edit=self.root_widget,
                           cancel_button=cancel_button)

        self._hp_text = ba.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.292, self._height * 0.48),
            size=(235, 50),
            editable=True,
            h_align='left',
            v_align='center',
            scale=1.0,
            autoselect=True,
            text=str(ba.app.config['Bots Hit Points']),
            maxwidth=200)

        ba.imagewidget(
            parent=self.root_widget,
            position=(self._width * 0.09, self._height * 0.445),
            size=(65, 65),
            color=(0.9, 0.2, 0.2),
            texture=ba.gettexture('heart'))

        ba.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.49, self._height - 32),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=0.9,
            text=title_text,
            color=(1.0, 1.0, 0.0),
            maxwidth=self._width * 0.7)

        ba.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.49, self._height * 0.39),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=0.8,
            text=default_text,
            color=ba.app.ui.title_color)

    def save(self) -> None:
        hp_text = cast(str, ba.textwidget(query=self._hp_text))
        if hp_text == '':
            ba.screenmessage(empty_text, color=(1.0, 1.0, 1.0))
            ba.playsound(ba.getsound('error'))
            return
        try:
            hp_int = int(hp_text)
        except Exception:
            ba.screenmessage(only_numbers, color=(1, 0, 0))
            ba.playsound(ba.getsound('error'))
            return
        if hp_int < 1:
            ba.screenmessage(minimum_number, color=(1, 0, 0))
            ba.playsound(ba.getsound('error'))
            return
        ba.app.config['Bots Hit Points'] = hp_int
        ba.app.config.apply_and_commit()
        ba.containerwidget(edit=self.root_widget, transition='out_scale')
        ba.playsound(ba.getsound('gunCocking'))

    def cancel(self) -> None:
        ba.containerwidget(edit=self.root_widget, transition='out_scale')


# ba_meta export plugin
class BHPPlugin(ba.Plugin):

    def has_settings_ui(self) -> bool:
        return True

    def show_settings_ui(self, source_widget: ba.Widget | None) -> None:
        BotsHitPointPopup()

    if 'Bots Hit Points' in ba.app.config:
        old_config = ba.app.config['Bots Hit Points']
        if not isinstance(old_config, int):
            ba.app.config['Bots Hit Points'] = 1000
            ba.app.config.apply_and_commit()
    else:
        ba.app.config['Bots Hit Points'] = 1000
        ba.app.config.apply_and_commit()
    SpazBot.__init__ = __init__
