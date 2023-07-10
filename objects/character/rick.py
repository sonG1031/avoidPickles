import pygame
from os import path
from spritesheet import SpriteSheet

vec = pygame.math.Vector2
class Rick(pygame.sprite.Sprite):
    def __init__(self, screen, rect, *groups):
        super().__init__(groups)
        self.screen = screen

        # position
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]

        # sprite
        self.image = pygame.surface((self.width, self.height))
        self.screen.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # physics
        self.pos = vec(self.x, self.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        # settings
        self.player_acc = 0.5
        self.player_friction = -0.12 # 마찰

    def load(self):
        spritesheet = SpriteSheet()
