import pygame

import images as imgs
from constants import *


class Fighter(pygame.sprite.Sprite):
    def __init__(self, imgs, bindings: dict):
        super().__init__()
        self.imgs = imgs
        self.speed = 10
        self.orientation = ""

        self.time_since_last_frame_change = 0
        self.anim_index = 0

        self.image = self.imgs["idle"][self.anim_index]
        self.rect = self.image.get_rect()

        self.status = "idle"

        self.max_pv = 250
        self.pv = self.max_pv

        self.ennemy = None
        self.binds = bindings

    def draw(self, win):
        win.blit(self.image, self.rect)
        pygame.draw.rect(win, RED, self.rect, 3)
        x = self.rect.x + (self.rect.w - self.max_pv) // 2
        pygame.draw.rect(win, RED, (x, self.rect.y - 50, self.max_pv, 30))
        pygame.draw.rect(win, GREEN, (x, self.rect.y - 50, self.pv, 30))
        pygame.draw.rect(win, BLACK, (x, self.rect.y - 50, self.max_pv, 30), 3)

        # draw status on top of character
        font = pygame.font.SysFont("None", 40)
        text = font.render(self.status, True, BLACK)
        win.blit(text, (self.rect.x, self.rect.y - 100))

    def change_status_to(self, new_status):
        if new_status != self.status:
            self.anim_index = 0
        self.status = new_status

    def update(self, dt):
        self.time_since_last_frame_change += dt
        if self.time_since_last_frame_change > 100:
            self.time_since_last_frame_change = 0
            self.anim_index += 1
            if self.anim_index >= len(self.imgs[self.status]):
                self.anim_index = 0
                if self.status == "punch":
                    self.change_status_to("idle")
            self.image = self.imgs[self.status][self.anim_index]
            if self.orientation == "left":
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def add_ennemy(self, ennemy):
        self.ennemy = ennemy

    def handle_events(self, events):
        binds = self.binds
        pressed = pygame.key.get_pressed()
        if pressed[binds["right"]] and pressed[binds["left"]]:
            self.status = "idle"
            return

        moving = False
        if pressed[binds["right"]] and self.rect.x + self.rect.w < 1530:
            self.rect.x += self.speed
            self.orientation = "right"
            self.change_status_to("run")
            moving = True
        if pressed[binds["left"]] and self.rect.x > 326:
            self.rect.x -= self.speed
            self.orientation = "left"
            self.change_status_to("run")
            moving = True

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == binds["punch"]:
                    self.punch()
        if not moving and self.status == "run":
            self.change_status_to("idle")

    def punch(self):
        self.change_status_to("punch")
        collide = pygame.Rect.colliderect(self.rect, self.ennemy.rect)
        if collide:
            self.ennemy.pv -= 10


class Sonic(Fighter):
    def __init__(self, x, y, bindings):
        super().__init__(imgs.sonic, bindings)
        self.rect.x, self.rect.y = x, y
        self.orientation = "right"


class SuperSonic(Fighter):
    def __init__(self, x, y, bindings):
        super().__init__(imgs.super_sonic, bindings)
        self.rect.x, self.rect.y = x, y
        self.orientation = "left"
        self.image = pygame.transform.flip(self.image, True, False)
