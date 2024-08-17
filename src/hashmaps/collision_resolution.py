import pygame, sys
from pygame import Surface
from config import VisualisationAborted, SCREEN_SIZE, BORDER, WHITE, NAVY, BLACK, RED, LIGHT_RED
from utils.text import draw_multiline_text
from utils.components import LinkedListNode
from hashmaps.operation_sequence import OPERATIONS

# Initialise pygame
pygame.init()
clock = pygame.time.Clock()

# Hashmap Visualisation Variables
SPEED_SCALE = 150
HASHMAP_SIZE = 8
INFORMATION_SIZE = 20
BUCKET_SIZE = (150, (SCREEN_SIZE[1] - 2 * BORDER - 2 * INFORMATION_SIZE) // HASHMAP_SIZE)
BUCKET_GAP = 2
CHAIN_GAP = 10
INDEX_MARKER_WIDTH = 15

# Used to denote emptied slots that used to contain an item
class Del(): pass
DELETED = Del()

# Visualisation Logic
def draw_bucket(screen:Surface, colour:tuple[int, int, int], position:tuple[int, int], contents:any, dimensions:tuple[int, int]=BUCKET_SIZE, link_to:tuple[int, int]=None) -> None:
    pygame.draw.rect(screen, colour, pygame.Rect(position[0] + BUCKET_GAP // 2, position[1] + BUCKET_GAP // 2, dimensions[0] - BUCKET_GAP, dimensions[1] - BUCKET_GAP))
    if contents != None:
        if isinstance(contents, tuple): contents = f"{contents[0]}, {contents[1]}"
        if contents == DELETED: contents = "EMPTY"
        draw_multiline_text(screen, position, contents, 20, BLACK, max_x=position[0]+dimensions[0])
    if link_to: pygame.draw.line(screen, WHITE, (position[0], position[1] + dimensions[1] // 2), (link_to[0] + BUCKET_SIZE[0], link_to[1] + BUCKET_SIZE[1] // 2))

def draw_linked_list(screen:Surface, node:LinkedListNode, position:tuple[int, int], highlight_index:int=None) -> None:
    pygame.draw.rect(screen, NAVY, pygame.Rect(*position, SCREEN_SIZE[0], BUCKET_SIZE[1]))
    
    index = 0
    highlight_node = node if index == highlight_index else None
    draw_bucket(screen, WHITE if index != highlight_index else LIGHT_RED, position, node.value)
    node = node.next
    prev_pos = position

    while node != None:
        index += 1
        node_position = (prev_pos[0] + BUCKET_SIZE[0] + CHAIN_GAP, prev_pos[1])
        if index == highlight_index: highlight_node = node
        draw_bucket(screen, WHITE if index != highlight_index else LIGHT_RED, node_position, node.value, link_to=position)
        prev_pos = node_position
        node = node.next
    
    pygame.display.update()
    if highlight_node: draw_bucket(screen, WHITE, (position[0] + (BUCKET_SIZE[0] + CHAIN_GAP) * highlight_index, position[1]), highlight_node.value)

def initialise_hashmap(screen:Surface, hashmap:list) -> None:
    screen.fill(NAVY)
    for index, bucket in enumerate(hashmap):
        draw_bucket(screen, RED, (BORDER, BORDER+index*BUCKET_SIZE[1]), str(index), (INDEX_MARKER_WIDTH, BUCKET_SIZE[1]))
        draw_bucket(screen, WHITE, (BORDER+INDEX_MARKER_WIDTH, BORDER+index*BUCKET_SIZE[1]), bucket)
    pygame.display.update()

def highlight_box(screen:Surface, value:any, index:int, depth:int) -> None:
    draw_bucket(screen, LIGHT_RED, (BORDER+INDEX_MARKER_WIDTH + (BUCKET_SIZE[0] + CHAIN_GAP) * depth, BORDER+index*BUCKET_SIZE[1]), value)
    pygame.display.update()
    draw_bucket(screen, WHITE, (BORDER+INDEX_MARKER_WIDTH + (BUCKET_SIZE[0] + CHAIN_GAP) * depth, BORDER+index*BUCKET_SIZE[1]), value)

def display_info(screen:Surface, text:str) -> None:
    pygame.draw.rect(screen, NAVY, pygame.Rect(0, SCREEN_SIZE[1] - BORDER - INFORMATION_SIZE, SCREEN_SIZE[0], BORDER + INFORMATION_SIZE))
    draw_multiline_text(screen, (BORDER, SCREEN_SIZE[1] - BORDER - INFORMATION_SIZE), text, INFORMATION_SIZE, WHITE)
    pygame.display.update()

def check_user_input() -> None:
    for event in pygame.event.get():
        # Handle Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Back Out to Menu
            if event.key==pygame.K_BACKSPACE:
                raise VisualisationAborted()

# Hashing Types
def integer_hash(key:any) -> int:
    if isinstance(key, str): return sum(map(ord, key)) % HASHMAP_SIZE

def polynomial_hash(key:any) -> int:
    MULTIPLIER = 3
    if isinstance(key, str): return sum([ord(key) * (MULTIPLIER**index) for index, key in enumerate(key)]) % HASHMAP_SIZE

# Probing Collision Resolution
def probing(screen:Surface, algorithm:str, speed:int, hashmap:list) -> None:

    # Probing Types
    def linear_probing(value:int, increment:int) -> int:
        return (value + increment) % HASHMAP_SIZE

    def quadratic_probing(value:int, increment:int) -> int:
        C1, C2 = 5, 12
        return (value + C1 + C2*((increment)**2)) % HASHMAP_SIZE
    
    def double_hashing(value:int, increment:int) -> int:
        return (value + poly_hash_value * increment) % HASHMAP_SIZE

    probing_type = {
        "Linear Probing": linear_probing,
        "Quadratic Probing": quadratic_probing,
        "Double Hashing": double_hashing
    }

    get_next_index = probing_type[algorithm]

    # Hashmap Logic
    def add(hashmap:list, index:int, key:any, value:any) -> None:
        check_index, increment = index, 0

        # Probe Until Space Found
        while hashmap[check_index] != None and hashmap[check_index] != DELETED and hashmap[check_index][0] != key:
            clock.tick(speed)
            highlight_box(screen, hashmap[check_index], check_index, 0)
            increment += 1

            # If Hashmap is Full
            if increment == HASHMAP_SIZE:
                clock.tick(speed)
                display_info(screen, "Full!")
                return None
            
            check_index = get_next_index(index, increment)
            check_user_input()
        
        # Add to Hashmap
        clock.tick(speed)
        hashmap[check_index] = (key, value)
        highlight_box(screen, hashmap[check_index], check_index, 0)

    def delete(hashmap:list, index:int, key:any) -> None:
        check_index, increment = index, 0

        # Probe Until Value is Found
        while hashmap[check_index] != None and (hashmap[check_index] == DELETED or hashmap[check_index][0] != key):
            clock.tick(speed)
            highlight_box(screen, hashmap[check_index], check_index, 0)
            
            increment += 1

            # If Hashmap is Full and Value Was Not Found
            if increment == HASHMAP_SIZE:
                display_info(screen, "Not Found!")
                return None
            
            check_index = get_next_index(index, increment)
            check_user_input()

        # Delete If Value Was Found
        if hashmap[check_index][0] != None:
            clock.tick(speed)
            hashmap[check_index] = DELETED
            highlight_box(screen, hashmap[check_index], check_index, 0)

        # Value Not Found
        else:
            clock.tick(speed)
            display_info(screen, "Not Found!")

    def search(hashmap:list, index:int, key:any) -> None:
        check_index, increment = index, 0

        # Probe Until Value is Found
        while hashmap[check_index] != None:
            clock.tick(speed)
            highlight_box(screen, hashmap[check_index], check_index, 0)
            
            # If Value Found
            if hashmap[check_index] != DELETED and hashmap[check_index][0] == key:
                clock.tick(speed)
                display_info(screen, f"Found: {str(hashmap[check_index][1])}")
                return None
            
            increment += 1

            # If Hashmap is Full and Value Not Found
            if increment == HASHMAP_SIZE:
                clock.tick(speed)
                display_info(screen, "Not Found!")
                return None
            
            check_index = get_next_index(index, increment)
            check_user_input()
        
        # Value Not Found
        clock.tick(speed)
        highlight_box(screen, hashmap[check_index], check_index, 0)
        clock.tick(speed)
        display_info(screen, "Not Found!")

    functions = {
        "Add" : add,
        "Delete" : delete,
        "Search" : search
    }

    # Execute Operations
    for operation in OPERATIONS:
        clock.tick(speed)
        display_info(screen, f"Current: {operation[0]} {operation[1] if operation[0] != 'Add' else f'({operation[1]}, {operation[2]})'}")
        
        index = integer_hash(operation[1])
        poly_hash_value = polynomial_hash(operation[1])
        functions[operation[0]](hashmap, index, *operation[1:])
        
        check_user_input()

# Chaining Collision Resolution
def chaining(screen:Surface, speed:int, hashmap:list) -> None:

    # Hashmap Logic
    def add(hashmap:list, index:int, key:any, value:any) -> None:
        new_node = LinkedListNode((key, value))

        # Add to the Start of Linked List (or create)
        if hashmap[index] != None:
            new_node.next = hashmap[index]
            hashmap[index].prev = new_node
        hashmap[index] = new_node

        clock.tick(speed)
        draw_linked_list(screen, hashmap[index], (BORDER+INDEX_MARKER_WIDTH, BORDER+index*BUCKET_SIZE[1]), 0)

    def delete(hashmap:list, index:int, key:any) -> None:
        depth, node = 0, hashmap[index]

        # If Index is Empty
        if node == None:
            clock.tick(speed)
            highlight_box(screen, None, index, depth)
            clock.tick(speed)
            display_info(screen, "Not Found!")
            return None

        # Traverse List Until Found or End
        while node != None and node.value[0] != key:
            clock.tick(speed)
            highlight_box(screen, node.value, index, depth)
            node = node.next
            depth += 1

            check_user_input()

        # If Not Found
        if node == None:
            clock.tick(speed)
            display_info(screen, "Not Found!")
        
        # If Found, Delete
        else:
            if node.prev: node.prev.next = node.next
            if node.next: node.next.prev = node.prev
            if hashmap[index] == node: hashmap[index] = node.next

            clock.tick(speed)
            draw_linked_list(screen, hashmap[index], (BORDER+INDEX_MARKER_WIDTH, BORDER+index*BUCKET_SIZE[1]))

    def search(hashmap:list, index:int, key:any) -> None:
        depth, node = 0, hashmap[index]

        # If Index is Empty
        if node == None:
            clock.tick(speed)
            highlight_box(screen, None, index, depth)
            clock.tick(speed)
            display_info(screen, "Not Found!")
            return None
        
        # Traverse List Until Found or End
        while node != None and node.value[0] != key:
            clock.tick(speed)
            highlight_box(screen, node.value, index, depth)
            node = node.next
            depth += 1

            check_user_input()

        # If Not Found
        if node == None:
            clock.tick(speed)
            display_info(screen, "Not Found!")
        
        # If Found
        else:
            clock.tick(speed)
            highlight_box(screen, node.value, index, depth)
            clock.tick(speed)
            display_info(screen, f"Found: {str(node.value[1])}")

    functions = {
        "Add" : add,
        "Delete" : delete,
        "Search" : search
    }

    # Operation Execution
    for operation in OPERATIONS:
        clock.tick(speed)
        display_info(screen, f"Current: {operation[0]} {operation[1] if operation[0] != 'Add' else f'({operation[1]}, {operation[2]})'}")
        
        index = integer_hash(operation[1])
        functions[operation[0]](hashmap, index, *operation[1:])
        
        check_user_input()

def visualise_hashmap(screen:Surface, algorithm:str, speed_slider:callable) -> None:
    speed = (speed_slider() // SPEED_SCALE) + 1 # +1 Prevents Speed = 0
    hashmap = [None] * HASHMAP_SIZE
    initialise_hashmap(screen, hashmap)

    try:
        probing(screen, algorithm, speed, hashmap) if algorithm != "Chaining" else chaining(screen, speed, hashmap)
        pygame.display.update()
        pygame.time.delay(3000)
    except VisualisationAborted:
        print("Visualisation Aborted.")