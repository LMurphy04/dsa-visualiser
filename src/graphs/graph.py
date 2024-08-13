import pygame, sys
from pygame import Surface
from config import VisualisationAborted, WHITE, NAVY, GREEN, RED
from utils.components import GraphNode
from utils.text import draw_multiline_text
from graphs.graph_structure import node_locations, edges

pygame.init()
clock = pygame.time.Clock()

SPEED_SCALE = 30
NODE_SIZE = 20

def initialise_graph(screen:Surface) -> tuple[GraphNode, GraphNode]:
    screen.fill(NAVY)
    
    nodes = [GraphNode(position, NODE_SIZE) for position in node_locations]

    for from_node, to_node, weight in edges:
        nodes[from_node].add_edge(nodes[to_node], weight)

    for node in nodes:
        node.draw(screen, WHITE)
        for edge in node.edges:
            pygame.draw.line(screen, WHITE, node.position, edge[0].position)

    return nodes[0], nodes[16]

def highlight_path(screen:Surface, path:list[GraphNode], tail_colour:tuple[int, int, int], head_colour:tuple[int, int, int]):
    for node in path[:-1]:
        node.draw(screen, tail_colour)
    path[-1].draw(screen, head_colour)

def bfs(screen:Surface, speed:int, start:GraphNode, end:GraphNode):
    visited = set()
    to_visit = [[start]]

    while to_visit:
        clock.tick(speed)

        # Get Path to Check
        checking_path = to_visit.pop(0)

        # Check if End has Been Found and Highlight
        if checking_path[-1] == end:
            highlight_path(screen, checking_path, GREEN, GREEN)
            return None
        
        # Highlight Path Being Checked
        highlight_path(screen, checking_path, (100, 30, 30), RED)
        pygame.display.update()

        # Remove Highlight
        highlight_path(screen, checking_path, WHITE, WHITE)

        # Get Next Steps
        for connected, weight in checking_path[-1].edges:
            if connected not in visited:
                to_visit.append([*checking_path, connected])

        # Add Current Node to Visited
        visited.add(checking_path[-1])

def dfs(screen:Surface, speed:int, start:GraphNode, end:GraphNode, path:list[GraphNode]=None, visited:set[GraphNode]=set()):
    clock.tick(speed)
    if path == None: path = [start]

    # Check if End has Been Found and Highlight
    if path[-1] == end:
        highlight_path(screen, path, GREEN, GREEN)
        return None
    
    # Highlight Path Being Checked
    highlight_path(screen, path, (100, 30, 30), RED)
    pygame.display.update()

    # Remove Highlight
    highlight_path(screen, path, WHITE, WHITE)

    visited.add(path[-1])

    # Get Next Steps
    for connected, weight in path[-1].edges:
        if connected not in visited:
            dfs(screen, speed, start, end, [*path, connected], visited)

def djkstra(screen:Surface, speed:int, start:GraphNode, end:GraphNode):
    pass

def bellman_ford(screen:Surface, speed:int, start:GraphNode, end:GraphNode):
    pass

def A_star(screen:Surface, speed:int, start:GraphNode, end:GraphNode):
    pass

# Map from Menu Buttons to Functions
algorithms = {
        "Breadth First Search": bfs,
        "Depth First Search": dfs,
        "Djkstra's": djkstra,
        "Bellman Ford": bellman_ford,
        "A*": A_star,
    }

def visualise_graph(screen:Surface, algorithm:str, speed_slider:callable) -> None:
    speed = (speed_slider() // SPEED_SCALE) + 1 # +1 Prevents Speed = 0

    start, end = initialise_graph(screen)

    try:
        algorithms[algorithm](screen, speed, start, end)
        clock.tick(speed)
        pygame.display.update()
        pygame.time.delay(3000)
    except VisualisationAborted:
        print("Visualisation Aborted.")