from pygame import Surface
import pygame

def draw_text(screen:Surface, text:str, size, font, colour, x, y, bold=False, italic=False, max_x=800):
    text_font = pygame.font.SysFont(font, size, bold, italic)
    cur_x = x
    cur_y = y
    space_size = size // 3
    if italic: space_size //= 2

    words = text.split(" ")

    for word in words:
        word_img = text_font.render(word, True, colour)
        if word_img.get_width() + cur_x >= max_x:
            cur_y += word_img.get_height()
            cur_x = x
        screen.blit(word_img, (cur_x, cur_y))
        cur_x += word_img.get_width() + space_size

    return size + cur_y - y

        
        