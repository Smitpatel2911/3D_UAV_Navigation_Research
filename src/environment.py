from random import randint
from math import sqrt
from typing import Dict, Tuple, List, Set

# Type Aliases for the whole project
Node3D = Tuple[int, int, int]
Graph = Dict[Node3D, Dict[Node3D, float]]

class DroneAirspaceSimulation:
    def __init__(self, width: int, length: int, height: int):
        self.width = width
        self.length = length
        self.height = height
        self.total_nodes = width * length * height
        self.obstacles: Set[Node3D] = set()

    def inject_obstacles(self, density_percentage: int) -> None:
        """Randomly blocks nodes to act as buildings/no-fly zones."""
        num_obstacles = int(self.total_nodes * (density_percentage / 100.0))
        
        while len(self.obstacles) < num_obstacles:
            x, y, z = randint(0, self.width - 1), randint(0, self.length - 1), randint(0, self.height - 1)
            self.obstacles.add((x, y, z))

    def _get_weighted_neighbors(self, node: Node3D) -> List[Tuple[Node3D, float]]:
        """Finds valid moves in all 26 directions (up, down, diagonal) and calculates flight cost."""
        x, y, z = node
        valid_moves = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue 
                        
                    nx, ny, nz = x + dx, y + dy, z + dz
                    
                    if (0 <= nx < self.width and 
                        0 <= ny < self.length and 
                        0 <= nz < self.height and 
                        (nx, ny, nz) not in self.obstacles):
                        
                        edge_weight = sqrt(dx**2 + dy**2 + dz**2)
                        valid_moves.append(((nx, ny, nz), edge_weight))
                        
        return valid_moves

    def build_graph(self) -> Graph:
        """Builds the actual graph dictionary. Only saves open air, ignores obstacles."""
        adjacency_list: Graph = {}
        for x in range(self.width):
            for y in range(self.length):
                for z in range(self.height):
                    current_node = (x, y, z)
                    
                    if current_node in self.obstacles:
                        continue 
                    
                    neighbors = self._get_weighted_neighbors(current_node)
                    adjacency_list[current_node] = {neighbor: weight for neighbor, weight in neighbors}
                    
        return adjacency_list