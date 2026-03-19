# UGV Navigation with Dynamic Obstacles

## Problem Statement

Design a path-planning algorithm for a UGV navigating a grid where obstacles are dynamic and not known a priori.

---

## Objective

* Navigate from Start → Goal
* Handle dynamically appearing obstacles
* Recompute path when necessary

---

## Algorithm Used

### Implemented:

Repeated A* Search

### Conceptual:

D* Lite Algorithm

---

## Implementation Details

* Grid initially generated with base obstacles
* New obstacles appear randomly during traversal
* UGV replans path whenever blocked

---

## Dynamic Behavior

* Detect obstacle during movement
* Re-run A* from current position
* Continue until goal reached or no path exists

---

## Measures of Effectiveness

* Path Found
* Path Length
* Nodes Explored
* Execution Time
* Number of Replans

---

## Observations

* Dynamic obstacles increase uncertainty
* Frequent replanning may occur
* Path may deviate significantly from initial plan

---

## Analysis

* Replanning increases computational cost
* Efficiency depends on how often obstacles appear
* Repeated A* is simple but not optimal
* D* Lite improves efficiency by reusing previous computations

---

## How to Run

```bash
python dynamic_astar.py
```

---

## Concepts Demonstrated

* Dynamic path planning
* Real-time decision making
* Incremental search
* Adaptive systems

---

## Conclusion

Dynamic environments require adaptive algorithms. While repeated A* provides a simple solution, advanced algorithms like D* Lite are more efficient for real-world robotics applications.

---
