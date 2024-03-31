# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
from bastd.ui import popup
from ba._generated.enums import UIScale

if TYPE_CHECKING:
	pass


class CustomLang:
	lang = ba.app.lang.language
	if lang == 'Spanish':
		title = 'Escala de Juego'
		change = 'Tipo de Escala'
		large = 'Largo'
		medium = 'Mediano'
		small = 'Pequeño'
	else:
		title = 'Game Scale'
		change = 'Scale Type'
		large = 'Large'
		medium = 'Medium'
		small = 'Small'


class ChangeUIPopup(popup.PopupWindow):

	def __init__(self):
		uiscale = ba.app.ui.uiscale
		self._transitioning_out = False
		self._width = 400
		self._height = 220
		bg_color = (0.4, 0.37, 0.49)

		# creates our _root_widget
		super().__init__(
			position=(0.0, 0.0),
			size=(self._width, self._height),
			scale=2.4 if uiscale is ba.UIScale.SMALL else 1.2,
			bg_color=bg_color)

		self._cancel_button = ba.buttonwidget(
			parent=self.root_widget,
			position=(25, self._height - 40),
			size=(50, 50),
			scale=0.58,
			label='',
			color=bg_color,
			on_activate_call=self._on_cancel_press,
			autoselect=True,
			icon=ba.gettexture('crossOut'),
			iconscale=1.2)
		ba.containerwidget(edit=self.root_widget,
						   cancel_button=self._cancel_button)

		ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.5, self._height - 27),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=0.8,
			text=CustomLang.title,
			maxwidth=self._width * 0.7,
			color=ba.app.ui.title_color)

		ba.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.265, self._height * 0.295 + 45),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.0,
            text=CustomLang.change,
            maxwidth=150,
            color=(0.8, 0.8, 0.8, 1.0))

		popup.PopupMenu(
			parent=self.root_widget,
			position=(self._width * 0.5, self._height * 0.18 + 45),
			width=150,
			scale=2.8 if uiscale is ba.UIScale.SMALL else 1.3,
			choices=[0, 1, 2],
			choices_display=[
				ba.Lstr(value=CustomLang.large),
				ba.Lstr(value=CustomLang.medium),
				ba.Lstr(value=CustomLang.small),
			],
			current_choice=ba.app.config['UIScale'],
			on_value_change_call=self._set_uiscale,
		)

	def _set_uiscale(self, val: int) -> None:
		cfg = ba.app.config
		cfg['UIScale'] = val
		cfg.apply_and_commit()
		self.update()

	def update(self) -> None:
		if ba.app.config['UIScale'] == 0:
			uiscale = UIScale.LARGE
		elif ba.app.config['UIScale'] == 1:
			uiscale = UIScale.MEDIUM
		else:
			uiscale = UIScale.SMALL
		ba.app.ui._uiscale = uiscale

	def _on_cancel_press(self) -> None:
		self._transition_out()

	def _transition_out(self) -> None:
		if not self._transitioning_out:
			self._transitioning_out = True
			ba.containerwidget(edit=self.root_widget, transition='out_scale')

	def on_popup_cancel(self) -> None:
		ba.playsound(ba.getsound('swish'))
		self._transition_out()


# ba_meta export plugin
class ChangeUIPlugin(ba.Plugin):

	def on_app_running(self) -> None:
		if not 'UIScale' in ba.app.config:
			if ba.app.ui._uiscale is UIScale.LARGE:
				scale = 0
			if ba.app.ui._uiscale is UIScale.MEDIUM:
				scale = 1
			else:
				scale = 2
			ba.app.config['UIScale'] = scale
			ba.app.config.apply_and_commit()
		if ba.app.config['UIScale'] == 0:
			uiscale = UIScale.LARGE
		elif ba.app.config['UIScale'] == 1:
			uiscale = UIScale.MEDIUM
		else:
			uiscale = UIScale.SMALL
		ba.app.ui._uiscale = uiscale

	def has_settings_ui(self) -> bool:
		return True

	def show_settings_ui(self, source_widget: ba.Widget | None) -> None:
		ChangeUIPopup()
