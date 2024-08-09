import pygame
from sorting_algorithms.sorting_algorithm_display import render_sorting_algorithm_display

pygame.init()
clock = pygame.time.Clock()

#rgb colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#screen properties
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
run = True

while run:
    clock.tick(60)
    
    screen.fill(BLACK)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                render_sorting_algorithm_display(screen, "Bogo")

pygame.quit()