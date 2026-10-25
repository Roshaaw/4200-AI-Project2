import random
import time


# Generate a random state where state[col] = row
# One queen per column placed in a random row
def generate_random_state(n):
    return [random.randint(0, n - 1) for _ in range(n)]


# Compute number of pairs of queens attacking each other
# Goal state has heuristic value h = 0
def heuristic(state):
    conflicts = 0
    n = len(state)

    for i in range(n):
        for j in range(i + 1, n):
            # same row
            if state[i] == state[j]:
                conflicts += 1

            # same diagonal
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1

    return conflicts


# Generate all neighboring states by moving one queen
# in one column to a different row
def generate_all_neighbors(state):
    neighbors = []
    n = len(state)

    for col in range(n):
        current_row = state[col]

        for row in range(n):
            if row != current_row:
                new_state = state.copy()
                new_state[col] = row
                neighbors.append(new_state)

    return neighbors


# Steepest-ascent hill climbing (no sideways moves)
# Returns final_state + number of steps taken
def hill_climbing(n):
    # Generate random starting state
    current_state = generate_random_state(n)
    current_h = heuristic(current_state)
    steps = 0

    while True:
        # Generate all neighbors of the current state
        neighbors = generate_all_neighbors(current_state)

        # Find the best heuristic value among neighbors
        best_h = min(heuristic(neighbor) for neighbor in neighbors)

        # Stop if no improvement is possible
        if best_h >= current_h:
            return current_state, steps

        # Choose randomly among neighbors with the best heuristic
        best_neighbors = [neighbor for neighbor in neighbors if heuristic(neighbor) == best_h]
        current_state = random.choice(best_neighbors)

        current_h = best_h
        steps += 1


# Run many random instances
def run_experiment(n, trials=200):
    solved = 0
    total_steps = 0
    total_time = 0.0

    solved_steps = 0
    solved_count = 0

    for _ in range(trials):
        start_time = time.perf_counter()
        final_state, steps = hill_climbing(n)
        end_time = time.perf_counter()

        h = heuristic(final_state)
        runtime = end_time - start_time

        total_steps += steps
        total_time += runtime

        if h == 0:
            solved += 1
            solved_steps += steps
            solved_count += 1

    success_rate = (solved / trials) * 100
    avg_steps = total_steps / trials
    avg_time = total_time / trials
    avg_solved_steps = solved_steps / solved_count if solved_count > 0 else 0

    return {
        "n": n,
        "trials": trials,
        "solved": solved,
        "success_rate": success_rate,
        "avg_steps": avg_steps,
        "avg_time": avg_time,
        "avg_solved_steps": avg_solved_steps,
    }


# Table form
def print_results_table(results):
    print("-" * 76)
    print(f"{'n':<6}{'Trials':<10}{'% Solved':<12}{'Avg Steps':<15}{'Avg Time (s)':<15}{'Avg Steps (Solved)':<18}")
    print("-" * 76)

    for r in results:
        print(f"{r['n']:<6}{r['trials']:<10}{r['success_rate']:<12.2f}{r['avg_steps']:<15.2f}{r['avg_time']:<15.6f}{r['avg_solved_steps']:<18.2f}")

    print("-" * 76)


# Print board configuration
def print_board(state):
    n = len(state)

    for row in range(n):
        line = ""
        for col in range(n):
            if state[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)


# Find and print multiple solved boards for a given n
# Only the final configurations are shown
def print_sample_solutions(n, num_samples=3):
    printed = 0
    seen_solutions = set()

    print(f"\nSample solutions for n = {n}:")

    while printed < num_samples:
        state, steps = hill_climbing(n)

        if heuristic(state) == 0:
            state_tuple = tuple(state)

            # Avoids printing the same solution twice
            if state_tuple not in seen_solutions:
                seen_solutions.add(state_tuple)
                printed += 1

                print(f"\nSolution {printed}:")
                print_board(state)


def main():
    # Use system randomness
    random.seed()

    # Test sizes
    test_sizes = [8, 12, 16]

    # Number of instances for each n (>100 as required)
    trials = 200

    results = []

    # Run experiments
    for n in test_sizes:
        result = run_experiment(n, trials)
        results.append(result)

    # Print table
    print_results_table(results)

    # Print 3 sample solutions for each n
    for n in test_sizes:
        print_sample_solutions(n, 3)


if __name__ == "__main__":
    main()