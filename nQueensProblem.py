from utils import Population

def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction):
    population=Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction)
    population.solve(maxGenerations)

solveNQueens(100, 5, 500, "highFitnessProportionSelection", "mutateConflictPosition", "crossHalf")
