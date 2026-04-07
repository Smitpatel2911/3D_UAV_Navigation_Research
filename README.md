# 🚁 3D UAV Pathfinding: A* vs. Dijkstra on Edge Hardware

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Overview
Autonomous Unmanned Aerial Vehicles (UAVs) face severe physical hardware limitations. Standard onboard flight controllers (e.g., Pixhawk series) frequently possess only ~1 MB of internal RAM. This project is a custom 3D spatial simulation designed to benchmark pathfinding algorithms strictly within these edge-computing constraints. 

It directly compares the **A* (A-star) algorithm** (using a 3D Euclidean heuristic) against **Dijkstra's algorithm** across massive, procedurally generated 3D sparse graphs simulating urban airspace.

**Key Conclusion:** Uninformed search algorithms like Dijkstra cause fatal Out-Of-Memory (OOM) crashes on edge hardware. A* is not just an optimization; it is a baseline safety requirement for drone flight.

## ✨ Key Features
* **Unconstrained 3D Kinematics:** Grants the drone 26-neighbor connectivity to simulate realistic, diagonal flight across all three axes.
* **Sparse Graph Architecture:** Models the sky using a strict adjacency list (rather than a heavy 3D matrix) to ensure memory efficiency.
* **Procedural Urban Obstacles:** Injects buildings and no-fly zones at varying density levels (5%, 15%, 25%).
* **Hardware Profiling:** Actively traces peak heap-memory allocation (RAM) in Megabytes and microsecond execution runtimes.
* **Scientific Control:** Both algorithms utilize the exact same underlying `heapq` (Min-Heap) data structure for absolute benchmarking validity.

## 📊 Key Findings (50,000 Node Simulation)
* **Memory Bottleneck:** Dijkstra required **2.45 MB** of RAM (guaranteeing a crash on a 1MB controller). A* required only **0.59 MB**—a **75.9% reduction**, keeping the drone safely within hardware limits.
* **Search Efficiency:** A* evaluated only **2,773 nodes** compared to Dijkstra's **36,506 nodes** (a 92.4% reduction in wasted computational effort).
* **Speed:** A* operated approximately **90% faster** (239ms vs. 2594ms), saving critical CPU cycles and battery life.

## 📂 Repository Structure
```text
3D_Drone_Navigation_Research/
├── src/                         # Core simulation logic
│   ├── main.py                  # Entry point for automated stress tests
│   ├── algorithms.py            # Dijkstra & A* routing implementations
│   ├── environment.py           # 3D spatial grid and obstacle generation
│   ├── profiler.py              # Execution time & RAM benchmarking tools
│   └── visualizer.py            # Generates IEEE-standard statistical plots
├── notebooks/                   # Interactive analysis
│   └── Visulizing.ipynb         # 3D spatial visualizations of search cones
├── data/                        # Simulation datasets
│   └── drone_navigation_results.csv 
├── conference_materials/        # Academic publication assets
│   └── figures/                 # Exported Seaborn/Matplotlib charts
├── requirements.txt             # Python dependencies
└── README.md
```

## 🚀 Quick Start

**1. Clone the repository**

```Bash
git clone [[https://github.com/Smitpatel2911/3D-UAV-Pathfinding.git]]
cd 3D-UAV-Pathfinding
```

**2. Install dependencies**

```Bash
pip install -r requirements.txt
```

**3. Run the benchmarking simulation**

```Bash
cd src
python main.py
```
**Note:** This will auto-generate drone_navigation_results.csv in the data/ directory.

**4. Generate statistical plots**

```Bash
python visualizer.py
```

## 🔮 Future Scope

* **Dynamic Obstacles:** Transitioning from static buildings to moving obstacles (e.g., other drones) using incremental search algorithms like D* Lite.
* **Kinematic Constraints:** Integrating the drone's physical turning radius and momentum into the heuristic function.
* **Swarm Intelligence:** Scaling the simulation for decentralized, multi-agent collision avoidance.
