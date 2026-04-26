import heapq

import graphs
import settings

def get_edge_weight(node1, node2):
    """
    Helper function to get the weight of the edge between two nodes.
    Returns the weight if an edge exists, otherwise returns infinity.
    """
    for edge in node1.edges:
        if (edge.node1 == node1 and edge.node2 == node2) or (edge.node1 == node2 and edge.node2 == node1):
            return edge.value
    return float('inf')

def dijkstra(start_node, end_node):
    """
    Implements Dijkstra's algorithm to find the shortest path between start_node and end_node.
    
    Dijkstra's algorithm is a greedy algorithm that finds the shortest path from a source node
    to all other nodes in a graph with non-negative edge weights. It uses a priority queue
    to always explore the node with the currently known shortest distance.
    
    Parameters:
    start_node: The starting node for the path
    end_node: The target node for the path
    
    Returns:
    A tuple containing:
    - The shortest distance from start_node to end_node (or float('inf') if no path exists)
    - The shortest path as a list of nodes from start_node to end_node (or None if no path exists)
    """
    
    # Step 1: Initialize distances and previous nodes
    # distances will store the shortest distance from start_node to each node
    distances = {node: float('inf') for node in graphs.get_all_nodes()}
    distances[start_node] = 0
    
    # previous will store the previous node in the shortest path
    previous = {node: None for node in graphs.get_all_nodes()}
    
    # Priority queue to store (distance, counter, node) tuples
    # We use a min-heap where the smallest distance is always at the front
    # The counter acts as a tiebreaker when distances are equal, preventing comparison of Node objects
    priority_queue = [(0, 0, start_node)]  # (distance, counter, node)
    counter = 0
    
    # Set to keep track of visited nodes to avoid re-processing
    visited = set()
    
    while priority_queue:
        # Step 2: Get the node with the smallest distance from the priority queue
        current_distance, _, current_node = heapq.heappop(priority_queue)
        
        # If we've already visited this node with a better distance, skip it
        if current_node in visited:
            continue
        
        # Mark the current node as visited
        visited.add(current_node)
        
        # If we've reached the end node, we can stop early
        if current_node == end_node:
            break
        
        # Step 3: Explore all neighbors of the current node
        for neighbor in graphs.get_neighbors(current_node):
            if neighbor in visited:
                continue
            
            # Calculate the weight of the edge to this neighbor
            edge_weight = get_edge_weight(current_node, neighbor)
            
            # Skip if there's no edge (infinite weight)
            if edge_weight == float('inf'):
                continue
            
            # Calculate the new distance to this neighbor through the current node
            new_distance = current_distance + edge_weight
            
            # If this new distance is shorter than the previously known distance
            if new_distance < distances[neighbor]:
                # Update the distance
                distances[neighbor] = new_distance
                # Update the previous node for path reconstruction
                previous[neighbor] = current_node
                # Increment counter for heap tiebreaker
                counter += 1
                # Add this neighbor to the priority queue with the new distance
                heapq.heappush(priority_queue, (new_distance, counter, neighbor)) #type: ignore
    
    # Step 4: Reconstruct the shortest path
    if distances[end_node] == float('inf'):
        # No path exists
        return float('inf'), []
    
    # Reconstruct the path by backtracking from end_node to start_node
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = previous[current]
    
    # Reverse the path so it goes from start to end
    path.reverse()
    
    # Return the shortest distance and the path
    return distances[end_node], path
   