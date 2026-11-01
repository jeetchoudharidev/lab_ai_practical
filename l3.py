
from collections import deque

# Initial and goal configurations
# Disks are stored from bottom to top.
initial_state = ((3, 2, 1), (), ())
goal_state = ((), (), (3, 2, 1))

rods = ["A", "B", "C"]


# Generate all legal next states
def get_successors(state):

    successors = []

    # Try every source rod
    for source in range(3):

        # Cannot move from an empty rod
        if len(state[source]) == 0:
            continue

        # Only the top disk can be moved
        disk = state[source][-1]

        # Try every destination rod
        for destination in range(3):

            # Cannot move to the same rod
            if source == destination:
                continue

            # Check whether destination is empty
            # or its top disk is larger
            if (
                len(state[destination]) == 0
                or state[destination][-1] > disk
            ):

                # Convert state into mutable lists
                new_state = [list(rod) for rod in state]

                # Move the top disk
                new_state[source].pop()
                new_state[destination].append(disk)

                # Convert back to immutable tuples
                new_state = tuple(
                    tuple(rod) for rod in new_state
                )

                move = (disk, rods[source], rods[destination])

                successors.append((new_state, move))

    return successors


# Breadth-First Search
def tower_of_hanoi_bfs(start, goal):

    queue = deque([start])

    visited = {start}

    # Store parent state and the move used
    parent = {start: None}

    while queue:

        current_state = queue.popleft()

        # Check goal
        if current_state == goal:

            path = []
            moves = []

            # Reconstruct path backwards
            while current_state is not None:

                path.append(current_state)

                previous = parent[current_state]

                if previous is not None:
                    previous_state, move = previous
                    moves.append(move)
                    current_state = previous_state
                else:
                    current_state = None

            path.reverse()
            moves.reverse()

            return path, moves

        # Explore legal next states
        for next_state, move in get_successors(current_state):

            if next_state not in visited:

                visited.add(next_state)

                parent[next_state] = (current_state, move)

                queue.append(next_state)

    return None, None


# Display solution
path, moves = tower_of_hanoi_bfs(
    initial_state,
    goal_state
)

print("TOWER OF HANOI - STATE SPACE SEARCH")
print("------------------------------------")

if path:

    print("Solution Found!")
    print("Total moves:", len(moves))

    for i, move in enumerate(moves, start=1):

        disk, source, destination = move

        print(
            f"Move {i}: Disk {disk} "
            f"from {source} to {destination}"
        )

    print("\nState-by-state representation:")

    for i, state in enumerate(path):

        print(f"State {i}: {state}")

else:
    print("No solution found.")
