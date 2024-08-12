import pygame
from config import WHITE, RED, BLACK
from pygame import Surface
from utils.text import draw_multiline_text

class Slider():

    def __init__(self, screen:Surface, position:tuple, dimensions:tuple, value_range:tuple, initial_value:int):
        HANDLE_WIDTH = 20
        x, y = position
        width, height = dimensions

        self.screen = screen
        self.min, self.max = value_range

        initial_percentage = initial_value / (self.max + self.min)
        handle_initial_x_offset = int((width - HANDLE_WIDTH) * initial_percentage)

        self.backing = pygame.Rect(x, y, width, height)
        self.slide = pygame.Rect(x + HANDLE_WIDTH // 2, y, width - HANDLE_WIDTH + 1, height) # Handle was 1px too small for some reason
        self.handle = pygame.Rect(x + handle_initial_x_offset, y, HANDLE_WIDTH, height)

    def draw(self):
        pygame.draw.rect(self.screen, WHITE, self.backing)
        pygame.draw.rect(self.screen, WHITE, self.slide)
        pygame.draw.rect(self.screen, RED, self.handle)

    def get_val(self):
        value_per_unit = (self.max - self.min) / self.slide.width
        relative_handle_pos = self.handle.centerx - self.slide.x
        return int(value_per_unit * relative_handle_pos + self.min)
    
    def move_slider(self, mouse_pos:tuple):
        self.handle.centerx = mouse_pos[0]
        self.draw()

class VisualiseButton():
    
    def __init__(self, screen:Surface, position:tuple, dimensions:tuple, text:str, func:callable, params:list):
        self.screen = screen
        self.text = text
        self.button = pygame.Rect(*position, *dimensions)
        self.action = (func, params)

    def draw(self, colour:tuple=WHITE):
        pygame.draw.rect(self.screen, colour, self.button)
        draw_multiline_text(self.screen, (self.button.x, self.button.y), self.text, 20, BLACK, max_x=self.button.x+self.button.width)

    def activate(self):
        self.action[0](*self.action[1])