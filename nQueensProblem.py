from utils import Population


#these are the developed functions
selectionFunctions=["tournamentSelection", "highFitnessProportionSelection", "lowFitnessProportionSelection"]
mutationFunctions=["mutateConflictPositions", "mutateIndividualForRandom", "shiftPositionOnConflictMutation"]
crossOverFunctions=["crossHalf", "singlePoint"]

def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction):
    population=Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction)
    population.solve(maxGenerations)

solveNQueens(100, 7, 10000, selectionFunctions[1], mutationFunctions[2], crossOverFunctions[1])