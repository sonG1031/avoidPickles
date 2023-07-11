import pygame

class Morty(pygame.sprite.Sprite):
    def __init__(self, screen_size):
        super().__init__()

        self.screen_size = screen_size

        og_morty = pygame.image.load("/Users/pulledsub/projects/pythonGame/assets/characters/Morty.png").convert_alpha()
        self.front_frames = [(26, 688, 81, 110), (155, 685, 81, 114), (284, 688, 81, 110), (413, 688, 81, 110)]
        self.left_frames = [(26, 855, 78, 110), (155, 855, 78, 110), (284, 855, 78, 110), (413, 856, 78, 110)]
        self.right_frames = self.left_frames

        self.images = {
            "front": [og_morty.subsurface(pygame.Rect(frame)) for frame in self.front_frames],
            "left": [og_morty.subsurface(pygame.Rect(frame)) for frame in self.left_frames],
            "right": [
                pygame.transform.flip(og_morty.subsurface(pygame.Rect(frame)), True, False) for frame in self.right_frames
            ]
        }

        self.animation = "front"
        self.animation_idx = 0
        self.animation_time = round(100 / (4 * 100), 2)
        self.current_time = 0

        self.width = self.front_frames[self.animation_idx][2]
        self.height = self.front_frames[self.animation_idx][3]

        self.image = self.images[self.animation][self.animation_idx]

        self.character_x_pos = (self.screen_size[0] / 2) - (self.width / 2)
        self.character_y_pos = self.screen_size[1] - self.height - 110
        self.rect = pygame.Rect((self.character_x_pos, self.character_y_pos), (self.width, self.height))


    def update(self, animation, pos, mt):

        self.animation = animation
        # update를 통해 캐릭터의 이미지가 계속 반복해서 나타나도록 한다.
        self.animation_idx += 1

        if self.animation_idx >= len(self.images[self.animation]):
            self.animation_idx = 0

        self.image = self.images[self.animation][self.animation_idx]
        self.rect = pygame.Rect((self.character_x_pos, self.character_y_pos), (self.width, self.height))

        self.current_time += mt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.image = self.images[self.animation][self.animation_idx]