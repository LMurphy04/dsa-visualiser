import pygame, os
from pygame import Surface
from config import SCREEN_SIZE, BORDER

PXL = f"{os.path.dirname(__file__)}/../assets/pxl.ttf"
PXL_BOLD = f"{os.path.dirname(__file__)}/../assets/pxl_bold.ttf"

def draw_multiline_text(screen:Surface, position:tuple[int, int], text:str, size:int, colour:tuple[int, int, int], bold:bool=False, max_x:int=SCREEN_SIZE[0]-BORDER) -> int:
    font = pygame.font.Font(PXL_BOLD if bold else PXL, size)
    cur_x, cur_y = position
    space_size = size // 3

    words = text.split(" ")

    for word in words:
        word_img = font.render(word, True, colour)

        # Check if newline is needed
        if word_img.get_width() + cur_x >= max_x:
            cur_y += word_img.get_height()
            cur_x = position[0]

        screen.blit(word_img, (cur_x, cur_y))
        cur_x += word_img.get_width() + space_size

    # Returns y value of bottom of text
    return word_img.get_height() + cur_y - position[1]

def centered_single_line(screen:Surface, position:tuple[int, int], text:str, size:int, colour:tuple[int, int, int], bold:bool=False) -> None:
    font = pygame.font.Font(PXL_BOLD if bold else PXL, size)
    text_img = font.render(text, True, colour)
    screen.blit(text_img, (position[0] - text_img.get_width() // 2, position[1] - text_img.get_height() // 2))