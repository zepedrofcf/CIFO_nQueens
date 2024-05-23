from utils import Population
import random

#these are the developed functions
selectionFunctions=["Tournament Selection", "Roulette Wheel Selection"]
mutationFunctions=["Conflict Position for Random", "Individual For Random", "Shift Position On Conflict", "Boundary Mutation"]
crossOverFunctions=["crossHalf", "singlePoint"]

def solveNQueens(populationSize, n, maxGenerations, selectionFunction, mutationFunction, crossOverFunction):
    population=Population(populationSize, n, selectionFunction, mutationFunction, crossOverFunction)
    population.solve(maxGenerations)

solveNQueens(200, 7, 10000, selectionFunctions[1], mutationFunctions[3], crossOverFunctions[1])