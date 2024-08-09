import json
import os
import pygame
from pygame import Surface
from text import draw_text
from sorting_algorithms.sorting_visualiser import run_sorting_algorithm

WHITE = (255, 255, 255)
CREAM = (245, 240, 198)
BLACK = (0, 0, 0)

pygame.init()
clock = pygame.time.Clock()

with open(f"{os.path.dirname(__file__)}/sorting_algorithm_information.json") as json_file:
    sorting_algorithm_info = json.load(json_file)

def render_static_content(screen:Surface, algorithm:str):
    screen.fill(CREAM)
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen.get_width(), 30))
    draw_text(screen, "Sorting Algorithms", 20, "Tahoma", CREAM, 5, 0)
    draw_text(screen, "Back to Menu [Backspace]", 20, "Tahoma", BLACK, 5, 570)
    draw_text(screen, "Visualise [Enter]", 20, "Tahoma", BLACK, 650, 570)

    info = sorting_algorithm_info[algorithm]
    
    draw_text(screen, info["name"], 30, "Tahoma", (0, 0, 0), 10, 30, True)

    pygame.draw.rect(screen, BLACK, (10, 60, 410, 105))
    pygame.draw.rect(screen, WHITE, (15, 65, 130, 45))
    pygame.draw.rect(screen, WHITE, (150, 65, 130, 45))
    pygame.draw.rect(screen, WHITE, (285, 65, 130, 45))
    pygame.draw.rect(screen, WHITE, (15, 115, 130, 45))
    pygame.draw.rect(screen, WHITE, (150, 115, 130, 45))
    pygame.draw.rect(screen, WHITE, (285, 115, 130, 45))

    draw_text(screen, "Worst", 30, "Tahoma", (0, 0, 0), 17, 67, True)
    draw_text(screen, "Average", 30, "Tahoma", (0, 0, 0), 152, 67, True)
    draw_text(screen, "Best", 30, "Tahoma", (0, 0, 0), 287, 67, True)
    draw_text(screen, info["time"]["worst"], 30, "Tahoma", (0, 0, 0), 17, 117)
    draw_text(screen, info["time"]["average"], 30, "Tahoma", (0, 0, 0), 152, 117)
    draw_text(screen, info["time"]["best"], 30, "Tahoma", (0, 0, 0), 287, 117)


    draw_text(screen, info["space"], 30, "Tahoma", (0, 0, 0), 510, 60)


    draw_text(screen, info["stable"], 30, "Tahoma", (0, 0, 0), 610, 60)


    draw_text(screen, info["description"], 20, "Tahoma", (0, 0, 0), 10, 400)

    pygame.display.update()

def render_sorting_algorithm_display(screen:Surface, algorithm:str):
    run = True
    render_static_content(screen, algorithm)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    run_sorting_algorithm(screen, algorithm)
                    render_static_content(screen, algorithm)

                if event.key==pygame.K_BACKSPACE:
                    run = False