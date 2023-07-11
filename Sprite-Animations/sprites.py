import pygame as pg
from os import path

from animated_sprite import AnimatedSprite
from spritesheet import SpriteSheet, Animation

vec = pg.math.Vector2


class Player(AnimatedSprite):
	def __init__(self, screen, x, y, *groups):
		super().__init__(groups)
		self.screen = screen

		self.load()

		# sprite
		self.image = self.active_anim.get_frame(0)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		# physics
		self.pos = vec(x, y)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)

		# settings
		self.player_acc = 0.5
		self.player_friction = -0.12

	def load(self):
		spritesheet = SpriteSheet(path.join(self.screen.game.img_dir, 'Rick.png'), self.screen.game.green)

		# front animation
		front_frames = [(5, 742, 122, 153), (135, 742, 122, 153), (264, 742, 122, 153), (264, 742, 122, 153)]
		entrance_animation = spritesheet.get_animation(front_frames, 0.10, Animation.PlayMode.LOOP) # resize=1.5
		self.store_animation('front', front_frames)

		# left-move animation
		left_move_frames = [(21, 906, 107, 154), (150, 905, 107, 156), (280, 906, 107, 153), (409, 905, 107, 155)]
		standing_animation = spritesheet.get_animation(left_move_frames, 0.10, Animation.PlayMode.NORMAL) # resize=1.5
		self.store_animation('left_move', left_move_frames)

		# right-move animation
		right_move_frames = left_move_frames
		running_animation = spritesheet.get_animation(right_move_frames, 0.095, Animation.PlayMode.LOOP, flip=True) # resize=1.5
		self.store_animation('right_move', right_move_frames)

	def get_keys(self):
		keys = pg.key.get_pressed()
		if self.active_name != 'front':
			if keys[pg.K_LEFT]:
				self.acc.x = -self.player_acc
			elif keys[pg.K_RIGHT]:
				self.acc.x = self.player_acc

	def animate(self):
		# change entrance animation
		if self.active_name == 'front':
			if self.active_anim.get_frame_index(self.elapsed_time) > 13 and \
				self.active_anim.get_frame_index(self.elapsed_time) < 17:
				self.vel.x = -3
			
			elif self.active_anim.get_frame_index(self.elapsed_time) > 17 and self.active_anim.get_frame_index(self.elapsed_time) < 25:
				self.vel.x = 1.5

			elif self.active_anim.get_frame_index(self.elapsed_time) > 25:
				self.vel.x = 0

			if self.is_animation_finished():
				self.set_active_animation('standing')

		# change standing animation
		if self.active_name == 'front':
			if self.acc.x > 0:
				self.set_active_animation('right_move')

		# change running animation
		if self.active_name == 'right_move':
			if self.acc.x < 0:
				self.set_active_animation('left_move')

		# # change halting animaiton
		# if self.active_name == 'halting':
		# 	if self.active_anim.is_animation_finished(self.elapsed_time):
		# 		self.set_active_animation('standing')


		bottom = self.rect.bottom
		self.image = self.active_anim.get_frame(self.elapsed_time)
		self.rect = self.image.get_rect()
		self.rect.bottom = bottom

	def update(self):
		super().update(1/self.screen.game.fps)
		self.animate()

		# update vectors
		self.acc = vec(0, 0)
		self.get_keys()

		# apply friction
		self.acc.x += self.vel.x*self.player_friction
		# equations of motion
		self.vel += self.acc
		self.pos += self.vel + 0.5*self.acc

		self.rect.midbottom = self.pos


class Enemy(AnimatedSprite):
	def __init__(self, screen, x, y, *groups):
		super().__init__(groups)
		self.screen = screen

		self.load()

		# sprite
		self.image = self.active_anim.get_frame(0)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		# physics
		self.pos = vec(x, y)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)

		# settings
		self.player_acc = 0.5
		self.player_friction = -0.12

	def load(self):
		spritesheet = SpriteSheet(path.join(self.screen.game.img_dir, 'enemy_spritesheet.png'), (34, 177, 76))

		# standing animation
		standing_frames = [(28, 247, 34, 63), (73, 248, 34, 62), (115, 248, 35, 61)]
		standing_animation = spritesheet.get_animation(standing_frames, 0.20, Animation.PlayMode.LOOP, flip=True)
		self.store_animation('standing', standing_animation)

	def animate(self):
		bottom = self.rect.bottom
		self.image = self.active_anim.get_frame(self.elapsed_time)
		self.rect = self.image.get_rect()
		self.rect.bottom = bottom

	def update(self):
		# update frame
		super().update(1/self.screen.game.fps)
		self.animate()

		# update vectors
		self.acc = vec(0, 0)

		# apply friction
		self.acc.x += self.vel.x*self.player_friction
		# equations of motion
		self.vel += self.acc
		self.pos += self.vel + 0.5*self.acc

		self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, *groups):
		super().__init__(groups)
		self.screen = game

		# position
		self.x = x
		self.y = y

		# sprite
		self.image = pg.Surface((w, h))
		self.image.fill(self.screen.game.black)
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.x = self.x
		self.rect.y = self.y
