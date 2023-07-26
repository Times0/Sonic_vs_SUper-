import pygame
import ctypes
from constants import *

# set dpi aware
ctypes.windll.user32.SetProcessDPIAware()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("sonic vs super sonic")
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    from game import Game

    game = Game(win)
    game.run()
