from utils import Population

def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction):
    population=Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction)
    population.solve(maxGenerations)

solveNQueens(200, 7, 100000, "highFitnessProportionSelection", "mutateConflictPosition", "crossHalf")