import pygame, sys

from pygame import Surface
from config import VisualisationAborted, BORDER, WHITE, NAVY, RED, SCREEN_SIZE, BLACK
from utils.components import RedBlackBinaryNode

# Initialise Clock
clock = pygame.time.Clock()

# Tree and Node Properties
DEPTH = 4
SPEED_SCALE = 150 # Frame Rate Adjustment as Speed Slider is Based on Sorting Algs
NODE_SIZE = (SCREEN_SIZE[1] - 2 * BORDER) // (2**(DEPTH+1))
X_OFFSET = SCREEN_SIZE[0] // 2 - BORDER
Y_OFFSET = (SCREEN_SIZE[1] - 2 * BORDER - 2 * NODE_SIZE) // DEPTH
root = None

def render_tree(screen:Surface, node:RedBlackBinaryNode, position=(SCREEN_SIZE[0] // 2, BORDER + NODE_SIZE), x_off=X_OFFSET) -> None:
    if node.left:
        left_position = (position[0] - x_off // 2, position[1] + Y_OFFSET)
        pygame.draw.line(screen, WHITE, position, left_position)
        render_tree(screen, node.left, left_position, x_off // 2)
    if node.right:
        right_position = (position[0] + x_off // 2, position[1] + Y_OFFSET)
        pygame.draw.line(screen, WHITE, position, right_position)
        render_tree(screen, node.right, right_position, x_off // 2)
    node.draw(screen, position, NODE_SIZE)

def update(screen:Surface, speed:int) -> None:
    clock.tick(speed)

    for event in pygame.event.get():
        # Handle Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Back Out to Menu
            if event.key==pygame.K_BACKSPACE:
                raise VisualisationAborted
    
    # Redraw Tree
    screen.fill(NAVY)
    render_tree(screen, root)
    pygame.display.update()

def left_rotate(x:RedBlackBinaryNode) -> None:
    global root
    y = x.right

    # Give y's left child to x
    x.right = y.left
    if y.left != None:
        y.left.parent = x

    y.parent = x.parent

    # Update x's parent
    if x.parent == None:
        root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y

    y.left = x
    x.parent = y

def right_rotate(x:RedBlackBinaryNode) -> None:
    global root
    y = x.left

    # Give y's right child to x
    x.left = y.right
    if y.right != None:
        y.right.parent = x

    y.parent = x.parent

    # Update x's parent
    if x.parent == None:
        root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y

    y.right = x
    x.parent = y

def fixup(x:RedBlackBinaryNode, screen:Surface, speed:int) -> None:
    # While Red-Black Tree properties are broken
    while x.parent and x.parent.parent and x.parent.colour == RED:
        if x.parent == x.parent.parent.left:
            # Get uncle
            y = x.parent.parent.right
            
            if y and y.colour == RED:
                # Flip colours of parent, uncle and grandparent
                y.colour = BLACK
                x.parent.colour = BLACK
                x = y.parent
                x.colour = RED
                update(screen, speed)
            
            else:
                if x == x.parent.right:
                    x = x.parent
                    left_rotate(x)
                    update(screen, speed)
                
                x.parent.colour = BLACK
                x.parent.parent.colour = RED
                update(screen, speed)
                right_rotate(x.parent.parent)
                update(screen, speed)
        
        # Symmetric to above
        else:
            y = x.parent.parent.left
            
            if y and y.colour == RED:
                y.colour = BLACK
                x.parent.colour = BLACK
                x = y.parent
                x.colour = RED
                update(screen, speed)
            
            else:
                if x == x.parent.left:
                    x = x.parent
                    right_rotate(x)
                    update(screen, speed)
                
                x.parent.colour = BLACK
                x.parent.parent.colour = RED
                update(screen, speed)
                left_rotate(x.parent.parent)
                update(screen, speed)
    
    # Fix Root
    root.colour = BLACK
    update(screen, speed)

def insert(z:RedBlackBinaryNode, screen:Surface, speed:int) -> None:
    global root
    y = None
    x = root

    # Find new nodes initial position
    while x != None:
        y = x
        if z.value < x.value:
            x = x.left
        else:
            x = x.right

    z.parent = y

    # If z is root
    if y == None:
        root = z
    
    # If z is not root
    else:
        # Update parent
        if z.value < y.value:
            y.left = z
        else:
            y.right = z

    # Update visual and fix tree
    update(screen, speed)
    fixup(z, screen, speed)

# Values to Insert into RBTree
insertions = [36,45,81,40,12,75,77,48,52,49,78,33,98,38,46,86]

def visualise_red_black_tree(screen:Surface, algorithm:str, speed_slider:callable) -> None:
    speed = (speed_slider() / SPEED_SCALE) + 1 # +1 Prevents Speed = 0
    
    # Reset Screen
    global root
    root = None
    screen.fill(NAVY)
    pygame.display.update()

    try:
        for value in insertions:
            node = RedBlackBinaryNode(value)
            insert(node, screen, speed)
        pygame.display.update()
        pygame.time.delay(3000)
    except VisualisationAborted:
        print("Visualisation Aborted.")