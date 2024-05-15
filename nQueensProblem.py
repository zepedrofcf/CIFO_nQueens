from utils import Population

#these are the possible functions
selectionFunctions=["highFitnessProportionSelection", "lowFitnessProportionSelection"]
mutationFunctions=["mutateConflictPosition", "mutateIndividualForRandom"]
crossOverFunctions=["crossHalf"]

def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction):
    population=Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction)
    population.solve(maxGenerations)

solveNQueens(200, 7, 10000, selectionFunctions[0], mutationFunctions[0], crossOverFunctions[0])