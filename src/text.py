from pygame import Surface
import pygame
import os

PXL = f"{os.path.dirname(__file__)}/fonts/pxl.ttf"
PXL_BOLD = f"{os.path.dirname(__file__)}/fonts/pxl_bold.ttf"

def draw_text(screen:Surface, text:str, size, colour, x, y, bold=False, max_x=790):
    if bold: font = PXL_BOLD
    else: font = PXL
    text_font = pygame.font.Font(font, size)
    cur_x = x
    cur_y = y
    space_size = size // 3

    words = text.split(" ")

    for word in words:
        word_img = text_font.render(word, True, colour)
        if word_img.get_width() + cur_x >= max_x:
            cur_y += word_img.get_height()
            cur_x = x
        screen.blit(word_img, (cur_x, cur_y))
        cur_x += word_img.get_width() + space_size

    return size + cur_y - y

        
        