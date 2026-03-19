# Dijkstra’s Algorithm on Indian Cities

## Problem Statement

When actions in a state-space search have different costs, an optimal approach is to use **Best-First Search** where the evaluation function is the path cost from the root to the current node.

This method is known as:

* **Dijkstra’s Algorithm** (in theoretical computer science)
* **Uniform-Cost Search (UCS)** (in artificial intelligence)

This assignment implements Dijkstra’s algorithm to compute the **shortest road distance between Indian cities**.

---

## Objective

* Represent Indian cities as nodes in a graph
* Represent road distances as weighted edges
* Compute the shortest path between a **user-specified source and destination city**

---

## Algorithm Used

### Dijkstra’s Algorithm (Uniform-Cost Search)

Evaluation function:
[
f(n) = g(n)
]

Where:

* ( g(n) ) = total path cost from the source node to node ( n )

---

## Implementation Details

* Graph is represented using an **adjacency list**
* Each city is connected to neighboring cities with road distances (in km)
* A **priority queue (min-heap)** is used to always expand the least-cost node
* A **parent dictionary** is used to reconstruct the shortest path

---

## How to Run

```bash
python dijkstra.py
```

### Input

* Source city
* Destination city

### Output

* Shortest distance (in km)
* Optimal path between the cities

---

## Example

**Input:**

```
Enter source city: Delhi
Enter destination city: Bengaluru
```

**Output:**

```
Shortest Path Found!
Distance: 2419 km
Path: Delhi -> Jaipur -> Ahmedabad -> Mumbai -> Pune -> Bengaluru
```

---

## Graph Representation

* Nodes → Cities
* Edges → Road connections
* Weights → Distance between cities (in km)

The data used is based on **publicly available road-distance estimates**.

---

## Time Complexity

[
O((V + E)\log V)
]

Where:

* ( V ) = number of cities
* ( E ) = number of roads

---

## Space Complexity

[
O(V + E)
]

---


## Key Learning

This implementation demonstrates how Dijkstra’s Algorithm efficiently computes the shortest path in a **weighted graph with non-negative edge costs**, making it ideal for real-world applications like road navigation systems.

---
