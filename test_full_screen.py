import pygame
import sys

# Initialise Variables
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
# font = pygame.font.Font(None, 74)
menu_options = ["New Game", "Load Game", "Exit"]
selected_option = 0


# Functions
def draw_menu():
    screen.fill(black)
    for i, option in enumerate(menu_options):
        color = red if i == selected_option else white
        text = font.render(option, True, color)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + i * 100))
        screen.blit(text, text_rect)
    pygame.display.flip()


# Game
pygame.display.set_caption("Start Menu")
pygame.init()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    pygame.display.flip()
pygame.quit()
sys.exit()