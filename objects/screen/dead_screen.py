import pygame
from objects.screen import start_screen
from objects.screen import game_screen

class DeadScreen:
    def __init__(self, score):
        self.dead_screen = pygame.image.load("/Users/pulledsub/projects/pythonGame/assets/screens/dead_screen.png")
        self.dead_screen_size = self.dead_screen.get_rect().size
        self.dead_screen_width = self.dead_screen_size[0]
        self.dead_screen_height = self.dead_screen_size[1]
        self.score = score
        self.font = None

        self.home_button = pygame.image.load("/Users/pulledsub/projects/pythonGame/assets/buttons/home_button.png")
        self.home_button_size = self.home_button.get_rect().size
        self.home_button_width = self.home_button_size[0]
        self.home_button_height = self.home_button_size[1]
        self.home_button_x_pos = (self.dead_screen_width / 2) - self.home_button_width - 15
        self.home_button_y_pos = 453 + self.home_button_height

        self.restart_button = pygame.image.load("/Users/pulledsub/projects/pythonGame/assets/buttons/restart_button.png")
        self.restart_button_size = self.restart_button.get_rect().size
        self.restart_button_width = self.restart_button_size[0] + 15
        self.restart_button_height = self.restart_button_size[1]
        self.restart_button_x_pos = (self.dead_screen_width / 2)
        self.restart_button_y_pos = 453 + self.restart_button_height

        self.exit_state = "quit"

    def show(self):
        pygame.init()

        self.font = pygame.font.Font("/Users/pulledsub/projects/pythonGame/assets/font/rickAndMorty.ttf", 30)
        text = self.font.render(f"SCORE  IS..{self.score}", True, (0,255,0))

        screen = pygame.display.set_mode((self.dead_screen_width, self.dead_screen_height))
        pygame.display.set_caption("Rick And Morty Avoid PICKLES")
        clock = pygame.time.Clock()


        running = True

        while running:
            clock.tick(144)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    home_button_rect = self.home_button.get_rect()
                    home_button_rect.left = self.home_button_x_pos
                    home_button_rect.top = self.home_button_y_pos

                    restart_button_rect = self.restart_button.get_rect()
                    restart_button_rect.left = self.restart_button_x_pos
                    restart_button_rect.top = self.restart_button_y_pos

                    if home_button_rect.collidepoint(pos):
                        self.exit_state = "home_screen"
                        running = False
                        break
                    elif restart_button_rect.collidepoint(pos):
                        self.exit_state = "game_screen"
                        running = False
                        break

            screen.blit(self.dead_screen, (0,0))
            screen.blit(text, ((self.dead_screen_width / 2) - (text.get_width() / 2), 453))
            screen.blit(self.home_button, (self.home_button_x_pos, self.home_button_y_pos))
            screen.blit(self.restart_button, (self.restart_button_x_pos, self.restart_button_y_pos))

            pygame.display.update()

        pygame.quit()

        if self.exit_state == "home_screen":
            screen = start_screen.StartScreen()
            screen.show()
        elif self.exit_state == "game_screen":
            screen = game_screen.GameScreen()
            screen.show()