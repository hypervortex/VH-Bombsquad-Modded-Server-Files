# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 7

from __future__ import annotations
import logging
import math

from typing import TYPE_CHECKING

import random
import ba
import _ba
from bastd.mainmenu import MainMenuActivity
from bastd.ui import popup
from bastd.ui.playlist.addgame import PlaylistAddGameWindow
from bastd.ui.popup import PopupMenu
from bastd.ui.coop.tournamentbutton import TournamentButton
from bastd.ui.mainmenu import MainMenuWindow
from bastd.ui.play import PlayWindow
from bastd.ui.coop.browser import CoopBrowserWindow
from bastd.ui.coop.gamebutton import GameButton
from bastd.ui.playlist.browser import PlaylistBrowserWindow
from bastd.ui.playoptions import PlayOptionsWindow
from bastd.ui.settings.allsettings import AllSettingsWindow
from bastd.ui.settings.plugins import PluginWindow

if TYPE_CHECKING:
	from typing import Any


class ModInfo:
	cfgname = 'Christmas Theme' # config name
	cfglist = {
		'enable_mod': True,
	} # config list
	url = 'https://youtu.be/XJw7TzN7oZA?si=4Uj8PcYjii8hAyCt' # video


class ModLang:
	lang = ba.app.lang.language
	if lang == 'Spanish':
		title = 'Opciones del Mod'
		enable = 'Habilitar Tema'
	elif lang == 'Chinese':
		title = '模组设置'
		enable = '启用主题'
	else:
		title = 'Mod Settings'
		enable = 'Enable Theme'


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
			bg_color=bg_color,
		)

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
		
		v = 0
		v += 165
		ba.checkboxwidget(
			parent=self.root_widget,
			position=(self._width * 0.155, self._height - v),
			size=checkbox_size,
			autoselect=True,
			maxwidth=checkbox_maxwidth,
			scale=1.0,
			textcolor=(0.8, 0.8, 0.8),
			value=ba.app.config[ModInfo.cfgname]['enable_mod'],
			text=ModLang.enable,
			on_value_change_call=self._enable_mod,
		)

	def _enable_mod(self, val: bool) -> None:
		ba.app.config[ModInfo.cfgname]['enable_mod'] = val
		ba.app.config.apply_and_commit()
		from bastd.mainmenu import MainMenuSession
		ba.app.ui.clear_main_menu_window()
		_ba.new_host_session(MainMenuSession)
		ModSettingsPopup()

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


# ba_meta export plugin
class ModPlugin(ba.Plugin):

	def on_app_running(self) -> None:
		self.setup_config()
		self.custom_mod()
		from bastd.mainmenu import MainMenuSession
		ba.app.ui.clear_main_menu_window()
		_ba.new_host_session(MainMenuSession)
		
	def custom_mod(self) -> None:
		blue = (0.2, 0.6, 0.8)
		light_blue = (0.3, 0.7, 0.8)
		dark_blue = (0.2, 0.5, 0.6)
		text_blue = (0.8, 1.0, 1.0)
		title_color = (0.45, 0.65, 0.7)
		heading_color = (0.45, 0.6, 0.7)
		bgcolor = (0.25, 0.3, 0.35)
		bgcolor2 = (0.3, 0.35, 0.4)
		button_color = blue
		ba.oldbuttonwidget = ba.buttonwidget
		def buttonwidget(**kwargs):
			if ba.app.config[ModInfo.cfgname]['enable_mod']:
				buttons = [
					'<ba.Lstr: {"r":"mainMenu.howToPlayText"}>',
					'<ba.Lstr: {"r":"mainMenu.creditsText"}>',
					'<ba.Lstr: {"r":"mainMenu.settingsText"}>',
					'<ba.Lstr: {"r":"storeText"}>',
					'-', '+', '<', '>', '...',
					'<ba.Lstr: {"r":"gatherWindow.makePartyPublicText","f":"gatherWindow.startAdvertisingText"}>',
					'<ba.Lstr: {"r":"gatherWindow.manualConnectText"}>',
					'<ba.Lstr: {"r":"gatherWindow.startHostingText"}>',
					'<ba.Lstr: {"r":"gatherWindow.favoritesSaveText"}>',
					'<ba.Lstr: {"r":"editText"}>',
					'<ba.Lstr: {"r":"deleteText"}>',
					'<ba.Lstr: {"r":"mapSelectText"}>',
					'<ba.Lstr: {"r":"configControllersWindow.configureTouchText"}>',
					'<ba.Lstr: {"r":"configControllersWindow.configureControllersText"}>',
					'<ba.Lstr: {"r":"configControllersWindow.configureKeyboardText"}>',
					'<ba.Lstr: {"r":"configControllersWindow.configureKeyboard2Text"}>',
					'<ba.Lstr: {"r":"configControllersWindow.configureMobileText"}>',
					'<ba.Lstr: {"r":"restartText"}>',
					'<ba.Lstr: {"r":"mainMenu.settingsText"}>',
					'<ba.Lstr: {"r":"mainMenu.endGameText"}>',
					'<ba.Lstr: {"r":"audioSettingsWindow.soundtrackButtonText"}>',
					'<ba.Lstr: {"r":"settingsWindowAdvanced.enterPromoCodeText"}>',
					'<ba.Lstr: {"r":"settingsWindowAdvanced.translationEditorButtonText","s":[["${APP_NAME}",{"r":"titleText"}]]}>',
					'<ba.Lstr: {"r":"settingsWindowAdvanced.moddingGuideText"}>',
					'<ba.Lstr: {"r":"settingsWindowAdvanced.showUserModsText"}>',
					'<ba.Lstr: {"r":"pluginsText"}>',
					'<ba.Lstr: {"r":"settingsWindowAdvanced.netTestingText"}>',
					'<ba.Lstr: {"r":"settingsWindowAdvanced.benchmarksText"}>',
					'<ba.Lstr: {"r":"pluginsEnableAllText"}>',
					'<ba.Lstr: {"r":"pluginsDisableAllText"}>',
					'<ba.Lstr: {"r":"copyText"}>',
					'<ba.Lstr: {"v":"..."}>',
					'<ba.Lstr: {"r":"debugWindow.runCPUBenchmarkText"}>',
					'<ba.Lstr: {"r":"debugWindow.runGPUBenchmarkText"}>',
					'<ba.Lstr: {"r":"debugWindow.runMediaReloadBenchmarkText"}>',
					'<ba.Lstr: {"r":"debugWindow.runStressTestText"}>',
					'<ba.Lstr: {"r":"gatherWindow.emailItText"}>',
					'<ba.Lstr: {"r":"configTouchscreenWindow.resetText"}>',
					'<ba.Lstr: {"r":"mainMenu.leavePartyText"}>',
				]
				if 'label' in kwargs:
					if str(kwargs['label']) in [
							'<ba.Lstr: {"r":"playText"}>',
							'<ba.Lstr: {"r":"partyWindow.sendText"}>']:
						kwargs['color'] = (0.5, 0.4, 0.9)
						kwargs['textcolor'] = text_blue
					elif str(kwargs['label']) == '<ba.Lstr: {"r":"mainMenu.exitGameText"}>':
						kwargs['color'] = (0.7, 0.4, 0.34)
						kwargs['textcolor'] = (0.9, 0.9, 1.0)
					elif str(kwargs['label']) in buttons:
						kwargs['color'] = button_color
						kwargs['textcolor'] = text_blue
				if 'button_type' in kwargs:
					if kwargs['button_type'] in ['back','backSmall']:
						kwargs['color'] = (0.7, 0.4, 0.34)
						kwargs['textcolor'] = (0.8, 1.1, 1.1)
					elif kwargs['button_type'] == 'tab':
						kwargs['textcolor'] = (0.6, 0.7, 0.8)
				if 'icon' in kwargs:
					if str(kwargs['icon']) == '<ba.Texture "crossOut">':
						kwargs['color'] = (0.7, 0.4, 0.34)
			return ba.oldbuttonwidget(**kwargs)
		ba.buttonwidget = buttonwidget

		ba.oldtextwidget = ba.textwidget
		def textwidget(**kwargs):
			if ba.app.config[ModInfo.cfgname]['enable_mod']:
				if 'text' in kwargs:
					texts = [
						'<ba.Lstr: {"r":"playModes.singlePlayerCoopText","f":"playModes.coopText"}>',
						'<ba.Lstr: {"r":"playModes.teamsText","f":"teamsText"}>',
						'<ba.Lstr: {"r":"playModes.freeForAllText","f":"freeForAllText"}>',
						'<ba.Lstr: {"r":"gatherWindow.titleText"}>',
						'<ba.Lstr: {"r":"watchWindow.titleText"}>',
					]
					if str(kwargs['text']) in texts and kwargs['color'] not in [ba.app.ui.title_color,ba.app.ui.heading_color]:
						kwargs['color'] = text_blue
					
				if 'color' in kwargs:
					if kwargs['color'] == ba.app.ui.title_color:
						kwargs['color'] = title_color
					elif kwargs['color'] == ba.app.ui.heading_color:
						kwargs['color'] = heading_color
					elif kwargs['color'] == (0.6, 1.0, 0.6):
						kwargs['color'] = (0.6, 1.0, 0.8)
					elif kwargs['color'] == (0.5, 0.4, 0.5):
						kwargs['color'] = (0.4, 0.5, 0.6)
					elif kwargs['color'] == (0.5, 0.8, 0.5, 1.0):
						kwargs['color'] = (0.4, 0.85, 0.85, 1.0)
					elif kwargs['color'] in [
							(0.7, 0.9, 0.7, 1.0),
							(0.5, 1, 0.5, 1),
							(0.3, 1.0, 0.3, 1.0),
							(0.7, 1.0, 0.7, 1.0)]:
						kwargs['color'] = (0.5, 0.9, 0.9, 1.0)
			return ba.oldtextwidget(**kwargs)
		ba.textwidget = textwidget

		ba.oldcheckboxwidget = ba.checkboxwidget
		def checkboxwidget(**kwargs):
			if ba.app.config[ModInfo.cfgname]['enable_mod']:
				if 'color' not in kwargs:
					kwargs['color'] = button_color
					kwargs['textcolor'] = text_blue
			return ba.oldcheckboxwidget(**kwargs)
		ba.checkboxwidget = checkboxwidget

		ba.oldcontainerwidget = ba.containerwidget
		def containerwidget(**kwargs):
			if ba.app.config[ModInfo.cfgname]['enable_mod']:
				if 'color' in kwargs:
					if kwargs['color'] == (0.35, 0.55, 0.15):
						kwargs['color'] = bgcolor
				else:
					kwargs['color'] = bgcolor2
			return ba.oldcontainerwidget(**kwargs)
		ba.containerwidget = containerwidget

		# MAIN MENU ACTIVITY
		MainMenuActivity.old_on_transition_in = MainMenuActivity.on_transition_in
		def on_transition_in(self) -> None:
			self.old_on_transition_in()
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				return
			# snow
			def snow():
				ba.emitfx(
					position=(
						-10 + 20 *random.random(),
						20,
						-10 + 20 *random.random(),
					),
					velocity=(0,0,0),
					scale=1.5 * random.random() + 0.2,
					count=20,
					chunk_type='ice',
				)
				ba.emitfx(
					position=(
						-10 + 20 * random.random(),
						-10 + 25 * random.random(),
						-10 + 20 * random.random(),
					),
					emit_type='fairydust',
				)
				ba.emitfx(
					position=(
						-10 + 20 * random.random(),
						-10 + 25 * random.random(),
						-10 + 20 * random.random(),
					),
					emit_type='fairydust',
				)
			ba.timer(0.1, snow, repeat=True)
			lang = ba.app.lang.language
			if lang == 'Spanish':
				text = '¡Feliz Navidad!'
			else:
				text = 'Merry Christmas!'
			if self.beta_info is not None:
				self.beta_info.node.text = text
				self.beta_info.node.color = (1, 0.2, 0.2)
			else:
				ba.newnode(
					'text',
					attrs={
						'v_attach': 'center',
						'h_align': 'center',
						'color': (1, 0.2, 0.2),
						'shadow': 0.5,
						'flatness': 0.5,
						'scale': 1,
						'vr_depth': -60,
						'position': (230, 35),
						'text': text,
					},
				)

			gnode = self.globalsnode
			gnode.tint = (0.6, 0.8, 1.1)
			self.trees.node.color = (0.2, 1.6, 1.8)
			self.trees.node.reflection_scale = [5]
			self.bgterrain.node.color = (0.9, 1.2, 1.2)
			tex = ba.gettexture('tipTopBGColor')
			self.bgterrain.node.color_texture = tex
			invert = False
			for actor in self._word_actors:
				if actor.node.vr_depth != -130:
					if invert:
						actor.node.color = (1.0, 0.2, 0.2)
					else:
						actor.node.color = (0.1, 0.8, 0.1)
				else:
					if invert:
						actor.node.color = (0.2, 0.3, 0.2, 0.6)
					else:
						actor.node.color = (0.5, 0.2, 0.2, 0.6)
				if invert:
					invert = False
				else:
					invert = True
			self._word_actors[-1].node.color = (1.0, 1.0, 1.0)
		MainMenuActivity.on_transition_in = on_transition_in

		# MAIN MENU WINDOW
		MainMenuWindow.oldrefresh = MainMenuWindow._refresh
		def _refresh(self) -> None:
			self.oldrefresh()
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				return
			if self._gather_button:
				ba.buttonwidget(
					edit=self._gather_button, color=button_color)
			if self._watch_button:
				ba.buttonwidget(
					edit=self._watch_button, color=button_color)
			if self._account_button:
				ba.buttonwidget(
					edit=self._account_button, color=button_color)
		MainMenuWindow._refresh = _refresh

		# PLAY WINDOW
		PlayWindow.oldinit = PlayWindow.__init__
		def __init__(self, **kwargs) -> None:
			self.oldinit(**kwargs)
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				return
			ba.buttonwidget(
				edit=self._coop_button, color=button_color)
			ba.buttonwidget(
				edit=self._teams_button, color=button_color)
			ba.buttonwidget(
				edit=self._free_for_all_button, color=button_color)
		PlayWindow.__init__ = __init__

		# COOP WINDOW
		CoopBrowserWindow._old_refresh_campaign_row = CoopBrowserWindow._refresh_campaign_row
		def _refresh_campaign_row(self) -> None:
			self._old_refresh_campaign_row()
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				return
			ba.buttonwidget(
				edit=self._easy_button, color=light_blue)
			ba.buttonwidget(
				edit=self._hard_button, color=dark_blue)
		CoopBrowserWindow._refresh_campaign_row = _refresh_campaign_row

		# GAME BUTTON WINDOW
		GameButton._old_update = GameButton._update
		def _update(self) -> None:
			self._old_update()
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				return
			# pylint: disable=too-many-boolean-expressions
			from ba.internal import getcampaign

			# In case we stick around after our UI...
			if not self._button:
				return

			game = self._game
			campaignname, levelname = game.split(':')

			# Hack - The Last Stand doesn't actually exist in the
			# easy tourney; we just want it for display purposes. Map it to
			# the hard-mode version.
			if game == 'Easy:The Last Stand':
				campaignname = 'Default'

			campaign = getcampaign(campaignname)

			# If this campaign is sequential, make sure we've unlocked
			# everything up to here.
			unlocked = True
			if campaign.sequential:
				for level in campaign.levels:
					if level.name == levelname:
						break
					if not level.complete:
						unlocked = False
						break

			# We never actually allow playing last-stand on easy mode.
			if game == 'Easy:The Last Stand':
				unlocked = False

			# Hard-code games we haven't unlocked.
			if (
				(
					game
					in (
						'Challenges:Infinite Runaround',
						'Challenges:Infinite Onslaught',
					)
					and not ba.app.accounts_v1.have_pro()
				)
				or (
					game in ('Challenges:Meteor Shower',)
					and not ba.internal.get_purchased('games.meteor_shower')
				)
				or (
					game
					in (
						'Challenges:Target Practice',
						'Challenges:Target Practice B',
					)
					and not ba.internal.get_purchased('games.target_practice')
				)
				or (
					game in ('Challenges:Ninja Fight',)
					and not ba.internal.get_purchased('games.ninja_fight')
				)
				or (
					game in ('Challenges:Pro Ninja Fight',)
					and not ba.internal.get_purchased('games.ninja_fight')
				)
				or (
					game
					in (
						'Challenges:Easter Egg Hunt',
						'Challenges:Pro Easter Egg Hunt',
					)
					and not ba.internal.get_purchased('games.easter_egg_hunt')
				)
			):
				unlocked = False
			unlocked_color = (
				light_blue if game.startswith('Easy:') else dark_blue
			)
			ba.buttonwidget(
				edit=self._button,
				color=unlocked_color if unlocked else (0.5, 0.5, 0.5),
			)
			ba.textwidget(
				edit=self._name_widget,
				color=text_blue if unlocked else (0.7, 0.7, 0.7, 0.7),
			)
		GameButton._update = _update

		TournamentButton.old_update_for_data = TournamentButton.update_for_data
		def update_for_data(self, entry: dict[str, Any]) -> None:
			self.old_update_for_data(entry)
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				return
			from ba.internal import getcampaign, get_tournament_prize_strings

			prize_y_offs = (
				34
				if 'prizeRange3' in entry
				else 20
				if 'prizeRange2' in entry
				else 12
			)
			x_offs = 90

			# This seems to be a false alarm.
			# pylint: disable=unbalanced-tuple-unpacking
			pr1, pv1, pr2, pv2, pr3, pv3 = get_tournament_prize_strings(entry)
			# pylint: enable=unbalanced-tuple-unpacking
			enabled = 'requiredLeague' not in entry
			ba.buttonwidget(
				edit=self.button,
				color=button_color if enabled else (0.5, 0.5, 0.5),
			)
			ba.textwidget(
				edit=self.button_text,
				color=text_blue if enabled else (0.5, 0.5, 0.5),
			)
		TournamentButton.update_for_data = update_for_data

		PlaylistBrowserWindow._old_refresh = PlaylistBrowserWindow._refresh
		def _refresh(self) -> None:
			self._old_refresh()
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				return
			# FIXME: Should tidy this up.
			# pylint: disable=too-many-statements
			# pylint: disable=too-many-branches
			# pylint: disable=too-many-locals
			# pylint: disable=too-many-nested-blocks
			from efro.util import asserttype
			from ba.internal import get_map_class, filter_playlist

			if not self._root_widget:
				return
			if self._subcontainer is not None:
				self._save_state()
				self._subcontainer.delete()

			# Make sure config exists.
			if self._config_name_full not in ba.app.config:
				ba.app.config[self._config_name_full] = {}

			items = list(ba.app.config[self._config_name_full].items())

			# Make sure everything is unicode.
			items = [
				(i[0].decode(), i[1]) if not isinstance(i[0], str) else i
				for i in items
			]

			items.sort(key=lambda x2: asserttype(x2[0], str).lower())
			items = [['__default__', None]] + items  # default is always first

			count = len(items)
			columns = 3
			rows = int(math.ceil(float(count) / columns))
			button_width = 230
			button_height = 230
			button_buffer_h = -3
			button_buffer_v = 0

			self._sub_width = self._scroll_width
			self._sub_height = (
				40.0 + rows * (button_height + 2 * button_buffer_v) + 90
			)
			assert self._sub_width is not None
			assert self._sub_height is not None
			self._subcontainer = ba.containerwidget(
				parent=self._scrollwidget,
				size=(self._sub_width, self._sub_height),
				background=False,
			)

			children = self._subcontainer.get_children()
			for child in children:
				child.delete()

			assert ba.app.classic is not None
			ba.textwidget(
				parent=self._subcontainer,
				text=ba.Lstr(resource='playlistsText'),
				position=(40, self._sub_height - 26),
				size=(0, 0),
				scale=1.0,
				maxwidth=400,
				color=ba.app.ui.title_color,
				h_align='left',
				v_align='center',
			)

			index = 0
			appconfig = ba.app.config

			model_opaque = ba.getmodel('level_select_button_opaque')
			model_transparent = ba.getmodel('level_select_button_transparent')
			mask_tex = ba.gettexture('mapPreviewMask')

			h_offs = 225 if count == 1 else 115 if count == 2 else 0
			h_offs_bottom = 0

			uiscale = ba.app.ui.uiscale
			for y in range(rows):
				for x in range(columns):
					name = items[index][0]
					assert name is not None
					pos = (
						x * (button_width + 2 * button_buffer_h)
						+ button_buffer_h
						+ 8
						+ h_offs,
						self._sub_height
						- 47
						- (y + 1) * (button_height + 2 * button_buffer_v),
					)
					btn = ba.buttonwidget(
						parent=self._subcontainer,
						button_type='square',
						size=(button_width, button_height),
						autoselect=True,
						label='',
						position=pos,
						color=button_color,
					)

					if (
						x == 0
						and ba.app.ui.use_toolbars
						and uiscale is ba.UIScale.SMALL
					):
						ba.widget(
							edit=btn,
							left_widget=ba.get_special_widget('back_button'),
						)
					if (
						x == columns - 1
						and ba.app.ui.use_toolbars
						and uiscale is ba.UIScale.SMALL
					):
						ba.widget(
							edit=btn,
							right_widget=ba.get_special_widget('party_button'),
						)
					ba.buttonwidget(
						edit=btn,
						on_activate_call=ba.Call(
							self._on_playlist_press, btn, name
						),
						on_select_call=ba.Call(self._on_playlist_select, name),
					)
					ba.widget(edit=btn, show_buffer_top=50, show_buffer_bottom=50)

					if self._selected_playlist == name:
						ba.containerwidget(
							edit=self._subcontainer,
							selected_child=btn,
							visible_child=btn,
						)

					if self._back_button is not None:
						if y == 0:
							ba.widget(edit=btn, up_widget=self._back_button)
						if x == 0:
							ba.widget(edit=btn, left_widget=self._back_button)

					print_name: str | ba.Lstr | None
					if name == '__default__':
						print_name = self._pvars.default_list_name
					else:
						print_name = name
					ba.textwidget(
						parent=self._subcontainer,
						text=print_name,
						position=(
							pos[0] + button_width * 0.5,
							pos[1] + button_height * 0.79,
						),
						size=(0, 0),
						scale=button_width * 0.003,
						maxwidth=button_width * 0.7,
						draw_controller=btn,
						h_align='center',
						v_align='center',
						color=text_blue,
					)

					# Poke into this playlist and see if we can display some of
					# its maps.
					map_images = []
					try:
						map_textures = []
						map_texture_entries = []
						if name == '__default__':
							playlist = self._pvars.get_default_list_call()
						else:
							if (
								name
								not in appconfig[
									self._pvars.config_name + ' Playlists'
								]
							):
								print(
									'NOT FOUND ERR',
									appconfig[
										self._pvars.config_name + ' Playlists'
									],
								)
							playlist = appconfig[
								self._pvars.config_name + ' Playlists'
							][name]
						playlist = filter_playlist(
							playlist,
							self._sessiontype,
							remove_unowned=False,
							mark_unowned=True,
							name=name,
						)
						for entry in playlist:
							mapname = entry['settings']['map']
							maptype: type[ba.Map] | None
							try:
								maptype = get_map_class(mapname)
							except ba.NotFoundError:
								maptype = None
							if maptype is not None:
								tex_name = maptype.get_preview_texture_name()
								if tex_name is not None:
									map_textures.append(tex_name)
									map_texture_entries.append(entry)
							if len(map_textures) >= 6:
								break

						if len(map_textures) > 4:
							img_rows = 3
							img_columns = 2
							scl = 0.33
							h_offs_img = 30
							v_offs_img = 126
						elif len(map_textures) > 2:
							img_rows = 2
							img_columns = 2
							scl = 0.35
							h_offs_img = 24
							v_offs_img = 110
						elif len(map_textures) > 1:
							img_rows = 2
							img_columns = 1
							scl = 0.5
							h_offs_img = 47
							v_offs_img = 105
						else:
							img_rows = 1
							img_columns = 1
							scl = 0.75
							h_offs_img = 20
							v_offs_img = 65

						v = None
						for row in range(img_rows):
							for col in range(img_columns):
								tex_index = row * img_columns + col
								if tex_index < len(map_textures):
									entry = map_texture_entries[tex_index]

									owned = not (
										(
											'is_unowned_map' in entry
											and entry['is_unowned_map']
										)
										or (
											'is_unowned_game' in entry
											and entry['is_unowned_game']
										)
									)

									tex_name = map_textures[tex_index]
									h = pos[0] + h_offs_img + scl * 250 * col
									v = pos[1] + v_offs_img - scl * 130 * row
									map_images.append(
										ba.imagewidget(
											parent=self._subcontainer,
											size=(scl * 250.0, scl * 125.0),
											position=(h, v),
											texture=ba.gettexture(tex_name),
											opacity=1.0 if owned else 0.25,
											draw_controller=btn,
											model_opaque=model_opaque,
											model_transparent=model_transparent,
											mask_texture=mask_tex,
										)
									)
									if not owned:
										ba.imagewidget(
											parent=self._subcontainer,
											size=(scl * 100.0, scl * 100.0),
											position=(h + scl * 75, v + scl * 10),
											texture=ba.gettexture('lock'),
											draw_controller=btn,
										)
							if v is not None:
								v -= scl * 130.0

					except Exception:
						logging.exception('Error listing playlist maps.')

					if not map_images:
						ba.textwidget(
							parent=self._subcontainer,
							text='???',
							scale=1.5,
							size=(0, 0),
							color=(1, 1, 1, 0.5),
							h_align='center',
							v_align='center',
							draw_controller=btn,
							position=(
								pos[0] + button_width * 0.5,
								pos[1] + button_height * 0.5,
							),
						)

					index += 1

					if index >= count:
						break
				if index >= count:
					break
			self._customize_button = btn = ba.buttonwidget(
				parent=self._subcontainer,
				size=(100, 30),
				position=(34 + h_offs_bottom, 50),
				text_scale=0.6,
				label=ba.Lstr(resource='customizeText'),
				on_activate_call=self._on_customize_press,
				color=(0.54, 0.52, 0.67),
				textcolor=(0.7, 0.65, 0.7),
				autoselect=True,
			)
			ba.widget(edit=btn, show_buffer_top=22, show_buffer_bottom=28)
			self._restore_state()
		PlaylistBrowserWindow._refresh = _refresh

		PlayOptionsWindow.oldinit = PlayOptionsWindow.__init__
		def __init__(self, **kwargs):
			self.oldinit(**kwargs)
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				return
			if self._custom_colors_names_button:
				ba.buttonwidgetwidget(
					edit=self._custom_colors_names_button,
					color=button_color,
				)
		PlayOptionsWindow.__init__ = __init__

		AllSettingsWindow.oldinit = AllSettingsWindow.__init__
		def __init__(self, **kwargs):
			self.oldinit(**kwargs)
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				return
			ba.buttonwidget(
				edit=self._controllers_button,
				color=button_color,
			)
			ba.buttonwidget(
				edit=self._graphics_button,
				color=button_color,
			)
			ba.buttonwidget(
				edit=self._audio_button,
				color=button_color,
			)
			ba.buttonwidget(
				edit=self._advanced_button,
				color=button_color,
			)
		AllSettingsWindow.__init__ = __init__

		PopupMenu.oldinit = PopupMenu.__init__
		def __init__(self, **kwargs):
			self.oldinit(**kwargs)
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				return
			ba.buttonwidget(
				edit=self._button,
				color=button_color,
				textcolor=text_blue,
			)
		PopupMenu.__init__ = __init__

		PluginWindow.oldinit = PluginWindow.__init__
		def __init__(self, **kwargs):
			self.oldinit(**kwargs)
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				return
			ba.buttonwidget(
				edit=self._settings_button,
				color=button_color,
				textcolor=text_blue,
			)
		PluginWindow.__init__ = __init__

		MainMenuWindow._old_refresh_in_game = MainMenuWindow._refresh_in_game
		def _refresh_in_game(
			self, positions: list[tuple[float, float, float]]
		) -> tuple[float, float, float]:
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				self._old_refresh_in_game(positions)
			else:
				# pylint: disable=too-many-branches
				# pylint: disable=too-many-locals
				# pylint: disable=too-many-statements
				custom_menu_entries: list[dict[str, Any]] = []
				session = ba.internal.get_foreground_host_session()
				if session is not None:
					try:
						custom_menu_entries = session.get_custom_menu_entries()
						for cme in custom_menu_entries:
							if (
								not isinstance(cme, dict)
								or 'label' not in cme
								or not isinstance(cme['label'], (str, ba.Lstr))
								or 'call' not in cme
								or not callable(cme['call'])
							):
								raise ValueError(
									'invalid custom menu entry: ' + str(cme)
								)
					except Exception:
						custom_menu_entries = []
						ba.print_exception(
							f'Error getting custom menu entries for {session}'
						)
				self._width = 250.0
				self._height = 250.0 if self._input_player else 180.0
				if (self._is_demo or self._is_arcade) and self._input_player:
					self._height -= 40
				if not self._have_settings_button:
					self._height -= 50
				if self._connected_to_remote_player:
					# In this case we have a leave *and* a disconnect button.
					self._height += 50
				self._height += 50 * (len(custom_menu_entries))
				uiscale = ba.app.ui.uiscale
				ba.containerwidget(
					edit=self._root_widget,
					size=(self._width, self._height),
					scale=(
						2.15
						if uiscale is ba.UIScale.SMALL
						else 1.6
						if uiscale is ba.UIScale.MEDIUM
						else 1.0
					),
				)
				h = 125.0
				v = self._height - 80.0 if self._input_player else self._height - 60
				h_offset = 0
				d_h_offset = 0
				v_offset = -50
				for _i in range(6 + len(custom_menu_entries)):
					positions.append((h, v, 1.0))
					v += v_offset
					h += h_offset
					h_offset += d_h_offset
				self._start_button = None
				ba.app.pause()

				# Player name if applicable.
				if self._input_player:
					player_name = self._input_player.getname()
					h, v, scale = positions[self._p_index]
					v += 35
					ba.textwidget(
						parent=self._root_widget,
						position=(h - self._button_width / 2, v),
						size=(self._button_width, self._button_height),
						color=(1, 1, 1, 0.5),
						scale=0.7,
						h_align='center',
						text=ba.Lstr(value=player_name),
					)
				else:
					player_name = ''
				h, v, scale = positions[self._p_index]
				self._p_index += 1
				btn = ba.buttonwidget(
					parent=self._root_widget,
					position=(h - self._button_width / 2, v),
					size=(self._button_width, self._button_height),
					scale=scale,
					label=ba.Lstr(resource=self._r + '.resumeText'),
					autoselect=self._use_autoselect,
					on_activate_call=self._resume,
				)
				ba.containerwidget(edit=self._root_widget, cancel_button=btn)

				# Add any custom options defined by the current game.
				for entry in custom_menu_entries:
					h, v, scale = positions[self._p_index]
					self._p_index += 1

					# Ask the entry whether we should resume when we call
					# it (defaults to true).
					resume = bool(entry.get('resume_on_call', True))

					if resume:
						call = ba.Call(self._resume_and_call, entry['call'])
					else:
						call = ba.Call(entry['call'], ba.WeakCall(self._resume))

					ba.buttonwidget(
						parent=self._root_widget,
						position=(h - self._button_width / 2, v),
						size=(self._button_width, self._button_height),
						scale=scale,
						on_activate_call=call,
						label=entry['label'],
						autoselect=self._use_autoselect,
					)
				# Add a 'leave' button if the menu-owner has a player.
				if (self._input_player or self._connected_to_remote_player) and not (
					self._is_demo or self._is_arcade
				):
					h, v, scale = positions[self._p_index]
					self._p_index += 1
					btn = ba.buttonwidget(
						parent=self._root_widget,
						position=(h - self._button_width / 2, v),
						size=(self._button_width, self._button_height),
						scale=scale,
						color=button_color,
						on_activate_call=self._leave,
						label='',
						autoselect=self._use_autoselect,
					)

					if (
						player_name != ''
						and player_name[0] != '<'
						and player_name[-1] != '>'
					):
						txt = ba.Lstr(
							resource=self._r + '.justPlayerText',
							subs=[('${NAME}', player_name)],
						)
					else:
						txt = ba.Lstr(value=player_name)
					ba.textwidget(
						parent=self._root_widget,
						position=(
							h,
							v
							+ self._button_height
							* (0.64 if player_name != '' else 0.5),
						),
						size=(0, 0),
						text=ba.Lstr(resource=self._r + '.leaveGameText'),
						scale=(0.83 if player_name != '' else 1.0),
						color=text_blue,
						h_align='center',
						v_align='center',
						draw_controller=btn,
						maxwidth=self._button_width * 0.9,
					)
					ba.textwidget(
						parent=self._root_widget,
						position=(h, v + self._button_height * 0.27),
						size=(0, 0),
						text=txt,
						color=text_blue,
						h_align='center',
						v_align='center',
						draw_controller=btn,
						scale=0.45,
						maxwidth=self._button_width * 0.9,
					)
				return h, v, scale
		MainMenuWindow._refresh_in_game = _refresh_in_game

		PlaylistAddGameWindow._old_refresh = PlaylistAddGameWindow._refresh
		def _refresh(self, select_get_more_games_button: bool = False) -> None:
			if not ba.app.config[ModInfo.cfgname]['enable_mod']:
				self._old_refresh(select_get_more_games_button)
			else:
				if self._column is not None:
					self._column.delete()

				self._column = ba.columnwidget(
					parent=self._scrollwidget, border=2, margin=0
				)

				for i, gametype in enumerate(self._game_types):

					def _doit() -> None:
						if self._select_button:
							ba.apptimer(0.1, self._select_button.activate)

					txt = ba.textwidget(
						parent=self._column,
						position=(0, 0),
						size=(self._scroll_width * 1.1, 24),
						text=gametype.get_display_string(),
						h_align='left',
						v_align='center',
						color=(0.8, 0.8, 0.8, 1.0),
						maxwidth=self._scroll_width * 0.8,
						on_select_call=ba.Call(self._set_selected_game_type, gametype),
						always_highlight=True,
						selectable=True,
						on_activate_call=_doit,
					)
					if i == 0:
						ba.widget(edit=txt, up_widget=self._back_button)

				self._get_more_games_button = ba.buttonwidget(
					parent=self._column,
					autoselect=True,
					label=ba.Lstr(resource=self._r + '.getMoreGamesText'),
					color=(0.54, 0.52, 0.67),
					textcolor=(0.7, 0.65, 0.7),
					on_activate_call=self._on_get_more_games_press,
					size=(178, 50),
				)
				if select_get_more_games_button:
					ba.containerwidget(
						edit=self._column,
						selected_child=self._get_more_games_button,
						visible_child=self._get_more_games_button,
					)
		PlaylistAddGameWindow._refresh = _refresh

	def installcfg(self) -> None:
		ba.app.config[ModInfo.cfgname] = ModInfo.cfglist
		ba.app.config.apply_and_commit()

	def setup_config(self) -> None:
		if ModInfo.cfgname in ba.app.config:
			for key in ModInfo.cfglist.keys():
				if not key in ba.app.config[ModInfo.cfgname]:
					self.installcfg()
					break
		else:
			self.installcfg()

	def has_settings_ui(self) -> bool:
		return True

	def show_settings_ui(self, source_widget: ba.Widget | None) -> None:
		ModSettingsPopup()