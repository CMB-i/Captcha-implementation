# CS2201 AI Assignments Repository 

This repository contains implementations of key concepts in **Artificial Intelligence and Intelligent Systems**, developed as part of coursework assignments.

---

# Repository Structure

```text
Assignment 2:
├── Task 1: CAPTCHA Implementation
├── Task 2: AQI Reflex Agent (Go CLI)
├── Task 3: Uninformed Search (Water Jug Problem)

Assignment 3:
├── Task 1: Dijkstra’s Algorithm (Indian Cities)
├── Task 2: UGV Static Obstacle Navigation (A*)
├── Task 3: UGV Dynamic Navigation (Repeated A*)
```

---

# Assignment 2

## Task 1: CAPTCHA — Human Verification System

A simple CAPTCHA system inspired by the **Turing Test**, designed to distinguish human users from automated bots.

### Key Idea

Instead of asking:

> “Can a machine behave like a human?”

CAPTCHA asks:

> “Does this interaction behave like a human?”

### Features

* Interactive 3×3 image grid
* Randomized challenges
* Server-side verification
* Limited attempts (3 tries)
* HMAC-based integrity protection

---

## Task 2: AQI Reflex Agent (Go CLI)

A **Simple Reflex Agent** that fetches real-time Air Quality Index (AQI) and provides health recommendations.

### Functionality

* Takes location input (State, Country)
* Converts location → coordinates using Geocoding API
* Fetches AQI data using Google Air Quality API
* Applies rule-based decision logic

---

## Task 3: Uninformed Search — Water Jug Problem

Implementation and comparison of classical **uninformed search algorithms**.

### Algorithms Implemented

* Breadth-First Search (BFS)
* Depth-First Search (DFS)
* Depth-Limited Search (DLS)
* Iterative Deepening DFS (IDDFS)

### Problem

Two jugs with fixed capacities — goal is to measure a target quantity using allowed operations.

### Metrics Compared

* Nodes Expanded
* Memory Usage (Frontier Size)
* Execution Time
* Solution Depth

### Key Insights

* BFS → optimal but memory-heavy
* DFS → memory-efficient but non-optimal
* DLS → controlled depth but risky
* IDDFS → best balance of optimality and memory

---

# Assignment 3

## Task 1: Dijkstra’s Algorithm — Indian Cities

Implementation of **Dijkstra’s Algorithm (Uniform-Cost Search)** on a weighted graph of Indian cities.

### Objective

* Compute shortest path between two cities
* Use road distances as edge weights

### Key Concepts

* Weighted graphs
* Priority queue (min-heap)
* Path reconstruction

### Data Source

Road distances based on publicly available **OpenStreetMap-derived references**.

---

## Task 2: UGV Navigation — Static Obstacles (A*)

Path planning for an Unmanned Ground Vehicle (UGV) in a **known obstacle grid**.

### Algorithm

**A*** Search
Evaluation function:

```
f(n) = g(n) + h(n)
```

### Features

* Grid-based environment (70×70 scalable)
* Three obstacle densities:

  * Low (10%)
  * Medium (20%)
  * High (30%)

### Measures of Effectiveness

* Path Found
* Path Length
* Nodes Explored
* Execution Time

### Insight

As density increases:

* complexity ↑
* time ↑
* success rate ↓
---

## Task 3: UGV Navigation — Dynamic Obstacles

Path planning in environments where obstacles are:

* Unknown initially
* Dynamic during traversal

### Algorithm

* Implemented: **Repeated A***
* Conceptual: **D* Lite**

### Dynamic Behavior

* Plan path using A*
* Move step-by-step
* Detect new obstacles
* Replan when blocked

### Measures of Effectiveness

* Path Found
* Path Length
* Nodes Explored
* Execution Time
* Number of Replans

### Key Insight

* Dynamic environments require **adaptive replanning**
* Repeated A* works but is inefficient
* D* Lite is more optimal for real-world systems

---
