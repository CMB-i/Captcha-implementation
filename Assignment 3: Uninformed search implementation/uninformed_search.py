from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Callable, Iterable, Set
import time

State = Tuple[int, int]
Action = str


@dataclass
class Result:
    found: bool
    path_states: List[State]
    path_actions: List[Action]
    nodes_expanded: int
    max_frontier_size: int
    time_sec: float
    depth: Optional[int]


# Problem Definition

class WaterJugProblem:
    def __init__(self, cap_a: int, cap_b: int, target: int, goal_in: str = "either"):
        """
        goal_in:
          - "either": either jug has target
          - "A": jug A has target
          - "B": jug B has target
        """
        self.cap_a = cap_a
        self.cap_b = cap_b
        self.target = target
        self.goal_in = goal_in

    def start(self) -> State:
        return (0, 0)

    def is_goal(self, s: State) -> bool:
        a, b = s
        if self.goal_in == "A":
            return a == self.target
        if self.goal_in == "B":
            return b == self.target
        return a == self.target or b == self.target

    def successors(self, s: State) -> Iterable[Tuple[Action, State]]:
        a, b = s
        A, B = self.cap_a, self.cap_b

        # Fill A
        yield ("Fill A", (A, b))
        # Fill B
        yield ("Fill B", (a, B))
        # Empty A
        yield ("Empty A", (0, b))
        # Empty B
        yield ("Empty B", (a, 0))

        # Pour A -> B
        pour = min(a, B - b)
        yield ("Pour A->B", (a - pour, b + pour))

        # Pour B -> A
        pour = min(b, A - a)
        yield ("Pour B->A", (a + pour, b - pour))

    def state_space_upper_bound(self) -> int:
        # number of possible states is (A+1)*(B+1)
        return (self.cap_a + 1) * (self.cap_b + 1)



# Path Reconstruction helpers
# -----------------------------
def reconstruct(parent: Dict[State, Tuple[Optional[State], Optional[Action]]], goal: State):
    states: List[State] = []
    actions: List[Action] = []
    cur = goal
    while True:
        p, act = parent[cur]
        states.append(cur)
        if p is None:
            break
        actions.append(act)  # type: ignore
        cur = p
    states.reverse()
    actions.reverse()
    return states, actions



# BFS (Graph Search)

def bfs(problem: WaterJugProblem) -> Result:
    t0 = time.perf_counter()
    start = problem.start()

    q = deque([start])
    visited: Set[State] = {start}
    parent: Dict[State, Tuple[Optional[State], Optional[Action]]] = {start: (None, None)}

    nodes_expanded = 0
    max_frontier = len(q)

    while q:
        max_frontier = max(max_frontier, len(q))
        s = q.popleft()

        if problem.is_goal(s):
            states, actions = reconstruct(parent, s)
            t1 = time.perf_counter()
            return Result(True, states, actions, nodes_expanded, max_frontier, t1 - t0, len(actions))

        nodes_expanded += 1
        for act, ns in problem.successors(s):
            if ns not in visited:
                visited.add(ns)
                parent[ns] = (s, act)
                q.append(ns)

    t1 = time.perf_counter()
    return Result(False, [], [], nodes_expanded, max_frontier, t1 - t0, None)



# DFS (Graph Search)

def dfs(problem: WaterJugProblem) -> Result:
    t0 = time.perf_counter()
    start = problem.start()

    stack = [start]
    visited: Set[State] = {start}
    parent: Dict[State, Tuple[Optional[State], Optional[Action]]] = {start: (None, None)}

    nodes_expanded = 0
    max_frontier = len(stack)

    while stack:
        max_frontier = max(max_frontier, len(stack))
        s = stack.pop()

        if problem.is_goal(s):
            states, actions = reconstruct(parent, s)
            t1 = time.perf_counter()
            return Result(True, states, actions, nodes_expanded, max_frontier, t1 - t0, len(actions))

        nodes_expanded += 1

        # push successors (reverse for stable-ish order)
        succs = list(problem.successors(s))
        for act, ns in reversed(succs):
            if ns not in visited:
                visited.add(ns)
                parent[ns] = (s, act)
                stack.append(ns)

    t1 = time.perf_counter()
    return Result(False, [], [], nodes_expanded, max_frontier, t1 - t0, None)



# Depth-Limited DFS (DLS)

def dls(problem: WaterJugProblem, limit: int) -> Result:
    t0 = time.perf_counter()
    start = problem.start()

    # stack entries: (state, depth)
    stack: List[Tuple[State, int]] = [(start, 0)]
    visited: Set[State] = {start}
    parent: Dict[State, Tuple[Optional[State], Optional[Action]]] = {start: (None, None)}

    nodes_expanded = 0
    max_frontier = len(stack)

    while stack:
        max_frontier = max(max_frontier, len(stack))
        s, d = stack.pop()

        if problem.is_goal(s):
            states, actions = reconstruct(parent, s)
            t1 = time.perf_counter()
            return Result(True, states, actions, nodes_expanded, max_frontier, t1 - t0, len(actions))

        if d == limit:
            continue

        nodes_expanded += 1
        succs = list(problem.successors(s))
        for act, ns in reversed(succs):
            if ns not in visited:
                visited.add(ns)
                parent[ns] = (s, act)
                stack.append((ns, d + 1))

    t1 = time.perf_counter()
    return Result(False, [], [], nodes_expanded, max_frontier, t1 - t0, None)



# Iterative Deepening DFS (IDDFS)

def iddfs(problem: WaterJugProblem, max_depth: int) -> Result:
    t0 = time.perf_counter()

    total_expanded = 0
    overall_max_frontier = 0

    for depth in range(max_depth + 1):
        res = dls(problem, depth)
        total_expanded += res.nodes_expanded
        overall_max_frontier = max(overall_max_frontier, res.max_frontier_size)
        if res.found:
            t1 = time.perf_counter()
            return Result(True, res.path_states, res.path_actions, total_expanded, overall_max_frontier, t1 - t0, res.depth)

    t1 = time.perf_counter()
    return Result(False, [], [], total_expanded, overall_max_frontier, t1 - t0, None)

# printing + comparison

def print_solution(res: Result):
    if not res.found:
        print("No solution found.")
        return
    print(f"Found solution in depth = {res.depth}")
    for i, st in enumerate(res.path_states):
        if i == 0:
            print(f"Start: {st}")
        else:
            print(f"{i:>2}. {res.path_actions[i-1]:<10} -> {st}")


def compare(problem: WaterJugProblem, dls_limit: int = 10, iddfs_max_depth: int = 20):
    algos: List[Tuple[str, Callable[[], Result]]] = [
        ("BFS", lambda: bfs(problem)),
        ("DFS", lambda: dfs(problem)),
        (f"DLS({dls_limit})", lambda: dls(problem, dls_limit)),
        (f"IDDFS({iddfs_max_depth})", lambda: iddfs(problem, iddfs_max_depth)),
    ]

    print("\n=== Water Jug Problem ===")
    print(f"Capacities: A={problem.cap_a}, B={problem.cap_b}, Target={problem.target}, GoalIn={problem.goal_in}")
    print(f"State space upper bound: {problem.state_space_upper_bound()} states\n")

    header = f"{'Algo':<12} {'Found':<6} {'Depth':<6} {'Expanded':<10} {'MaxFrontier':<12} {'Time(s)':<10}"
    print(header)
    print("-" * len(header))

    results = []
    for name, fn in algos:
        r = fn()
        results.append((name, r))
        print(f"{name:<12} {str(r.found):<6} {str(r.depth):<6} {r.nodes_expanded:<10} {r.max_frontier_size:<12} {r.time_sec:<10.6f}")

    # exmaple
    chosen = None
    for name, r in results:
        if name == "BFS" and r.found:
            chosen = (name, r)
            break
    if chosen is None:
        for name, r in results:
            if r.found:
                chosen = (name, r)
                break

    if chosen:
        print(f"\n--- Example solution path ({chosen[0]}) ---")
        print_solution(chosen[1])


if __name__ == "__main__":

    # A=4L, B=3L, target=2L 
    p = WaterJugProblem(cap_a=4, cap_b=3, target=2, goal_in="either")
    compare(p, dls_limit=8, iddfs_max_depth=15)
