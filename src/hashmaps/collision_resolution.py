import pygame, sys
from pygame import Surface
from config import VisualisationAborted, SCREEN_SIZE, BORDER, WHITE, NAVY, BLACK, RED, LIGHT_RED
from utils.text import draw_multiline_text
from hashmaps.operation_sequence import OPERATIONS

pygame.init()
clock = pygame.time.Clock()

SPEED_SCALE = 150
HASHMAP_SIZE = 8
INFORMATION_SIZE = 20
BUCKET_WIDTH = 150
BUCKET_HEIGHT = (SCREEN_SIZE[1] - 2 * BORDER - 2 * INFORMATION_SIZE) // HASHMAP_SIZE
BUCKET_GAP = 2
INDEX_MARKER_WIDTH = 15

class Del(): pass # Used to mark empty slots that used to contain an item
DELETED = Del()

def display_info(screen:Surface, text:str) -> None:
    pygame.draw.rect(screen, NAVY, pygame.Rect(0, SCREEN_SIZE[1] - BORDER - INFORMATION_SIZE, SCREEN_SIZE[0], BORDER + INFORMATION_SIZE))
    draw_multiline_text(screen, (BORDER, SCREEN_SIZE[1] - BORDER - INFORMATION_SIZE), text, INFORMATION_SIZE, WHITE)
    pygame.display.update()

def highlight_box(screen:Surface, hashmap:int, position:tuple[int, int], index:int) -> None:
    draw_bucket(screen, LIGHT_RED, position, hashmap[index])
    pygame.display.update()
    draw_bucket(screen, WHITE, position, hashmap[index])

def draw_bucket(screen:Surface, colour:tuple[int, int, int], position:tuple[int, int], contents:any, dimensions:tuple[int, int]=(BUCKET_WIDTH, BUCKET_HEIGHT), link_to:tuple[int, int]=None) -> None:
    pygame.draw.rect(screen, colour, pygame.Rect(position[0] + BUCKET_GAP // 2, position[1] + BUCKET_GAP // 2, dimensions[0] - BUCKET_GAP, dimensions[1] - BUCKET_GAP))
    if contents != None:
        if isinstance(contents, tuple): contents = f"{contents[0]}, {contents[1]}"
        if contents == DELETED: contents = "EMPTY"
        draw_multiline_text(screen, position, contents, 20, BLACK, max_x=position[0]+dimensions[0])
    if link_to:
        pygame.draw.line(screen, WHITE, (position[0], position[1] + dimensions[1] // 2), link_to)

def draw_hashmap(screen:Surface, hashmap:list) -> None:
    screen.fill(NAVY)
    for index, bucket in enumerate(hashmap):
        draw_bucket(screen, RED, (BORDER, BORDER+index*BUCKET_HEIGHT), str(index), (INDEX_MARKER_WIDTH, BUCKET_HEIGHT))
        draw_bucket(screen, WHITE, (BORDER+INDEX_MARKER_WIDTH, BORDER+index*BUCKET_HEIGHT), bucket)
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

def hash(key:any) -> int:
    if isinstance(key, str): return sum(map(ord, key)) % HASHMAP_SIZE
    if isinstance(key, int): return key % HASHMAP_SIZE

def linear_probing(value:int, increment:int) -> int:
    return hash(value + increment)

def quadratic_probing(value:int, increment:int) -> int:
    C1, C2 = 5, 12
    return hash(value + C1 + C2*((increment)**2))

probing_type = {
    "Linear Probing": linear_probing,
    "Quadratic Probing": quadratic_probing,
}

def probing(screen:Surface, algorithm:str, speed:int, hashmap:list) -> list:

    get_next_index = probing_type[algorithm]

    def add(hashmap:list, index:int, key:any, value:any) -> bool:
        clock.tick(speed)
        increment = 0
        check_index = index
        while hashmap[check_index] != None and hashmap[check_index] != DELETED and hashmap[check_index][0] != key:
            highlight_box(screen, hashmap, (BORDER+INDEX_MARKER_WIDTH, BORDER+check_index*BUCKET_HEIGHT), check_index)
            clock.tick(speed)
            increment += 1
            if increment == HASHMAP_SIZE:
                display_info(screen, "Full!")
                return False
            check_index = get_next_index(index, increment)
            check_user_input()
        hashmap[check_index] = (key, value)
        highlight_box(screen, hashmap, (BORDER+INDEX_MARKER_WIDTH, BORDER+check_index*BUCKET_HEIGHT), check_index)

    def delete(hashmap:list, index:int, key:any) -> bool:
        clock.tick(speed)
        increment = 0
        check_index = index
        while hashmap[check_index] != None and (hashmap[check_index] == DELETED or hashmap[check_index][0] != key):
            highlight_box(screen, hashmap, (BORDER+INDEX_MARKER_WIDTH, BORDER+check_index*BUCKET_HEIGHT), check_index)
            clock.tick(speed)
            increment += 1
            if increment == HASHMAP_SIZE:
                display_info(screen, "Not Found!")
                return None
            check_index = get_next_index(index, increment)
            check_user_input()
        if hashmap[check_index][0] != None:
            hashmap[check_index] = DELETED
            highlight_box(screen, hashmap, (BORDER+INDEX_MARKER_WIDTH, BORDER+check_index*BUCKET_HEIGHT), check_index)
        else:
            display_info(screen, "Not Found!")

    def search(hashmap:list, index:int, key:any) -> any:
        clock.tick(speed)
        increment = 0
        check_index = index
        while hashmap[check_index] != None:
            highlight_box(screen, hashmap, (BORDER+INDEX_MARKER_WIDTH, BORDER+check_index*BUCKET_HEIGHT), check_index)
            clock.tick(speed)
            if hashmap[check_index] != DELETED and hashmap[check_index][0] == key:
                display_info(screen, f"Found: {str(hashmap[check_index][1])}")
                return hashmap[check_index][1]
            increment += 1
            if increment == HASHMAP_SIZE: 
                display_info(screen, "Not Found!")
                return None
            check_index = get_next_index(index, increment)
            check_user_input()
        highlight_box(screen, hashmap, (BORDER+INDEX_MARKER_WIDTH, BORDER+check_index*BUCKET_HEIGHT), check_index)
        clock.tick(speed)
        display_info(screen, "Not Found!")

    functions = {"Add" : add, "Delete" : delete, "Search" : search}

    for operation in OPERATIONS:
        display_info(screen, f"Current: {operation[0]} {operation[1] if operation[0] != 'Add' else f'({operation[1]}, {operation[2]})'}")
        clock.tick(speed)
        index = hash(operation[1])
        result = functions[operation[0]](hashmap, index, *operation[1:])
        clock.tick(speed)
        check_user_input()

    clock.tick(speed)
    draw_hashmap(screen, hashmap)

    return hashmap

def visualise_hashmap(screen:Surface, algorithm:str, speed_slider:callable) -> None:
    speed = (speed_slider() // SPEED_SCALE) + 1 # +1 Prevents Speed = 0

    hashmap = [None] * HASHMAP_SIZE

    draw_hashmap(screen, hashmap)

    try:
        hashmap = probing(screen, algorithm, speed, hashmap)
        pygame.display.update()
        pygame.time.delay(3000)
    except VisualisationAborted:
        print("Visualisation Aborted.")