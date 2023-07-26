import pygame.sprite

import images
from character import Sonic, SuperSonic
from constants import *

touches_super_sonic = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "punch": pygame.K_KP2,
    "kick": pygame.K_KP5,
    "spin_dash": pygame.K_DOWN
}
touches_sonic = {
    "left": pygame.K_q,
    "right": pygame.K_d,
    "punch": pygame.K_e,
    "kick": pygame.K_a,
    "spin_dash": pygame.K_s
}


class Game:
    def __init__(self, win):
        self.game_is_on = True
        self.win = win

        self.sonic = Sonic(350, 350, touches_sonic)
        self.s_sonic = SuperSonic(WIDTH - 600, 320, touches_super_sonic)

        self.sonic.add_ennemy(self.s_sonic)
        self.s_sonic.add_ennemy(self.sonic)

    def run(self):
        clock = pygame.time.Clock()
        while self.game_is_on:
            dt = clock.tick(FPS)  # dt = nb de ms depuis la derniere frame
            self.events()
            self.update(dt)
            self.draw(self.win)

    def events(self):
        events = pygame.event.get()
        self.sonic.handle_events(events)
        self.s_sonic.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.game_is_on = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

    def update(self, dt):
        self.sonic.update(dt)
        self.s_sonic.update(dt)

    def draw(self, win):
        win.blit(images.bg, (0, 0))
        self.sonic.draw(win)
        self.s_sonic.draw(win)
        pygame.display.update()
