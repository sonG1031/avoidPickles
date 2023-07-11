import pygame
from objects.screen import game_screen


class StartScreen:
    def __init__(self):
        self.start_screen = pygame.image.load("./assets/screens/start_screen.png")
        self.start_screen_size = self.start_screen.get_rect().size
        self.start_screen_width = self.start_screen_size[0]
        self.start_screen_height = self.start_screen_size[1]
        self.start_button = pygame.image.load("/Users/pulledsub/projects/pythonGame/assets/buttons/start_button.png")
        self.start_button_size = self.start_button.get_rect().size
        self.start_button_width = self.start_button_size[0]
        self.start_button_height = self.start_button_size[1]
        self.start_screen_x_pos = (self.start_screen_width / 2) - (self.start_button_width / 2)
        self.start_screen_y_pos = (self.start_screen_height / 2)
        self.exit_state = "quit"

    def show(self):
        pygame.init()

        screen = pygame.display.set_mode((self.start_screen_width, self.start_screen_height))
        pygame.display.set_caption("Rick And Morty Avoid PICKLES")

        running = True

        clock = pygame.time.Clock()

        while running:
            clock.tick(144)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    start_screen_rect = self.start_screen.get_rect()
                    start_screen_rect.left = self.start_screen_x_pos
                    start_screen_rect.top = self.start_screen_y_pos

                    if start_screen_rect.collidepoint(pos):
                        self.exit_state = "game_screen"
                        running = False
                        break

            screen.blit(self.start_screen, (0,0))
            screen.blit(self.start_button, (self.start_screen_x_pos, self.start_screen_y_pos))
            pygame.display.update()

        pygame.quit()

        if self.exit_state == "game_screen":
            screen = game_screen.GameScreen()
            screen.show()