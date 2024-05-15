import random
import time 
import datetime


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
        startTime = time.time()
        if self.n==1:
            print("Answer: (0,0)  duh")
            print("X")
            return 
        elif self.n==2 or self.n==3 or self.n<1:
            print("No solution")
            return
        else:
            self.getFitnessOnPopulation()
            while self.generationCount<maxGenerations:
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
            print("Execution time: ", format_time(time.time() - startTime))

    def crossOver(self):
        if self.crossOverFunction=="crossHalf":
            for _ in range(len(self.currentPopulation)):
                first=self.pick()
                second=self.pick()
                newIndividuals=self.mixTwoHalves(self.currentPopulation[first], self.currentPopulation[second])
                self.currentPopulation[first]=newIndividuals[0]
                self.currentPopulation[second]=newIndividuals[1]
                self.currentFitness[first]=self.getFitnessOnIndividual(self.currentPopulation[first])
                self.currentFitness[second]=self.getFitnessOnIndividual(self.currentPopulation[second])

    def mixTwoHalves(self, first, second):
        firstNew=[]
        secondNew=[]
        all=sorted(first+second)            
        firstNew=[]
        secondNew=[]
        for i in range(len(all)):
            if(i%2==0):
                firstNew.append(all[i])
            else:
                secondNew.append(all[i])
        return [list(firstNew), list(secondNew)]

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
            individual=self.currentPopulation[i].copy()
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
    
def format_time(seconds):
    td = datetime.timedelta(seconds=seconds)
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = td.seconds % 60
    if hours==0:
        if minutes==0:
            return "{:d} seconds".format(seconds)
        return "{:d} minutes, {:d} seconds".format(minutes, seconds)
    return "{:d} hours, {:d} minutes, {:d} seconds".format(hours, minutes, seconds)