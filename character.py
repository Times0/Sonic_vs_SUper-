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

        self.is_alive = True

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
                if self.status == "kick":
                    self.change_status_to("idle")
            self.image = self.imgs[self.status][self.anim_index]
            if self.orientation == "left":
                self.image = pygame.transform.flip(self.image, True, False)

            if self.orientation == "right":
                self.rect = self.image.get_rect(topleft=self.rect.topleft)
            else:
                self.rect = self.image.get_rect(topright=self.rect.topright)

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
                    self.attack("punch")
                if event.key == binds["kick"]:
                    self.attack("kick")
        if not moving and self.status == "run":
            self.change_status_to("idle")

    def attack(self, attack_type: str):
        self.change_status_to(attack_type)
        if self.orientation == "right":
            punch_rect = pygame.Rect(self.rect.x + self.rect.w, self.rect.y, 100, self.rect.h)
        else:
            punch_rect = pygame.Rect(self.rect.x - 100, self.rect.y, 100, self.rect.h)

        collide = pygame.Rect.colliderect(punch_rect, self.ennemy.rect)
        if collide:
            self.ennemy.take_dmg(10 if attack_type == "punch" else 20 if attack_type == "kick" else 0)

    def take_dmg(self, dmg):
        self.pv -= dmg
        if self.pv == 0:
            self.is_alive = False
        if self.pv <= 0:
            self.is_alive = False

    def draw(self, win, debug=True):
        win.blit(self.image, self.rect)
        x = self.rect.x + (self.rect.w - self.max_pv) // 2
        pygame.draw.rect(win, RED, (x, self.rect.y - 50, self.max_pv, 30))
        pygame.draw.rect(win, GREEN, (x, self.rect.y - 50, self.pv, 30))
        pygame.draw.rect(win, BLACK, (x, self.rect.y - 50, self.max_pv, 30), 3)

        if debug:
            pygame.draw.rect(win, RED, self.rect, 3)

            # draw status on top of character
            font = pygame.font.SysFont("None", 40)
            text = font.render(self.status, True, BLACK)
            win.blit(text, (self.rect.x, self.rect.y - 100))

            if self.status == "punch" or self.status == "kick":
                if self.orientation == "right":
                    punch_rect = pygame.Rect(self.rect.x + self.rect.w, self.rect.y, 100, self.rect.h)
                else:
                    punch_rect = pygame.Rect(self.rect.x - 100, self.rect.y, 100, self.rect.h)
                pygame.draw.rect(win, RED, punch_rect, 3)


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
