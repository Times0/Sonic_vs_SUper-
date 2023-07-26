import os

import pygame
from PIL import Image

from constants import *

bg = pygame.image.load("assets/bg_pa.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))


def crop_image(file_path, x, y, w, h, output_file):
    try:
        img = Image.open(file_path)
    except FileNotFoundError:
        print(f"No file found at {file_path}")
        return
    # create directory for output file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    cropped_img = img.crop((x, y, x + w, y + h))
    cropped_img.save(os.path.join(output_file))


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1, 1))

    crop_image("assets/super_sonic.png",0 , 327, 59, 40, "assets/characters/super_sonic/kick/kick2.png")


def load_image(path, size=None):
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image


def split_image_horizontally(img, parts):
    width = img.get_width()
    height = img.get_height()
    part_width = width // parts
    print(f"width is {part_width} for {parts}")
    part_height = height
    images = []
    for i in range(parts):
        image = img.subsurface((part_width * i, 0, part_width, part_height))
        images.append(pygame.transform.scale_by(image, 5))

    return images


"""format = run_down_40x40.png"""
nb_img_ssonic = {
    "idle": 6,
    "run": 4,
    "punch":6,
}

nb_img_sonic = {
    "idle": 6,
    "run": 9,
    "punch":6,
}

folders = list(nb_img_sonic.keys())


def load_character_images(path, nb_img) -> dict:
    images = {}
    for folder in folders:
        images[folder] = {}
        n = nb_img[folder]
        p = os.path.join(path, folder, f"{folder}.png")
        sprite_sheet = load_image(p)
        img = split_image_horizontally(sprite_sheet, n)
        images[folder] = img
    return images


sonic = load_character_images(os.path.join("assets", "characters", "sonic"), nb_img_sonic)
super_sonic = load_character_images(os.path.join("assets", "characters", "super_sonic"), nb_img_ssonic)
