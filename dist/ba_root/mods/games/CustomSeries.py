# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
from ba._multiteamsession import MultiTeamSession
from bastd.mainmenu import MainMenuSession
from ba._coopsession import CoopSession
from bastd.ui import popup

if TYPE_CHECKING:
	from typing import Any, Callable


class ModInfo:
	url = 'https://youtu.be/MGTbod4lbp8' # video


class ModLang:
	lang = ba.app.lang.language
	if lang == 'Spanish':
		title = 'Opciones del Mod'
		enable = 'Habilitar Mod'
		ffaseries = 'Series en TCT'
		teamseries = 'Series en Equipo'
	elif lang == 'Chinese':
		title = '模组选项'
		enable = '启用模组'
		ffaseries = 'FFA系列'
		teamseries = '团队系列'
	else:
		title = 'Mod Settings'
		enable = 'Enable Mod'
		ffaseries = 'FFA Series'
		teamseries = 'Team Series'


class ConfigNumberEdit:
	"""A set of controls for editing a numeric config value.

	It will automatically save and apply the config when its
	value changes.
	"""

	nametext: ba.Widget
	"""The text widget displaying the name."""

	valuetext: ba.Widget
	"""The text widget displaying the current value."""

	minusbutton: ba.Widget
	"""The button widget used to reduce the value."""

	plusbutton: ba.Widget
	"""The button widget used to increase the value."""

	def __init__(
		self,
		parent: ba.Widget,
		configkey: str,
		position: tuple[float, float],
		minval: int = 0,
		maxval: int = 1000000,
		increment: int = 1.0,
		callback: Callable[[int], Any] | None = None,
		xoffset: float = 0.0,
		displayname: str | ba.Lstr | None = None,
		changesound: bool = True,
		textscale: float = 1.0,
		value: int = None,
	):
		if displayname is None:
			displayname = configkey

		self._configkey = configkey
		self._minval = minval
		self._maxval = maxval
		self._increment = increment
		self._callback = callback
		self._value = int(value)

		self.nametext = ba.textwidget(
			parent=parent,
			position=position,
			size=(100, 30),
			text=displayname,
			maxwidth=160 + xoffset,
			color=(0.8, 0.8, 0.8, 1.0),
			h_align='left',
			v_align='center',
			scale=textscale,
		)
		self.valuetext = ba.textwidget(
			parent=parent,
			position=(246 + xoffset, position[1]),
			size=(60, 28),
			editable=False,
			color=(0.3, 1.0, 0.3, 1.0),
			h_align='right',
			v_align='center',
			text=str(self._value),
			padding=2,
			maxwidth=90,
		)
		self.minusbutton = ba.buttonwidget(
			parent=parent,
			position=(330 + xoffset, position[1]),
			size=(28, 28),
			label='-',
			autoselect=True,
			on_activate_call=ba.Call(self._down),
			repeat=True,
			enable_sound=changesound,
		)
		self.plusbutton = ba.buttonwidget(
			parent=parent,
			position=(380 + xoffset, position[1]),
			size=(28, 28),
			label='+',
			autoselect=True,
			on_activate_call=ba.Call(self._up),
			repeat=True,
			enable_sound=changesound,
		)
		# Complain if we outlive our widgets.
		ba.uicleanupcheck(self, self.nametext)
		self._update_display()

	def _up(self) -> None:
		self._value = min(self._maxval, self._value + self._increment)
		self._value = int(self._value)
		self._changed()

	def _down(self) -> None:
		self._value = max(self._minval, self._value - self._increment)
		self._value = int(self._value)
		self._changed()

	def _changed(self) -> None:
		self._update_display()
		ba.app.config['Custom Series'][self._configkey] = self._value
		ba.app.config.apply_and_commit()
		if self._callback:
			self._callback(self._value)

	def _update_display(self) -> None:
		ba.textwidget(edit=self.valuetext, text=str(self._value))
	

class ModSettingsPopup(popup.PopupWindow):

	def __init__(self):
		uiscale = ba.app.ui.uiscale
		self._transitioning_out = False
		self._width = 480
		self._height = 260
		bg_color = (0.4, 0.37, 0.49)

		# creates our _root_widget
		super().__init__(
			position=(0.0, 0.0),
			size=(self._width, self._height),
			scale=(
				2.06
				if uiscale is ba.UIScale.SMALL
				else 1.4
				if uiscale is ba.UIScale.MEDIUM
				else 1.0
			),
			bg_color=bg_color)

		self._cancel_button = ba.buttonwidget(
			parent=self.root_widget,
			position=(34, self._height - 48),
			size=(50, 50),
			scale=0.7,
			label='',
			color=bg_color,
			on_activate_call=self._on_cancel_press,
			autoselect=True,
			icon=ba.gettexture('crossOut'),
			iconscale=1.2)
		ba.containerwidget(edit=self.root_widget,
						   cancel_button=self._cancel_button)

		if ModInfo.url != '':
			url_button = ba.buttonwidget(
				parent=self.root_widget,
				position=(self._width - 86, self._height - 51),
				size=(82, 82),
				scale=0.5,
				label='',
				color=(1.1, 0.0, 0.0),
				on_activate_call=self._open_url,
				autoselect=True,
				icon=ba.gettexture('startButton'),
				iconscale=1.83,
				icon_color=(1.3, 1.3, 1.3))

		title = ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.49, self._height - 27 - 5),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=1.0,
			text=ModLang.title,
			maxwidth=self._width * 0.6,
			color=ba.app.ui.title_color)

		checkbox_size = (self._width * 0.7, 50)
		checkbox_maxwidth = 250
		v = -94
		ConfigNumberEdit(
			parent=self.root_widget,
			position=(self._width * 0.08, self._height * 0.2 - v),
			value=ba.app.config['Custom Series']['ffa series'],
			configkey='ffa series',
			displayname=ModLang.ffaseries,
			callback=self._update_series,
		)
		v += 50
		ConfigNumberEdit(
			parent=self.root_widget,
			position=(self._width * 0.08, self._height * 0.2 - v),
			value=ba.app.config['Custom Series']['team series'],
			configkey='team series',
			displayname=ModLang.teamseries,
			callback=self._update_series,
		)
		v += 66
		ba.checkboxwidget(
			parent=self.root_widget,
			position=(self._width * 0.155, self._height * 0.2 - v),
			size=checkbox_size,
			autoselect=True,
			maxwidth=checkbox_maxwidth,
			scale=1.0,
			textcolor=(0.8, 0.8, 0.8),
			value=ba.app.config['Custom Series']['enable mod'],
			text=ModLang.enable,
			on_value_change_call=self._set_enable,
		)
		self._update()
	
	def _update(self) -> None:
		session = _ba.get_foreground_host_session()
		session_list = (MainMenuSession, CoopSession)
		if session and not isinstance(session, session_list):
			if ba.app.config['Custom Series']['enable mod']:
				session._ffa_series_length = (
					ba.app.config['Custom Series']['ffa series'])
				session._series_length = (
					ba.app.config['Custom Series']['team series'])
			else:
				session._ffa_series_length = 24
				session._series_length = 7

	def _update_series(self, val: int) -> None:
		self._update()

	def _set_enable(self, val: bool) -> None:
		cfg = ba.app.config
		cfg['Custom Series']['enable mod'] = val
		cfg.apply_and_commit()
		self._update()

	def _open_url(self) -> None:
		ba.open_url(ModInfo.url)

	def _on_cancel_press(self) -> None:
		self._transition_out()

	def _transition_out(self) -> None:
		if not self._transitioning_out:
			self._transitioning_out = True
			ba.containerwidget(edit=self.root_widget, transition='out_scale')

	def on_popup_cancel(self) -> None:
		ba.playsound(ba.getsound('swish'))
		self._transition_out()


class CustomMod:
	def __init__(self):
		MultiTeamSession.oldinit = MultiTeamSession.__init__
		def __init__(self) -> None:
			self.oldinit()
			cfgname = 'Custom Series'
			if ba.app.config[cfgname]['enable mod']:
				self._series_length = ba.app.config[cfgname]['team series']
				self._ffa_series_length = ba.app.config[cfgname]['ffa series']
			else:
				self._series_length = 7
				self._ffa_series_length = 24
		MultiTeamSession.__init__ = __init__


# ba_meta export plugin
class ModPlugin(ba.Plugin):

	def on_app_running(self) -> None:
		self.setup_config()
		self.custom_plugin()

	def setup_config(self) -> None:
		cfgname = 'Custom Series'
		if not cfgname in ba.app.config:
			mod_list = {
				'ffa series': 24,
				'team series': 7,
				'enable mod': True,
			}
			ba.app.config[cfgname] = mod_list
			ba.app.config.apply_and_commit()

	def custom_plugin(self) -> None:
		CustomMod()

	def has_settings_ui(self) -> bool:
		return True

	def show_settings_ui(self, source_widget: ba.Widget | None) -> None:
		ModSettingsPopup()
