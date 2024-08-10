import pygame
from pygame import Surface
pygame.init()
import sys
clock = pygame.time.Clock()

class Node():
    
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.left = None
        self.right = None

    def draw(self, screen, colour, text=None):
        pygame.draw.circle(screen, colour, (self.x , self.y), self.radius)

DEPTH = 3
SPEED_SCALE = 50
NODE_SIZE = 580 // (2**(DEPTH+1))
BORDER = 10
X_OFFSET = 390
Y_OFFSET = (580 - (2 * NODE_SIZE)) // DEPTH

x, y = BORDER + X_OFFSET, BORDER + NODE_SIZE

root = [None]

def build_tree(node_x, node_y, depth=0):
    node = Node(node_x, node_y, NODE_SIZE)
    if root[0] == None: root[0] = node
    if depth < DEPTH:
        node.left = build_tree(node_x - X_OFFSET // (2**(depth+1)), node_y + Y_OFFSET, depth + 1)
        node.right = build_tree(node_x + X_OFFSET // (2**(depth+1)), node_y + Y_OFFSET, depth + 1)
    return node

build_tree(x, y)

def initial_render(screen:Surface):
    
    def render_tree(node = root[0]):
        if node.left:
            pygame.draw.line(screen, (255, 255, 255), (node.x, node.y), (node.left.x, node.left.y))
            render_tree(node.left)
        if node.right:
            pygame.draw.line(screen, (255, 255, 255), (node.x, node.y), (node.right.x, node.right.y))
            render_tree(node.right)
        node.draw(screen, (255, 255, 255))

    render_tree()
    pygame.display.update()

def flag(speed, node):
    clock.tick(speed // SPEED_SCALE)
    node.draw(screen, (255, 0, 0))
    pygame.display.update()
    node.draw(screen, (100, 100, 100))

def preorder(screen:Surface, speed, node = root[0]):
    flag(speed, node)
    if node.left: preorder(screen, speed, node.left)
    if node.right: preorder(screen, speed, node.right)

def postorder(screen:Surface, speed, node = root[0]):
    if node.left: postorder(screen, speed, node.left)
    if node.right: postorder(screen, speed, node.right)
    flag(speed, node)

def inorder(screen:Surface, speed, node = root[0]):
    if node.left: inorder(screen, speed, node.left)
    flag(speed, node)
    if node.right: inorder(screen, speed, node.right)

def visualise_tree(screen:Surface, speed=120):
    initial_render(screen)
    pygame.time.delay(1000)
    preorder(screen, speed)
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

screen = pygame.display.set_mode((800, 600))
screen.fill((0, 0, 50))
pygame.display.update()
visualise_tree(screen)