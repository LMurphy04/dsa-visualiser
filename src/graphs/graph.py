import pygame, sys, math
from pygame import Surface
from config import VisualisationAborted, WHITE, NAVY, GREEN, RED, LIGHT_RED
from utils.components import GraphNode
from utils.text import draw_multiline_text, centered_single_line
from graphs.graph_structure import node_locations, edges

# Initialise pygame
pygame.init()
clock = pygame.time.Clock()

# Visualisation settings
SPEED_SCALE = 30
NODE_SIZE = 20
START_INDEX = 0
END_INDEX = 16

# Create the Graph
nodes = [GraphNode(position, NODE_SIZE) for position in node_locations]
for from_node, to_node, weight in edges:
    nodes[from_node].add_edge(nodes[to_node], weight)

def reset_nodes() -> None:
    for node in nodes:
        node.value = float("inf")
        node.predecessor = None
    nodes[START_INDEX].value = 0

def initialise_graph(screen:Surface, show_value:bool) -> tuple[GraphNode, GraphNode]:
    reset_nodes()

    # Draw Graph
    screen.fill(NAVY)
    centered_single_line(screen, (nodes[START_INDEX].position[0], nodes[START_INDEX].position[1] + 30), "START", 20, WHITE)
    centered_single_line(screen, (nodes[END_INDEX].position[0], nodes[END_INDEX].position[1] - 30), "FINISH", 20, WHITE)  

    for node in nodes:
        node.draw(screen, WHITE, show_value)
        for edge in node.edges:
            pygame.draw.line(screen, WHITE, node.position, edge[0].position)
            if show_value: draw_multiline_text(screen, ((node.position[0] + edge[0].position[0]) // 2, (node.position[1] + edge[0].position[1]) // 2), str(edge[1]), 20, WHITE)

    pygame.display.update()

    return nodes[START_INDEX], nodes[END_INDEX]

def highlight_path(screen:Surface, path:list[GraphNode], tail_colour:tuple[int, int, int], head_colour:tuple[int, int, int], show_values:bool) -> None:
    for index, node in enumerate(path[:-1]):
        node.draw(screen, tail_colour, show_values)
        pygame.draw.line(screen, tail_colour, node.position, path[index+1].position)
    path[-1].draw(screen, head_colour, show_values)

def generate_predecessor_path(node:GraphNode, start:GraphNode) -> list[GraphNode]:
    # Create a list of nodes going from start to node via node predecessors
    path = [node]
    while node != start:
        node = node.predecessor
        path.append(node)
    return path[::-1]

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

# Get node distance from start and end
def get_distance(node:GraphNode, start:GraphNode, end:GraphNode) -> float:
    dist_from_start = math.sqrt(abs(node.position[0] - start.position[0])**2 + abs(node.position[1] - start.position[1])**2)
    dist_from_end = math.sqrt(abs(node.position[0] - end.position[0])**2 + abs(node.position[1] - end.position[1])**2)
    return dist_from_end + dist_from_start 

def bfs(screen:Surface, speed:int, start:GraphNode, end:GraphNode) -> None:
    visited = set()
    to_visit = [[start]]

    while to_visit:
        clock.tick(speed)

        # Get Path to Check
        checking_path = to_visit.pop(0)

        # Check if End has Been Found and Highlight
        if checking_path[-1] == end:
            highlight_path(screen, checking_path, GREEN, GREEN, False)
            return None
        
        # Highlight Path Being Checked
        highlight_path(screen, checking_path, LIGHT_RED, RED, False)
        pygame.display.update()

        # Remove Highlight
        highlight_path(screen, checking_path, WHITE, WHITE, False)

        # Get Next Steps
        for connected, weight in checking_path[-1].edges:
            if connected not in visited:
                to_visit.append([*checking_path, connected])

        # Add Current Node to Visited
        visited.add(checking_path[-1])

        check_user_input()

def dfs(screen:Surface, speed:int, start:GraphNode, end:GraphNode, path:list[GraphNode]=None, visited:set[GraphNode]=None) -> None:
    clock.tick(speed)
    if visited == None: visited = set()
    if path == None: path = [start]

    # Check if End has Been Found and Highlight
    if path[-1] == end:
        highlight_path(screen, path, GREEN, GREEN, False)
        pygame.display.update()
        pygame.time.delay(3000)
        raise VisualisationAborted
    
    # Highlight Path Being Checked
    highlight_path(screen, path, LIGHT_RED, RED, False)
    pygame.display.update()

    # Remove Highlight
    highlight_path(screen, path, WHITE, WHITE, False)

    visited.add(path[-1])
    
    check_user_input()

    # Get Next Steps
    for connected, weight in path[-1].edges:
        if connected not in visited:
            dfs(screen, speed, start, end, [*path, connected], visited)

def djkstra(screen:Surface, speed:int, start:GraphNode, end:GraphNode) -> None:
    visited = set()
    priority_queue = [[start, 0]] #priority queue should be a heap

    while priority_queue:
        # Get Node with Shortest Cost to Start in Queue
        current_node, current_distance = priority_queue.pop(0)

        # If We Haven't Calculated Distances from Node
        if current_node not in visited:
            visited.add(current_node)

            # Check Neighbours
            for connected_node, weight in current_node.edges:
                clock.tick(speed)
                new_dist = weight + current_distance

                # Update Distances if Needed
                if new_dist < connected_node.value:
                    connected_node.value = new_dist
                    connected_node.predecessor = current_node
                    priority_queue.append([connected_node, new_dist])

                path = generate_predecessor_path(connected_node, start)

                highlight_path(screen, path, LIGHT_RED, RED, True)
                pygame.display.update()
                highlight_path(screen, path, WHITE, WHITE, True)

                check_user_input()

        priority_queue.sort(key=lambda x:x[1]) #priority queue should be a heap

    # Highlight Shortest Path
    shortest_path = generate_predecessor_path(end, start)
    highlight_path(screen, shortest_path, GREEN, GREEN, True)

def bellman_ford(screen:Surface, speed:int, start:GraphNode, end:GraphNode) -> None:
    sweep = 1
    updated = True
    
    # check all nodes and update costs n times
    while sweep <= len(nodes) and updated:
        updated = False

        # for every node check every neighbour and check if cost needs update
        for node in nodes:
            for connected_node, weight in node.edges:
                clock.tick(speed)
                new_dist = weight + node.value

                if new_dist < connected_node.value:
                    connected_node.value = new_dist
                    connected_node.predecessor = node
                    updated = True

                highlight_path(screen, [connected_node, node], LIGHT_RED, RED, True)
                pygame.display.update()
                highlight_path(screen, [connected_node, node], WHITE, WHITE, True)

                check_user_input()

        sweep += 1

    # if costs were updated on the nth sweep a negative cycle was found
    if updated:
        print("Negative Cycle Found!")
    else:
        # Highlight Shortest Path
        shortest_path = generate_predecessor_path(end, start)
        highlight_path(screen, shortest_path, GREEN, GREEN, True) 

def A_star(screen:Surface, speed:int, start:GraphNode, end:GraphNode) -> None:
    has_been_in_queue = set([start])
    priority_queue = [[start, get_distance(start, start, end)]] #priority queue should be a heap

    while priority_queue:
        clock.tick(speed)

        # Get current node and highlight path
        current_node, current_distance = priority_queue.pop(0)
        path = generate_predecessor_path(current_node, start)
        highlight_path(screen, path, LIGHT_RED, RED, False)
        pygame.display.update()
        highlight_path(screen, path, WHITE, WHITE, False)

        # Add neighbours to queue whilst checking for goal
        for connected_node, weight in current_node.edges:
            if connected_node not in has_been_in_queue:
                has_been_in_queue.add(connected_node)
                connected_node.predecessor = current_node
                if connected_node == end:
                    path = generate_predecessor_path(end, start)
                    highlight_path(screen, path, GREEN, GREEN, False)
                    pygame.display.update()
                    return None
                priority_queue.append([connected_node, get_distance(connected_node, start, end)])
        
        check_user_input()
        priority_queue.sort(key=lambda x:x[1]) #priority queue should be a heap

# Map from Menu Buttons to Functions and whether node values should be shown
algorithms = {
        "Breadth First Search": (bfs, False),
        "Depth First Search": (dfs, False),
        "Djkstra's": (djkstra, True),
        "Bellman Ford": (bellman_ford, True),
        "A*": (A_star, False),
    }

def visualise_graph(screen:Surface, algorithm:str, speed_slider:callable) -> None:
    speed = (speed_slider() // SPEED_SCALE) + 1 # +1 Prevents Speed = 0

    algorithm_info = algorithms[algorithm]
    start, end = initialise_graph(screen, algorithm_info[1])

    try:
        algorithm_info[0](screen, speed, start, end)
        pygame.display.update()
        pygame.time.delay(3000)
    except VisualisationAborted:
        print("Visualisation Aborted.")