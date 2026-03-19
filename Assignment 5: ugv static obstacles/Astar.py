import heapq
import random
import time

GRID_SIZE = 20   # Change to 70 for actual requirement

DENSITY_LEVELS = {
    "low": 0.10,
    "medium": 0.20,
    "high": 0.30
}

def create_grid(size, density, start, goal):
    grid = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if (i, j) != start and (i, j) != goal:
                if random.random() < density:
                    grid[i][j] = 1   # obstacle

    return grid

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(node, grid):
    x, y = node
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up, down, left, right
    neighbors = []

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] == 0:
                neighbors.append((nx, ny))

    return neighbors

def reconstruct_path(parent, goal):
    path = []
    current = goal
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append(current)
    path.reverse()
    return path

def astar(grid, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))

    g_cost = {start: 0}
    f_cost = {start: heuristic(start, goal)}
    parent = {}

    explored_nodes = 0
    visited = set()

    while open_list:
        _, current = heapq.heappop(open_list)

        if current in visited:
            continue

        visited.add(current)
        explored_nodes += 1

        if current == goal:
            path = reconstruct_path(parent, goal)
            return path, explored_nodes

        for neighbor in get_neighbors(current, grid):
            tentative_g = g_cost[current] + 1

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f_cost[neighbor] = tentative_g + heuristic(neighbor, goal)
                parent[neighbor] = current
                heapq.heappush(open_list, (f_cost[neighbor], neighbor))

    return None, explored_nodes

def print_grid(grid, path=None, start=None, goal=None):
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
                row += "* "
            elif grid[i][j] == 1:
                row += "X "
            else:
                row += ". "
        print(row)

def main():
    print("UGV Navigation using A* Search")
    print("Grid size:", GRID_SIZE, "x", GRID_SIZE)
    print("Obstacle density levels: low, medium, high")

    density_choice = input("Enter obstacle density level: ").strip().lower()

    if density_choice not in DENSITY_LEVELS:
        print("Invalid density level.")
        return

    try:
        sx, sy = map(int, input("Enter start coordinates (row col): ").split())
        gx, gy = map(int, input("Enter goal coordinates (row col): ").split())
    except ValueError:
        print("Invalid input format.")
        return

    start = (sx, sy)
    goal = (gx, gy)

    if not (0 <= sx < GRID_SIZE and 0 <= sy < GRID_SIZE and 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE):
        print("Start or goal is out of grid bounds.")
        return

    density = DENSITY_LEVELS[density_choice]
    grid = create_grid(GRID_SIZE, density, start, goal)

    start_time = time.time()
    path, explored_nodes = astar(grid, start, goal)
    end_time = time.time()

    print("\nGenerated Battlefield Grid:\n")
    print_grid(grid, path, start, goal)

    print("\nMeasures of Effectiveness:")
    print("Obstacle Density Level:", density_choice)
    print("Obstacle Percentage:", density * 100, "%")
    print("Nodes Explored:", explored_nodes)
    print("Execution Time: {:.6f} seconds".format(end_time - start_time))

    if path:
        print("Path Found: Yes")
        print("Path Length:", len(path) - 1)
        print("Path:", path)
    else:
        print("Path Found: No")
        print("Path Length: N/A")

if __name__ == "__main__":
    main()