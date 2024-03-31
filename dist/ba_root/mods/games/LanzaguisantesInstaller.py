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
from bastd.actor.spaz import Spaz
from bastd.game.football import FootballCoopGame
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
	from typing import Any, Sequence


class ModInfo:
	mod_dir = 'lanzaguisantesData'  # folder
	mod_name = 'Lanzaguisantes'  # name
	creator = 'byANG3L' # creator
	url = 'https://youtu.be/CvX0riD18Vc' # video


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

		v = - 12
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
		v += -10
		checkbox_size = (self._width * 0.7, 50)
		checkbox_maxwidth = 250
		ba.checkboxwidget(
			parent=self.root_widget,
			position=(self._width * 0.155, self._height * 0.2 - v),
			size=checkbox_size,
			autoselect=True,
			maxwidth=checkbox_maxwidth,
			scale=1.0,
			textcolor=(0.8, 0.8, 0.8),
			value=plugin_mode['enable power'],
			text=ModLang.enable_power,
			on_value_change_call=self._set_enable,
		)
		v += 24
		ba.checkboxwidget(
			parent=self.root_widget,
			position=(self._width * 0.155, self._height * 0.1 - v),
			size=checkbox_size,
			autoselect=True,
			maxwidth=checkbox_maxwidth,
			scale=1.0,
			textcolor=(0.8, 0.8, 0.8),
			value=plugin_mode['enable power bots'],
			text=ModLang.enable_power_bots,
			on_value_change_call=self._set_enable_bots,
		)

	def _set_mode(self, val: str) -> None:
		cfg = ba.app.config
		cfg[self.cfgname]['type'] = val
		cfg.apply_and_commit()

	def _set_enable(self, val: bool) -> None:
		cfg = ba.app.config
		cfg[self.cfgname]['enable power'] = val
		cfg.apply_and_commit()

	def _set_enable_bots(self, val: bool) -> None:
		cfg = ba.app.config
		cfg[self.cfgname]['enable power bots'] = val
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


class Ball(ba.Actor):

	def __init__(self,
				 position: Sequence[float] = (0.0, 1.0, 0.0),
				 velocity: Sequence[float] = (0.0, 0.0, 0.0),
				 blast_radius: float = 0.7,
				 bomb_scale: float = 0.8,
				 source_player: ba.Player | None = None,
				 owner: ba.Node | None = None,
				 melt: bool = True,
				 bounce: bool = True,
				 explode: bool = False):
		super().__init__()
		shared = SharedObjects.get()
		self._exploded = False
		self.scale = bomb_scale
		self.blast_radius = blast_radius
		self._source_player = source_player
		self.owner = owner
		self._hit_nodes = set()
		self.ball_melt = melt
		self.ball_bounce = bounce
		self.ball_explode = explode
		self.radius = bomb_scale * 0.1
		if bomb_scale <= 1.0:
			shadow_size = 0.6
		elif bomb_scale <= 2.0:
			shadow_size = 0.4
		elif bomb_scale <= 3.0:
			shadow_size = 0.2
		else:
			shadow_size = 0.1

		self.snowball_material = ba.Material()
		self.snowball_material.add_actions(
			conditions=(
				(
					('we_are_younger_than', 5),
					'or',
					('they_are_younger_than', 100),
				),
				'and',
				('they_have_material', shared.object_material),
			),
			actions=('modify_node_collision', 'collide', False),
		)

		self.snowball_material.add_actions(
			conditions=('they_have_material', shared.pickup_material),
			actions=('modify_part_collision', 'use_node_collide', False),
		)

		self.snowball_material.add_actions(actions=('modify_part_collision',
												'friction', 0.3))

		self.snowball_material.add_actions(
			conditions=('they_have_material', shared.player_material),
			actions=(('modify_part_collision', 'physical', False),
					 ('call', 'at_connect', self.hit)))

		self.snowball_material.add_actions(
			conditions=(('they_dont_have_material', shared.player_material),
						 'and',
						('they_have_material', shared.object_material),
						 'or',
						('they_have_material', shared.footing_material)),
			actions=('call', 'at_connect', self.bounce))

		self.node = ba.newnode(
			'prop',
			delegate=self,
			attrs={
				'position': position,
				'velocity': velocity,
				'body': 'sphere',
				'body_scale': self.scale,
				'model': ba.getmodel('frostyPelvis'),
				'shadow_size': shadow_size,
				'color_texture': ba.gettexture('powerupStickyBombs'),
				'reflection': 'soft',
				'reflection_scale': [0.15],
				'density': 1.0,
				'materials': [self.snowball_material]
			})
		self.light = ba.newnode(
			'light',
			owner=self.node,
			attrs={
				'color': (0.5, 1.0, 0.5),
				'intensity': 0.8,
				'radius': self.radius
			})
		self.node.connectattr('position', self.light, 'position')
		ba.animate(self.node, 'model_scale', {
			0: 0,
			0.1: 1.3 * self.scale,
			0.26: self.scale
		})
		ba.animate(self.light, 'radius', {
			0: 0,
			0.1: 1.3 * self.radius,
			0.26: self.radius
		})
		if self.ball_melt:
			ba.timer(1.5, ba.WeakCall(self._disappear))

	def hit(self) -> None:
		if not self.node:
			return
		if self._exploded:
			return
		self._exploded = True
		if self.ball_explode:
			self.do_explode()
		self.do_hit()
		ba.timer(0.001, ba.WeakCall(self.handlemessage, ba.DieMessage()))

	def do_hit(self) -> None:
		v = self.node.velocity
		if ba.Vec3(*v).length() > 5.0:
			node = ba.getcollision().opposingnode
			if node is not None and node and not (
					node in self._hit_nodes):
				t = self.node.position
				hitdir = self.node.velocity
				self._hit_nodes.add(node)
				node.handlemessage(
					ba.HitMessage(
						pos=t,
						velocity=v,
						magnitude=ba.Vec3(*v).length()*0.5,
						velocity_magnitude=ba.Vec3(*v).length()*0.5,
						radius=0,
						srcnode=self.node,
						source_player=self._source_player,
						force_direction=hitdir,
						hit_type='snoBall',
						hit_subtype='default'))

		if self.ball_bounce:
			ba.timer(0.05, ba.WeakCall(self.do_bounce))

	def do_explode(self) -> None:
		Blast(position=self.node.position,
			  velocity=self.node.velocity,
			  blast_radius=self.blast_radius,
			  source_player=ba.existing(self._source_player),
			  blast_type='impact',
			  hit_subtype='explode').autoretain()

	def bounce(self) -> None:
		if not self.node:
			return
		vel = self.node.velocity
		ba.timer(0.1, ba.WeakCall(self.calc_bounce, vel))

	def calc_bounce(self, vel) -> None:
		if not self.node:
			return
		ospd = ba.Vec3(*vel).length()
		dot = sum(x*y for x, y in zip(vel, self.node.velocity))
		if ospd*ospd - dot > 50.0:
			ba.timer(0.05, ba.WeakCall(self.do_bounce))

	def do_bounce(self) -> None:
		if not self.node:
			return
		if not self._exploded:
			self._exploded = True
			ba.emitfx(position=self.node.position,
					  velocity=[v*0.1 for v in self.node.velocity],
					  count=10,
					  spread=0.1,
					  scale=0.4,
					  chunk_type='slime')
			sound = ba.getsound('impactMedium')
			ba.playsound(sound, 1.0, position=self.node.position)
			scl = self.node.model_scale
			ba.animate(self.node, 'model_scale', {
				0.0: scl*1.0,
				0.02: scl*0.5,
				0.05: 0.0
			})
			lr = self.light.radius
			ba.animate(self.light, 'radius', {
				0.0: lr*1.0,
				0.02: lr*0.5,
				0.05: 0.0
			})
			ba.timer(0.08,
				ba.WeakCall(self.handlemessage, ba.DieMessage()))

	def _disappear(self) -> None:
		self._exploded = True
		if self.node:
			scl = self.node.model_scale
			ba.animate(self.node, 'model_scale', {
				0.0: scl*1.0,
				0.3: scl*0.5,
				0.5: 0.0
			})
			lr = self.light.radius
			ba.animate(self.light, 'radius', {
				0.0: lr*1.0,
				0.3: lr*0.5,
				0.5: 0.0
			})
			ba.timer(0.55,
				ba.WeakCall(self.handlemessage, ba.DieMessage()))

	def handlemessage(self, msg: Any) -> Any:
		if isinstance(msg, ba.DieMessage):
			if self.node:
				self.node.delete()
		elif isinstance(msg, ba.OutOfBoundsMessage):
			self.handlemessage(ba.DieMessage())
		else:
			super().handlemessage(msg)


class CustomPower:
	def __init__(self):
		Spaz.oldinit = Spaz.__init__
		def __init__(self, **kwargs):
			self.oldinit(**kwargs)
			if not 'character' in kwargs:
				return
			self.character = kwargs['character']
			self.oldpc = self.punch_callback
			def punch_callback(player: Spaz) -> None:
				cfgname = ModInfo.mod_dir + ModInfo.mod_name
				plugin_mode = ba.app.config[cfgname]
				cfgplayer = plugin_mode['enable power']
				cfgbot = plugin_mode['enable power bots']
				if self.source_player and not cfgplayer:
					return
				if not self.source_player and not cfgbot:
					return
				if not self.character == 'Lanzaguisantes':
					return
				self.ball_scale = 0.5
				self.ball_melt = True
				self.ball_bounce = True
				self.ball_explode = False
				pos = self.node.position
				p1 = self.node.position_center
				p2 = self.node.position_forward
				direction = [p1[0]-p2[0],p2[1]-p1[1],p1[2]-p2[2]]
				direction[1] = 0.03
				mag = 20.0/ba.Vec3(*direction).length()
				vel = [v * mag for v in direction]
				Ball(position=(pos[0], pos[1] + 0.1, pos[2]),
						 velocity=vel,
						 blast_radius=self.blast_radius,
						 bomb_scale=self.ball_scale,
						 source_player=self.source_player,
						 owner=self.node,
						 melt=self.ball_melt,
						 bounce=self.ball_bounce,
						 explode=self.ball_explode).autoretain()
			self.punch_callback = punch_callback
		Spaz.__init__ = __init__

		FootballCoopGame.oldhpp = FootballCoopGame._handle_player_punched
		def spawn_player(self, player: Player) -> ba.Actor:
			spaz = self.spawn_player_spaz(
				player, position=self.map.get_start_position(player.team.id)
			)
			if self._preset in ['rookie_easy', 'pro_easy', 'uber_easy']:
				spaz.impact_scale = 0.25
			spaz.add_dropped_bomb_callback(self._handle_player_dropped_bomb)
			spaz.oldpc = spaz.punch_callback
			def _handle_player_punched(player: Spaz) -> None:
				if spaz.oldpc is not None:
					spaz.oldpc(player)
			spaz.punch_callback = _handle_player_punched
			return spaz
		FootballCoopGame.spawn_player = spawn_player


# ba_meta export plugin
class ModPlugin(ba.Plugin):

	def on_app_running(self) -> None:
		self.setup_config()
		self.custom_plugin()

	def setup_config(self) -> None:
		cfgname = ModInfo.mod_dir + ModInfo.mod_name
		if not cfgname in ba.app.config:
			mod_list = {
				'type': 'install',
				'enable power': True,
				'enable power bots': True,
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

	def custom_plugin(self) -> None:
		if ModInstaller()._installed():
			CustomPower()

	def has_settings_ui(self) -> bool:
		return True

	def show_settings_ui(self, source_widget: ba.Widget | None) -> None:
		ModSettingsPopup()
