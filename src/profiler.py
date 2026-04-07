from time import perf_counter
from tracemalloc import start, get_traced_memory, stop
from typing import Callable, Tuple
from environment import Node3D, Graph

def benchmark_algorithm(algorithm_func: Callable, graph: Graph, start_node: Node3D, target_node: Node3D, algo_name: str) -> Tuple[float, float, int]:
    """Runs the algorithm and records execution time and peak memory footprint."""
    print(f"  -> Profiling {algo_name}...")
    
    start()  # Start watching RAM
    start_time = perf_counter()
    
    path_cost, nodes_evaluated = algorithm_func(graph, start_node, target_node)
    
    end_time = perf_counter()
    _, peak_memory_bytes = get_traced_memory()
    stop()   # Stop watching RAM
    
    # Convert to readable units (ms and MB)
    runtime_ms = (end_time - start_time) * 1000
    peak_memory_mb = peak_memory_bytes / (1024 * 1024)
    
    return runtime_ms, peak_memory_mb, nodes_evaluated