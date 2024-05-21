import random
import time 
import datetime
import os


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
                self.crossOver()
                self.pickAndMutate()
                self.generationCount+=1
            print("Best Fitness: ", self.bestFitness)
            print("n =", self.n)
            print("Population Size =", self.size)
            print("Best Position: ", self.bestPosition)
            print("Generation Count: ", self.generationCount)
            self.printPosition(self.bestPosition)
            print("Execution time: ", format_time(time.time() - startTime))

    def crossOver(self):
        if self.crossOverFunction=="crossHalf" or self.crossOverFunction=="singlePoint":
            for _ in range(len(self.currentPopulation)):
                first=self.pick()
                second=self.pick()
                if self.crossOverFunction=="singlePoint":
                    newIndividuals=self.singlePoint(self.currentPopulation[first], self.currentPopulation[second])
                elif self.crossOverFunction=="crossHalf":
                    newIndividuals=self.mixTwoHalves(self.currentPopulation[first], self.currentPopulation[second])
                self.currentPopulation[first]=newIndividuals[0]
                self.currentPopulation[second]=newIndividuals[1]
                self.currentFitness[first]=self.getFitnessOnIndividual(self.currentPopulation[first])
                self.currentFitness[second]=self.getFitnessOnIndividual(self.currentPopulation[second])

    def singlePoint(self, first, second):
        firstNew=[]
        secondNew=[]
        while len(set(firstNew))!=self.n and len(set(secondNew))!=self.n:
            idx = random.randint(1, len(first) - 1)
            firstNew = first[:idx] + second[idx:]
            secondNew = first[:idx] + second[idx:]
        return firstNew, secondNew

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
        if(self.selectionFunction=="tournamentSelection"):
            contestants=random.sample(self.currentPopulation, 2)
            return self.currentPopulation.index(self.makeTournament(contestants[0],contestants[1]))
        else:
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
            individual.pop(conflictIndexes[1] - 1)
            individual=set(individual)
        elif self.mutationFunction=="shiftPositionOnConflictMutation":
            individual=self.currentPopulation[i].copy()
            idx=self.getConflictPositions(individual)[random.randint(0,1)]
            oldPosition=list(individual.pop(idx))
            shiftOrientation=random.randint(0,1)
            shiftDirection=random.choice([-1, 1])
            individual=set(individual)
            while len(individual)<self.n:
                newPosition=oldPosition
                newPosition[shiftOrientation]=(newPosition[shiftOrientation]+shiftDirection)%self.n
                newPosition=tuple(newPosition)
                individual.add(newPosition)
            #for the case where all positions were lined up
            if len(individual)<self.n:
                newPosition=oldPosition
                newPosition[(shiftOrientation+1)%2]=(newPosition[shiftOrientation]+shiftDirection)%self.n
                newPosition=tuple(newPosition)
                individual.add(newPosition) 
        """ elif self.mutationFunction == "boundaryMutation":
            individual = set(self.currentPopulation[i])
            queen_to_move = random.choice(list(individual))
            new_position = (random.randint(0, self.n - 1), random.choice([0, self.n - 1]))
            individual.remove(queen_to_move)
            individual.add(new_position) """
        while len(individual) < self.n:
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
                    fitnessCount += hasHorizontalConflict(p1, p2) + hasVerticalConflict(p1, p2) + hasDiagonalConflict(p1, p2)
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