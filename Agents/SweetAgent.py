import random


def printTerrain(terrain, order):
    for row in range(order):
        for col in range(order):
            print(f"{terrain[row][col]}\t\t", end="")
        print()


class Agent:
    def __init__(self, currentPosition):
        self.currentPosition = currentPosition
        self.sweetsConsumed = 0
        self.tangyConsumed = 0

    def returnCurrentPosition(self):
        return self.currentPosition

    def incrementSweetsConsumed(self):
        self.sweetsConsumed += 1

    def changeCurrentPosition(self, newPosition):
        self.currentPosition = newPosition

    def getNextObject(self, terrain, order):
        row, col = self.returnCurrentPosition()
        nextObject = 'No Object'
        nextPosition = [0, 0]
        if(col < order-1):
            nextPosition = [row, col+1]
        elif(col == order-1 and row < order-1):
            nextPosition = [row+1, 0]
        self.checkObjectAndTakeAction(nextPosition, order, terrain)
        nextObject = terrain[nextPosition[0]][nextPosition[1]]

    def checkObjectAndTakeAction(self, nextPosition, order, terrain):
        row, col = nextPosition
        nextObject = terrain[row][col]
        if(nextObject == "T"):
            if(self.sweetsConsumed != 0 and self.sweetsConsumed >= 2):
                self.tangyConsumed += 1
                self.sweetsConsumed -= 2
                self.consumeObject(terrain, nextPosition)
            else:
                self.jumpOverTangyObject(order)
        elif(nextObject == "S"):
            self.sweetsConsumed += 1
            self.consumeObject(terrain, nextPosition)

    def consumeObject(self, terrain, nextPosition):
        row, col = nextPosition
        terrain[row][col] = "X"

    def jumpOverTangyObject(self, order):
        row, col = self.returnCurrentPosition()
        if(col < order-1):
            self.changeCurrentPosition([row, col+2])
        else:
            if(row < order-1):
                self.changeCurrentPosition([row+1, col])
            else:
                print("Cannot Jump Over Tangy Object")
                exit(1)


class Environment:
    terrain = []
    order = 0
    agent = Agent([0, 0])
    goal = []

    def __init__(self, order):
        self.order = order
        self.terrain = [[0 for i in range(self.order)]
                        for j in range(self.order)]
        index = self.agent.returnCurrentPosition()
        self.makeRandomTerrain()
        self.terrain[index[0]][index[1]] = "start"
        self.goal = [order-1, order-1]
        self.terrain[order-1][order-1] = "goal"

    def makeRandomTerrain(self):
        choices = ["S", "T"]
        for i in range(self.order):
            for j in range(self.order):
                self.terrain[i][j] = random.choice(choices)

    def traverseTerrain(self):
        print("Traversing")
        for i in range(self.order):
            for j in range(self.order):
                self.agent.changeCurrentPosition([i, j])
                self.agent.getNextObject(self.terrain, self.order)


env = Environment(8)
printTerrain(env.terrain, env.order)
env.traverseTerrain()
printTerrain(env.terrain, env.order)
print(
    f"Sweets Consumed:{env.agent.sweetsConsumed+2*env.agent.tangyConsumed}\nTangy Consumed:{env.agent.tangyConsumed}")
