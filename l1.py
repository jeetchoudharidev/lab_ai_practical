
# Model-Based Reflex Agent
# Improved version of the vacuum cleaner

environment = {
    "A": "Dirty",
    "B": "Dirty"
}

location = "A"

# Internal memory of the agent
internal_state = {
    "A": "Unknown",
    "B": "Unknown"
}


def model_based_agent(location, status, memory):

    # Update memory with current observation
    memory[location] = status

    # Clean the current room if dirty
    if status == "Dirty":
        return "SUCK"

    # If A is clean but B is unknown or dirty
    if location == "A":
        if memory["B"] != "Clean":
            return "RIGHT"

    # If B is clean but A is unknown or dirty
    if location == "B":
        if memory["A"] != "Clean":
            return "LEFT"

    # Both rooms have been observed clean
    return "STOP"


def execute_action(action, location, environment):

    if action == "SUCK":
        environment[location] = "Clean"

    elif action == "RIGHT":
        location = "B"

    elif action == "LEFT":
        location = "A"

    return location


# Simulation
for step in range(10):

    status = environment[location]

    action = model_based_agent(
        location,
        status,
        internal_state
    )

    print(
        f"Step {step + 1}: "
        f"Location={location}, "
        f"Status={status}, "
        f"Action={action}"
    )

    if action == "STOP":
        break

    location = execute_action(
        action,
        location,
        environment
    )

print("\nFinal Environment:", environment)
print("Agent Memory:", internal_state)
