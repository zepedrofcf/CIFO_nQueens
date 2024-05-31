import random
import time 
import datetime
import os
from random import sample, uniform

class Population:
    def __init__(self, populationSize, n, selectionFunction, mutationFunction, crossOverFunction, elitism=False, elitismRate=0.1):
        self.populationSize = populationSize
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
        self.same=0
        self.notSame=0
        for indNumber in range(self.populationSize):
            position=[]
            for i in range(n):
                if indNumber%2==0:
                    position.append((random.randint(0, n-1),i))
                else:
                    position.append((i,random.randint(0, n-1)))
            firstPopulation.append(position)
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
            while self.generationCount < maxGenerations:
                self.getFitnessOnPopulation()
                self.doSelectionOfPopulation()
                if self.bestFitness==0:
                    break              
                self.crossOver()
                if self.elitismEnabled:
                    best = self.getbest()
                self.selectAndMutate()
                self.getFitnessOnPopulation()
                if self.elitismEnabled:
                    self.reintroduceBest(best)
                self.generationCount+=1
            #print("Best Fitness: ", self.bestFitness)
            #print("n =", self.n)
            #print("Population Size =", self.populationSize)
            #print("Best Position: ", self.bestPosition)
            #print("Generation Count: ", self.generationCount)
            #self.printPosition(self.bestPosition)
            executionTime = time.time() - startTime
            print("Execution time: ", format_time(executionTime))
            print("%"," of usefull crossOvers: ", ((self.notSame/(self.same+self.notSame))*100), "%")
            return executionTime

    def doSelectionOfPopulation(self):
        newPopulation=[]
        for _ in range(len(self.currentPopulation)):
            newPopulation.append(self.currentPopulation[self.select()])
        self.currentPopulation=newPopulation

    def getbest(self):
        numbest = int(self.elitismRate * self.populationSize)
        sortedPopulation = sorted(zip(self.currentPopulation, self.currentFitness), key=lambda x: x[1])
        return [individual for individual, _ in sortedPopulation[:numbest]]

    def reintroduceBest(self, best):
        numbest = len(best)
        remaining_population_size = self.populationSize - numbest
        self.currentPopulation[:numbest] = best
        for i in range(numbest):
            rand_individual = random.choice(self.currentPopulation[numbest:])
            self.currentPopulation[i] = rand_individual
            self.currentFitness[i] = self.getFitnessOnIndividual(best[i])

    def crossOver(self):
        for _ in range(len(self.currentPopulation)//2):
            firstParent = self.select()
            secondParent = self.select()
            count=0
            while firstParent==secondParent:
                secondParent=self.select()
                count+=1
            #print(count)
            if self.crossOverFunction == "crossHalf":
                newIndividuals = self.crossHalf(self.currentPopulation[firstParent], self.currentPopulation[secondParent])
            elif self.crossOverFunction == "crossSinglePoint":
                newIndividuals = self.singlePoint(self.currentPopulation[firstParent], self.currentPopulation[secondParent])
            elif self.crossOverFunction == "crossCycle":
                newIndividuals = self.Cycle(self.currentPopulation[firstParent], self.currentPopulation[secondParent])
            #elif self.crossOverFunction == "crossPartialMatched":
                #newIndividuals = self.PartialMatched(self.currentPopulation[firstParent], self.currentPopulation[secondParent])
            elif self.crossOverFunction == "crossGeometricSemantic":
                newIndividuals = self.GeometricSemantic(self.currentPopulation[firstParent], self.currentPopulation[secondParent])
        self.currentPopulation[firstParent] = newIndividuals[0]
        self.currentPopulation[secondParent] = newIndividuals[1]
        self.currentFitness[firstParent] = self.getFitnessOnIndividual(self.currentPopulation[firstParent])
        self.currentFitness[secondParent] = self.getFitnessOnIndividual(self.currentPopulation[secondParent])

    def crossHalf(self, firstParent, secondParent):
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
        if(firstParent==firstOffspring and secondParent==secondOffspring):
            self.same+=1
        else:
            self.notSame+=1
        return [list(firstOffspring), list(secondOffspring)]

    def singlePoint(self, firstParent, secondParent):
        firstOffspring = []
        secondOffspring = []
        attempts = 0
        idx = random.randint(1, len(firstParent) - 2)
        while len(set(firstOffspring)) != self.n and len(set(secondOffspring)) != self.n:
            firstOffspring = firstParent[:idx] + secondParent[idx:]
            secondOffspring = secondParent[:idx] + firstParent[idx:]
            idx = ((idx) % (self.n-1)) + 1
            attempts += 1
            if attempts==self.n-1:
                firstParent==firstOffspring
                secondParent==secondOffspring
                break
        if(firstParent==firstOffspring and secondParent==secondOffspring):
            self.same+=1
            #print("first par", firstParent, "second par",secondParent)
            #print("first off", firstOffspring, "second off",  secondOffspring)
        else:
            self.notSame+=1
        return firstOffspring, secondOffspring


    def Cycle(self, firstParent, secondParent):
        size = len(firstParent)
        firstOffspring = [None]*size
        secondOffspring = [None]*size
        while None in firstOffspring:
            index = firstOffspring.index(None)
            val1 = firstParent[index]
            val2 = secondParent[index]
            while val1 != val2:
                firstOffspring[index] = firstParent[index]
                secondOffspring[index] = secondParent[index]
                val2 = secondParent[index]
                if val2 in firstParent:
                    index = firstParent.index(val2)
                else:
                    val1 = val2
            for element in firstOffspring:
                if element is None:
                    index = firstOffspring.index(None)
                    if firstOffspring[index] is None:
                        firstOffspring[index] = secondParent[index]
                        secondOffspring[index] = firstParent[index]
        if(firstParent==firstOffspring and secondParent==secondOffspring):
            self.same+=1
        else:
            self.notSame+=1

        return firstOffspring, secondOffspring

    def PartialMatched(self, firstParent, secondParent):
        start = sample(range(len(firstParent)),2)
        start.sort()

        def PartialMatched_offspring(x,y):
            startNew = [None]*len(x)
            startNew[start[0]:start[1]] = x[start[0]:start[1]]
            list = set(y[start[0]:start[1]]) - set(x[start[0]:start[1]])

            for i in list:
                temp = x[y.index(i)]
                if temp in y:
                    index = y.index(temp)
                    while startNew[index] is not None:
                        temp = x[index]
                        if temp in y:
                            index = y.index(temp)
                    startNew[index] = i

            while None in startNew:
                index = startNew.index(None)
                startNew[index] = y[index]
            return startNew

        firstOffspring, secondOffspring = PartialMatched_offspring(firstParent, secondParent), PartialMatched_offspring(secondParent, firstParent)

        return firstOffspring, secondOffspring

    def GeometricSemantic(self, firstParent, secondParent):
        firstOffspring = [None]*len(firstParent)
        secondOffspring = [None]*len(firstParent)
        for i in range(len(firstParent)):
            r1 = uniform(0,1)
            r2 = uniform(0,1)
            firstOffspring[i] = (
                float(firstParent[i][0]) * r1 + (1 - r1) * float(secondParent[i][0]),
                float(firstParent[i][1]) * r1 + (1 - r1) * float(secondParent[i][1])
            )
            secondOffspring[i] = (
                float(firstParent[i][0]) * r2 + (1 - r2) * float(secondParent[i][0]),
                float(firstParent[i][1]) * r2 + (1 - r2) * float(secondParent[i][1])
            )
        if(firstParent==firstOffspring and secondParent==secondOffspring):
            self.same+=1
        else:
            self.notSame+=1
        return firstOffspring, secondOffspring


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
        for _ in range(self.populationSize - numbest):
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
            i=0
            while rnd < fitnessDistribution[i+1] and i<len(fitnessDistribution):
                i+=1
            return i

    def mutate(self, i):
        individual=set()
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
        while len(individual)<self.n:
            individual.add((random.randint(0, self.n-1), random.randint(0, self.n-1)))
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
        poweredFitness = [individual for individual in self.currentFitness]
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