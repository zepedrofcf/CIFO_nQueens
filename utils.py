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
                x = random.randint(0, n-1)
                y = random.randint(0, n-1)
                position.add((x, y))
            firstPopulation.append(list(position))
        self.currentPopulation=firstPopulation
        self.currentFitness=[]
    
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
                self.generationCount+=1
                print("Best Fitness: ", self.bestFitness)
            print("Best Fitness: ", self.bestFitness)
            print("Best Position: ", self.bestPosition)
            print("Generation Count: ", self.generationCount)
            self.printPosition(self.bestPosition)

    def printPosition(self, pos):
        for i in range(self.n):
            str = ""
            for j in range(self.n):
                queen_found = False
                for queen in pos:
                    if queen[0] == i and queen[1] == j:
                        str += "Q"
                        queen_found = True
                        break
                if not queen_found:
                    str += "x"
            print(str)

    def pickAndMutate(self):
        for _ in range(self.size):
            self.mutate(self.pick())

    def pick(self):
        normalizedCumulativeFitness= self.normalizeFitness()
        rnd = random.uniform(0, 1)
        for i in range(len(normalizedCumulativeFitness)):
            if normalizedCumulativeFitness[i] > rnd:
                return i
        return len(normalizedCumulativeFitness) - 1

    def mutate(self, i):
        position=set()
        while len(position)<self.n:
            x = random.randint(0, self.n-1)
            y = random.randint(0, self.n-1)
            position.add((x, y))
        #print(self.currentPopulation[i])
        #print("mutate")
        self.currentPopulation[i]=list(position)
        #print(self.currentPopulation[i])


    def getFitnessOnPopulation(self):
        populationFitness=[]
        for position in self.currentPopulation:
            populationFitness.append(self.getFitnessOnPosition(position))
        self.currentFitness=populationFitness
        
        
    def getFitnessOnPosition(self, position):
        fitnessCount=0
        for p1 in position:
            for p2 in position:
                if(p1!=p2):
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