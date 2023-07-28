import pygame.sprite
from PygameUIKit import button

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

font_sonic = pygame.font.Font("assets/fonts/sonic.ttf", 150)


class Game:
    def __init__(self, win):
        self.game_is_on = True
        self.win = win

        self.sonic = Sonic(350, 370, touches_sonic)
        self.s_sonic = SuperSonic(WIDTH - 600, 320, touches_super_sonic)

        self.sonic.add_ennemy(self.s_sonic)
        self.s_sonic.add_ennemy(self.sonic)

        self.btn_menu = button.ButtonPngIcon(images.menu_icon, (0, 0, 0), self.open_menu)
        self.menu = MenuInGame(target=self.btn_menu, game=self)

    def run(self):
        clock = pygame.time.Clock()
        pygame.mixer.music.load("assets/song.mp3")
        pygame.mixer.music.play(-1)
        while self.game_is_on:
            dt = clock.tick(FPS)  # dt = nb de ms depuis la derniere frame
            self.update(dt)
            self.events()
            self.draw(self.win)

    def events(self):
        events = pygame.event.get()
        self.btn_menu.handle_events(events)
        self.menu.handle_events(events)
        if self.sonic.is_alive and self.s_sonic.is_alive:
            self.sonic.handle_events(events)
            self.s_sonic.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

    def update(self, dt):
        self.sonic.update(dt)
        self.s_sonic.update(dt)

    def draw(self, win):
        win.blit(images.bg, (0, 0))
        self.sonic.draw(win)
        self.s_sonic.draw(win)

        if not self.sonic.is_alive:
            pygame.draw.circle(win, YELLOW, (WIDTH / 2, HEIGHT / 2), 400)
            text = font_sonic.render("Super Sonic", True, BLUE)
            win.blit(text, text.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
            text2 = "wins"
            text = font_sonic.render(text2, True, BLUE)
            win.blit(text, text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100)))

        if not self.s_sonic.is_alive:
            text = font_sonic.render("Sonic wins", True, YELLOW)
            pygame.draw.circle(win, BLUE, (WIDTH / 2, HEIGHT / 2), 400)
            win.blit(text, text.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

        self.btn_menu.draw(win, WIDTH - self.btn_menu.rect.w - 10, 10)
        self.menu.draw(win)

        pygame.display.update()

    def open_menu(self):
        self.menu.is_open = not self.menu.is_open

    def reset(self):
        self.__init__(self.win)

class MenuInGame:
    def __init__(self, target, game):
        self.is_open = False
        self.target = target
        self.game = game

        font = pygame.font.SysFont("None", 70)
        font2 = pygame.font.SysFont("None", 50)
        self.btn_quit = button.ButtonText(WHITE, pygame.quit, "QUIT", font, 5, font_color=BLACK)
        self.btn_restart = button.ButtonText(WHITE, self.start_new_game, "RESTART", font2, 5, font_color=BLACK)

        self.x = -1
        self.y = -1
        self.w = 200
        self.h = 400
        self.surface = pygame.surface.Surface((self.w, self.h), pygame.SRCALPHA)
        self.surface.fill(BROWN)
        self.surface.set_alpha(200)

        self.buttons = [self.btn_quit, self.btn_restart]

    def handle_events(self, events):
        for btn in self.buttons:
            btn.handle_events(events)

    def start_new_game(self):
        self.game.reset()

    def draw(self, win):
        if not self.is_open:
            return

        self.x = self.target.rect.bottomleft[0] - self.w / 2 - 20
        self.y = self.target.rect.bottomleft[1] + 10

        self.btn_quit.draw(self.surface, 10, 10)
        self.btn_restart.draw(self.surface, 10, 100)

        for btn in self.buttons:
            btn.rect.x += self.x
            btn.rect.y += self.y

        win.blit(self.surface, (self.x, self.y))


img_sonic = images.sonic["idle"][0]
img_ssonic = images.super_sonic["idle"][0]
img_ssonic = pygame.transform.flip(img_ssonic, True, False)
img_ssonic = pygame.transform.scale_by(img_ssonic, 2)
img_sonic = pygame.transform.scale_by(img_sonic, 2)
ssonic_height = img_ssonic.get_height()
sonic_height = img_sonic.get_height()


class Menu:
    def __init__(self, win, game: Game):
        self.win = win
        self.menu_is_on = True
        self.game = game
        font = pygame.font.SysFont("None", 100)
        self.btn_play = button.ButtonText(GREEN, self.start_game, "PLAY", font, 5, font_color=BLACK)

    def run(self):
        clock = pygame.time.Clock()
        while self.menu_is_on:
            self.events()
            self.draw(self.win)

    def events(self):
        events = pygame.event.get()
        self.btn_play.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

    def draw(self, win):
        x = WIDTH / 2 - self.btn_play.rect.w / 2
        y = HEIGHT / 2 - self.btn_play.rect.h / 2 + 200
        win.blit(images.menu_bg, (0, 0))
        win.blit(img_sonic, (200, HEIGHT / 2 - sonic_height / 2))
        win.blit(img_ssonic, (WIDTH - 400, HEIGHT / 2 - ssonic_height / 2))

        self.btn_play.draw(win, x, y)
        pygame.display.flip()

    def start_game(self):
        self.menu_is_on = False
        self.game.run()
