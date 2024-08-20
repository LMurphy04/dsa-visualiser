import pygame, sys

from utils.components import Slider, VisualiseButton
from pygame import Surface
from utils.text import draw_multiline_text
from config import SCREEN_SIZE, NAVY, WHITE, RED, BORDER, VISUALISATIONS

# Import Visualisations
from sorting_algorithms.sorting_visualiser import run_sorting_algorithm
from graphs.tree import visualise_tree
from graphs.graph import visualise_graph
from hashmaps.collision_resolution import visualise_hashmap
from miscellaneous.binary_search import visualise_binary_search
from graphs.red_black_tree import visualise_red_black_tree

# Initialise clock
clock = pygame.time.Clock()

# Button Variables
BUTTON_SIZE = (150, 40)
BUTTON_GAP = 5
SUBMENU_TITLE_SIZE = 20

# Menu Screen
def visualiser_select_screen(screen:Surface):
    
    run = True

    # Slider for Visualisation Speed: screen, position, dimensions, value range, initial value
    speed_slider = Slider(screen, (BORDER, 90), (600, 10), (10, 1000), 120)

    def create_buttons(menu_pos: tuple[int, int]) -> tuple[list[tuple[str, int]], list[list[VisualiseButton]]]:

        buttons, submenu_titles = [], []
        x, y = menu_pos
        current_row = 0

        SUBMENU_GAP = BUTTON_GAP * 3
        EDGE_OF_MENU = SCREEN_SIZE[0] - BORDER

        for submenu, visuals in VISUALISATIONS.items():

            # Submenu Title
            submenu_titles.append((submenu, y))
            y += SUBMENU_TITLE_SIZE + BUTTON_GAP
            misc = False

            # Button Logic
            if submenu == "Sorting Algorithms":
                func = run_sorting_algorithm
            elif submenu == "Binary Tree Traversals":
                func = visualise_tree
            elif submenu == "Graph Traversals":
                func = visualise_graph
            elif submenu == "Hashmaps":
                func = visualise_hashmap
            elif submenu == "Miscellaneous":
                misc = True
            
            # New Button Row
            buttons.append([])

            for visual in visuals:
                if misc:
                    if visual == "Binary Search":
                        func = visualise_binary_search
                    elif visual == "Red Black Tree":
                        func = visualise_red_black_tree
                
                if x > EDGE_OF_MENU - BUTTON_SIZE[0]:
                    # Newline
                    x = menu_pos[0]
                    y += BUTTON_SIZE[1] + BUTTON_GAP
                    current_row += 1
                    buttons.append([])
                    
                buttons[current_row].append(VisualiseButton(screen, (x, y), BUTTON_SIZE, visual, func, [screen, visual, speed_slider.get_val]))
                x += BUTTON_SIZE[0] + BUTTON_GAP
            
            # Prepare for next submenu
            current_row += 1
            x = menu_pos[0]
            y += BUTTON_SIZE[1] + SUBMENU_GAP

        return submenu_titles, buttons
    
    # Visualisation Buttons
    menu_pos = (BORDER, 115)
    submenu_titles, buttons = create_buttons(menu_pos)
    active_row, active_col = 0, 0

    def display_menu(screen:Surface) -> None:
        screen.fill(NAVY)

        # Title and Subtitle
        draw_multiline_text(screen, (BORDER, 10), "select a visual", 40, WHITE, True)
        draw_multiline_text(screen, (BORDER, 40), "use arrows, wasd or mouse to select; use backspace to exit early", 20, WHITE, )

        # Speed Slider
        draw_multiline_text(screen, (BORDER, 70), "speed", 20, WHITE, True)
        speed_slider.draw()

        # Submenu Titles
        for title, y in submenu_titles:
            draw_multiline_text(screen, (BORDER, y), title, SUBMENU_TITLE_SIZE, WHITE, True)

        # Buttons
        for row in range(len(buttons)):
            buttons_row = buttons[row]

            for col in range(len(buttons_row)):
                colour = RED if col == active_col and row == active_row else WHITE
                buttons_row[col].draw(colour)

    # Handle keyboard button navigation
    def change_active(direction:str, active_row:int, active_col:int) -> tuple[int, int]:
        
        if direction == "LEFT":
            return active_row, (active_col - 1) % len(buttons[active_row])

        elif direction == "RIGHT":
            return active_row, (active_col + 1) % len(buttons[active_row])

        elif direction == "UP" and active_row != 0: # Not on First Row
            if active_col >= len(buttons[active_row - 1]): active_col = len(buttons[active_row - 1]) - 1 #Logic for if directly above button doesn't exist
            return active_row - 1, active_col

        elif direction == "DOWN" and active_row != len(buttons) - 1: # Not on Last Row
            if active_col >= len(buttons[active_row + 1]): active_col = len(buttons[active_row + 1]) - 1 #Logic for if directly below button doesn't exist
            return active_row + 1, active_col

        return active_row, active_col

    display_menu(screen)
    
    while run:
        clock.tick(60)
        pygame.display.update()

        # Get Mouse State
        mouse_pos, mouse_clicked = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        # Speed Slider
        if mouse_clicked[0] and speed_slider.slide.collidepoint(mouse_pos):
            speed_slider.move_slider(mouse_pos)

        # Check for Button Clicks
        if mouse_clicked[0]:
            for click_row in range(len(buttons)):
                for click_col in range(len(buttons[click_row])):
                    if mouse_clicked[0] and buttons[click_row][click_col].button.collidepoint(mouse_pos):
                        # Activate Visual
                        active_row, active_col = click_row, click_col
                        buttons[click_row][click_col].activate()
                        display_menu(screen)

        for event in pygame.event.get():
            # Handle Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Load Currently Selected Visualisation
                if event.key==pygame.K_RETURN:
                    buttons[active_row][active_col].activate()
                    display_menu(screen)
                
                # Back Out to Title
                if event.key==pygame.K_BACKSPACE:
                    run = False

                # Change Selected Button
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