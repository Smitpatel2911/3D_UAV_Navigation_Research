from csv import writer
from random import choice
from environment import DroneAirspaceSimulation
from algorithms import run_dijkstra, run_a_star
from profiler import benchmark_algorithm

def run_stress_tests(output_filename: str = "data/drone_navigation_results.csv") -> None:
    """Runs the whole pipeline and saves the data to a CSV."""
    grid_sizes = [(20, 20, 10), (30, 30, 15), (50, 50, 20)]
    obstacle_densities = [5, 15, 25]
    trials_per_configuration = 5
    
    print(f"Initializing 3D Benchmarking Suite. Output: {output_filename}\n")
    
    with open(output_filename, mode='w', newline='') as file:
        csv_writer = writer(file)
        csv_writer.writerow(['Graph_Nodes', 'Obstacle_Density_Pct', 'Trial_ID', 
                             'Algorithm', 'Runtime_ms', 'Peak_Memory_MB', 'Nodes_Evaluated', 'Path_Found'])
        
        for width, length, height in grid_sizes:
            total_nodes = width * length * height
            
            for density in obstacle_densities:
                print(f"Testing Array: {total_nodes} Nodes | {density}% Obstacle Density")
                
                for trial in range(1, trials_per_configuration + 1):
                    # 1. Setup the map from environment.py
                    sim = DroneAirspaceSimulation(width, length, height)
                    sim.inject_obstacles(density)
                    graph = sim.build_graph()
                    
                    valid_nodes = list(set(graph.keys()) - sim.obstacles)
                    if len(valid_nodes) < 2:
                        continue 
                        
                    start_node, target_node = choice(valid_nodes), choice(valid_nodes)
                    while target_node == start_node:
                        target_node = choice(valid_nodes)
                    
                    # 2. Race Dijkstra using algorithms.py and profiler.py
                    d_time, d_mem, d_eval = benchmark_algorithm(run_dijkstra, graph, start_node, target_node, "Dijkstra")
                    d_path_found = d_eval > 0 and d_time > 0
                    csv_writer.writerow([total_nodes, density, trial, "Dijkstra", 
                                         round(d_time, 4), round(d_mem, 6), d_eval, d_path_found])
                    
                    # 3. Race A* using algorithms.py and profiler.py
                    a_time, a_mem, a_eval = benchmark_algorithm(run_a_star, graph, start_node, target_node, "A*")
                    a_path_found = a_eval > 0 and a_time > 0
                    csv_writer.writerow([total_nodes, density, trial, "A*", 
                                         round(a_time, 4), round(a_mem, 6), a_eval, a_path_found])
                                         
    print(f"\nBenchmarking Phase Complete. Data saved to {output_filename}.")

if __name__ == "__main__":
    run_stress_tests()