import random
import time


def generate_random_board(n):
    # Create a random permutation of 0 to n-1
    board = list(range(n))
    random.shuffle(board)
    return board


def count_conflicts(board):
    # Count diagonal conflicts
    n = len(board)
    conflicts = 0

    for i in range(n):
        for j in range(i + 1, n):
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def fitness(board):
    # Higher fitness is better
    n = len(board)
    max_pairs = n * (n - 1) // 2
    return max_pairs - count_conflicts(board)


def is_solution(board):
    # A solution = zero conflicts
    return count_conflicts(board) == 0


def tournament_selection(population, tournament_size=3):
    # Pick a few random individuals and return the best one
    candidates = random.sample(population, tournament_size)
    return max(candidates, key=fitness)


def ordered_crossover(parent1, parent2):
    # Ordered crossover for permutation representation
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))

    child = [-1] * n

    for i in range(start, end + 1):
        child[i] = parent1[i]

    p2_index = 0
    for i in range(n):
        if child[i] == -1:
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]

    return child


def mutate(board, mutation_rate=0.1):
    # Swap mutation
    new_board = board[:]

    if random.random() < mutation_rate:
        i, j = random.sample(range(len(new_board)), 2)
        new_board[i], new_board[j] = new_board[j], new_board[i]

    return new_board


def genetic_algorithm(n, population_size=100, max_generations=3000, mutation_rate=0.15, elite_size=10):
    # Genetic algorithm
    start_time = time.time()

    population = [generate_random_board(n) for _ in range(population_size)]

    for generation in range(1, max_generations + 1):
        best = max(population, key=fitness)

        if is_solution(best):
            runtime = time.time() - start_time
            return best, generation, runtime

        population.sort(key=fitness, reverse=True)
        new_population = population[:elite_size]

        while len(new_population) < population_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)

            child = ordered_crossover(parent1, parent2)
            child = mutate(child, mutation_rate)

            new_population.append(child)

        population = new_population

    runtime = time.time() - start_time
    best = max(population, key=fitness)

    if is_solution(best):
        return best, max_generations, runtime

    return None, max_generations, runtime


def print_board_grid(board):
    # Print board (grid format) 
    n = len(board)

    for row in range(n):
        line = []
        for col in range(n):
            if board[col] == row:
                line.append("Q")
            else:
                line.append(".")
        print(" ".join(line))
    print()


def run_experiments():
    # Running 10 instances for each n
    test_sizes = [8, 12, 16]
    runs_per_n = 10

    for n in test_sizes:
        solved = 0
        total_generations = 0
        total_runtime = 0.0
        sample_solutions = []

        print("=" * 60)
        print(f"Genetic Algorithm Results for n = {n}")
        print("=" * 60)

        for run in range(runs_per_n):
            solution, generations, runtime = genetic_algorithm(
                n=n,
                population_size=100,
                max_generations=3000,
                mutation_rate=0.15,
                elite_size=10
            )

            total_generations += generations
            total_runtime += runtime

            if solution is not None:
                solved += 1

                if len(sample_solutions) < 3 and solution not in sample_solutions:
                    sample_solutions.append(solution)

        success_rate = (solved / runs_per_n) * 100
        avg_generations = total_generations / runs_per_n
        avg_runtime = total_runtime / runs_per_n

        print("Summary:")
        print(f"Success rate: {success_rate:.1f}%")
        print(f"Average generations: {avg_generations:.2f}")
        print(f"Average runtime: {avg_runtime:.6f} sec")
        print()

        print(f"3 sample solutions for n = {n}:")
        if sample_solutions:
            for i, solution in enumerate(sample_solutions, start=1):
                print(f"Sample {i}:")
                print_board_grid(solution)
        else:
            print("No solved configurations found.")
            print()


if __name__ == "__main__":
    run_experiments()