from utils import Population

def solveNQueens(n, populationSize, maxGenerations):
    population=Population(populationSize, n)
    population.solve(maxGenerations)

solveNQueens(4, 10, 10)
