import pygame
from sorting_algorithms.sorting_algorithm_display import render_sorting_algorithm_display
from pygame import Surface
from text import draw_text
import os
import sys
from sorting_algorithms.sorting_visualiser import run_sorting_algorithm

pygame.init()

clock = pygame.time.Clock()

#rgb colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
NAVY = (0, 0, 50)

#screen properties
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('DSA VISUAL')
ico = pygame.image.load(f"{os.path.dirname(__file__)}/ico.png").convert_alpha()
pygame.display.set_icon(ico)
run = True

class Button():
    
    def __init__(self, x, y, width, height, text, func, params):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = (func, params)

    def draw(self, colour=WHITE):
        pygame.draw.rect(screen, colour, self.rect)
        draw_text(screen, self.text, 20, BLACK, self.rect.x, self.rect.y, max_x=self.rect.x+self.rect.width)

    def activate(self):
        self.action[0](*self.action[1])

def title_screen(screen:Surface):
    screen.fill(NAVY)
    imp = pygame.image.load(f"{os.path.dirname(__file__)}/logo.png").convert_alpha()
    screen.blit(imp, (200, 100))
    draw_text(screen, "dsa visualisation", 40, WHITE, 150, 400, True)
    draw_text(screen, "press enter to start", 30, WHITE, 215, 440)
    draw_text(screen, "made by liam murphy 2024", 20, WHITE, 240, 570)

def visualiser_select_screen(screen:Surface):
    run = True

    submenus = {
        "Sorting Algorithms" : {
            "y" : 0,
            "buttons" : [
                ("Bogo Sort","Bogo"),
                ("Cocktail Sort","Cocktail"),
                ("Bubble Sort Up","Bubble Up"),
                ("Bubble Sort Down","Bubble Down"),
                ("Insertion Sort","Insertion"),
                ("Selection Sort Max","Selection Max"),
                ("Selection Sort Min","Selection Min"),
                ("Merge Sort","Merge"),
                ("Quick Sort","Quick"),
                ("Radix Sort","Radix"),
                ("Counting Sort","Counting"),
                ("Shell Sort","Shell"),
                ("3-Way Quick Sort","Dutch"),
            ]
        },
        "Sorting Algorithms 2" : {
            "y" : 0,
            "buttons" : [
                ("Selection Sort Max", "Selection Max"),
                ("Selection Sort Min", "Selection Min"),
                ("Insertion Sort", "Insertion"),
                ("Selection Sort Max", "Selection Max"),
                ("Selection Sort Min", "Selection Min"),
                ("Insertion Sort", "Insertion"),
                ("Selection Sort Max", "Selection Max"),
            ]
        },
        "Sorting Algorithms 3" : {
            "y" : 0,
            "buttons" : [
                ("Selection Sort Max", "Selection Max"),
                ("Selection Sort Min", "Selection Min"),
                ("Insertion Sort", "Insertion"),
            ]
        },
        "Sorting Algorithms 4" : {
            "y" : 0,
            "buttons" : [
                ("Selection Sort Max", "Selection Max"),
                ("Selection Sort Min", "Selection Min"),
                ("Insertion Sort", "Insertion"),
                ("Selection Sort Max", "Selection Max"),
                ("Selection Sort Min", "Selection Min"),
                ("Insertion Sort", "Insertion"),
            ]
        },
    }

    buttons = []
    submenu_lengths = []
    active_row, active_col = 0, 0

    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 40
    BUTTON_GAP = 5
    SUBMENU_TITLE_SIZE = 20

    y = 85
    x = 10
    row = 0

    for submenu in submenus.items():

        submenu[1]["y"] = y
        submenu_lengths.append(len(submenu[1]["buttons"]))
        y += SUBMENU_TITLE_SIZE + BUTTON_GAP
        buttons.append([])

        for button in submenu[1]["buttons"]:
            if x <= SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_GAP:
                buttons[row].append(Button(x, y, BUTTON_WIDTH, BUTTON_HEIGHT, button[0], run_sorting_algorithm, [screen, button[1]]))
                x += BUTTON_WIDTH + BUTTON_GAP
            else:
                x = 10
                y += BUTTON_HEIGHT + BUTTON_GAP
                buttons.append([])
                row += 1
                buttons[row].append(Button(x, y, BUTTON_WIDTH, BUTTON_HEIGHT, button[0], run_sorting_algorithm, [screen, button[1]]))
                x += BUTTON_WIDTH + BUTTON_GAP
        row += 1
        x = 10
        y += BUTTON_HEIGHT + BUTTON_GAP * 3

    for index in range(1, len(submenu_lengths)):
        submenu_lengths[index] += submenu_lengths[index - 1]

    def display_menu(screen:Surface):
        screen.fill(NAVY)
        draw_text(screen, "select a visual", 40, WHITE, 10, 10, True)
        draw_text(screen, "use arrow keys or wasd to select and press enter to start", 20, WHITE, 10, 50)
        for submenu in submenus.items():
            draw_text(screen, submenu[0], SUBMENU_TITLE_SIZE, WHITE, 10, submenu[1]["y"], True)
        for row in range(len(buttons)):
            buttons_row = buttons[row]
            for col in range(len(buttons_row)):
                if col == active_col and row == active_row:
                    colour = RED
                else:
                    colour = WHITE
                buttons_row[col].draw(colour)

    def change_active(direction, active_row, active_col):
        if direction == "LEFT":
            if active_col == 0:
                if active_row != 0:
                    return active_row - 1, len(buttons[active_row - 1]) - 1
            else:
                return active_row, active_col - 1

        elif direction == "RIGHT":
            if active_col == len(buttons[active_row]) - 1:
                if active_row != len(buttons) - 1:
                    return active_row + 1, 0
            else:
                return active_row, active_col + 1

        elif direction == "UP":
            if active_row != 0:
                if active_col >= len(buttons[active_row - 1]): active_col = len(buttons[active_row - 1]) - 1
                return active_row - 1, active_col

        elif direction == "DOWN":
            if active_row != len(buttons) - 1:
                if active_col >= len(buttons[active_row + 1]): active_col = len(buttons[active_row + 1]) - 1
                return active_row + 1, active_col

        return active_row, active_col

    display_menu(screen)
    
    while run:
        clock.tick(60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    buttons[active_row][active_col].activate()
                    display_menu(screen)
                
                if event.key==pygame.K_BACKSPACE:
                    run = False

                if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    active_row, active_col = change_active("LEFT", active_row, active_col)
                    display_menu(screen)

                if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                    active_row, active_col = change_active("RIGHT", active_row, active_col)
                    display_menu(screen)

                if event.key==pygame.K_UP or event.key==pygame.K_w:
                    active_row, active_col = change_active("UP", active_row, active_col)
                    display_menu(screen)

                if event.key==pygame.K_DOWN or event.key==pygame.K_s:
                    active_row, active_col = change_active("DOWN", active_row, active_col)
                    display_menu(screen)

title_screen(screen)

while run:
    clock.tick(60)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                if visualiser_select_screen(screen): 
                    run = False
                    pygame.quit()
                else:
                    title_screen(screen)