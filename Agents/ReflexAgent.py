import random


def getRandomNumber(lowerBound=0, upperBound=10):
    return random.randint(lowerBound, upperBound)


class Agent:
    remainingCharge = 100
    fuelLeak = False

    def __init__(self, currentPosition):
        self.currentPosition = currentPosition

    def returnCurrentPosition(self):
        print(self.currentPosition)
        return self.currentPosition

    def updateFuelLeak(self):
        values = [True, False, False, False, False, False]
        self.fuelLeak = random.choice(values)

    def updateRemainingCharge(self, obstacle):
        lowerBound = getRandomNumber()
        upperBound = lowerBound+5
        if(obstacle != "fuel"):
            self.remainingCharge -= getRandomNumber(lowerBound, upperBound)
        else:
            self.remainingCharge += getRandomNumber(
                lowerBound+10, upperBound+10)
        print("Remaining Charge:", self.remainingCharge)

    def goUpHill(self):
        print("Going up the Hill")
        self.updateRemainingCharge("hill")

    def travelThroughRocks(self):
        self.updateFuelLeak()
        print("Going around the rock")
        self.updateRemainingCharge("rock")
        if(self.fuelLeak):
            self.remainingCharge -= 2

    def raceThroughPlain(self):
        print("Racing through the plain")
        self.updateRemainingCharge("plain")

    def rechargeBattery(self):
        print("Yay! I got some fuel!")
        self.updateRemainingCharge("fuel")
        print(f"Charge Left:", self.remainingCharge)

    def reachedGoal(self):
        self.updateRemainingCharge("goal")
        print("Reached the Goal!")
        exit(1)

    def moveAgent(self, obstacle):
        if(obstacle == "goal"):
            self.reachedGoal()
        elif(obstacle == "hill"):
            self.goUpHill()
        elif(obstacle == "rock"):
            self.travelThroughRocks()
        elif(obstacle == "plain"):
            self.raceThroughPlain()
        elif(obstacle == "fuel"):
            self.rechargeBattery()
        if(self.fuelLeak):
            print("Uh, Oh! I am leaking fuel")
            self.remainingCharge -= 1
        if(self.remainingCharge <= 0):
            print("Out of Charge! Cannot reach the Goal!")
            exit(1)


class Environment:
    terrain = []
    order = 0
    choices = ["hill", "rock", "plain", "fuel"]
    agent = Agent([0, 0])
    goal = []

    def __init__(self, order):
        self.order = order
        self.terrain = [[0 for i in range(self.order)]
                        for j in range(self.order)]
        self.agent = Agent([0, 0])
        index = self.agent.returnCurrentPosition()
        self.makeRandomTerrain()
        self.terrain[index[0]][index[1]] = "start"
        self.goal = [order-1, order-1]
        self.terrain[order-1][order-1] = "goal"

    def makeRandomTerrain(self):
        for i in range(self.order):
            for j in range(self.order):
                self.terrain[i][j] = random.choice(self.choices)

    def printTerrain(self):
        for row in range(self.order):
            for col in range(self.order):
                print(f"{self.terrain[row][col]}\t\t", end="")
            print()

    def traverseTerrain(self):
        for row in range(self.order):
            for col in range(self.order):
                self.agent.moveAgent(self.terrain[row][col])


env = Environment(getRandomNumber())
env.printTerrain()
env.traverseTerrain()
