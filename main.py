from objects.screen import start_screen
from objects.screen import dead_screen

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 0)  # 윈도우 창 위치

def main():
    # screen = game_screen.GameScreen()
    # screen = start_screen.StartScreen()
    screen = dead_screen.DeadScreen(0)
    screen.show()

if __name__ == "__main__":
    main()