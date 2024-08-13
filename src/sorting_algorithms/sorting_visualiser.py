import pygame, sys, random
from pygame import Surface
from config import SCREEN_SIZE, WHITE, NAVY, RED, GREEN, VisualisationAborted

# Initialise pygame
pygame.init()
clock = pygame.time.Clock()

unsorted_data = [36,45,81,40,12,75,77,48,52,49,78,17,33,98,38,42,2,86,59,85,94,20,53,60,67,9,29,89,37,21,88,57,100,10,1,64,51,8,18,35,70,41,84,5,80,63,96,72,13,83,23,71,50,69,11,79,14,66,65,73,22,54,19,43,58,74,4,15,97,6,7,26,87,39,68,82,28,99,76,31,3,90,93,16,46,30,56,91,92,34,55,47,32,95,44,61,27,62,24,25]

# Bar properties
n = len(unsorted_data)
max_height = max(unsorted_data)
HEIGHT_AMPLIFIER = SCREEN_SIZE[1] // max_height
BAR_WIDTH = SCREEN_SIZE[0] // n

# Display Data
def render_bars(bar_data:list[int], highlight:set[int]=set(), highlight_colour:tuple[int, int, int]=RED) -> None:
    screen.fill(NAVY)

    for index in range(len(bar_data)):
        height = bar_data[index] * HEIGHT_AMPLIFIER
        bar_x_offset = BAR_WIDTH * index
        colour = highlight_colour if index in highlight else WHITE

        # Render Bar
        pygame.draw.rect(screen, colour, (bar_x_offset, SCREEN_SIZE[1] - height, BAR_WIDTH, height))

    pygame.display.update()

def comparison(bar_data:list[int]=None, highlight:set[int]=set(), highlight_colour:tuple[int, int, int]=RED) -> None:
    clock.tick(comparisons_per_second)

    for event in pygame.event.get():
        # Handle Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Backout to Menu
            if event.key==pygame.K_BACKSPACE:
                raise VisualisationAborted

    if bar_data: render_bars(bar_data, highlight, highlight_colour)

# Sorting Algorithms
def selection_sort_min(data:list[int]) -> None:
    for i in range(len(data) - 1):
        minimum = i
        for j in range(i + 1, len(data)):
            comparison()
            if data[j] < data[minimum]:
                minimum = j
        data[i], data[minimum] = data[minimum], data[i]
        comparison(data, set([i, minimum]))

def selection_sort_max(data:list[int]) -> None:
    for i in range(len(data) - 1, 0, -1):
        maximum = i
        for j in range(i):
            comparison()
            if data[j] > data[maximum]:
                maximum = j
        data[i], data[maximum] = data[maximum], data[i]
        comparison(data, set([i, maximum]))

def bogo_sort(data:list[int]) -> None:
    complete = False
    while not complete:
        complete = True
        for i in range(len(data) - 1):
            comparison()
            if data[i] > data[i+1]:
                complete = False
                break
        if not complete: random.shuffle(data)
        comparison(data)

def insertion_sort(data:list[int]) -> None:
    for i in range(1, len(data)):
        key, index = data[i], i
        while index > 0 and key < data[index - 1]:
            data[index] = data[index - 1]
            comparison(data, set([index, index-1]))
            index -= 1
        data[index] = key
        comparison(data, set([index]))

def bubble_sort_bottom_to_top(data:list[int]) -> None:
    complete = False
    inplace = 0
    while not complete:
        complete = True
        for i in range(len(data) - 1 - inplace):
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                comparison(data, set([i, i + 1]))
                complete = False
            else:
                comparison()
        inplace += 1

def bubble_sort_top_to_bottom(data:list[int]) -> None:
    complete = False
    inplace = 0
    while not complete:
        complete = True
        for i in range(len(data) - 1, inplace, -1):
            if data[i] < data[i - 1]:
                data[i], data[i - 1] = data[i - 1], data[i]
                comparison(data, set([i, i - 1]))
                complete = False
            else:
                comparison()
        inplace += 1

def cocktail_shaker(data:list[int]) -> None:
    complete = False
    inplace_top = 0
    inplace_bottom = 0
    while not complete:
        complete = True

        for i in range(inplace_bottom, len(data) - 1 - inplace_top):
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                comparison(data, set([i, i + 1]))
                complete = False
            else:
                comparison()

        inplace_top += 1

        for i in range(len(data) - 1 - inplace_top, inplace_bottom, -1):
            if data[i] < data[i - 1]:
                data[i], data[i - 1] = data[i - 1], data[i]
                comparison(data, set([i, i - 1]))
                complete = False
            else:
                comparison()

        inplace_bottom += 1

def quick_sort(data:list[int], low:int=0, high:int=len(unsorted_data) - 1) -> None:
    if low < high:
        pivot = partition(data,low,high)
        quick_sort(data, low, pivot - 1)
        quick_sort(data, pivot + 1, high)

def partition(data:list[int], low:int, high:int) -> int:
    pivot = data[high]
    i, j = low, low
    while j < high:
        if data[j] < pivot:
            data[j], data[i] = data[i], data[j]
            comparison(data, set([i, j]))
            i += 1
        else:
            comparison()
        j += 1
    data[i], data[high] = data[high], data[i]
    comparison(data, set([i, high]))
    return i

def dutch_quick_sort(data:list[int], low:int=0, high:int=len(unsorted_data) - 1) -> None:
    if low < high:
        bottom, top = dutch_partition(data,low,high)
        dutch_quick_sort(data, low, bottom - 1)
        dutch_quick_sort(data, top, high)

def dutch_partition(data:list[int], low:int, high:int) -> tuple[int, int]:
    pivot = data[high]
    i, j, k = low, low, low
    while i < high:
        val = data[i]
        if val < pivot:
            data[k], data[i] = data[i], data[k]
            comparison(data, set([i, k]))
            k += 1
            j += 1
        elif val == pivot:
            data[j], data[i] = data[i], data[j]
            comparison(data, set([i, j]))
            j += 1
        else:
            comparison()
        i += 1
    data[j], data[high] = data[high], data[j]
    comparison(data, set([j, high]))
    return k, j

def merge_sort(data:list[int], low:int=0, high:int=len(unsorted_data) - 1) -> None:
    if low < high:
        mid = (low + high) // 2
        merge_sort(data, low, mid)
        merge_sort(data, mid + 1, high)
        merge(data, low, mid, high)

def merge(data:list[int], low:int, mid:int, high:int) -> None:
    l = data[low:mid+1]
    r = data[mid+1:high+1]
    l.append(float("inf"))
    r.append(float("inf"))
    index = low
    l_count, r_count = 0, 0
    while index <= high:
        if l[l_count] <= r[r_count]:
            data[index] = l[l_count]
            comparison(data, set([index, l_count]))
            l_count += 1
        else:
            data[index] = r[r_count]
            comparison(data, set([index, r_count]))
            r_count += 1
        index += 1

def counting_sort(data:list[int]) -> None:
    count = [0] * (max(data) + 1)
    for num in data:
        comparison()
        count[num] += 1
    total = 0
    for index, num in enumerate(count):
        comparison()
        total += num
        count[index] = total
    output = data[:]
    for index in range(len(data) - 1, -1, -1):
        num = data[index]
        output[count[num] - 1] = num
        count[num] = count[num] - 1
        comparison(output, set([count[num]]))
    global sorting_data
    sorting_data = output

def radix_sort(data:list[int]) -> None:
    biggest = max(data)
    digits = len(str(biggest))
    for digit in range(digits - 1, -1, -1):
        data = digit_counting_sort(data, digit, digits)
    global sorting_data
    sorting_data = data
        
def digit_counting_sort(data:list[int], digit:int, digits:int) -> list[int]:
    count = [0] * 10
    for num in data:
        comparison()
        count[int(str(num).rjust(digits, "0")[digit])] += 1
    total = 0
    for index, num in enumerate(count):
        comparison()
        total += num
        count[index] = total
    output = data[:]
    for index in range(len(data) - 1, -1, -1):
        num = data[index]
        num_digit = int(str(num).rjust(digits, "0")[digit])
        output[count[num_digit] - 1] = num
        count[num_digit] = count[num_digit] - 1
        comparison(output, set([count[num_digit]]))
    return output

def shell_sort(data:list[int]) -> None:
    n = len(data)
    gap = n // 3
    
    while gap > 0:
        
        for i in range(gap, n):
            key, index = data[i], i
            while index >= gap and key < data[index - gap]:
                data[index] = data[index - gap]
                comparison(data, set([index, index-gap]))
                index -= gap
            data[index] = key
            comparison(data, set([index]))
        
        gap //= 3

def heap_sort(data:list[int]) -> None:

    def left(index:int) -> int:
        return (2 * index) + 1

    def right(index:int) -> int:
        return (2 * index) + 2

    def build_max_heap(data:list[int]) -> None:
        for index in range(len(data) // 2 - 1, -1, -1):
            max_heapify(data, index, len(data))

    def max_heapify(data:list[int], index:int, max_index:int) -> None:
        l, r, largest = left(index), right(index), index
        if l < max_index and data[l] > data[largest]:
            largest = l
        if r < max_index and data[r] > data[largest]:
            largest = r
        if largest != index:
            data[index], data[largest] = data[largest], data[index]
            comparison(data, set([index, largest]))
            max_heapify(data, largest, max_index)
        else:
            comparison()

    build_max_heap(data)

    for index in range(len(data) - 1, 0, -1):
        data[0], data[index] = data[index], data[0]
        comparison(data, set([0, index]))
        max_heapify(data, 0, index)

# Map from Menu Buttons to Functions
algorithms = {
        "Bogo Sort" : bogo_sort,
        "Cocktail Sort" : cocktail_shaker,
        "Bubble Sort Up" : bubble_sort_bottom_to_top,
        "Bubble Sort Down" : bubble_sort_top_to_bottom,
        "Insertion Sort" : insertion_sort,
        "Selection Sort Max" : selection_sort_max,
        "Selection Sort Min" : selection_sort_min,
        "Merge Sort" : merge_sort,
        "Quick Sort" : quick_sort,
        "Radix Sort" : radix_sort,
        "Counting Sort" : counting_sort,
        "Shell Sort" : shell_sort,
        "3-Way Quick Sort" : dutch_quick_sort,
        "Heap Sort" : heap_sort,
    }

def run_sorting_algorithm(user_screen:Surface, algorithm:str, speed_slider:callable) -> None:
    global screen, comparisons_per_second, sorting_data
    screen = user_screen
    comparisons_per_second = speed_slider()
    
    try:
        # Run Visualisation
        sorting_data = unsorted_data[:]
        render_bars(sorting_data)
        algorithms[algorithm](sorting_data)
        # Show Completed Visual in Green
        render_bars(sorting_data, set(list(range(len(sorting_data)))), GREEN)
        pygame.time.delay(1000)
        
    except VisualisationAborted:
        print("Visualisation Aborted.")

if __name__ == '__main__':
    algorithm = ""
    while algorithm.title() not in algorithms:
        algorithm = input(f"Choose an Algorithm {list(algorithms.keys())}:")
    run_sorting_algorithm(algorithm.title())