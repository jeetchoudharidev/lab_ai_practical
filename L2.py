
# Experiment 2: A* Search Algorithm
# Game-based Maze Pathfinding

import heapq


# -----------------------------------------
# 1. CREATE THE GAME ENVIRONMENT
# -----------------------------------------

# 0 = Empty / Walkable
# 1 = Wall / Obstacle

grid = [
    [0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 5)


# -----------------------------------------
# 2. HEURISTIC FUNCTION
# -----------------------------------------

def heuristic(current, goal):

    # Manhattan Distance
    return (
        abs(current[0] - goal[0]) +
        abs(current[1] - goal[1])
    )


# -----------------------------------------
# 3. A* SEARCH ALGORITHM
# -----------------------------------------

def astar(grid, start, goal):

    rows = len(grid)
    cols = len(grid[0])

    # Check valid starting and goal positions
    for position in [start, goal]:
        r, c = position

        if not (0 <= r < rows and 0 <= c < cols):
            return None, None, 0

        if grid[r][c] == 1:
            return None, None, 0

    # Priority Queue (Min Heap)
    # Stores: (f_score, g_score, counter, position)

    open_list = []

    heapq.heappush(
        open_list,
        (heuristic(start, goal), 0, 0, start)
    )

    counter = 1

    # Store the parent of each node
    came_from = {}

    # Store the cheapest known path cost
    g_score = {
        start: 0
    }

    expanded_nodes = 0

    # Possible movements:
    # Up, Down, Left, Right

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    # -------------------------------------
    # 4. MAIN SEARCH LOOP
    # -------------------------------------

    while open_list:

        # Extract node with minimum f-score

        f, pushed_g, _, current = heapq.heappop(
            open_list
        )

        # Ignore outdated heap entries
        if pushed_g != g_score.get(current):
            continue

        expanded_nodes += 1

        # Check whether goal is reached

        if current == goal:

            path = [current]

            # Reconstruct the path
            while current in came_from:

                current = came_from[current]

                path.append(current)

            path.reverse()

            return path, g_score[goal], expanded_nodes

        # ---------------------------------
        # 5. EXPLORE NEIGHBOURS
        # ---------------------------------

        for dr, dc in directions:

            neighbor = (
                current[0] + dr,
                current[1] + dc
            )

            nr, nc = neighbor

            # Check grid boundaries

            if not (
                0 <= nr < rows and
                0 <= nc < cols
            ):
                continue

            # Avoid obstacles

            if grid[nr][nc] == 1:
                continue

            # Calculate new path cost

            tentative_g = g_score[current] + 1

            # Update if a better path is found

            if tentative_g < g_score.get(
                neighbor, float("inf")
            ):

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g

                h = heuristic(neighbor, goal)

                f = tentative_g + h

                heapq.heappush(
                    open_list,
                    (f, tentative_g, counter, neighbor)
                )

                counter += 1

    # No valid path found

    return None, None, expanded_nodes


# -----------------------------------------
# 6. DISPLAY THE FINAL PATH
# -----------------------------------------

def display_grid(grid, path, start, goal):

    path_set = set(path) if path else set()

    for r in range(len(grid)):

        for c in range(len(grid[0])):

            position = (r, c)

            if position == start:
                print("S", end=" ")

            elif position == goal:
                print("G", end=" ")

            elif grid[r][c] == 1:
                print("#", end=" ")

            elif position in path_set:
                print("*", end=" ")

            else:
                print(".", end=" ")

        print()


# -----------------------------------------
# 7. RUN THE ALGORITHM
# -----------------------------------------

path, cost, expanded = astar(
    grid,
    start,
    goal
)

print("\nA* SEARCH RESULT")

if path:

    print("Path Found!")

    print("Path:", path)

    print("Total Path Cost:", cost)

    print("Expanded Nodes:", expanded)

    print("\nFINAL MAZE:")

    display_grid(
        grid,
        path,
        start,
        goal
    )

else:

    print("No valid path found!")
