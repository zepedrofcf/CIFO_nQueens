from utils import Population

def solveNQueens(populationSize, n, maxGenerations):
    population=Population(populationSize, n)
    population.solve(maxGenerations)

solveNQueens(100, 8, 100)
