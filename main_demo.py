import pygame

# 125 × 162 이미지 크기

# 4 길이 차이
# 732 높이 차이


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, position):
        super(AnimatedSprite, self).__init__()

        # 이미지를 Rect안에 넣기 위해 Rect의 크기 지정
        # 이미지의 크기와 같게 하거나, 크기를 다르게 한다면 pygame.transform.scale을 사용하여 rect 안에
        # 이미지를 맞추도록 한다.
        size = (125, 162)

        # 여러장의 이미지를 리스트로 저장한다. 이미지 경로는 자신들의 경로를 사용한다.
        character = pygame.image.load("assets/characters/Rick.png")
        images = []
        for i in range(4):
            cropped = pygame.Surface((125, 162))
            top = 736
            left = 4 + (125 * i) + (4 * i)
            cropped.blit(character, (0, 0), (left, top, 125, 162))
            images.append(cropped)

        # rect 만들기
        self.rect = pygame.Rect(position, size)

        # Rect 크기와 Image 크기 맞추기. pygame.transform.scale
        self.images = [pygame.transform.scale(image, size) for image in images]

        # 캐릭터의 첫번째 이미지
        self.index = 0
        self.image = images[self.index]  # 'image' is the current image of the animation.

        self.animation_time = round(100 / len(self.images * 100), 2)

        self.current_time = 0

    def update(self, mt):
        # update를 통해 캐릭터의 이미지가 계속 반복해서 나타나도록 한다.

        # loop 시간 더하기
        self.current_time += mt

        # loop time 경과가 animation_time을 넘어서면 새로운 이미지 출력
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.image = self.images[self.index]

            self.index += 1
            if self.index >= len(self.images):
                self.index = 0


import pygame

# 스크린 전체 크기 지정

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 480

# pygame 초기화

pygame.init()

# 스크린 객체 저장
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pygame Sprite")

# FPS를 위한 Clock 생성
clock = pygame.time.Clock()

FPS = 60

BACKGROUND_COLOR = pygame.Color('white')

def main():
    # player 생성
    player = AnimatedSprite(position=(100, 8))
    # 생성된 player를 그룹에 넣기
    all_sprites = pygame.sprite.Group(player)

    running = True
    while running:
        mt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # all_sprites 그룹안에 든 모든 Sprite update
        all_sprites.update(mt)
        # 배경색
        SCREEN.fill(BACKGROUND_COLOR)
        # 모든 sprite 화면에 그려주기
        all_sprites.draw(SCREEN)
        pygame.display.update()

        clock.tick(FPS)

if __name__ == '__main__':
    main()
    pygame.quit()
