
from collections import deque

# Initial state
initial_state = (
    1, 2, 3,
    4, 0, 6,
    7, 5, 8
)

# Goal state
goal_state = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)


# Display puzzle board
def display(state):

    for i in range(0, 9, 3):
        print(state[i:i+3])


# Generate possible next states
def get_neighbors(state):

    neighbors = []

    # Find blank position
    zero = state.index(0)

    row = zero // 3
    col = zero % 3

    # Possible movements
    moves = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    for dr, dc in moves:

        new_row = row + dr
        new_col = col + dc

        # Check board boundaries
        if 0 <= new_row < 3 and 0 <= new_col < 3:

            new_position = new_row * 3 + new_col

            # Swap blank with adjacent tile
            new_state = list(state)

            new_state[zero], new_state[new_position] = (
                new_state[new_position],
                new_state[zero]
            )

            neighbors.append(tuple(new_state))

    return neighbors


# BFS algorithm
def bfs(start, goal):

    queue = deque([start])

    visited = {start}

    parent = {start: None}

    while queue:

        current = queue.popleft()

        # Goal test
        if current == goal:

            path = []

            while current is not None:

                path.append(current)

                current = parent[current]

            path.reverse()

            return path

        # Generate successor states
        for neighbor in get_neighbors(current):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                queue.append(neighbor)

    return None


# Execute BFS
solution = bfs(initial_state, goal_state)


# Display solution
if solution:

    print("Solution Found!")

    print("Minimum moves:", len(solution) - 1)

    for step, state in enumerate(solution):

        print("\nStep", step)
        display(state)

else:

    print("No solution exists!")
