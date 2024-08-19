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
        "Selection Sort Max",
        "Selection Sort Min",
        "Insertion Sort",
        "Shell Sort",
        "Bubble Sort Up",
        "Bubble Sort Down",
        "Cocktail Sort",        
        "Merge Sort",
        "Quick Sort",
        "3-Way Quick Sort",
        "Heap Sort",
        "Counting Sort",
        "Radix Sort",
        "Bogo Sort",
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