import random


class Agent:
    currentPosition = [5, 0]
    directions = ["up", "down", "left", "right"]
    hasGold = False
    reachedDestination = False

    def returnCurrentPosition(self):
        return self.currentPosition

    def changeCurrentPosition(self, newPosition):
        self.currentPosition = newPosition

    def moveAgent(self, direction):
        row, col = self.returnCurrentPosition()
        if(direction == "up"):
            print("Moving Up")
            self.changeCurrentPosition([row-1, col])
            return "move"
        elif(direction == "down"):
            print("Moving Down")
            self.changeCurrentPosition([row+1, col])
            return "move"
        elif(direction == "left"):
            print("Going Left")
            self.changeCurrentPosition([row, col-1])
            return "move"
        elif(direction == "right"):
            print("Going Right")
            self.changeCurrentPosition([row, col+1])
            return "move"
        elif(direction == "stop"):
            return "stop"

    def detectEnvironment(self, terrain):
        row, col = self.returnCurrentPosition()
        if(terrain[row][col] == "V"):
            print("Reached the Villain")
            printTerrain(terrain, len(terrain))
            exit(1)
        elif(terrain[row][col] == "G"):
            self.hasGold = True
            print("Got the Gold!")
        elif(terrain[row][col] == "g" or terrain[row][col] == "gs"):
            print("There is gold nearby!")
        elif(terrain[row][col] == "s"):
            print("The Villain is nearby!")


class Environment:
    agent = Agent()
    goldPosition = []
    destinationPosition = []
    choices = ["up", "down", "left", "right"]

    def __init__(self, order):
        self.order = order
        self.terrain = [["." for i in range(order)] for j in range(order)]
        self.assignAgentPosition()
        self.assignDestination()

    def assignDestination(self):
        self.terrain[self.order-1][self.order-1] = "D"
        self.destinationPosition = [self.order-1, self.order-1]

    def assignAgentPosition(self):
        row, col = self.agent.returnCurrentPosition()
        self.terrain[row][col] = "A"

    def assignSurroundings(self, value, position):
        row, col = position
        for i in range(max(row-1, 0), min(self.order, row+2)):
            for j in range(max(col-1, 0), min(self.order, col+2)):
                if(i == row and j == col):
                    continue
                elif((i == row and j != col) or (i != row and j == col)):
                    if(self.terrain[i][j] == "."):
                        self.terrain[i][j] = value
                    else:
                        self.terrain[i][j] = self.terrain[i][j]+value

    def assignGold(self, goldPosition):
        row, col = goldPosition
        self.terrain[row][col] = "G"
        self.assignSurroundings("g", goldPosition)
        self.goldPosition = goldPosition

    def assignVillain(self, villainPosition):
        row, col = villainPosition
        self.terrain[row][col] = "V"
        self.assignSurroundings("s", villainPosition)
        self.villainPosition = villainPosition

    def assignPit(self, pitPosition):
        row, col = pitPosition
        self.terrain[row][col] = "P"
        self.assignSurroundings("b", pitPosition)

    def changeAgentPosition(self, direction):
        status = self.agent.moveAgent(direction)
        self.assignAgentPosition()
        return status

    def chooseDirection(self, destination, terrain):
        row, col = self.agent.returnCurrentPosition()
        destRow, destCol = destination
        xValue = destRow-row
        yValue = destCol-col
        if(xValue > 0):
            return "down"
        elif(xValue < 0):
            return "up"
        if(xValue == 0):
            if(yValue > 0):
                return "right"
            elif(yValue < 0):
                return "left"
            elif(xValue == 0 and yValue == 0):
                print("Found Gold!")
                printTerrain(terrain, len(terrain))
                return "stop"

    def goToDestination(self, destination):
        row, col = self.agent.returnCurrentPosition()
        destRow, destCol = destination
        xValue = destRow-row
        yValue = destCol-col
        if(xValue > 0):
            return "down"
        elif(xValue < 0):
            return "up"
        if(yValue > 0):
            return "right"
        elif(yValue < 0):
            return "left"
        elif(xValue == 0 and yValue == 0):
            self.agent.reachedDestination = True
            print("Reached Destination")
            printTerrain(self.terrain, self.order)
            exit(1)

    def traverseTerrain(self):
        while(1):
            self.agent.detectEnvironment(self.terrain)
            status = self.changeAgentPosition(
                self.chooseDirection(self.goldPosition, self.terrain))
            if(status == "stop"):
                break

        while(1):
            self.agent.detectEnvironment
            self.changeAgentPosition(
                self.goToDestination(self.destinationPosition))


def printTerrain(terrain, order):
    for row in range(order):
        for col in range(order):
            print(f"{terrain[row][col]}\t\t", end="")
        print()


def getRandomPosition(l):
    x = random.choice(l)
    y = random.choice(l)
    return [x, y]


env = Environment(6)
l1 = [i for i in range(6)]
env.assignGold(getRandomPosition(l1))
env.assignVillain(getRandomPosition(l1))
env.assignPit(getRandomPosition(l1))
env.assignAgentPosition()
env.assignDestination()
printTerrain(env.terrain, env.order)
env.traverseTerrain()
printTerrain(env.terrain, env.order)
