
def get_successors(state):
    a, b = state
    capacity_a = 4
    capacity_b = 3

    successors = []

    # 1. Fill Jug A
    successors.append((capacity_a, b))

    # 2. Fill Jug B
    successors.append((a, capacity_b))

    # 3. Empty Jug A
    successors.append((0, b))

    # 4. Empty Jug B
    successors.append((a, 0))

    # 5. Pour water from A into B
    pour = min(a, capacity_b - b)
    successors.append((a - pour, b + pour))

    # 6. Pour water from B into A
    pour = min(b, capacity_a - a)
    successors.append((a + pour, b - pour))

    # Remove duplicate states
    return list(dict.fromkeys(successors))


def dfs(start, goal_amount):
    stack = [start]
    visited = {start}
    parent = {start: None}

    while stack:
        current = stack.pop()

        # Check whether Jug A contains the target amount
        if current[0] == goal_amount:
            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            path.reverse()
            return path

        for neighbor in get_successors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return None


# Initial state and goal
start = (0, 0)
goal_amount = 2

solution = dfs(start, goal_amount)

if solution:
    print("Solution found!")
    print("Number of operations:", len(solution) - 1)

    for step, state in enumerate(solution):
        print(
            f"Step {step}: Jug A = {state[0]} L, "
            f"Jug B = {state[1]} L"
        )
else:
    print("No solution found.")
