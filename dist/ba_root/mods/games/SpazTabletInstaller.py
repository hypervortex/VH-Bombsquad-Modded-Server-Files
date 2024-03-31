# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
import os
import shutil
import hashlib
from bastd.ui import popup

if TYPE_CHECKING:
	pass


class ModInfo:
	mod_dir = 'spazTabletData'  # folder
	mod_name = 'Spaz Tablet'  # name
	creator = 'byANG3L' # creator
	url = 'https://youtu.be/WCq3yAis7VU' # video


class ModLang:
	lang = ba.app.lang.language
	if lang == 'Spanish':
		install_success = '¡Instalación Exitosa!'
		install_fail = '¡Instalación Fallida!'
		uninstall_success = '¡Desinstalación Exitosa!'
		uninstall_fail = '¡Desinstalación Fallida!'
		created = 'Creado por: ' + ModInfo.creator
		title = 'Opciones del Mod'
		install_type = 'Tipo de Instalación'
		enable_power = 'Habilitar Poder'
		enable_power_bots = 'Habilitar Poder en Bots'
		install = 'Instalar'
		uninstall = 'Desinstalar'
	elif lang == 'Chinese':
		install_success = '安装成功！'
		install_fail = '安装失败！'
		uninstall_success = '卸载成功！'
		uninstall_fail = '卸载失败！'
		created = '由...制作： ' + ModInfo.creator
		title = '模组设置'
		install_type = '安装类型'
		enable_power = '启用电源'
		enable_power_bots = '启用机器人电源'
		install = '安装'
		uninstall = '卸载'
	else:
		install_success = 'Installation Successful!'
		install_fail = 'Installation Failed!'
		uninstall_success = 'Uninstallation Successful!'
		uninstall_fail = 'Uninstallation Failed!'
		created = 'Created by: ' + ModInfo.creator
		title = 'Mod Settings'
		install_type = 'Installation Type'
		enable_power = 'Enable Power'
		enable_power_bots = 'Enable Power on Bots'
		install = 'Install'
		uninstall = 'Uninstall'


class ModInstallPopup(popup.PopupWindow):

	def __init__(self, success: bool = True, unistall: bool = False):
		app = ba.app
		uiscale = app.ui.uiscale
		self._width = 400
		self._height = 310
		bg_color = (0.5, 0.4, 0.6)
		scale = (1.8 if uiscale is ba.UIScale.SMALL else
				 1.4 if uiscale is ba.UIScale.MEDIUM else 1.0)
		popup.PopupWindow.__init__(self,
								   position=(0.0, 0.0),
								   size=(self._width, self._height),
								   scale=scale,
								   bg_color=bg_color)

		mode = 'uninstall' if unistall else 'install'

		if mode == 'install' and success:
			install = ModLang.install_success
			sound = 'achievement'
			image = 'chestOpenIcon'
			color = (0.0, 1.0, 0.0)
			modcolor = (1.0, 1.0, 1.0)
			extray = 0
		elif mode == 'install' and not success:
			install = ModLang.install_fail
			sound = 'kronk2'
			image = 'chestIcon'
			color = (1.0, 0.1, 0.1)
			modcolor = (0.7, 0.7, 0.7)
			extray = -2
		elif mode == 'uninstall' and success:
			install = ModLang.uninstall_success
			sound = 'achievement'
			image = 'chestOpenIcon'
			color = (0.0, 1.0, 0.0)
			modcolor = (1.0, 1.0, 1.0)
			extray = 0
		elif mode == 'uninstall' and not success:
			install = ModLang.uninstall_fail
			sound = 'kronk2'
			image = 'chestIcon'
			color = (1.0, 0.1, 0.1)
			modcolor = (0.7, 0.7, 0.7)
			extray = -2

		save_button = btn = ba.buttonwidget(
			parent=self.root_widget,
			position=(self._width * 0.5 - 75, self._height * 0.07),
			size=(150, 52),
			scale=1.0,
			autoselect=True,
			color=(0.2, 0.8, 0.55),
			label=ba.Lstr(resource='okText'),
			on_activate_call=self.close
		)
		ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.5, self._height * 0.9),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=1.1,
			text=install,
			maxwidth=self._width * 0.7,
			color=color
		)
		ba.imagewidget(
			parent=self.root_widget,
			position=(self._width * 0.5 - 55, self._height * 0.494 + extray),
			size=(110, 110),
			texture=ba.gettexture(image)
		)
		ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.5, self._height * 0.426),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=1.3,
			text=ModInfo.mod_name,
			maxwidth=self._width * 0.7,
			color=modcolor
		)
		ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.5, self._height * 0.314),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=0.8,
			text=ModLang.created,
			maxwidth=self._width * 0.7,
			color=(1.0, 1.0, 0.0)
		)
		if not success:
			ba.playsound(ba.getsound('error'))
		ba.playsound(ba.getsound(sound))

	def close(self) -> None:
		ba.containerwidget(
			edit=self.root_widget,
			transition='out_scale'
		)


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

		self.cfgname = ModInfo.mod_dir + ModInfo.mod_name
		plugin_mode = ba.app.config[self.cfgname]

		v = 20
		ba.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.304, self._height * 0.57 - v),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=1.0,
			text=ModLang.install_type,
			maxwidth=230,
			color=(0.8, 0.8, 0.8, 1.0),
		)
		popup.PopupMenu(
			parent=self.root_widget,
			position=(self._width * 0.58, self._height * 0.48 - v),
			width=150,
			choices=['install', 'uninstall'],
			choices_display=[
				ba.Lstr(value=ModLang.install),
				ba.Lstr(value=ModLang.uninstall),
			],
			current_choice=plugin_mode['type'],
			on_value_change_call=self._set_mode,
		)

	def _set_mode(self, val: str) -> None:
		cfg = ba.app.config
		cfg[self.cfgname]['type'] = val
		cfg.apply_and_commit()

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


class ModInstaller:

	def __init__(self) -> None:
		self.python_user = _ba.env()["python_directory_user"]
		self.cfiles = self.python_user + '/' + ModInfo.mod_dir + '/'
		self.app_dir = _ba.env()["python_directory_app"] + '/'
		self.data_dir = self.app_dir + '../'
		self.models_dir = self.data_dir + 'models/'
		self.audios_dir = self.data_dir + 'audio/'
		self.textures_dir = self.data_dir + 'textures/'
		self.platform = _ba.app.platform
		self.audios: list = []
		self.models: list = []
		self.textures: list = []
		self.get_mod()

	def get_mod(self) -> None:
		fls = os.listdir(self.cfiles)
		for fl in fls:
			if fl.endswith('.ogg'): # audio
				self.audios.append(fl)
			if fl.endswith('.bob') or fl.endswith('.cob'): # models
				self.models.append(fl)
			if fl.endswith('.ktx') or fl.endswith('.dds'): # textures
				self.textures.append(fl)

	@staticmethod
	def check_file_same(f1, f2):
		try:
			md5s = [hashlib.md5(), hashlib.md5()]
			fs = [f1, f2]
			for i in range(2):
				f = open(fs[i], 'rb')
				block_size = 2 ** 20
				while True:
					data = f.read(block_size)
					if not data: break
					md5s[i].update(data)
				f.close()
				md5s[i] = md5s[i].hexdigest()
			return md5s[0] == md5s[1]
		except Exception as e:
			return False

	def _installed(self) -> None:
		installed = True
		for a in self.audios:
			app = self.audios_dir + a
			user = self.cfiles + a
			if not os.path.isfile(app):
				installed = False
				break
			if not self.check_file_same(app, user):
				installed = False
				break
		for m in self.models:
			app = self.models_dir + m
			user = self.cfiles + m
			if not os.path.isfile(app):
				installed = False
				break
			if not self.check_file_same(app, user):
				installed = False
				break
		for t in self.textures:
			if self.platform == 'android':
				if t.endswith('.dds'):
					continue
			else:
				if t.endswith('.ktx'):
					continue
			app = self.textures_dir + t
			user = self.cfiles + t
			if not os.path.isfile(app):
				installed = False
				break
			if not self.check_file_same(app, user):
				installed = False
				break
		return installed

	def install_mod(self) -> None:
		if self._installed():
			return
		try:
			for a in self.audios:
				app = self.audios_dir + a
				user = self.cfiles + a
				shutil.copyfile(user, app)
			for m in self.models:
				app = self.models_dir + m
				user = self.cfiles + m
				shutil.copyfile(user, app)
			for t in self.textures:
				if self.platform == 'android':
					if t.endswith('.dds'):
						continue
				else:
					if t.endswith('.ktx'):
						continue
				app = self.textures_dir + t
				user = self.cfiles + t
				shutil.copyfile(user, app)
			ba.timer(1.0, ba.Call(ModInstallPopup, True))
		except:
			ba.timer(1.0, ba.Call(ModInstallPopup, False))

	def uninstall_mod(self) -> None:
		if not self._installed():
			return
		try:
			for a in self.audios:
				app = self.audios_dir + a
				os.remove(app)
			for m in self.models:
				app = self.models_dir + m
				os.remove(app)
			for t in self.textures:
				if self.platform == 'android':
					if t.endswith('.dds'):
						continue
				else:
					if t.endswith('.ktx'):
						continue
				app = self.textures_dir + t
				os.remove(app)
			ba.timer(1.0, ba.Call(ModInstallPopup, True, True))
		except:
			ba.timer(1.0, ba.Call(ModInstallPopup, False, True))


# ba_meta export plugin
class ModPlugin(ba.Plugin):

	def on_app_running(self) -> None:
		self.setup_config()

	def setup_config(self) -> None:
		cfgname = ModInfo.mod_dir + ModInfo.mod_name
		if not cfgname in ba.app.config:
			mod_list = {
				'type': 'install',
			}
			ba.app.config[cfgname] = mod_list
			ba.app.config.apply_and_commit()
		plugin_mode = ba.app.config[cfgname]
		if plugin_mode['type'] == 'install':
			ModInstaller().install_mod()
			if ModInstaller()._installed():
				exec('import ' + ModInfo.mod_dir + '.banewmod')
		else:
			ModInstaller().uninstall_mod()

	def has_settings_ui(self) -> bool:
		return True

	def show_settings_ui(self, source_widget: ba.Widget | None) -> None:
		ModSettingsPopup()
