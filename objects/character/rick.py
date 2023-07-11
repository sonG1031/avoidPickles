import pygame


class Rick(pygame.sprite.Sprite):
    def __init__(self, screen_size):
        super().__init__()

        self.screen_size = screen_size

        og_rick = pygame.image.load("/Users/pulledsub/projects/pythonGame/assets/characters/Rick.png").convert_alpha()
        self.front_frames = [(5, 742, 122, 153), (135, 742, 122, 153), (264, 742, 122, 153), (264, 742, 122, 153)]
        self.left_frames = [(21, 906, 107, 156), (150, 905, 107, 156), (280, 906, 107, 156), (409, 905, 107, 156)]
        self.right_frames = self.left_frames
        # 여러장의 이미지를 리스트로 저장한다. 이미지 경로는 자신들의 경로를 사용한다.

        self.images = {
            "front": [og_rick.subsurface(pygame.Rect(frame)) for frame in self.front_frames],
            "left": [og_rick.subsurface(pygame.Rect(frame)) for frame in self.left_frames],
            "right": [
                pygame.transform.flip(og_rick.subsurface(pygame.Rect(frame)), True, False) for frame in self.right_frames
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
