# Uninformed Search Algorithms — Water Jug Problem

This project demonstrates the implementation and comparison of classic **uninformed search strategies** using the **Water Jug Problem** as the state-space search environment.

The following algorithms are implemented:

* **Breadth-First Search (BFS)**
* **Depth-First Search (DFS)**
* **Depth-Limited Search (DLS)**
* **Iterative Deepening Depth-First Search (IDDFS)**

The goal is to compare these algorithms based on:

* Number of nodes expanded
* Memory usage (frontier size)
* Execution time
* Solution depth

This project is useful for understanding **AI search strategies** and their practical performance differences.

---

# Problem Description — Water Jug Problem

You are given two water jugs with fixed capacities.

For example:

* Jug A capacity = **4 liters**
* Jug B capacity = **3 liters**

Initial state:

(0,0)

Meaning both jugs are empty.

Allowed operations:

1. **Fill Jug A**
2. **Fill Jug B**
3. **Empty Jug A**
4. **Empty Jug B**
5. **Pour water from Jug A → Jug B**
6. **Pour water from Jug B → Jug A**

Goal:

Reach a state where **either jug contains the target amount of water**.

Example target:

2 liters

---

# State Representation

Each state is represented as:

```
(x, y)
```

Where:

* `x` = water in Jug A
* `y` = water in Jug B

Example states:

```
(0,0)
(4,0)
(1,3)
(2,3)
```

---

# Implemented Algorithms

## 1. Breadth-First Search (BFS)

BFS explores the search tree **level by level**.

Properties:

* Guarantees **shortest path solution**
* Uses a **queue**
* Higher memory usage

Pseudo flow:

```
enqueue start state
while queue not empty:
    dequeue state
    if goal → return
    expand successors
    enqueue successors
```

---

## 2. Depth-First Search (DFS)

DFS explores **as deep as possible before backtracking**.

Properties:

* Uses **stack**
* Lower memory usage
* Does **not guarantee shortest solution**

Pseudo flow:

```
push start state
while stack not empty:
    pop state
    if goal → return
    push successors
```

---

## 3. Depth-Limited Search (DLS)

DLS is DFS with a **maximum depth limit**.

Purpose:

* Prevents infinite exploration in deep trees.

Rule:

```
if depth == limit:
    stop expanding
```

---

## 4. Iterative Deepening DFS (IDDFS)

IDDFS repeatedly runs **Depth-Limited DFS** with increasing depth.

Example:

```
Depth 0
Depth 1
Depth 2
Depth 3
...
```

Advantages:

* Memory efficient like **DFS**
* Finds shortest solution like **BFS**

---

# Performance Metrics

Each algorithm records:

| Metric            | Description                 |
| ----------------- | --------------------------- |
| Nodes Expanded    | Number of states explored   |
| Max Frontier Size | Maximum size of queue/stack |
| Execution Time    | Runtime in seconds          |
| Solution Depth    | Number of steps to goal     |

---

# Running the Program

Clone the repository:

Run the program:

```bash
python water_jug_search.py
```

---

# Example Output

```
=== Water Jug Problem ===
Capacities: A=4, B=3, Target=2

Algo         Found  Depth  Expanded  MaxFrontier  Time(s)
---------------------------------------------------------
BFS          True   6      15        6            0.0002
DFS          True   8      20        5            0.0001
DLS(8)       True   6      18        5            0.0002
IDDFS(15)    True   6      22        4            0.0003
```

Example solution path:

```
Start: (0,0)
Fill B       -> (0,3)
Pour B→A     -> (3,0)
Fill B       -> (3,3)
Pour B→A     -> (4,2)
Empty A      -> (0,2)
```

Goal achieved: **2 liters in Jug B**

## conclusion:

From the experimental results, the following observations were made:
- BFS consistently finds the shortest solution path because it explores the state space level-by-level. However, it requires more memory since it stores many states in the queue at once.
- DFS uses much less memory because it explores one branch deeply before backtracking. However, it does not guarantee the shortest solution and may explore unnecessary paths.
- DLS helps control DFS by restricting the search depth, preventing infinite or excessively deep exploration. However, if the depth limit is set too low, the algorithm may fail to find a solution even if one exists.
- IDDFS combines the advantages of BFS and DFS. It uses less memory like DFS while still guaranteeing the optimal solution depth like BFS. The trade-off is that some nodes are revisited multiple times, increasing computation slightly.

For the Water Jug problem:
- BFS is best when the goal is to guarantee the shortest solution.
- DFS is useful when memory is limited.
- DLS provides control over DFS but requires choosing a good depth limit.
- IDDFS provides a balanced approach, making it one of the most practical uninformed search strategies.
