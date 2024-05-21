from utils import Population


#these are the developed functions
selectionFunctions=["tournamentSelection", "highFitnessProportionSelection", "lowFitnessProportionSelection"]
mutationFunctions=["mutateConflictPositions", "mutateIndividualForRandom", "shiftPositionOnConflictMutation"]
crossOverFunctions=["crossHalf", "singlePoint"]

def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction):
    population=Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction)
    population.solve(maxGenerations)

solveNQueens(200, 8, 10000, selectionFunctions[0], mutationFunctions[2], crossOverFunctions[1])