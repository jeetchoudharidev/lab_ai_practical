
import random
from itertools import permutations

# Step 1: Define cities
cities = ["A", "B", "C", "D", "E"]

# Step 2: Define distance matrix
distance = {
    "A": {"A": 0, "B": 10, "C": 15, "D": 20, "E": 12},
    "B": {"A": 10, "B": 0, "C": 35, "D": 25, "E": 18},
    "C": {"A": 15, "B": 35, "C": 0, "D": 30, "E": 20},
    "D": {"A": 20, "B": 25, "C": 30, "D": 0, "E": 16},
    "E": {"A": 12, "B": 18, "C": 20, "D": 16, "E": 0}
}

# Step 3: Calculate total route cost
def calculate_cost(route):

    total = 0

    # Distance between consecutive cities
    for i in range(len(route) - 1):
        total += distance[route[i]][route[i + 1]]

    # Return to starting city
    total += distance[route[-1]][route[0]]

    return total


# Step 4: Generate neighbouring routes
def get_neighbors(route):

    neighbors = []

    # Keep starting city A fixed
    for i in range(1, len(route)):
        for j in range(i + 1, len(route)):

            new_route = list(route)

            # Swap two cities
            new_route[i], new_route[j] = (
                new_route[j], new_route[i]
            )

            neighbors.append(tuple(new_route))

    return neighbors


# Step 5: Local Beam Search
def local_beam_search(k, max_iterations):

    # Generate all possible routes with A fixed
    all_routes = [
        ("A",) + p
        for p in permutations(cities[1:])
    ]

    # Generate K random initial routes
    random.seed(42)
    beam = random.sample(all_routes, k)

    best_route = min(beam, key=calculate_cost)
    best_cost = calculate_cost(best_route)

    visited = set(beam)

    print("INITIAL CANDIDATE ROUTES")

    for route in beam:
        print(route, "Cost:", calculate_cost(route))

    # Search iterations
    for iteration in range(max_iterations):

        candidates = []

        # Generate neighbours of every route
        for route in beam:

            for neighbor in get_neighbors(route):

                if neighbor not in visited:
                    candidates.append(neighbor)
                    visited.add(neighbor)

        # Stop if no new candidates are available
        if not candidates:
            break

        # Select the K routes with minimum cost
        candidates.sort(key=calculate_cost)

        beam = candidates[:k]

        # Update best solution
        current_best = min(beam, key=calculate_cost)
        current_cost = calculate_cost(current_best)

        if current_cost < best_cost:
            best_route = current_best
            best_cost = current_cost

        print(
            f"Iteration {iteration + 1}: "
            f"Best Cost = {best_cost}"
        )

    return best_route, best_cost


# Step 6: Execute the algorithm
K = 3
MAX_ITERATIONS = 20

best_route, best_cost = local_beam_search(
    K,
    MAX_ITERATIONS
)

# Step 7: Display result
print("\nFINAL RESULT")
print("Best Route:", " -> ".join(
    best_route + (best_route[0],)
))
print("Minimum Distance Found:", best_cost)
