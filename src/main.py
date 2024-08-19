import pygame, os, sys

from config import SCREEN_SIZE, WHITE, NAVY
from pygame import Surface
from utils.text import draw_multiline_text
from visualisation_menu import visualiser_select_screen

# Screen Setup
pygame.init()
run = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
ico = pygame.image.load(f"{os.path.dirname(__file__)}/assets/ico.png").convert_alpha()
pygame.display.set_caption('DSA VISUAL')
pygame.display.set_icon(ico)

# Title Screen
def draw_title_screen(screen:Surface) -> None:
    screen.fill(NAVY)

    logo_position, logo = (200, 100), pygame.image.load(f"{os.path.dirname(__file__)}/assets/logo.png").convert_alpha()
    screen.blit(logo, logo_position)

    draw_multiline_text(screen, (150, 400), "dsa visualisation", 40, WHITE, True)
    draw_multiline_text(screen, (215, 440), "press enter to start", 30, WHITE)
    draw_multiline_text(screen, (240, 570), "made by liam murphy 2024", 20, WHITE)

    pygame.display.update()
    

draw_title_screen(screen)

# Title Screen Gameloop
while run:
    clock.tick(60)

    for event in pygame.event.get():

        # Handle Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Load Menu
            if event.key==pygame.K_RETURN:
                visualiser_select_screen(screen)
                draw_title_screen(screen)