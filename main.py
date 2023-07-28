import ctypes
import os.path

import pygame

from constants import *

# set dpi aware
ctypes.windll.user32.SetProcessDPIAware()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("sonic vs super sonic")
    icon_32x32 = pygame.image.load(os.path.join(script_dir,"assets","icon.jpeg"))
    pygame.display.set_icon(icon_32x32)
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    from game import Game, Menu

    start_menu = Menu(win, Game(win))
    start_menu.run()
