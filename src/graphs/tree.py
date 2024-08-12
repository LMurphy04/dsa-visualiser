import pygame
from pygame import Surface
pygame.init()
import sys
clock = pygame.time.Clock()

class VisualisationAborted(Exception):
    pass

class Node():
    
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.left = None
        self.right = None

    def draw(self, screen, colour, text=None):
        pygame.draw.circle(screen, colour, (self.x , self.y), self.radius)

DEPTH = 4
SPEED_SCALE = 35
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

    screen.fill((0, 0, 50))
    render_tree()
    pygame.display.update()

def flag(screen, speed, node):
    clock.tick(speed)
    node.draw(screen, (255, 0, 0))
    pygame.display.update()
    node.draw(screen, (100, 100, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_BACKSPACE:
                raise VisualisationAborted

def preorder(screen:Surface, speed, node = root[0]):
    flag(screen, speed, node)
    if node.left: preorder(screen, speed, node.left)
    if node.right: preorder(screen, speed, node.right)

def postorder(screen:Surface, speed, node = root[0]):
    if node.left: postorder(screen, speed, node.left)
    if node.right: postorder(screen, speed, node.right)
    flag(screen, speed, node)

def inorder(screen:Surface, speed, node = root[0]):
    if node.left: inorder(screen, speed, node.left)
    flag(screen, speed, node)
    if node.right: inorder(screen, speed, node.right)

def bfs(screen:Surface, speed):
    to_visit = [root[0]]
    while to_visit:
        node = to_visit.pop(0)
        flag(screen, speed, node)
        if node.left: to_visit.append(node.left)
        if node.right: to_visit.append(node.right)

def boundary(screen, speed):

    def down_left(screen, speed, node = root[0]):
        if node.left:
            flag(screen, speed, node)
            down_left(screen, speed, node.left)
        elif node.right:
            flag(screen, speed, node)

    def leaves(screen, speed, node = root[0]):
        if not node.left and not node.right:
            flag(screen, speed, node)
        else:
            if node.left: leaves(screen, speed, node.left)
            if node.right: leaves(screen, speed, node.right)

    def up_right(screen, speed, node = root[0]):
        if node.right:
            up_right(screen, speed, node.right)
            flag(screen, speed, node)
        elif node.left:
            flag(screen, speed, node)

    down_left(screen, speed)
    leaves(screen, speed)
    up_right(screen, speed)

algorithms = {
        "Inorder" : inorder,
        "Postorder" : postorder,
        "Preorder" : preorder,
        "Breadth First Search" : bfs,
        "Boundary" : boundary,
    }

def visualise_tree(screen:Surface, algorithm, speed_slider):
    initial_render(screen)

    speed = (speed_slider() // SPEED_SCALE) + 1

    try:
        algorithms[algorithm](screen, speed)
        clock.tick(speed)
        pygame.display.update()
    except VisualisationAborted:
        print("Visualisation Aborted.")