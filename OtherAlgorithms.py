from nQueensProblem import Population
from itertools import permutations
import random
import math
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter



def is_valid(board, n):
    for i in range(n):
        for j in range(i + 1, n):
            if abs(board[i] - board[j]) == j - i:
                return False
    return True

def bruteforce(n):
    results = []
    cols = range(n)
    for combo in permutations(cols):
        if is_valid(combo, n):
            results.append(combo)
    return results



def heuristic(state):
    n = len(state)
    attacking_pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                attacking_pairs += 1
    return attacking_pairs


def neighbor(state):
    n = len(state)
    new_state = state[:]
    col1 = random.randint(0, n - 1)
    col2 = random.randint(0, n - 1)
    while col1 == col2:
        col2 = random.randint(0, n - 1)
    new_state[col1], new_state[col2] = new_state[col2], new_state[col1]
    return new_state


def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)


def simulated_annealing(n):
    current_state = list(range(n))
    random.shuffle(current_state)
    current_cost = heuristic(current_state)

    T = 1.0
    T_min = 0.00001
    alpha = 0.99

    while T > T_min:
        i = 0
        while i < 100:
            new_state = neighbor(current_state)
            new_cost = heuristic(new_state)
            if acceptance_probability(current_cost, new_cost, T) > random.random():
                current_state = new_state
                current_cost = new_cost
            i += 1
        T *= alpha

    return current_state, current_cost


def is_safe(board, row, col):
    for i in range(col):
        if board[i] == row or \
                abs(board[i] - row) == abs(i - col):
            return False
    return True


def solve_nqueens_util(board, col, solutions):
    n = len(board)
    if col == n:
        solutions.append(board[:])
        return

    for row in range(n):
        if is_safe(board, row, col):
            board[col] = row
            solve_nqueens_util(board, col + 1, solutions)
            board[col] = -1


def solve_nqueens(n):
    board = [-1] * n
    solutions = []
    solve_nqueens_util(board, 0, solutions)
    return solutions

def solve_nqueens_one(n):
    def solve_util(board, col):
        if col == n:
            return board[:]
        for row in range(n):
            if is_safe(board, row, col):
                board[col] = row
                result = solve_util(board, col + 1)
                if result:
                    return result
                board[col] = -1
        return False

    board = [-1] * n
    return solve_util(board, 0)




def solveNQueensGA(n):
    populationSize = 100
    maxGenerations = 1000
    selectionFunction = "Tournament Selection"
    mutationFunction = "Position with conflict for random"
    crossOverFunction = "crossSinglePoint"
    population = Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction, elitism=True, eliteProportion=0.1)
    found = population.solve(maxGenerations)
    if population.bestFitness == 0:
        return [population.bestPosition]
    return []

def time_algorithm(algo, n, *args):
    start_time = time.time()
    results = algo(n, *args)
    end_time = time.time()
    return len(results), end_time - start_time

def time_simulated_annealing(algo, n):
    start_time = time.time()
    solution, cost = algo(n)
    end_time = time.time()
    found_solution = (cost == 0)
    return found_solution, end_time - start_time

def time_algorithm_one_solution(algo, n):
    start_time = time.time()
    solution = algo(n)
    end_time = time.time()
    found_solution = isinstance(solution, list)
    return found_solution, end_time - start_time

def format_time(x, pos=None):
    total_seconds = int(x)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"

n_values = range(4, 26)
algorithms = {
#    "Brute Force": bruteforce,
#    "Backtracking": solve_nqueens,
#    "Backtracking (One solution)": solve_nqueens_one,
    "Simulated Annealing": simulated_annealing,
    "Genetic Algorithm": solveNQueensGA
}
times = {name: [] for name in algorithms.keys()}
solutions_count = {name: [] for name in algorithms.keys()}

for n in n_values:
    print(f"Board Size: {n}")
    for name, algo in algorithms.items():
        if "One solution" in name:
            found_solution, time_taken = time_algorithm_one_solution(algo, n)
            num_solutions = 1 if found_solution else 0
        else:
            num_solutions, time_taken = time_algorithm(algo, n)
        times[name].append(time_taken)
        solutions_count[name].append(num_solutions)
        print(f"{name}: {num_solutions} solutions found in {time_taken:.4f} seconds")


# Plotting time comparison
plt.figure(figsize=(10, 6))
formatter = FuncFormatter(format_time)
for name, time_data in times.items():
    plt.plot(list(n_values), time_data, label=name + " Time", marker='o')

plt.xlabel('Number of Queens (N)')
plt.ylabel('Time Taken')
plt.title('Time Comparison of N-Queens Solution Algorithms')
plt.legend()
plt.grid(True)
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()

