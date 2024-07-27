# pathfinding-project

## Overview

This project implements and visualizes the A* (A-star) pathfinding algorithm, which is widely used in various applications requiring efficient pathfinding. The A* algorithm combines aspects of Dijkstra's algorithm and Greedy Best-First Search to find the shortest path from a start node to a goal node in a grid-based environment

## Features

- **A {*} Algorithm**: Visualizes the pathfinding process using the A* algorithm.
- **Interactive Pygame Visualization**: Utilizes Pygame to render a dynamic grid-based environment, including obstacles, start, and goal positions. Provides real-time visualization of the pathfinding process and the resulting path.
- **Detailed Performance Metrics**: Displays key performance metrics including the total number of nodes processed and the final path length. This information is presented below the visualization, offering insights into the algorithm’s      efficiency and performance.

## Installation
```
1. Clone the Repository:
   git clone https://github.com/Rohnnam/pathfinding-project.git
   cd pathfinding-project

2. Set Up the Virtual Environment (optional but recommended):

  python3 -m venv .venv
  source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

3. Install Dependencies:
  pip install -r requirements.txt
```


**Working**
```
Grid Initialization:
 A grid is initialized with random obstacles and a fixed start point at the center of the grid. The goal point is set by user interaction.

Algorithm Execution:
Upon setting the goal point, the A* algorithm is executed. The algorithm explores nodes using a priority queue, considering both the cost to reach a node and an estimate of the cost to reach the goal.

Visualization and Animation:
The pathfinding process is visualized in real-time. The grid updates to show the exploration of nodes and the final path, with an incremental animation to depict the algorithm's progress.

Metrics Display:
After the pathfinding completes, performance metrics are updated and displayed, showing the efficiency of the algorithm in terms of nodes processed and path length.
```
