import pygame, sys

from pygame import Surface
from config import VisualisationAborted, BORDER, WHITE, NAVY, GREY, RED, SCREEN_SIZE
from utils.components import BinaryNode

# Initialise Clock
clock = pygame.time.Clock()

# Tree and Node Properties
DEPTH = 4
SPEED_SCALE = 35 # Frame Rate Adjustment as Speed Slider is Based on Sorting Algs
NODE_SIZE = (SCREEN_SIZE[1] - 2 * BORDER) // (2**(DEPTH+1))
X_OFFSET = SCREEN_SIZE[0] // 2 - BORDER
Y_OFFSET = (SCREEN_SIZE[1] - 2 * BORDER - 2 * NODE_SIZE) // DEPTH
counter = 1

def build_tree(position:tuple[int, int], depth:int=0) -> BinaryNode:
    node = BinaryNode(position, NODE_SIZE)
    if depth < DEPTH:
        node.left = build_tree((position[0] - X_OFFSET // (2**(depth+1)), position[1] + Y_OFFSET), depth + 1)
        node.right = build_tree((position[0] + X_OFFSET // (2**(depth+1)), position[1] + Y_OFFSET), depth + 1)
    return node

root_position = (SCREEN_SIZE[0] // 2, BORDER + NODE_SIZE)
root = build_tree(root_position)

def reset_values(node:BinaryNode=root) -> None:
    node.value = None
    if node.left: reset_values(node.left)
    if node.right: reset_values(node.right)

def initial_render(screen:Surface) -> None:
    screen.fill(NAVY)

    # Reset Counter Values
    global counter
    counter = 1
    reset_values()

    def render_tree(node:BinaryNode = root) -> None:
        if node.left:
            pygame.draw.line(screen, WHITE, node.position, node.left.position)
            render_tree(node.left)
        if node.right:
            pygame.draw.line(screen, WHITE, node.position, node.right.position)
            render_tree(node.right)
        node.draw(screen, WHITE)

    render_tree()
    pygame.display.update()

def flag(screen:Surface, speed:int, node:BinaryNode) -> None:
    global counter
    clock.tick(speed)

    node.value = counter
    counter += 1

    # Flag Node
    node.draw(screen, RED)
    pygame.display.update()

    # Mark Node as Visited
    node.draw(screen, GREY)

    for event in pygame.event.get():
        # Handle Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Back Out to Menu
            if event.key==pygame.K_BACKSPACE:
                raise VisualisationAborted

# Traversals
def preorder(screen:Surface, speed:int, node:BinaryNode = root) -> None:
    flag(screen, speed, node)
    if node.left: preorder(screen, speed, node.left)
    if node.right: preorder(screen, speed, node.right)

def postorder(screen:Surface, speed:int, node:BinaryNode = root) -> None:
    if node.left: postorder(screen, speed, node.left)
    if node.right: postorder(screen, speed, node.right)
    flag(screen, speed, node)

def inorder(screen:Surface, speed:int, node:BinaryNode = root) -> None:
    if node.left: inorder(screen, speed, node.left)
    flag(screen, speed, node)
    if node.right: inorder(screen, speed, node.right)

def bfs(screen:Surface, speed:int) -> None:
    to_visit = [root]
    while to_visit:
        node = to_visit.pop(0)
        flag(screen, speed, node)
        if node.left: to_visit.append(node.left)
        if node.right: to_visit.append(node.right)

def boundary(screen:Surface, speed:int) -> None:

    def down_left(screen:Surface, speed:int, node:BinaryNode = root) -> None:
        if node.left:
            flag(screen, speed, node)
            down_left(screen, speed, node.left)
        elif node.right:
            flag(screen, speed, node)

    def leaves(screen:Surface, speed:int, node:BinaryNode = root) -> None:
        if not node.left and not node.right:
            flag(screen, speed, node)
        else:
            if node.left: leaves(screen, speed, node.left)
            if node.right: leaves(screen, speed, node.right)

    def up_right(screen:Surface, speed:int, node:BinaryNode = root) -> None:
        if node.right:
            up_right(screen, speed, node.right)
            flag(screen, speed, node)
        elif node.left:
            flag(screen, speed, node)

    down_left(screen, speed)
    leaves(screen, speed)
    up_right(screen, speed)

# Map from Menu Buttons to Functions
algorithms = {
        "Inorder" : inorder,
        "Postorder" : postorder,
        "Preorder" : preorder,
        "Breadth First Search" : bfs,
        "Boundary" : boundary,
    }

def visualise_tree(screen:Surface, algorithm:str, speed_slider:callable) -> None:
    speed = (speed_slider() // SPEED_SCALE) + 1 # +1 Prevents Speed = 0

    initial_render(screen)

    try:
        algorithms[algorithm](screen, speed)
        pygame.display.update()
        pygame.time.delay(3000)
    except VisualisationAborted:
        print("Visualisation Aborted.")