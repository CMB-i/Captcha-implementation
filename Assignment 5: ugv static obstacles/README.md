# UGV Navigation in Static Obstacle Grid

## Problem Statement

Design a path-planning algorithm for an Unmanned Ground Vehicle (UGV) navigating a **70×70 grid** with known static obstacles.

---

## Objective

* Generate a battlefield grid with obstacles
* Support 3 obstacle density levels:

  * Low (10%)
  * Medium (20%)
  * High (30%)
* Compute the shortest collision-free path from Start → Goal
* Evaluate performance using **Measures of Effectiveness (MoE)**

---

## Algorithm Used

### A* Search Algorithm

Evaluation function:
[
f(n) = g(n) + h(n)
]

Where:

* ( g(n) ): cost from start to current node
* ( h(n) ): heuristic estimate to goal (Manhattan distance)

---

## ⚙️ Implementation Details

* Grid represented as a 2D matrix
* Obstacles randomly generated based on density
* Valid moves:

  * Up, Down, Left, Right
* Priority queue (min-heap) used for efficient node selection

---

## Experimental Setup

The algorithm is tested under **three different obstacle density levels**:

| Density Level | Obstacle Percentage | Environment Difficulty |
| ------------- | ------------------- | ---------------------- |
| Low           | 10%                 | Easy                   |
| Medium        | 20%                 | Moderate               |
| High          | 30%                 | Hard                   |

For each run:

* Start and goal positions are user-defined
* Obstacles are randomly generated
* A* search is executed to find the shortest path

---

## 📊 Measures of Effectiveness (MoE)

The following metrics are recorded:

* **Path Found** → whether the goal was reached
* **Path Length** → number of steps in final path
* **Nodes Explored** → search effort
* **Execution Time** → efficiency
* **Obstacle Density** → environment complexity

---

## Observations

### Low Density (10%)

* Path is usually found easily
* Multiple routes available
* Fewer nodes explored
* Fast execution time

### Medium Density (20%)

* Path still exists in most cases
* Fewer alternative routes
* Moderate number of nodes explored
* Slight increase in execution time

### High Density (30%)

* Path may or may not exist
* Very constrained movement
* Large number of nodes explored
* Increased execution time
* Higher chance of failure

---

## Analysis

* As obstacle density increases:

  * **Search complexity increases**
  * **Execution time increases**
  * **Nodes explored increases**
  * **Success rate decreases**

* A* performs efficiently because:

  * The heuristic guides the search toward the goal
  * It avoids unnecessary exploration compared to uninformed search

* In dense environments:

  * The heuristic becomes less effective due to limited paths
  * The algorithm behaves closer to Dijkstra’s algorithm

---

## How to Run

```bash
python astar_static.py
```

---

## Input

* Obstacle density level (low / medium / high)
* Start coordinates
* Goal coordinates

---

## Output

* Generated battlefield grid
* Shortest path (if exists)
* Measures of Effectiveness

---

## Concepts Demonstrated

* State-space search
* Heuristic search (A*)
* Grid-based path planning
* Static obstacle avoidance
* Performance evaluation

---

## Conclusion

This implementation demonstrates how A* efficiently computes shortest paths in grid environments with known obstacles. The use of multiple obstacle densities allows evaluation of the algorithm’s robustness and scalability under varying environmental complexities.

---
