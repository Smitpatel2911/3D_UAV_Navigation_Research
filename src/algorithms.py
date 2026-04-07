from math import sqrt
from heapq import heappush, heappop
from typing import Tuple, List, Dict
from environment import Node3D, Graph  # Importing your custom types

def calculate_euclidean_distance(node: Node3D, target: Node3D) -> float:
    """Simple 3D Euclidean distance math to act as our A* heuristic."""
    return sqrt((node[0] - target[0])**2 + 
                (node[1] - target[1])**2 + 
                (node[2] - target[2])**2)

def run_dijkstra(graph: Graph, start_node: Node3D, target_node: Node3D) -> Tuple[float, int]:
    """Standard Dijkstra implementation. Expands uniformly in all directions."""
    open_list: List[Tuple[float, Node3D]] = [(0.0, start_node)]
    accumulated_costs: Dict[Node3D, float] = {start_node: 0.0}
    nodes_evaluated = 0

    while open_list:
        current_cost, current_node = heappop(open_list)
        nodes_evaluated += 1

        if current_node == target_node:
            break

        if current_cost > accumulated_costs.get(current_node, float('inf')):
            continue

        for neighbor, edge_weight in graph.get(current_node, {}).items():
            new_cost = current_cost + edge_weight
            if new_cost < accumulated_costs.get(neighbor, float('inf')):
                accumulated_costs[neighbor] = new_cost
                heappush(open_list, (new_cost, neighbor))
                
    return accumulated_costs.get(target_node, float('inf')), nodes_evaluated

def run_a_star(graph: Graph, start_node: Node3D, target_node: Node3D) -> Tuple[float, int]:
    """A* implementation guided by the Euclidean heuristic."""
    initial_heuristic = calculate_euclidean_distance(start_node, target_node)
    open_list: List[Tuple[float, float, Node3D]] = [(initial_heuristic, 0.0, start_node)]
    accumulated_costs: Dict[Node3D, float] = {start_node: 0.0}
    nodes_evaluated = 0

    while open_list:
        _, current_cost, current_node = heappop(open_list)
        nodes_evaluated += 1

        if current_node == target_node:
            break

        if current_cost > accumulated_costs.get(current_node, float('inf')):
            continue

        for neighbor, edge_weight in graph.get(current_node, {}).items():
            new_cost = current_cost + edge_weight
            
            if new_cost < accumulated_costs.get(neighbor, float('inf')):
                accumulated_costs[neighbor] = new_cost
                estimated_total_cost = new_cost + calculate_euclidean_distance(neighbor, target_node)
                heappush(open_list, (estimated_total_cost, new_cost, neighbor))
                
    return accumulated_costs.get(target_node, float('inf')), nodes_evaluated