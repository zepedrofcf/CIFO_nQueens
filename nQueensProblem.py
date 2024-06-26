import random
import time 
import datetime
import os
from random import sample, uniform
import logging

class Population:
    def __init__(self, populationSize, n, selectionFunction, mutationFunction, crossOverFunction, elitism=True, eliteProportion=0.1):
        self.populationSize = populationSize
        self.n = n
        self.selectionFunction=selectionFunction
        self.mutationFunction=mutationFunction
        self.crossOverFunction=crossOverFunction
        self.elitismEnabled = elitism      # Set elitism True or False
        self.eliteProportion = eliteProportion     # Fraction of pop kept
        self.bestPosition=[]
        self.bestFitness=100000
        self.generationCount=0
        firstPopulation=[]
        self.same=0
        self.notSame=0
        self.startTime = time.time()
        for _ in range(self.populationSize):
            position=set()
            while len(position)< n:
                position.add((random.randint(0, n-1), random.randint(0, n-1)))
            firstPopulation.append(list(position))
        self.currentPopulation=firstPopulation
        self.currentFitness=[]
        self.cumulativeNormalizedFitness=[]
        self.nextPopulation=[]
    
    def solve(self, maxGenerations):
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
                self.doSelectionOfPopulation()
                if self.bestFitness==0:
                    break              
                self.nextPopulation=[]
                if self.elitismEnabled:
                    self.nextPopulation = self.getBest()
                self.crossOver()
                self.selectAndMutate()
                self.currentPopulation=self.nextPopulation
                self.getFitnessOnPopulation()
                self.generationCount+=1
            #print("Best Fitness: ", self.bestFitness)
            #print("n =", self.n)
            #print("Population Size =", self.populationSize)
            #print("Best Position: ", self.bestPosition)
            #print("Generation Count: ", self.generationCount)
            #self.printPosition(self.bestPosition)
            if self.bestFitness==0:
                print("Success!")
            else: 
                print("Failed to reach solution in ", self.generationCount, " generations...")
            executionTime = time.time() - self.startTime
            print("Execution time: ", format_time(executionTime))
            #print("%"," of usefull crossOvers: ", ((self.notSame/(self.same+self.notSame))*100), "%")
            return executionTime

    def doSelectionOfPopulation(self):
        newPopulation=[]
        for _ in range(len(self.currentPopulation)):
            newPopulation.append(self.currentPopulation[self.select()])
        self.currentPopulation=newPopulation

    def getBest(self):
        numbest = int(self.eliteProportion * self.populationSize)
        sortedPopulation = sorted(zip(self.currentPopulation, self.currentFitness), key=lambda x: x[1])
        return [individual for individual, _ in sortedPopulation[:numbest]]

    def crossOver(self):
        for _ in range(len(self.currentPopulation)):
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
                newIndividuals = self.cycleCrossOver(self.currentPopulation[firstParent], self.currentPopulation[secondParent])
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


    def cycleCrossOver(self, firstParent, secondParent):
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

    def GeometricSemantic(self, firstParent, secondParent):
        while True:
            firstOffspring = []
            secondOffspring = []
            for i in range(len(firstParent)):
                r1 = random.randint(0,1)
                r2 = random.randint(0,1)
                firstOffspring.append((
                    firstParent[i][0] * r1 + (1 - r1) * secondParent[i][0],
                    firstParent[i][1] * r1 + (1 - r1) * secondParent[i][1]))
                secondOffspring.append((
                    firstParent[i][0] * r2 + (1 - r2) * secondParent[i][0],
                    firstParent[i][1] * r2 + (1 - r2) * secondParent[i][1]))

            firstOffspring = list(set(firstOffspring))
            secondOffspring = list(set(secondOffspring))

            if len(firstOffspring) == self.n and len(secondOffspring) == self.n:
                break

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
        logging.debug("Starting selection and mutation process")
        # If the best fitness is already optimal (0), skip mutation
        if self.bestFitness == 0:
            logging.info("Optimal solution already found, skipping mutation")
            return
        while len(self.nextPopulation) < self.populationSize:
            selected_individual = self.select()
            if selected_individual is not None:
                logging.debug(f"Selected individual: {selected_individual}")
                self.mutate(selected_individual)
                if self.bestFitness == 0:
                    logging.info("Optimal solution found during mutation, stopping further mutations")
                    break
            else:
                logging.warning("Selected individual is None")
        logging.debug("Completed selection and mutation process")

    def select(self):
        #print(f"Generation: {self.generationCount}")
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
        self.nextPopulation.append(list(individual))
        #self.currentFitness[i]=self.getFitnessOnIndividual(self.currentPopulation[i])

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
            print("n =" , self.n)
            self.printPosition(self.bestPosition)
            genCount=self.generationCount
            print("Best Fitness ", self.bestFitness, ", at Generation ", genCount)
            if genCount>0:
                print("Average Rythm: ", round(genCount/(time.time() - self.startTime), 1),"Generations per second")
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