# Screen Values
SCREEN_SIZE = (800, 600)
BORDER = 10

# RGB Colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 127, 127)
BLACK = (0, 0, 0)
NAVY = (0, 0, 50)
GREY = (100, 100, 100)

# Visualisations: { Submenu : [Visuals] }
VISUALISATIONS = {
    "Sorting Algorithms" : [
        "Bogo Sort",
        "Cocktail Sort",
        "Bubble Sort Up",
        "Bubble Sort Down",
        "Insertion Sort",
        "Selection Sort Max",
        "Selection Sort Min",
        "Merge Sort",
        "Quick Sort",
        "Radix Sort",
        "Counting Sort",
        "Shell Sort",
        "3-Way Quick Sort",
        "Heap Sort",
    ],
    "Binary Tree Traversals" : [
        "Inorder",
        "Preorder",
        "Postorder",
        "Breadth First Search",
        "Boundary",
    ],
    "Graph Traversals" : [
        "Breadth First Search",
        "Depth First Search",
        "Djkstra's",
        "Bellman Ford",
        "A*",
    ],
    "Hashmaps" : [
        "Chaining",
        "Linear Probing",
        "Quadratic Probing",
        "Double Hashing",
    ],
    "Miscellaneous" : [
        "Binary Search",
    ],
}

class VisualisationAborted(Exception): pass