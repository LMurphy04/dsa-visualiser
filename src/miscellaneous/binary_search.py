import pygame, sys
from pygame import Surface
from config import VisualisationAborted, WHITE, NAVY

pygame.init()
clock = pygame.time.Clock()

SPEED_SCALE = 1

def visualise_binary_search(screen:Surface, algorithm:str, speed_slider:callable) -> None:
    speed = (speed_slider() // SPEED_SCALE) + 1 # +1 Prevents Speed = 0
    screen.fill(NAVY)

    try:
        pygame.display.update()
        pygame.time.delay(3000)
    except VisualisationAborted:
        print("Visualisation Aborted.")