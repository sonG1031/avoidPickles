import pygame
import cv2
import numpy as np
import random

from detectLR.detection import DetectionLR

from objects.character.rick import Rick
from objects.character.morty import Morty
from objects.character.pickle_rick import PickleRick
from objects.screen.dead_screen import DeadScreen

class GameScreen:

    def __init__(self):
        self.font = None
        self.background_sound = None
        self.game_screen = pygame.image.load("./assets/screens/game_screen.png")
        self.game_screen_size = self.game_screen.get_rect().size
        self.game_screen_width = self.game_screen_size[0]
        self.game_screen_height = self.game_screen_size[1]
        self.score = 0
        self.exit_state = "quit"

    def show(self):
        pygame.mixer.init(44100, -16, 2, 64)
        pygame.mixer.init()
        pygame.init()

        self.font = pygame.font.Font("/Users/pulledsub/projects/pythonGame/assets/font/rickAndMorty.ttf", 30)
        self.background_sound = pygame.mixer.Sound("/Users/pulledsub/projects/pythonGame/assets/sounds/background_music.mp3")

        screen = pygame.display.set_mode((self.game_screen_width, self.game_screen_height))
        pygame.display.set_caption("Rick And Morty Avoid PICKLES")

        # character = Rick((self.game_screen_width, self.game_screen_height))
        character = Morty((self.game_screen_width, self.game_screen_height))

        to_x = 0
        character_speed = 12

        clock = pygame.time.Clock()

        running = True

        detect_left_right = DetectionLR()

        webcam = cv2.VideoCapture(0)
        webcam_x_pos = (self.game_screen_width / 2) - (detect_left_right.WIDTH / 2)
        webcam_y_pos = self.game_screen_height - detect_left_right.HEIGHT - 13

        character_sprites = pygame.sprite.Group(character)
        character_direction = "front"

        # pickle = PickleRick((self.game_screen_width, self.game_screen_height))
        pickles = [PickleRick((self.game_screen_width, self.game_screen_height)) for _ in range(7)]
        rand_pickle_speed = [random.randrange(2, 7) for _ in range(7)]
        pickle_sprites = pygame.sprite.Group(pickles)


        start_time = pygame.time.get_ticks()
        acc_speed_unit = 20


        # landing_sound = pygame.mixer.Sound("/Users/pulledsub/projects/pythonGame/assets/sounds/landing_sound.mp3")
        landed_sound = pygame.mixer.Sound("/Users/pulledsub/projects/pythonGame/assets/sounds/landed_sound.mp3")

        self.background_sound.play(-1)
        while running and webcam.isOpened():
            dt = clock.tick(144) / 1000

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

            for idx, pickle in enumerate(pickles):
                pickle.pickle_rick_speed = rand_pickle_speed[idx]
                pickle.to_y += pickle.pickle_rick_speed
                pickle.pickle_rick_y_pos += pickle.to_y * dt

                if pickle.pickle_rick_y_pos > (self.game_screen_height - pickle.pickle_rick_height - 110):
                    landed_sound.play()
                    pickle.pickle_rick_y_pos = 0
                    pickle.to_y = 0
                    pickle.pickle_rick_x_pos = random.randint(0, self.game_screen_width - pickle.pickle_rick_width)
                    self.score += 1



                if pygame.sprite.spritecollide(pickle, character_sprites, True):
                    running = False
                    self.exit_state = "dead"
                    break


            if direction == detect_left_right.DIRECTION_MID:
                to_x = 0
                character_direction = "front"
            elif direction == detect_left_right.DIRECTION_LEFT:
                to_x -= character_speed
                character_direction = "left"
            elif direction == detect_left_right.DIRECTION_RIGHT:
                to_x += character_speed
                character_direction = "right"

            character.character_x_pos += to_x * dt

            if character.character_x_pos < 0:
                character.character_x_pos = 0
            elif character.character_x_pos > (self.game_screen_width - character.width):
                character.character_x_pos = self.game_screen_width - character.width


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            screen.blit(self.game_screen, (0, 0))
            character_sprites.update(character_direction, (character.character_x_pos, character.character_y_pos), dt)
            character_sprites.draw(screen)

            pickle_sprites.update(dt)
            # landing_sound.play(5)
            pickle_sprites.draw(screen)


            screen.blit(cam_frame, (webcam_x_pos, webcam_y_pos))

            text = self.font.render(f"SCORE  IS.. {str(self.score)}", True, (0,255,0))
            screen.blit(text, ((webcam_x_pos / 2) - (text.get_width() / 2), (self.game_screen_height - (115 / 2) - (text.get_height() / 2))))


            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000 # 밀리초를 초로 바꿈
            acc_speed = elapsed_time % acc_speed_unit
            if elapsed_time > 0 and acc_speed == 0:
                for pickle in pickles:
                    pickle.pickle_rick_speed += 0.125

            rand_pickle_speed = [random.randrange(2, 7) for _ in range(7)]
            pygame.display.update()


        self.background_sound.stop()
        pygame.quit()
        webcam.release()

        if self.exit_state == 'dead':
            dead_screen = DeadScreen(self.score)
            dead_screen.show()


