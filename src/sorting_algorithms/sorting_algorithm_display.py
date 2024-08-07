import json
import os
import pygame
from pygame import Surface
from sorting_algorithms.sorting_visualiser import run_sorting_algorithm

pygame.init()
clock = pygame.time.Clock()

with open(f"{os.path.dirname(__file__)}/sorting_algorithm_information.json") as json_file:
    sorting_algorithm_info = json.load(json_file)

def render_sorting_algorithm_display(screen:Surface, algorithm:str):
    run = True

    while run:
        clock.tick(60)
        screen.fill((255, 0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    run_sorting_algorithm(screen, algorithm)

                if event.key==pygame.K_BACKSPACE:
                    run = False