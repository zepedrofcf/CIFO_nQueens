import random

class Population:
    def __init__(self, size, n):
        self.size = size
        self.n = n
        self.bestPosition=[]
        self.bestFitness=100000
        self.generationCount=0
        firstPopulation=[]
        for _ in range(self.size):
            position=set()
            while len(position)<n:
                x = random.randint(0, n)
                y = random.randint(0, n)
                position.add((x, y))
            firstPopulation.append(list(position))
        self.currentPopulation=firstPopulation
        self.currentFitness=[]
    
    def solve(self, maxGenerations):
        while self.generationCount<maxGenerations:
            self.getFitnessOnPopulation()
            if self.bestFitness==0:
                break
            self.pickAndMutate()
            self.generationCount+=1
            print("Best Fitness: ", self.bestFitness)
            #print("Best Position: ", self.bestPosition)
        print("Generation Count: ", self.generationCount)

    def pickAndMutate(self):
        for _ in range(50):
            self.mutate(self.pick())
        

    def pick(self):
        normalizedCumulativeFitness= self.normalizeFitness()
        #print(normalizedCumulativeFitness)
        rnd= random.uniform(0,1)
        pick=0
        for i in range(len(normalizedCumulativeFitness)):
            if normalizedCumulativeFitness[i]>rnd:
                pick=i
                break
            else:
                pick = len(normalizedCumulativeFitness) - 1
        return pick

    def mutate(self, i):
        position=set()
        while len(position)<self.n:
            x = random.randint(0, self.n)
            y = random.randint(0, self.n)
            position.add((x, y))
        print(self.currentPopulation[i])
        print("mutate")
        self.currentPopulation[i]=list(position)
        print(self.currentPopulation[i])


    def getFitnessOnPopulation(self):
        populationFitness=[]
        for position in self.currentPopulation:
            populationFitness.append(self.getFitnessOnPosition(position))
        self.currentFitness=populationFitness
        
        
    def getFitnessOnPosition(self, position):
        fitnessCount=0
        for p1 in position:
            for p2 in position:
                fitnessCount += self.isHorizontal(p1, p2) + self.isVertical(p1, p2) + self.isDiagonal(p1, p2)
        fitnessCount/=2
        if(self.bestFitness>fitnessCount):
            self.bestFitness=fitnessCount
            self.bestPosition=position
        return int(fitnessCount)
    

    def normalizeFitness(self):
        totalFitness = sum(self.currentFitness)
        cumulativeNormalizedFitness = []
        fit = 0
        for fitness in self.currentFitness:
            fit += fitness / totalFitness
            cumulativeNormalizedFitness.append(fit)
        return cumulativeNormalizedFitness

    def isHorizontal(self, p1, p2):
        return p1[0]==p2[0]

    def isVertical(self, p1, p2):
        return p1[1]==p2[1]

    def isDiagonal(self, p1, p2):
        majorDiagonal = p1[0] - p1[1] == p2[0] - p2[1]
        minorDiagonal = p1[0] + p1[1] == p2[0] + p2[1]
        return majorDiagonal or minorDiagonal
        
