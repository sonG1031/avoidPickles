import pygame

class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, frame): # frame = (x, y, width,height)
        image = self.spritesheet.subsurface(pygame.Rect(frame))
        return image
