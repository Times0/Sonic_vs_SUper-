import pygame
import sys

# Pygame Initialization
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_button(screen, message, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    text = FONT.render(message, True, BLACK)
    screen.blit(text, (x + (w - text.get_width()) / 2, y + (h - text.get_height()) / 2))

def quit_game():
    pygame.quit()
    sys.exit()

def start_game():
    print("Game is starting...")

def game_loop():
    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        button_width, button_height = 200, 50
        gap = 20  # gap between buttons

        # Calculate positions for the buttons to be centered
        play_button_x = WIDTH / 2 - button_width / 2
        play_button_y = HEIGHT / 2 - button_height / 2
        quit_button_x = WIDTH / 2 - button_width / 2
        quit_button_y = play_button_y + button_height + gap

        draw_button(screen, "Play", play_button_x, play_button_y, button_width, button_height, (0,255,0), (0,200,0), start_game)
        draw_button(screen, "Quit", quit_button_x, quit_button_y, button_width, button_height, (255,0,0), (200,0,0), quit_game)

        pygame.display.update()

game_loop()
