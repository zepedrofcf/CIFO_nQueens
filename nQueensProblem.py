from utils import Population

def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction):
    population=Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction)
    population.solve(maxGenerations)

solveNQueens(100, 6, 200, "highFitnessProportionSelection", "mutateConflictPosition", "crossHalf")