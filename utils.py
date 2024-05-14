import random

class Population:
    def __init__(self, size, n, selectionFunction, mutationFunction, crossOverFunction):
        self.size = size
        self.n = n
        self.selectionFunction=selectionFunction
        self.mutationFunction=mutationFunction
        self.crossOverFunction=crossOverFunction
        self.bestPosition=[]
        self.bestFitness=100000
        self.generationCount=0
        firstPopulation=[]
        for _ in range(self.size):
            position=set()
            while len(position)<n:
                x = random.randint(0, n-1)
                y = random.randint(0, n-1)
                position.add((x, y))
            firstPopulation.append(list(position))
        self.currentPopulation=firstPopulation
        self.currentFitness=[]
        self.cumulativeNormalizedFitness=[]
    
    def solve(self, maxGenerations):
        if self.n==1:
            print("Answer: (0,0),  duh")
            return 
        elif self.n==2 or self.n==3 or self.n<1:
            print("No solution")
            return
        else:
            while self.generationCount<maxGenerations:
                self.getFitnessOnPopulation()
                if self.bestFitness==0:
                    break
                self.pickAndMutate()
                self.crossOver()
                self.generationCount+=1
                print("Current Best Fitness: ", self.bestFitness)
            print("Best Fitness: ", self.bestFitness)
            print("Best Position: ", self.bestPosition)
            print("Generation Count: ", self.generationCount)
            self.printPosition(self.bestPosition)

    def crossOver(self):
        if self.crossOverFunction=="crossHalf":
            return 0

    def printPosition(self, pos):
        for i in range(self.n):
            str = ""
            for j in range(self.n):
                queen_found = False
                for queen in pos:
                    if queen[0] == i and queen[1] == j:
                        str += "Q  "
                        queen_found = True
                        break
                if not queen_found:
                    str += "X  "
            print(str)

    def pickAndMutate(self):
        for _ in range(len(self.currentPopulation)):
            self.mutate(self.pick())
            if self.bestFitness==0:
                break

    def pick(self):
        if(self.selectionFunction=="lowFitnessProportionSelection"):
            fitnessDistribution=self.cumulativeNormalizedFitness
        elif(self.selectionFunction=="highFitnessProportionSelection"):
            fitnessDistribution=[1 - x for x in self.cumulativeNormalizedFitness]
        rnd = random.uniform(0, 1)
        for i in range(len(fitnessDistribution)):
            if fitnessDistribution[i] > rnd:
                return i
        return len(fitnessDistribution) - 1

    def mutate(self, i):
        if self.mutationFunction=="mutateIndividualForRandom":
            individual=set()
        elif self.mutationFunction=="mutateConflictPosition":
            individual=self.currentPopulation[i]
            conflictIndexes=self.getConflictPositions(individual)
            individual.pop(conflictIndexes[0])
            individual.pop(conflictIndexes[1]-1)
            individual=set(individual)
        while len(individual)<self.n:
            x = random.randint(0, self.n-1)
            y = random.randint(0, self.n-1)
            individual.add((x, y))
        self.currentPopulation[i]=list(individual)
        self.currentFitness[i]=self.getFitnessOnIndividual(self.currentPopulation[i])
            
    def getConflictPositions(self, individual):
        fitnessCount=0
        for p1 in individual:
            for p2 in individual:
                if(p1!=p2):
                    fitnessCount += self.hasHorizontalConflict(p1, p2) + self.hasVerticalConflict(p1, p2) + self.hasDiagonalConflict(p1, p2)
                if fitnessCount>0:
                    return sorted([individual.index(p1), individual.index(p2)], reverse=True)

    def getFitnessOnPopulation(self):
        populationFitness=[]
        for position in self.currentPopulation:
            populationFitness.append(self.getFitnessOnIndividual(position))
        self.currentFitness=populationFitness
        self.cumulativeNormalizedFitness=self.normalizeFitness()
        
        
    def getFitnessOnIndividual(self, individual):
        fitnessCount=0
        for p1 in individual:
            for p2 in individual:
                if(p1!=p2):
                    fitnessCount += self.hasHorizontalConflict(p1, p2) + self.hasVerticalConflict(p1, p2) + self.hasDiagonalConflict(p1, p2)
        fitnessCount/=2
        if(self.bestFitness>fitnessCount):
            self.bestFitness=fitnessCount
            self.bestPosition=individual
        return int(fitnessCount)


    def normalizeFitness(self):
        totalFitness = sum(self.currentFitness)
        cumulativeNormalizedFitness = []
        fit = 0
        for fitness in self.currentFitness:
            fit += fitness / totalFitness
            cumulativeNormalizedFitness.append(fit)
        return cumulativeNormalizedFitness

    def hasHorizontalConflict(self, p1, p2):
        return p1[0]==p2[0]

    def hasVerticalConflict(self, p1, p2):
        return p1[1]==p2[1]

    def hasDiagonalConflict(self, p1, p2):
        majorDiagonal = p1[0] - p1[1] == p2[0] - p2[1]
        minorDiagonal = p1[0] + p1[1] == p2[0] + p2[1]
        return majorDiagonal or minorDiagonal