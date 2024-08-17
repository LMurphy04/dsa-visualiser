import pygame, sys, random
from pygame import Surface
from config import VisualisationAborted, WHITE, NAVY, GREY, RED, SCREEN_SIZE, BORDER, BLACK
from utils.text import draw_multiline_text, centered_single_line

# Initialise pygame
pygame.init()
clock = pygame.time.Clock()

# Visualisation Variables
ARRAY_SIZE = 30
SPEED_SCALE = 150
BOX_SIZE = (SCREEN_SIZE[0] - 2 * BORDER) // ARRAY_SIZE
BOX_OUTLINE_THICKNESS = 1

# Initialise Array
array = list(range(1, ARRAY_SIZE + 1))

def draw_box(screen:Surface, index:int, value:int, colour:tuple[int, int, int]) -> None:
    x, y = BORDER + index * BOX_SIZE, (SCREEN_SIZE[1] - BOX_SIZE) // 2
    pygame.draw.rect(screen, colour, pygame.Rect(x + BOX_OUTLINE_THICKNESS, y + BOX_OUTLINE_THICKNESS, BOX_SIZE - 2 * BOX_OUTLINE_THICKNESS, BOX_SIZE - 2 * BOX_OUTLINE_THICKNESS))
    draw_multiline_text(screen, (x + 1, y + BOX_SIZE // 4), str(value), BOX_SIZE // 2, BLACK)

def draw_array(screen:Surface, array:list[int], greyed_out:set[int]=set(), highlight:int=None) -> None:
    for index, value in enumerate(array):
        if index in greyed_out:
            colour = GREY
        elif index == highlight:
            colour = RED
        else:
            colour = WHITE
        draw_box(screen, index, value, colour)
    pygame.display.update()

def check_user_input() -> None:
    for event in pygame.event.get():
        # Handle Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Back Out to Menu
            if event.key==pygame.K_BACKSPACE:
                raise VisualisationAborted()

def binary_search(screen:Surface, speed:int, array:list[int], search:int) -> None:
    low, high = 0, len(array) - 1

    # While Uncheck Indexes
    while low <= high:
        mid = (low + high) // 2

        clock.tick(speed)
        draw_box(screen, mid, array[mid], RED)
        pygame.display.update()

        # If Middle Index is Goal
        if array[mid] == search:
            clock.tick(speed)
            draw_array(screen, array, set(list(range(ARRAY_SIZE))) - set(list(range(low, high + 1))), mid)
            return None
        
        if search > array[mid]:
            low = mid + 1

        else:
            high = mid - 1 

        # Show New Range
        clock.tick(speed)
        draw_array(screen, array, set(list(range(ARRAY_SIZE))) - set(list(range(low, high + 1))))

        check_user_input()

def visualise_binary_search(screen:Surface, algorithm:str, speed_slider:callable) -> None:
    speed = (speed_slider() // SPEED_SCALE) + 1 # +1 Prevents Speed = 0
    screen.fill(NAVY)

    # Generate and Display Target (can deliberately be out of range)
    target = random.randint(0, ARRAY_SIZE + 1)
    centered_single_line(screen, (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 2 * BOX_SIZE), f"Target: {str(target)}", 30, WHITE)
    pygame.display.update()

    try:
        clock.tick(speed)
        draw_array(screen, array)
        binary_search(screen, speed, array, target)
        pygame.display.update()
        pygame.time.delay(3000)
    except VisualisationAborted:
        print("Visualisation Aborted.")