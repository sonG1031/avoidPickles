import pygame
import cv2
from detectLR.detection import DetectionLR
import numpy as np

class GameScreen:
    def __init__(self):
        self.game_screen = pygame.image.load("./assets/screens/game_screen.png")
        self.game_screen_size = self.game_screen.get_rect().size
        self.game_screen_width = self.game_screen_size[0]
        self.game_screen_height = self.game_screen_size[1]

    def show(self):
        pygame.init()

        screen = pygame.display.set_mode((self.game_screen_width, self.game_screen_height))
        pygame.display.set_caption("test")

        character = pygame.image.load("assets/characters/Rick.png").convert_alpha()
        character_width = 125
        character_height = 162
        images = []
        for i in range(4):
            cropped = pygame.Surface((125, 162)).convert_alpha()
            cropped.fill((0, 0, 0, 0))
            top = 736
            left = 4 + (125 * i) + (4 * i)
            cropped.blit(character, (0, 0), (left, top, 125, 162))
            # cropped.set_colorkey((255, 0, 255))
            # cropped.set_alpha()
            images.append(cropped)

        character_x_pos = (self.game_screen_width / 2) - (character_width / 2)
        character_y_pos = self.game_screen_height - character_height - 110
        to_x = 0
        character_speed = 0.025

        clock = pygame.time.Clock()

        running = True

        detect_left_right = DetectionLR()

        webcam = cv2.VideoCapture(0)
        webcam_x_pos = (self.game_screen_width / 2) - (detect_left_right.WIDTH / 2)
        webcam_y_pos = self.game_screen_height - detect_left_right.HEIGHT - 13

        while running and webcam.isOpened():
            dt = clock.tick(60)

            success, img = webcam.read()
            flip_img = cv2.flip(img, 1)  # 거울 모드 뒤집기, 보이는 화면이 움직이는 방향과 맞추기 위해
            resized_img = cv2.resize(
                flip_img,
                dsize=(detect_left_right.WIDTH, detect_left_right.HEIGHT),
                interpolation=cv2.INTER_LINEAR
            )

            resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)  # opencv는 BGR이라서 바꿔줘야함

            direction = detect_left_right.detect(resized_img)

            resized_img = cv2.cvtColor(resized_img, cv2.COLOR_RGB2BGR)

            draw_img = detect_left_right.draw(resized_img)
            draw_img = cv2.flip(draw_img, 1)
            draw_img = np.rot90(cv2.cvtColor(draw_img, cv2.COLOR_BGR2RGB))

            cam_frame = pygame.surfarray.make_surface(draw_img)


            if direction == detect_left_right.DIRECTION_MID:
                to_x = 0
            elif direction == detect_left_right.DIRECTION_LEFT:
                to_x -= character_speed
            elif direction == detect_left_right.DIRECTION_RIGHT:
                to_x += character_speed

            character_x_pos += to_x * dt
            # webcam_x_pos += to_x * dt

            if character_x_pos < 0:
                character_x_pos = 0
            elif character_x_pos > (self.game_screen_width - character_width):
                character_x_pos = self.game_screen_width - character_width

            # if webcam_x_pos < 13:
            #     webcam_x_pos = 13
            # elif webcam_x_pos > (self.game_screen_width - detect_left_right.WIDTH) - 13:
            #     webcam_x_pos = self.game_screen_width - detect_left_right.WIDTH - 13

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            screen.blit(self.game_screen, (0, 0))
            screen.blit(images[0], (character_x_pos, character_y_pos))
            screen.blit(cam_frame, (webcam_x_pos, webcam_y_pos))
            pygame.display.update()

        pygame.quit()
        webcam.release()
