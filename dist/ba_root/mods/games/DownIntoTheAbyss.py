# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
import random
from ba._map import register_map
from bastd.actor.spaz import PickupMessage
from bastd.actor.playerspaz import PlayerSpaz
from bastd.actor.spazfactory import SpazFactory
from bastd.gameutils import SharedObjects
from bastd.actor.spazbot import SpazBotSet, ChargerBotPro, TriggerBotPro
from bastd.actor.bomb import Blast
from bastd.actor.powerupbox import PowerupBoxFactory
from bastd.actor.onscreentimer import OnScreenTimer

if TYPE_CHECKING:
	from typing import Any, Sequence


lang = ba.app.lang.language

if lang == 'Spanish':
	name = 'Abajo en el Abismo'
	description = 'Sobrevive tanto como puedas'
	help = 'El mapa es 3D, ¡ten cuidado!'
	author = 'Autor: Deva'
	github = 'GitHub: spdv123'
	blog = 'Blog: superdeva.info'
	peaceTime = 'Tiempo de Paz'
	npcDensity = 'Densidad de Enemigos'
	hint_use_punch = '¡Ahora puedes golpear a los enemigos!'
elif lang == 'Chinese':
	name = '无尽深渊'
	description = '在无穷尽的坠落中存活更长时间'
	help = ''
	author = '作者: Deva'
	github = 'GitHub: spdv123'
	blog = '博客: superdeva.info'
	peaceTime = '和平时间'
	npcDensity = 'NPC密度'
	hint_use_punch = u'现在可以使用拳头痛扁你的敌人了'
else:
	name = 'Down Into The Abyss'
	description = 'Survive as long as you can'
	help = 'The map is 3D, be careful!'
	author = 'Author: Deva'
	github = 'GitHub: spdv123'
	blog = 'Blog: superdeva.info'
	peaceTime = 'Peace Time'
	npcDensity = 'NPC Density'
	hint_use_punch = 'You can punch your enemies now!'


class AbyssMap(ba.Map):
	from bastd.mapdata import happy_thoughts as defs
	# Add the y-dimension space for players
	defs.boxes['map_bounds'] = (-0.8748348681, 9.212941713, -9.729538885) \
								+ (0.0, 0.0, 0.0) \
								+ (36.09666006, 26.19950145, 20.89541168)
	name = 'Abyss Unhappy'

	@classmethod
	def get_play_types(cls) -> list[str]:
		"""Return valid play types for this map."""
		return ['abyss']

	@classmethod
	def get_preview_texture_name(cls) -> str:
		return 'alwaysLandPreview'

	@classmethod
	def on_preload(cls) -> Any:
		data: dict[str, Any] = {
			'model': ba.getmodel('alwaysLandLevel'),
			'bottom_model': ba.getmodel('alwaysLandLevelBottom'),
			'bgmodel': ba.getmodel('alwaysLandBG'),
			'collide_model': ba.getcollidemodel('alwaysLandLevelCollide'),
			'tex': ba.gettexture('alwaysLandLevelColor'),
			'bgtex': ba.gettexture('alwaysLandBGColor'),
			'vr_fill_mound_model': ba.getmodel('alwaysLandVRFillMound'),
			'vr_fill_mound_tex': ba.gettexture('vrFillMound')
		}
		return data

	@classmethod
	def get_music_type(cls) -> ba.MusicType:
		return ba.MusicType.FLYING

	def __init__(self) -> None:
		super().__init__(vr_overlay_offset=(0, -3.7, 2.5))
		self.background = ba.newnode(
			'terrain',
			attrs={
				'model': self.preloaddata['bgmodel'],
				'lighting': False,
				'background': True,
				'color_texture': self.preloaddata['bgtex']
			})
		ba.newnode('terrain',
				   attrs={
					   'model': self.preloaddata['vr_fill_mound_model'],
					   'lighting': False,
					   'vr_only': True,
					   'color': (0.2, 0.25, 0.2),
					   'background': True,
					   'color_texture': self.preloaddata['vr_fill_mound_tex']
				   })
		gnode = ba.getactivity().globalsnode
		gnode.happy_thoughts_mode = True
		gnode.shadow_offset = (0.0, 8.0, 5.0)
		gnode.tint = (1.3, 1.23, 1.0)
		gnode.ambient_color = (1.3, 1.23, 1.0)
		gnode.vignette_outer = (0.64, 0.59, 0.69)
		gnode.vignette_inner = (0.95, 0.95, 0.93)
		gnode.vr_near_clip = 1.0
		self.is_flying = True

register_map(AbyssMap)


class SpazTouchFoothold:
	pass

class BombToDieMessage:
	pass


class Foothold(ba.Actor):

	def __init__(self,
				 position: Sequence[float] = (0.0, 1.0, 0.0),
				 power: str = 'random',
				 size: float = 6.0,
				 breakable: bool = True,
				 moving: bool = False):
		super().__init__()
		shared = SharedObjects.get()
		powerup = PowerupBoxFactory.get()

		fmodel = ba.getmodel('landMine')
		fmodels = ba.getmodel('powerupSimple')
		self.died = False
		self.breakable = breakable
		self.moving = moving  # move right and left
		self.lrSig = 1  # left or right signal
		self.lrSpeedPlus = random.uniform(1 / 2.0, 1 / 0.7)
		self._npcBots = SpazBotSet()

		self.foothold_material = ba.Material()
		self.impact_sound = ba.getsound('impactMedium')

		self.foothold_material.add_actions(
			conditions=(('they_dont_have_material', shared.player_material),
						'and',
						('they_have_material', shared.object_material),
						'or',
						('they_have_material', shared.footing_material)),
			actions=(('modify_node_collision', 'collide', True),
		))

		self.foothold_material.add_actions(
			conditions=('they_have_material', shared.player_material),
			actions=(('modify_part_collision', 'physical', True),
					 ('modify_part_collision', 'stiffness', 0.05),
					 ('message', 'our_node', 'at_connect', SpazTouchFoothold()),
		))

		self.foothold_material.add_actions(
			conditions=('they_have_material', self.foothold_material),
			actions=('modify_node_collision', 'collide', False),
		)

		tex = {
			'punch': powerup.tex_punch,
			'sticky_bombs': powerup.tex_sticky_bombs,
			'ice_bombs': powerup.tex_ice_bombs,
			'impact_bombs': powerup.tex_impact_bombs,
			'health': powerup.tex_health,
			'curse': powerup.tex_curse,
			'shield': powerup.tex_shield,
			'land_mines': powerup.tex_land_mines,
			'tnt': ba.gettexture('tnt'),
		}.get(power, ba.gettexture('tnt'))

		powerupdist = {
			powerup.tex_bomb: 3,
			powerup.tex_ice_bombs: 2,
			powerup.tex_punch: 3,
			powerup.tex_impact_bombs: 3,
			powerup.tex_land_mines: 3,
			powerup.tex_sticky_bombs: 4,
			powerup.tex_shield: 4,
			powerup.tex_health: 3,
			powerup.tex_curse: 1,
			ba.gettexture('tnt'): 2
		}

		self.randtex = []

		for keyTex in powerupdist:
			for i in range(powerupdist[keyTex]):
				self.randtex.append(keyTex)

		if power == 'random':
			random.seed()
			tex = random.choice(self.randtex)

		self.tex = tex
		self.powerup_type = {
			powerup.tex_punch: 'punch',
			powerup.tex_bomb: 'triple_bombs',
			powerup.tex_ice_bombs: 'ice_bombs',
			powerup.tex_impact_bombs: 'impact_bombs',
			powerup.tex_land_mines: 'land_mines',
			powerup.tex_sticky_bombs: 'sticky_bombs',
			powerup.tex_shield: 'shield',
			powerup.tex_health: 'health',
			powerup.tex_curse: 'curse',
			ba.gettexture('tnt'): 'tnt'
		}.get(self.tex, '')

		self._spawn_pos = (position[0], position[1], position[2])

		self.node = ba.newnode(
			'prop',
			delegate=self,
			attrs={
				'body': 'landMine',
				'position': self._spawn_pos,
				'model': fmodel,
				'light_model': fmodels,
				'shadow_size': 0.5,
				'velocity': (0, 0, 0),
				'density': 90000000000,
				'sticky': False,
				'body_scale': size,
				'model_scale': size,
				'color_texture': tex,
				'reflection': 'powerup',
				'is_area_of_interest': True,
				'gravity_scale': 0.0,
				'reflection_scale': [0],
				'materials': [self.foothold_material,
							  shared.object_material,
							  shared.footing_material]
				})
		self.touchedSpazs = set()
		self.keep_vel()

	def keep_vel(self) -> None:
		if self.node and not self.died:
			speed = ba.getactivity().cur_speed
			if self.moving:
				if abs(self.node.position[0]) > 10:
					self.lrSig *= -1
				self.node.velocity = (
					self.lrSig * speed * self.lrSpeedPlus,speed, 0)
				ba.timer(0.1, ba.WeakCall(self.keep_vel))
			else:
				self.node.velocity = (0, speed, 0)
				# self.node.extraacceleration = (0, self.speed, 0)
				ba.timer(0.1, ba.WeakCall(self.keep_vel))

	def tnt_explode(self) -> None:
		pos = self.node.position
		Blast(position=pos,
			  blast_radius=6.0,
			  blast_type='tnt',
			  source_player=None).autoretain()

	def spawn_npc(self) -> None:
		if not self.breakable:
			return
		if self._npcBots.have_living_bots():
			return
		if random.randint(0, 3) >= ba.getactivity().npc_density:
			return
		pos = self.node.position
		pos = (pos[0], pos[1] + 1, pos[2])
		self._npcBots.spawn_bot(
			bot_type=random.choice([ChargerBotPro, TriggerBotPro]),
			pos=pos,
			spawn_time=10)

	def handlemessage(self, msg: Any) -> Any:
		if isinstance(msg, ba.DieMessage):
			if self.node:
				self.node.delete()
				self.died = True
		elif isinstance(msg, ba.OutOfBoundsMessage):
			self.handlemessage(ba.DieMessage())
		elif isinstance(msg, BombToDieMessage):
			if self.powerup_type == 'tnt':
				self.tnt_explode()
			self.handlemessage(ba.DieMessage())
		elif isinstance(msg, ba.HitMessage):
			ispunched = (msg.srcnode and msg.srcnode.getnodetype() == 'spaz')
			if not ispunched:
				if self.breakable:
					self.handlemessage(BombToDieMessage())
		elif isinstance(msg, SpazTouchFoothold):
			node = ba.getcollision().opposingnode
			if node is not None and node:
				try:
					spaz = node.getdelegate(object)
					if not isinstance(spaz, AbyssPlayerSpaz):
						return
					if spaz in self.touchedSpazs:
						return
					self.touchedSpazs.add(spaz)
					self.spawn_npc()
					spaz.fix_2D_position()
					if self.powerup_type not in ['', 'tnt']:
						node.handlemessage(
							ba.PowerupMessage(self.powerup_type))
				except Exception as e:
					print(e)
					pass


class AbyssPlayerSpaz(PlayerSpaz):

	def __init__(self,
				 player: ba.Player,
				 color: Sequence[float] = (1.0, 1.0, 1.0),
				 highlight: Sequence[float] = (0.5, 0.5, 0.5),
				 character: str = 'Spaz',
				 powerups_expire: bool = True):
		super().__init__(player=player,
						 color=color,
						 highlight=highlight,
						 character=character,
						 powerups_expire=powerups_expire)
		self.node.fly = False
		self.node.hockey = True
		self.hitpoints_max = self.hitpoints = 1500  # more HP to handle drop
		ba.timer(ba.getactivity().peace_time,
				 ba.WeakCall(self.safe_connect_controls_to_player))

	def safe_connect_controls_to_player(self) -> None:
		try:
			self.connect_controls_to_player()
		except:
			pass

	def on_move_up_down(self, value: float) -> None:
		"""
		Called to set the up/down joystick amount on this spaz;
		used for player or AI connections.
		value will be between -32768 to 32767
		WARNING: deprecated; use on_move instead.
		"""
		if not self.node:
			return
		if self.node.run > 0.1:
			self.node.move_up_down = value
		else:
			self.node.move_up_down = value / 3.

	def on_move_left_right(self, value: float) -> None:
		"""
		Called to set the left/right joystick amount on this spaz;
		used for player or AI connections.
		value will be between -32768 to 32767
		WARNING: deprecated; use on_move instead.
		"""
		if not self.node:
			return
		if self.node.run > 0.1:
			self.node.move_left_right = value
		else:
			self.node.move_left_right = value / 1.5

	def fix_2D_position(self) -> None:
		self.node.fly = True
		ba.timer(0.02, ba.WeakCall(self.disable_fly))

	def disable_fly(self) -> None:
		if self.node:
			self.node.fly = False

	def curse(self) -> None:
		"""
		Give this poor spaz a curse;
		he will explode in 5 seconds.
		"""
		if not self._cursed:
			factory = SpazFactory.get()
			self._cursed = True

			# Add the curse material.
			for attr in ['materials', 'roller_materials']:
				materials = getattr(self.node, attr)
				if factory.curse_material not in materials:
					setattr(self.node, attr,
							materials + (factory.curse_material, ))

			# None specifies no time limit
			assert self.node
			if self.curse_time == -1:
				self.node.curse_death_time = -1
			else:
				# Note: curse-death-time takes milliseconds.
				tval = ba.time()
				assert isinstance(tval, (float, int))
				self.node.curse_death_time = ba.time() + 15
				ba.timer(15, ba.WeakCall(self.curse_explode))

	def handlemessage(self, msg: Any) -> Any:
		dontUp = False

		if isinstance(msg, PickupMessage):
			dontUp = True
			collision = ba.getcollision()
			opposingnode = collision.opposingnode
			opposingbody = collision.opposingbody

			if opposingnode is None or not opposingnode:
				return True
			opposingdelegate = opposingnode.getdelegate(object)
			# Don't pick up the foothold
			if isinstance(opposingdelegate, Foothold):
				return True

			# dont allow picking up of invincible dudes
			try:
				if opposingnode.invincible:
					return True
			except Exception:
				pass

			# if we're grabbing the pelvis of a non-shattered spaz,
			# we wanna grab the torso instead
			if (opposingnode.getnodetype() == 'spaz'
					and not opposingnode.shattered and opposingbody == 4):
				opposingbody = 1


			# Special case - if we're holding a flag, don't replace it
			# (hmm - should make this customizable or more low level).
			held = self.node.hold_node
			if held and held.getnodetype() == 'flag':
				return True

			# Note: hold_body needs to be set before hold_node.
			self.node.hold_body = opposingbody
			self.node.hold_node = opposingnode

		if not dontUp:
			PlayerSpaz.handlemessage(self, msg)


class Player(ba.Player['Team']):
	"""Our player type for this game."""

	def __init__(self) -> None:
		super().__init__()
		self.death_time: float | None = None
		self.notIn: bool = None


class Team(ba.Team[Player]):
	"""Our team type for this game."""


# ba_meta export game
class AbyssGame(ba.TeamGameActivity[Player, Team]):

	name = name
	description = description
	scoreconfig = ba.ScoreConfig(label='Survived',
								 scoretype=ba.ScoreType.MILLISECONDS,
								 version='B')

	# Print messages when players die (since its meaningful in this game).
	announce_player_deaths = True

	# We're currently hard-coded for one map.
	@classmethod
	def get_supported_maps(cls, sessiontype: type[ba.Session]) -> list[str]:
		return ['Abyss Unhappy']

	@classmethod
	def get_available_settings(
			cls, sessiontype: type[ba.Session]) -> list[ba.Setting]:
		settings = [
			ba.FloatChoiceSetting(
				peaceTime,
				choices=[
					('None', 0.0),
					('Shorter', 2.5),
					('Short', 5.0),
					('Normal', 10.0),
					('Long', 15.0),
					('Longer', 20.0),
				],
				default=10.0,
			),
			ba.FloatChoiceSetting(
				npcDensity,
				choices=[
					('0%', 0),
					('25%', 1),
					('50%', 2),
					('75%', 3),
					('100%', 4),
				],
				default=2,
			),
			ba.BoolSetting('Epic Mode', default=False),
		]
		return settings

	# We support teams, free-for-all, and co-op sessions.
	@classmethod
	def supports_session_type(cls, sessiontype: type[ba.Session]) -> bool:
		return (issubclass(sessiontype, ba.DualTeamSession)
				or issubclass(sessiontype, ba.FreeForAllSession)
				or issubclass(sessiontype, ba.CoopSession))

	def __init__(self, settings: dict):
		super().__init__(settings)
		self._epic_mode = settings.get('Epic Mode', False)
		self._last_player_death_time: float | None = None
		self._timer: OnScreenTimer | None = None
		self.fix_y = -5.614479365
		self.start_z = 0
		self.init_position = (0, self.start_z, self.fix_y)
		self.team_init_positions = [(-5, self.start_z, self.fix_y),
									(5, self.start_z, self.fix_y)]
		self.cur_speed = 2.5
		# TODO: The variable below should be set in settings
		self.peace_time = float(settings[peaceTime])
		self.npc_density = float(settings[npcDensity])

		# Some base class overrides:
		self.default_music = (ba.MusicType.EPIC
							  if self._epic_mode else ba.MusicType.SURVIVAL)
		if self._epic_mode:
			self.slow_motion = True

		self._game_credit = ba.NodeActor(
			ba.newnode(
				'text',
				attrs={
					'v_attach': 'bottom',
					'h_align': 'center',
					'vr_depth': 0,
					'color': (0.0, 0.7, 1.0),
					'shadow': 1.0 if True else 0.5,
					'flatness': 1.0 if True else 0.5,
					'position': (0, 0),
					'scale': 0.8,
					'text': ' | '.join([author, github, blog])
			}))

	def get_instance_description(self) -> str | Sequence:
		return description

	def get_instance_description_short(self) -> str | Sequence:
		return self.get_instance_description() + '\n' + help

	def on_player_join(self, player: Player) -> None:
		if self.has_begun():
			player.notIn = True
			ba.screenmessage(ba.Lstr(
				resource='playerDelayedJoinText',
				subs=[('${PLAYER}', player.getname(full=True))]),
				color=(0, 1, 0))
		self.spawn_player(player)

	def on_begin(self) -> None:
		super().on_begin()
		self._timer = OnScreenTimer()
		self._timer.start()

		self.level_cnt = 1

		if self.teams_or_ffa() == 'teams':
			ip0 = self.team_init_positions[0]
			ip1 = self.team_init_positions[1]
			Foothold(
				(ip0[0], ip0[1] - 2, ip0[2]),
				power='shield', breakable=False).autoretain()
			Foothold(
				(ip1[0], ip1[1] - 2, ip1[2]),
				power='shield', breakable=False).autoretain()
		else:
			ip = self.init_position
			Foothold(
				(ip[0], ip[1] - 2, ip[2]),
				power='shield', breakable=False).autoretain()

		ba.timer(int(5.0 / self.cur_speed),
				 ba.WeakCall(self.add_foothold), repeat=True)

		# Repeat check game end
		ba.timer(1.0, self._check_end_game, repeat=True)
		ba.timer(self.peace_time + 0.1,
				 ba.WeakCall(self.tip_hint, hint_use_punch))
		ba.timer(6.0, ba.WeakCall(self.faster_speed), repeat=True)

	def tip_hint(self, text: str) -> None:
		ba.screenmessage(text, color=(0.2, 0.2, 1))

	def faster_speed(self) -> None:
		self.cur_speed *= 1.15

	def add_foothold(self) -> None:
		ip = self.init_position
		ip_1 = (ip[0] - 7, ip[1], ip[2])
		ip_2 = (ip[0] + 7, ip[1], ip[2])
		ru = random.uniform
		self.level_cnt += 1
		if self.level_cnt % 3:
			Foothold((
				ip_1[0] + ru(-5, 5),
				ip[1] - 2,
				ip[2] + ru(-0.0, 0.0))).autoretain()
			Foothold((
				ip_2[0] + ru(-5, 5),
				ip[1] - 2,
				ip[2] + ru(-0.0, 0.0))).autoretain()
		else:
			Foothold((
				ip[0] + ru(-8, 8),
				ip[1] - 2,
				ip[2]), moving=True).autoretain()

	def teams_or_ffa(self) -> None:
		if isinstance(self.session, ba.DualTeamSession):
			return 'teams'
		return 'ffa'

	def spawn_player_spaz(self,
						  player: Player,
						  position: Sequence[float] = (0, 0, 0),
						  angle: float | None = None) -> PlayerSpaz:
		# pylint: disable=too-many-locals
		# pylint: disable=cyclic-import
		from ba import _math
		from ba._gameutils import animate

		position = self.init_position
		if self.teams_or_ffa() == 'teams':
			position = self.team_init_positions[player.team.id % 2]
		angle = None

		name = player.getname()
		color = player.color
		highlight = player.highlight

		light_color = _math.normalized_color(color)
		display_color = _ba.safecolor(color, target_intensity=0.75)
		spaz = AbyssPlayerSpaz(color=color,
							  highlight=highlight,
							  character=player.character,
							  player=player)

		player.actor = spaz
		assert spaz.node

		spaz.node.name = name
		spaz.node.name_color = display_color
		spaz.connect_controls_to_player(enable_punch=False,
										enable_bomb=True,
										enable_pickup=False)

		# Move to the stand position and add a flash of light.
		spaz.handlemessage(
			ba.StandMessage(
				position,
				angle if angle is not None else random.uniform(0, 360)))
		_ba.playsound(self._spawn_sound, 1, position=spaz.node.position)
		light = _ba.newnode('light', attrs={'color': light_color})
		spaz.node.connectattr('position', light, 'position')
		animate(light, 'intensity', {0: 0, 0.25: 1, 0.5: 0})
		_ba.timer(0.5, light.delete)
		return spaz

	def handlemessage(self, msg: Any) -> Any:
		if isinstance(msg, ba.PlayerDiedMessage):

			# Augment standard behavior.
			super().handlemessage(msg)

			curtime = ba.time()

			# Record the player's moment of death.
			# assert isinstance(msg.spaz.player
			msg.getplayer(Player).death_time = curtime

			# In co-op mode, end the game the instant everyone dies
			# (more accurate looking).
			# In teams/ffa, allow a one-second fudge-factor so we can
			# get more draws if players die basically at the same time.
			if isinstance(self.session, ba.CoopSession):
				# Teams will still show up if we check now.. check in
				# the next cycle.
				ba.pushcall(self._check_end_game)

				# Also record this for a final setting of the clock.
				self._last_player_death_time = curtime
			else:
				ba.timer(1.0, self._check_end_game)

		else:
			# Default handler:
			return super().handlemessage(msg)
		return None

	def _check_end_game(self) -> None:
		living_team_count = 0
		for team in self.teams:
			for player in team.players:
				if player.is_alive():
					living_team_count += 1
					break

		# In co-op, we go till everyone is dead.. otherwise we go
		# until one team remains.
		if isinstance(self.session, ba.CoopSession):
			if living_team_count <= 0:
				self.end_game()
		else:
			if living_team_count <= 0:
				self.end_game()

	def end_game(self) -> None:
		cur_time = ba.time()
		assert self._timer is not None
		start_time = self._timer.getstarttime()

		# Mark death-time as now for any still-living players
		# and award players points for how long they lasted.
		# (these per-player scores are only meaningful in team-games)
		for team in self.teams:
			for player in team.players:
				survived = False
				if player.notIn:
					player.death_time = 0

				# Throw an extra fudge factor in so teams that
				# didn't die come out ahead of teams that did.
				if player.death_time is None:
					survived = True
					player.death_time = cur_time + 1

				# Award a per-player score depending on how many seconds
				# they lasted (per-player scores only affect teams mode;
				# everywhere else just looks at the per-team score).
				score = int(player.death_time - self._timer.getstarttime())
				if survived:
					score += 50  # A bit extra for survivors.
				self.stats.player_scored(player, score, screenmessage=False)

		# Stop updating our time text, and set the final time to match
		# exactly when our last guy died.
		self._timer.stop(endtime=self._last_player_death_time)

		# Ok now calc game results: set a score for each team and then tell
		# the game to end.
		results = ba.GameResults()

		# Remember that 'free-for-all' mode is simply a special form
		# of 'teams' mode where each player gets their own team, so we can
		# just always deal in teams and have all cases covered.
		for team in self.teams:

			# Set the team score to the max time survived by any player on
			# that team.
			longest_life = 0.0
			for player in team.players:
				assert player.death_time is not None
				longest_life = max(longest_life,
								   player.death_time - start_time)

			# Submit the score value in milliseconds.
			results.set_team_score(team, int(1000.0 * longest_life))

		self.end(results=results)
