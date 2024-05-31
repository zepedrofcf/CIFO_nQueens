from nQueensProblem import Population
import random
#import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches


#these are the developed functions
selectionFunctions=["Tournament Selection", "Roulette Wheel Selection"]
mutationFunctions=["Position with conflict for random", "Individual For Random", "Shift Coordinate on Position with Conflict"]
crossOverFunctions=["crossHalf", "crossSinglePoint", "crossCycle", "crossGeometricSemantic"]


def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction):
    population=Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction)
    population.solve(maxGenerations)

solveNQueens(150, 15, 1000, selectionFunctions[0], mutationFunctions[2], crossOverFunctions[3])



##################################################################################################
# For 2D graphs we can only have 2 sets of parameters changing max.
# So need to do it in more than one section to compare everything.

#### VARIABLE PARAMETERS: "n" and "populationSize" with elitism option ####

'''
def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction, elitism, elitismRate=0.1):
    population = Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction, elitism, elitismRate)
    executionTime = population.solve(maxGenerations)
    return executionTime     # Return execution time

def Statistics(populationSizes, maxGenerations, selectionFunction, mutationFunction, crossOverFunction, n_values, elitismoption, num_runs=30):
    results = {elitism: {size: {} for size in populationSizes} for elitism in elitismoption}

    for elitism in elitismoption:
        for populationSize in populationSizes:
            for n in n_values:
                total_time = 0
                for _ in range(num_runs):
                    executionTime = solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction, elitism)
                    if executionTime is not None:
                        total_time += executionTime
                average_time = total_time / num_runs
                results[elitism][populationSize][n] = average_time
                print(f"Elitism {elitism}: Average time for n={n} with population size {populationSize}: {average_time:.4f} seconds")

    return results

def plotResults(results):
    plt.figure(figsize=(9, 6))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple']

    for elitism, elitism_results in results.items():
        for pop_size, pop_results in elitism_results.items():
            n_values = sorted(pop_results.keys())
            average_times = [pop_results[n] for n in n_values]
            plt.plot(n_values, average_times, marker='o', color=colors[len(plt.gca().lines) % len(colors)],
                     label=f'Elitism: {elitism}, Population Size: {pop_size}')

    plt.xlabel('Board Size (n)')
    plt.ylabel('Average Time to Solve (seconds)')
    plt.title('Average Time vs Board Size')
    plt.grid(True)
    plt.xticks(range(min(n_values), max(n_values) + 1))
    plt.legend()
    plt.show()


n_values = range(4, 10)   # only from 4 onwards
populationSizes = [100]
elitismoption = [True]
results = Statistics(populationSizes, 20000, selectionFunctions[1], mutationFunctions[2], crossOverFunctions[0], n_values, elitismoption=elitismoption)
plotResults(results)
'''


#### VARIABLE PARAMETERS: "n" and "[selectionFunctions,mutationFunctions,crossOverFunctions]" ####

'''
def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction):
    population = Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction)
    executionTime = population.solve(maxGenerations)
    return executionTime  # Return execution time

def Statistics(populationSize, maxGenerations, selectionFunctions_, mutationFunctions_, crossOverFunctions_, n_values, num_runs=30):
    results = {(sel_func, mut_func, cross_func): {} for sel_func in selectionFunctions_ for mut_func in mutationFunctions_ for cross_func in crossOverFunctions_}

    for sel_func in selectionFunctions_:
        for mut_func in mutationFunctions_:
            for cross_func in crossOverFunctions_:
                for n in n_values:
                    total_time = 0
                    for _ in range(num_runs):
                        executionTime = solveNQueens(populationSize, n, maxGenerations, sel_func, mut_func, cross_func)
                        if executionTime is not None:
                            total_time += executionTime
                    average_time = total_time / num_runs
                    results[(sel_func, mut_func, cross_func)][n] = average_time
                    print(f"Average time for n={n} with selection={sel_func}, mutation={mut_func}, crossover={cross_func}: {average_time:.4f} seconds")

    return results

def plotResults(results):
    plt.figure(figsize=(12, 8))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'cyan', 'magenta', 'gold', 'navy', 'teal']

    for i, ((sel_func, mut_func, cross_func), func_results) in enumerate(results.items()):
        n_values = sorted(func_results.keys())
        average_times = [func_results[n] for n in n_values]
        plt.plot(n_values, average_times, color=colors[i % len(colors)],
                 label=f'Sel: {sel_func}, Mut: {mut_func}, Cross: {cross_func}')

    plt.xlabel('Board Size (n)')
    plt.ylabel('Average Time to Solve (seconds)')
    plt.title('Average Time vs Different Function Combinations')
    plt.grid(True)
    plt.xticks(range(min(n_values), max(n_values) + 1))
    plt.legend()
    plt.show()


n_values = range(4, 8)
populationSize = 200
selectionFunctions_=["Roulette Wheel Selection"]
mutationFunctions_=["Position with conflict for random", "Shift Coordinate on Position with Conflict"]
crossOverFunctions_=["crossHalf","crossSinglePoint"]
results = Statistics(populationSize, 10000, selectionFunctions_, mutationFunctions_, crossOverFunctions_, n_values)
plotResults(results)
'''


#### ANALYZE IMPACT OF RANDOM INITIAL POSITIONS ####

'''
def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction, elitism, elitismRate=0.1):
    population = Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction, elitism, elitismRate)
    executionTime = population.solve(maxGenerations)
    return executionTime     # Return execution time

def Statistics(changing_variable, values, maxGenerations, selectionFunction, mutationFunction, crossOverFunction, n, populationSize, num_runs=30, elitism=True, elitismRate=0.1):
    results = {value: [] for value in values}

    for value in values:
        execution_times = []
        for _ in range(num_runs):
            if changing_variable == "populationSize":
                executionTime = solveNQueens(value, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction, elitism, elitismRate)
            elif changing_variable == "selectionFunction":
                executionTime = solveNQueens(populationSize, n, maxGenerations, value, mutationFunction, crossOverFunction, elitism, elitismRate)
            elif changing_variable == "mutationFunction":
                executionTime = solveNQueens(populationSize, n, maxGenerations, selectionFunction, value, crossOverFunction, elitism, elitismRate)
            elif changing_variable == "crossOverFunction":
                executionTime = solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, value, elitism, elitismRate)
            elif changing_variable == "n":
                executionTime = solveNQueens(populationSize, value, maxGenerations, selectionFunction, mutationFunction, crossOverFunction, elitism, elitismRate)

            if executionTime is not None:
                execution_times.append(executionTime)
        results[value] = execution_times
        print(f"Execution times for {changing_variable}={value}: {execution_times}")

    # Turning measured change into percentage to the average value
    for value in results:
        avg_time = sum(results[value]) / len(results[value])
        results[value] = [((time - avg_time) / avg_time) * 100 for time in results[value]]
    return results

def plotResults(results, changing_variable):
    plt.figure(figsize=(10, 7))
    boxplot_data = []
    labels = []
    colors = [
        'lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightcyan',
        'lightgoldenrodyellow', 'lightgray', 'lightsalmon', 'lightsteelblue', 'lightpink']

    for idx, (value, times) in enumerate(results.items()):
        boxplot_data.append(times)
        labels.append(f'{value}')

    box = plt.boxplot(boxplot_data, patch_artist=True)
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    plt.axhline(0, color='black', linestyle='-', linewidth=1)
    plt.xlabel(changing_variable.capitalize())
    plt.ylabel('Relative Change (%)')
    plt.title(f'Impact of {changing_variable.capitalize()}')
    plt.xticks(range(1, len(labels) + 1), labels, rotation=0)
    plt.grid(True)

    legend_handles = [mpatches.Patch(color=colors[i], label=f'{changing_variable.capitalize()} {value}') for i, value in enumerate(results.keys())]
    plt.legend(handles=legend_handles, loc='upper left')
    plt.show()

# Inputs:
maxGenerations = 15000
num_runs = 30
changing_variable = "n"    # Change what you want to analyze
values = [5, 6, 7, 8]      # Values for the chosen variable
selectionFunction = "Roulette Wheel Selection"
mutationFunction = "Shift Coordinate on Position with Conflict"
crossOverFunction = "crossHalf"
n = 5
populationSize = 100
elitism = True
elitismRate = 0.1

# Get statistics
results = Statistics(changing_variable, values, maxGenerations, selectionFunction, mutationFunction, crossOverFunction, n, populationSize, num_runs, elitism, elitismRate)
plotResults(results, changing_variable)
'''




