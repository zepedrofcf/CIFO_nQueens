import random
import time 
import datetime
import os


class Population:
    def __init__(self, size, n, selectionFunction, mutationFunction, crossOverFunction, elitism=False, elitismRate=0.1):
        self.size = size
        self.n = n
        self.selectionFunction=selectionFunction
        self.mutationFunction=mutationFunction
        self.crossOverFunction=crossOverFunction
        self.elitismEnabled = elitism      # Set elitism True or False
        self.elitismRate = elitismRate     # Fraction of pop kept
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
            while self.generationCount < maxGenerations:
                if self.bestFitness==0:
                    break
                if self.elitismEnabled:
                    best = self.getbest()
                self.crossOver()
                self.selectAndMutate()
                if self.elitismEnabled:
                    self.reintroducebest(best)
                self.generationCount+=1
            #print("Best Fitness: ", self.bestFitness)
            #print("n =", self.n)
            #print("Population Size =", self.size)
            #print("Best Position: ", self.bestPosition)
            #print("Generation Count: ", self.generationCount)
            #self.printPosition(self.bestPosition)
            executionTime = time.time() - startTime
            print("Execution time: ", format_time(executionTime))
            return executionTime

    def getbest(self):
        numbest = int(self.elitismRate * self.size)
        sortedPopulation = sorted(zip(self.currentPopulation, self.currentFitness), key=lambda x: x[1])
        return [individual for individual, _ in sortedPopulation[:numbest]]

    def reintroducebest(self, best):
        numbest = len(best)
        remaining_population_size = self.size - numbest
        self.currentPopulation[:numbest] = best
        for i in range(numbest):
            rand_individual = random.choice(self.currentPopulation[numbest:])
            self.currentPopulation[i] = rand_individual
            self.currentFitness[i] = self.getFitnessOnIndividual(best[i])

    def crossOver(self):
        if self.crossOverFunction == "crossHalf" or self.crossOverFunction == "Single Point":
            for _ in range(len(self.currentPopulation) - len(self.getbest())):
                firstParent = self.select()
                secondParent = self.select()
                if self.crossOverFunction == "Single Point":
                    newIndividuals = self.singlePoint(self.currentPopulation[firstParent],
                                                      self.currentPopulation[secondParent])
                elif self.crossOverFunction == "crossHalf":
                    newIndividuals = self.mixTwoHalves(self.currentPopulation[firstParent],
                                                       self.currentPopulation[secondParent])
                self.currentPopulation[firstParent] = newIndividuals[0]
                self.currentPopulation[secondParent] = newIndividuals[1]
                self.currentFitness[firstParent] = self.getFitnessOnIndividual(self.currentPopulation[firstParent])
                self.currentFitness[secondParent] = self.getFitnessOnIndividual(self.currentPopulation[secondParent])

    def singlePoint(self, firstParent, secondParent):
        firstOffspring=[]
        secondOffspring=[]
        attempts=0
        idx = random.randint(1, len(firstParent) - 1)
        while len(set(firstOffspring))!=self.n and len(set(secondOffspring))!=self.n or attempts>self.n:
            firstOffspring = firstParent[:idx] + secondParent[idx:]
            secondOffspring = firstParent[:idx] + secondParent[idx:]
            idx=(idx+1)%self.n
            attempts+=1
        return firstOffspring, secondOffspring

    def mixTwoHalves(self, firstParent, secondParent):
        firstOffspring=[]
        secondOffspring=[]
        all=sorted(firstParent+secondParent)
        firstOffspring=[]
        secondOffspring=[]
        for i in range(len(all)):
            if(i%2==0):
                firstOffspring.append(all[i])
            else:
                secondOffspring.append(all[i])
        return [list(firstOffspring), list(secondOffspring)]

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

    def selectAndMutate(self):
        numbest = len(self.getbest())
        for _ in range(self.size - numbest):
            self.mutate(self.select())
            if self.bestFitness == 0:
                break

    def select(self):
        if(self.selectionFunction=="Tournament Selection"):
            contestants=random.sample(self.currentPopulation, 2)
            return self.currentPopulation.index(self.makeTournament(contestants[0],contestants[1]))
        else:
            if(self.selectionFunction=="Roulette Wheel Selection"):
                fitnessDistribution=[1 - x for x in self.cumulativeNormalizedFitness]
            rnd = random.uniform(0, 1)
            for i in range(len(fitnessDistribution)):
                if fitnessDistribution[i] > rnd:
                    return i
            return len(fitnessDistribution) - 1

    def mutate(self, i):
        individual=set()
    #if self.mutationFunction=="Individual For Random":
        if self.mutationFunction=="Position with conflict for random":
            individual=self.currentPopulation[i].copy()
            conflictIndex=self.getConflictPosition(individual)
            individual.pop(conflictIndex)
            individual=set(individual)
        elif self.mutationFunction=="Shift Coordinate on Position with Conflict":
            individual=self.currentPopulation[i].copy()
            idx=self.getConflictPosition(individual)
            oldPosition=list(individual.pop(idx))
            shiftOrientation=random.randint(0,1)
            individual=set(individual)
            while len(individual)<self.n:
                newPosition=oldPosition
                newPosition[shiftOrientation]=(newPosition[shiftOrientation]+1)%self.n
                newPosition=tuple(newPosition)
                individual.add(newPosition)
            #for the case where all positions were lined up
            if len(individual)<self.n:
                newPosition=oldPosition
                newPosition[(shiftOrientation+1)%2]=(newPosition[shiftOrientation]+1)%self.n
                newPosition=tuple(newPosition)
                individual.add(newPosition)
        """elif self.mutationFunction == "Boundary Mutation":
            individual = self.currentPopulation[i]
            queen_to_move = random.choice(individual)
            new_position = (random.randint(0, self.n - 1), random.choice([0, self.n - 1]))
            if new_position not in individual:
                individual.pop(individual.index(queen_to_move))
                individual.append(new_position)"""
        while len(individual) < self.n:
            x = random.randint(0, self.n-1)
            y = random.randint(0, self.n-1)
            individual.add((x, y))
        self.currentPopulation[i]=list(individual)
        self.currentFitness[i]=self.getFitnessOnIndividual(self.currentPopulation[i])

    def getConflictPosition(self, individual):
        fitnessCount=0
        for p1 in individual:
            for p2 in individual:
                if(p1!=p2):
                    fitnessCount += hasHorizontalConflict(p1, p2) + hasVerticalConflict(p1, p2) + hasDiagonalConflict(p1, p2)
                if fitnessCount>0:
                    return random.choice([individual.index(p1), individual.index(p2)])

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
                    fitnessCount += hasHorizontalConflict(p1, p2) + hasVerticalConflict(p1, p2) + hasDiagonalConflict(p1, p2)
        fitnessCount/=2
        if(self.bestFitness>fitnessCount):
            self.bestFitness=fitnessCount
            self.bestPosition=individual
            clear_console()
            print("n =", self.n)
            self.printPosition(self.bestPosition)
            print("Best Fitness so far ", self.bestFitness, ", at Generation ", self.generationCount)
        return int(fitnessCount)


    def normalizeFitness(self):
        poweredFitness = [individual ** 10 for individual in self.currentFitness]
        totalFitness = sum(poweredFitness)
        cumulativeNormalizedFitness = []
        fit = 0
        for fitness in poweredFitness:
            fit += fitness / totalFitness
            cumulativeNormalizedFitness.append(fit)
        return cumulativeNormalizedFitness

    def makeTournament(self, p1,p2):
        f1=self.getFitnessOnIndividual(p1)
        f2=self.getFitnessOnIndividual(p2)
        if f1<f2:
            return p1
        else:
            return p2

def clear_console():
    if os.name == 'nt':
        os.system('cls')

def hasHorizontalConflict(p1, p2):
    return p1[0]==p2[0]

def hasVerticalConflict(p1, p2):
    return p1[1]==p2[1]

def hasDiagonalConflict(p1, p2):
    majorDiagonal = p1[0] - p1[1] == p2[0] - p2[1]
    minorDiagonal = p1[0] + p1[1] == p2[0] + p2[1]
    return majorDiagonal or minorDiagonal

def format_time(seconds):
    td = datetime.timedelta(seconds=seconds)
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)
    if hours == 0:
        if minutes == 0:
            if seconds == 0:
                return "{:d} milliseconds".format(milliseconds)
            return "{:d} seconds, {:d} milliseconds".format(seconds, milliseconds)
        return "{:d} minutes, {:d} seconds, {:d} milliseconds".format(minutes, seconds, milliseconds)
    return "{:d} hours, {:d} minutes, {:d} seconds, {:d} milliseconds".format(hours, minutes, seconds, milliseconds)