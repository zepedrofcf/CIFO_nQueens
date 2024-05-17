from utils import Population
import random


#these are the developed functions
selectionFunctions=["tournamentSelection", "highFitnessProportionSelection", "lowFitnessProportionSelection"]
mutationFunctions=["mutateConflictPositions", "mutateIndividualForRandom", "shiftPositionOnConflictMutation"]
crossOverFunctions=["crossHalf"]

def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction):
    population=Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction)
    population.solve(maxGenerations)

solveNQueens(150, 7, 10000, selectionFunctions[1], mutationFunctions[2], crossOverFunctions[0])
