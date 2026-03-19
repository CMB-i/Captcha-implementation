import heapq
import random
import time

GRID_SIZE = 20
INITIAL_DENSITY = 0.05          # initial obstacle density
DYNAMIC_OBSTACLE_PROB = 0.005   # probability of new obstacles appearing


def create_grid(size, density, start, goal):
    """Create initial grid with static obstacles, keeping start and goal free."""
    grid = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if (i, j) != start and (i, j) != goal:
                if random.random() < density:
                    grid[i][j] = 1

    return grid


def heuristic(a, b):
    """Manhattan distance."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(node, grid):
    """Return valid 4-directional neighbors that are not obstacles."""
    x, y = node
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] == 0:
                neighbors.append((nx, ny))

    return neighbors


def reconstruct_path(parent, goal):
    """Reconstruct path from parent dictionary."""
    path = []
    current = goal

    while current in parent:
        path.append(current)
        current = parent[current]

    path.append(current)
    path.reverse()
    return path


def astar(grid, start, goal):
    """A* search from start to goal."""
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), start))

    g_cost = {start: 0}
    parent = {}
    visited = set()
    nodes_explored = 0

    while open_list:
        _, current = heapq.heappop(open_list)

        if current in visited:
            continue

        visited.add(current)
        nodes_explored += 1

        if current == goal:
            return reconstruct_path(parent, goal), nodes_explored

        for neighbor in get_neighbors(current, grid):
            new_g = g_cost[current] + 1

            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                f_cost = new_g + heuristic(neighbor, goal)
                parent[neighbor] = current
                heapq.heappush(open_list, (f_cost, neighbor))

    return None, nodes_explored


def add_dynamic_obstacles(grid, start, goal, current, probability=DYNAMIC_OBSTACLE_PROB):
    """
    Randomly add new obstacles during traversal.
    Protect start, goal, and current robot position.
    Only add obstacles to empty cells.
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) != start and (i, j) != goal and (i, j) != current:
                if grid[i][j] == 0 and random.random() < probability:
                    grid[i][j] = 1


def dynamic_navigation(grid, start, goal):
    """
    Repeated A*:
    - Plan path
    - Move one step
    - Add dynamic obstacles
    - Replan if next step gets blocked
    """
    current = start
    full_path = [current]

    total_nodes = 0
    replans = 0

    while current != goal:
        path, explored = astar(grid, current, goal)
        total_nodes += explored

        if not path:
            return None, total_nodes, replans

        # If already at goal
        if len(path) == 1:
            return full_path, total_nodes, replans

        next_step = path[1]

        # Simulate new dynamic obstacles appearing
        add_dynamic_obstacles(grid, start, goal, current, probability=DYNAMIC_OBSTACLE_PROB)

        # If next step got blocked, replan
        if grid[next_step[0]][next_step[1]] == 1:
            replans += 1
            continue

        # Move to next step
        current = next_step
        full_path.append(current)

    return full_path, total_nodes, replans


def print_grid(grid, path=None, start=None, goal=None):
    """Print grid with symbols."""
    path_set = set(path) if path else set()

    for i in range(len(grid)):
        row = ""
        for j in range(len(grid[0])):
            cell = (i, j)

            if cell == start:
                row += "S "
            elif cell == goal:
                row += "G "
            elif cell in path_set:
                row += "O "
            elif grid[i][j] == 1:
                row += "X "
            else:
                row += ". "
        print(row)


def main():
    print("Dynamic UGV Navigation")

    try:
        sx, sy = map(int, input("Enter start (row col): ").split())
        gx, gy = map(int, input("Enter goal (row col): ").split())
    except ValueError:
        print("Invalid input. Please enter exactly two integers for each coordinate.")
        return

    start = (sx, sy)
    goal = (gx, gy)

    if not (0 <= sx < GRID_SIZE and 0 <= sy < GRID_SIZE and 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE):
        print("Start or goal is outside the grid.")
        return

    grid = create_grid(GRID_SIZE, INITIAL_DENSITY, start, goal)

    start_time = time.time()
    path, nodes, replans = dynamic_navigation(grid, start, goal)
    end_time = time.time()

    print("\nFinal Grid:\n")
    print_grid(grid, path, start, goal)

    print("\nMeasures of Effectiveness:")
    print("Nodes Explored:", nodes)
    print("Replans:", replans)
    print("Execution Time:", end_time - start_time)

    if path:
        print("Path Found: Yes")
        print("Path Length:", len(path) - 1)
        print("Path:", path)
    else:
        print("Path Found: No")
        print("No feasible path due to obstacle configuration.")


if __name__ == "__main__":
    main()