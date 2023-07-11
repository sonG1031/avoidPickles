import pygame
import random

class PickleRick(pygame.sprite.Sprite):
    def __init__(self, screen_size):
        super().__init__()
        pickle_rick = pygame.image.load("/Users/pulledsub/projects/pythonGame/assets/characters/Pickle_Rick.png").convert_alpha()
        self.screen_size = screen_size

        image = pickle_rick.subsurface(pygame.Rect((424, 782, 68, 117)))
        self.image = pygame.transform.scale(image, (68 / 2, 117 / 2)) # 34, 59

        self.pickle_rick_size = self.image.get_rect().size
        self.pickle_rick_width = self.pickle_rick_size[0]
        self.pickle_rick_height = self.pickle_rick_size[1]

        self.pickle_rick_x_pos = random.randint(0, screen_size[0] - self.pickle_rick_width)
        self.pickle_rick_y_pos = 0

        self.pickle_rick_speed = 5

        self.to_y = 0

        # orginal rect
        # self.rect = pygame.Rect((self.pickle_rick_x_pos, self.pickle_rick_y_pos), (self.pickle_rick_width, self.pickle_rick_height))

        self.small_rect_width = 51 / 2
        self.small_rect_height = 93 / 2

        self.small_rect_x_margin = 9
        self.small_rect_y_margin = 12

        # 축소한 rect
        self.rect = pygame.Rect((self.pickle_rick_x_pos + self.small_rect_x_margin, self.pickle_rick_y_pos + self.small_rect_y_margin), (self.small_rect_width, self.small_rect_height))

    def update(self, mt):
        self.rect = pygame.Rect((self.pickle_rick_x_pos + self.small_rect_x_margin, self.pickle_rick_y_pos + self.small_rect_y_margin), (self.small_rect_width, self.small_rect_height))

