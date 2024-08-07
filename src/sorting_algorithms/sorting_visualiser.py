import pygame
import random

pygame.init()
clock = pygame.time.Clock()
comparisons_per_second = 120

#rgb colours
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#screen properties
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

unsorted_data = [36,45,81,40,12,75,77,48,52,49,78,17,33,98,38,42,2,86,59,85,94,20,53,60,67,9,29,89,37,21,88,57,100,10,1,64,51,8,18,35,70,41,84,5,80,63,96,72,13,83,23,71,50,69,11,79,14,66,65,73,22,54,19,43,58,74,4,15,97,6,7,26,87,39,68,82,28,99,76,31,3,90,93,16,46,30,56,91,92,34,55,47,32,95,44,61,27,62,24,25]

#bar properties
n = len(unsorted_data)
max_height = max(unsorted_data)
HEIGHT_AMPLIFIER = SCREEN_HEIGHT // max_height
BAR_WIDTH = SCREEN_WIDTH // n

"""
DISPLAY DATA AS BARS
"""
def render_bars(bar_data:list, highlight:set=set(), highlight_colour:tuple=RED):
    screen.fill(BLACK)
    for i in range(len(bar_data)):
        height = bar_data[i] * HEIGHT_AMPLIFIER
        bar_x_offset = BAR_WIDTH * i

        if i in highlight:
            colour = highlight_colour
        else:
            colour = WHITE

        pygame.draw.rect(screen, colour, (bar_x_offset, SCREEN_HEIGHT - height, BAR_WIDTH, height))
    pygame.display.update()

def comparison(bar_data:list=None, highlight:set=set(), highlight_colour:tuple=RED):
    clock.tick(comparisons_per_second)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if bar_data:
        render_bars(bar_data, highlight, highlight_colour)

"""
SORTING ALGORITHMS
"""
def selection_sort_min(data):
    for i in range(len(data) - 1):
        minimum = i
        for j in range(i + 1, len(data)):
            comparison()
            if data[j] < data[minimum]:
                minimum = j
        data[i], data[minimum] = data[minimum], data[i]
        comparison(data, set([i, minimum]))

def selection_sort_max(data):
    for i in range(len(data) - 1, 0, -1):
        maximum = i
        for j in range(i):
            comparison()
            if data[j] > data[maximum]:
                maximum = j
        data[i], data[maximum] = data[maximum], data[i]
        comparison(data, set([i, maximum]))

def bogo_sort(data):
    complete = False
    while not complete:
        complete = True
        for i in range(len(data) - 1):
            comparison()
            if data[i] > data[i+1]:
                complete = False
                break
        if not complete: random.shuffle(data)
        comparison(data, delay=0)

def insertion_sort(data):
    for i in range(1, len(data)):
        key, index = data[i], i
        while index > 0 and key < data[index - 1]:
            data[index] = data[index - 1]
            comparison(data, set([index, index-1]))
            index -= 1
        data[index] = key
        comparison(data, set([index]))

def bubble_sort_bottom_to_top(data):
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

def bubble_sort_top_to_bottom(data):
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

def cocktail_shaker(data):
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

def quick_sort(data, low=0, high=len(unsorted_data) - 1):
    if low < high:
        pivot = partition(data,low,high)
        quick_sort(data, low, pivot - 1)
        quick_sort(data, pivot + 1, high)

def partition(data, low, high):
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

def merge_sort(data, low=0, high=len(unsorted_data) - 1):
    if low < high:
        mid = (low + high) // 2
        merge_sort(data, low, mid)
        merge_sort(data, mid + 1, high)
        merge(data, low, mid, high)

def merge(data, low, mid, high):
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

def counting_sort(data):
    count = [0] * (max(data) + 1)
    for num in data:
        count[num] += 1
    total = 0
    for index, num in enumerate(count):
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

def radix_sort(data):
    biggest = max(data)
    digits = len(str(biggest))
    for digit in range(digits - 1, -1, -1):
        data = digit_counting_sort(data, digit, digits)
    global sorting_data
    sorting_data = data
        
def digit_counting_sort(data, digit, digits):
    count = [0] * 10
    for num in data:
        count[int(str(num).rjust(digits, "0")[digit])] += 1
    total = 0
    for index, num in enumerate(count):
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

def shell_sort(data):
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

"""
MAIN SORTING ALGORITHM VISUALISER FUNCTION
"""

algorithms = {
        "Bogo" : bogo_sort,
        "Cocktail" : cocktail_shaker,
        "Bubble Up" : bubble_sort_bottom_to_top,
        "Bubble Down" : bubble_sort_top_to_bottom,
        "Insertion" : insertion_sort,
        "Selection Max" : selection_sort_max,
        "Selection Min" : selection_sort_min,
        "Merge" : merge_sort,
        "Quick" : quick_sort,
        "Radix" : radix_sort,
        "Counting" : counting_sort,
        "Shell" : shell_sort,
    }

def run_sorting_algorithm(user_screen, algorithm:str=None, speed:int=120):
    global screen, comparisons_per_second, sorting_data
    screen = user_screen
    comparisons_per_second = speed
    
    sorting_data = unsorted_data[:]
    render_bars(sorting_data)
    algorithms[algorithm](sorting_data)
    print(sorting_data)
    render_bars(sorting_data, set(list(range(len(sorting_data)))), GREEN)
    pygame.time.delay(1000)

if __name__ == '__main__':
    algorithm = input(f"Choose an Algorithm {list(algorithms.keys())}:")
    while algorithm.title() not in algorithms:
        algorithm = input(f"Choose an Algorithm {list(algorithms.keys())}:")
    run_sorting_algorithm(algorithm.title())