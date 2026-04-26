import draw_basic
import settings
import pygame
import math

class Node():
    def __init__(self, name: str, x, y):
        self.name = name
        self.edges = []
        self.x = x
        self.y = y
    
    def add_edge(self, edge):
        self.edges.append(edge)
    
    def draw(self, screen, start_end_nodes, path):
        if self in start_end_nodes:
            color = settings.NODE_START_END_NODE_COLOR
        elif self in path:
            color = settings.NODE_PATH_COLOR
        else:
            color = settings.NODE_COLOR
        draw_basic.draw_circle(screen, color, (int(self.x), int(self.y)), settings.NODE_SIZE)
        font = pygame.font.SysFont("Arial", settings.NODE_SIZE)
        draw_basic.draw_text(screen, self.x, self.y, 0, 0, settings.EDGE_COLOR, font, str(self.name))

    def set_position(self, x, y):
        self.x = x
        self.y = y

class Edge():
    def __init__(self, node1: Node, node2: Node, directed: bool, value: int):
        self.node1 = node1
        self.node2 = node2
        self.directed = directed
        self.value = value
    
    def draw(self, screen, path):
        half_point = ((self.node1.x + self.node2.x) / 2, (self.node1.y + self.node2.y) / 2)

        vx = self.node2.x - self.node1.x
        vy = self.node2.y - self.node1.y

        length = (vx ** 2 + vy ** 2) ** 0.5
        if length == 0:
            # Identical node positions cause division by zero.
            # Skip drawing edge or draw small self-loop.
            return

        delta_distance = settings.NODE_SIZE

        dx = vx / length * delta_distance
        dy = vy / length * delta_distance

        path_edge = [(path[i], path[i+1]) for i in range(len(path)-1)]

        if (self.node1, self.node2) in path_edge or (self.node2, self.node1) in path_edge:
            color = settings.EDGE_PATH_COLOR
        else:
            color = settings.EDGE_COLOR

        draw_basic.draw_line(
            screen, 
            color, 
            (int(half_point[0] - dx), int(half_point[1] - dy)), 
            (int(self.node1.x + dx), int(self.node1.y + dy)), 
            settings.EDGE_SIZE
            )
        
        draw_basic.draw_line(
            screen,
            color,
            (int(half_point[0] + dx), int(half_point[1] + dy)),
            (int(self.node2.x - dx), int(self.node2.y - dy)),
            settings.EDGE_SIZE
            )
        
        font = pygame.font.SysFont("Arial", settings.NODE_SIZE)
        draw_basic.draw_text(screen, int(half_point[0]), int(half_point[1]), 0, 0, settings.EDGE_COLOR, font, str(self.value))

        if self.directed:
            arrow_point = (int(half_point[0] - dx), int(half_point[1] - dy))

            arrow_size = settings.NODE_SIZE
            angle = math.atan2(-vy, -vx)
            arrow_x = int(arrow_point[0] + arrow_size * math.cos(angle + 3.14 / 6))
            arrow_y = int(arrow_point[1] + arrow_size * math.sin(angle + 3.14 / 6))
            draw_basic.draw_line(screen, settings.EDGE_COLOR, (int(arrow_point[0]), int(arrow_point[1])), (arrow_x, arrow_y), settings.EDGE_SIZE)

            arrow_x = int(arrow_point[0] + arrow_size * math.cos(angle - 3.14 / 6))
            arrow_y = int(arrow_point[1] + arrow_size * math.sin(angle - 3.14 / 6))
            draw_basic.draw_line(screen, settings.EDGE_COLOR, (int(arrow_point[0]), int(arrow_point[1])), (arrow_x, arrow_y), settings.EDGE_SIZE)

all_nodes: list[Node] = []
all_edges: list[Edge] = []

def clear_graph():
    """
    Clear all nodes and edges from the current graph.
    """
    all_edges.clear()
    all_nodes.clear()


def create_node(name: str, x = 0, y = 0):
    """
    Create a new node with the given name.
    If a node with the same name exists, return it to avoid duplicates.
    """
    for existing in all_nodes:
        if existing.name == name:
            existing.x = x
            existing.y = y
            return existing

    node = Node(name, x, y)
    all_nodes.append(node)
    return node


def create_edge(node1: Node, node2: Node, directed: bool, value: int):
    """
    Create a new edge between node1 and node2 with the given value.
    If directed is True, the edge will be directed from node1 to node2.
    If directed is False, the edge will be undirected between node1 and node2.
    """
    edge = Edge(node1, node2, directed, value)
    all_edges.append(edge)
    node1.add_edge(edge)
    if not directed:
        node2.add_edge(edge)
    return edge

def get_neighbors(node: Node):
    """
    Get the neighbors of a node.
    """
    neighbors = []
    for edge in node.edges:
        if edge.node1 == node:
            neighbors.append(edge.node2)
        else:
            neighbors.append(edge.node1)
    return neighbors

def get_next_available_name():
    """
    Get the next available name for a new node.
    """
    i = 0
    while True:
        name = str(i)
        if not any(node.name == name for node in all_nodes):
            return name
        i += 1

def get_edge(node1: Node, node2: Node) -> Edge | None:
    """
    Get the edge between node1 and node2.
    """
    for edge in all_edges:
        if (edge.node1 == node1 and edge.node2 == node2) or (edge.node1 == node2 and edge.node2 == node1):
            return edge
    return None

def delete_node(node: Node):
    """
    Delete a node and all its edges.
    """
    edges_to_remove = []
    for edge in all_edges:
        if edge.node1 == node or edge.node2 == node:
            edges_to_remove.append(edge)
    
    for edge in edges_to_remove:
        all_edges.remove(edge)
        other_node = edge.node1 if edge.node1 != node else edge.node2
        if edge in other_node.edges:
            other_node.edges.remove(edge)
    
    all_nodes.remove(node)

def delete_edge(node1: Node, node2: Node):
    """
    Delete the edge between node1 and node2.
    """
    edges_to_remove = []
    for edge in all_edges:
        if (edge.node1 == node1 and edge.node2 == node2) or (edge.node1 == node2 and edge.node2 == node1):
            edges_to_remove.append(edge)
    
    for edge in edges_to_remove:
        all_edges.remove(edge)
        if edge in node1.edges:
            node1.edges.remove(edge)
        if edge in node2.edges:
            node2.edges.remove(edge)

def get_all_nodes():
    """
    Get all the nodes in the graph.
    """
    return all_nodes

def get_all_edges():
    """
    Get all the edges in the graph.
    """
    return all_edges

def is_neighbor(node1: Node, node2: Node):
    """
    Check if node1 and node2 are neighbors.
    """
    for edge in node1.edges:
        if edge.node1 == node2 or edge.node2 == node2:
            return True
    
    for edge in node2.edges:
        if edge.node1 == node1 or edge.node2 == node1:
            return True
    return False

def get_node_by_name(name: str) -> Node:
    """
    Get a node by its name.
    """
    for node in all_nodes:
        if node.name == name:
            return node
        
    raise ValueError(f"No node with name {name} found.")

def get_adjacency_matrix():
    """
    Get the adjacency matrix of the graph 
    taking in consideration if the edge is directed or not.
    """
    nodes = sorted(get_all_nodes(), key=lambda n: n.name)  # Sort nodes by name for consistent ordering
    matrix = [[0] * len(nodes) for _ in range(len(nodes))]

    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            if i == j:
                matrix[i][j] = 0
            else:
                edge = get_edge(node1, node2)
                if edge is not None and (not edge.directed or edge.node1 == node1):
                    matrix[i][j] = edge.value

    return matrix

def print_adjacency_matrix():
    """
    Print the adjacency matrix of the graph, with the name of the nodes.
    """
    matrix = get_adjacency_matrix()
    nodes = sorted(get_all_nodes(), key=lambda n: n.name)  # Sort nodes by name for consistent ordering
    print("        " + " ".join(f"{node.name:5}" for node in nodes))
    print("       " + "-" * (6 * len(nodes)))
    for i, row in enumerate(matrix):
        print(f"{nodes[i].name:3}|" + " ".join(f"{value:5}" for value in row))

def load_graph_from_json(file_path: str):
    """
    Load a graph from a JSON file.
    """
    import json

    # Reset internal state before loading to avoid duplicate nodes/edges.
    clear_graph()

    with open(file_path, 'r') as f:
        data = dict(json.load(f))

    for node_data in data.get("nodes", []):
        create_node(node_data["name"], node_data["x"], node_data["y"])

    for edge_data in data.get("edges", []):
        from_node = get_node_by_name(edge_data["from"])
        to_node = get_node_by_name(edge_data["to"])

        if from_node == to_node:
            # ignore self-loop edges that might come from corrupted JSON
            continue

        existing_edge = get_edge(from_node, to_node)
        if existing_edge is not None:
            # avoid duplicate edges on load
            continue

        create_edge(from_node, to_node, edge_data.get("directed", False), edge_data.get("values", 0))

def save_graph_to_json(file_path: str):
    """
    Save the graph to a JSON file.
    """
    import json
    data = {"nodes": [], "edges": []}

    seen_node_names = set()
    for node in all_nodes:
        if node.name in seen_node_names:
            continue
        seen_node_names.add(node.name)
        data["nodes"].append({"name": node.name, "x": node.x, "y": node.y})

    seen_edges = set()
    for edge in all_edges:
        key = (edge.node1.name, edge.node2.name, edge.directed, edge.value)
        if key in seen_edges:
            continue
        seen_edges.add(key)
        data["edges"].append({"from": edge.node1.name, "to": edge.node2.name, "directed": edge.directed, "values": edge.value})

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def create_json_from_adjacency_matrix(matrix: list[list[int]], node_names: list[str]):
    """
    Create a JSON representation of a graph from an adjacency matrix and node names.
    """
    import json
    data = {"nodes": [], "edges": []}

    for i, name in enumerate(node_names):
        data["nodes"].append({"name": name, "x": 0, "y": 0})

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            if matrix[i][j] != 0:
                data["edges"].append({"from": node_names[i], "to": node_names[j], "directed": True, "values": matrix[i][j]})

    with open("graph_from_matrix.json", 'w') as f:
        json.dump(data, f, indent=4)

