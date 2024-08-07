import pygame
from pygame import Surface
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

def render_title(screen:Surface):
    screen.fill(BLACK)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                return render_sorting_algorithm_display, [screen, render_title, "Quick"]

#currently handling screen display
renderer = render_title

#information for the renderer
renderer_values = [screen]

while run:
    clock.tick(60)
    change_renderer = renderer(*renderer_values)
    
    if change_renderer:
        renderer = change_renderer[0]
        renderer_values = change_renderer[1]