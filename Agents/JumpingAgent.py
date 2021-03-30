import random


def printTerrain(terrain, order):
    for row in range(order):
        for col in range(order):
            print(f"{terrain[row][col]}\t\t", end="")
        print()


class Agent:
    def __init__(self, currentPosition):
        self.currentPosition = currentPosition

    def returnCurrentPosition(self):
        return self.currentPosition

    def getNextPosition(self, order, terrain):
        row, col = self.returnCurrentPosition()
        print(row, col)
        if(terrain[row][col] == "goal"):
            print("reached Goal")
            printTerrain(terrain, order)
            exit(1)
        if(row < order-1):
            if(col < order-2):
                if(terrain[row][col+1] == "O"):
                    return [row, col+2]
                else:
                    return [row, col+1]
            elif(col == order-2):
                if(terrain[row][col+1] == "O"):
                    return [row+1, 0]
                else:
                    return [row, col+1]
            else:
                if(terrain[row+1][0] == "O"):
                    return [row+1, 1]
                else:
                    return [row+1, 0]
        else:
            if(col < order-2):
                if(terrain[row][col+1] == "O"):
                    return [row, col+2]
                else:
                    return [row, col+1]
            elif(terrain[row][col+1] == "goal"):
                print("Reached Goal")
                printTerrain(terrain, order)
                exit(1)
            else:
                print("Cannot Reach Goal")
                return[-1, -1]

    def detectEnvironmentAndTakeAction(self, terrain, order):
        row, col = self.returnCurrentPosition()
        nextRow, nextCol = self.getNextPosition(
            order, terrain)
        terrain[row][col] = 'X'
        if(row > -1 and row < order):
            self.changeCurrentPosition([nextRow, nextCol])

    def changeCurrentPosition(self, newPosition):
        self.currentPosition = newPosition


class Environment:
    terrain = []
    order = 0
    choices = ["O", "F"]
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
        choices = ["O", "F"]
        previousChoice = ""
        currentChoice = ""
        for i in range(self.order):
            for j in range(self.order):
                if(previousChoice == "O"):
                    currentChoice = "F"
                else:
                    currentChoice = random.choice(choices)
                self.terrain[i][j] = currentChoice
                previousChoice = currentChoice
                currentChoice = ""

    def traverseTerrain(self):
        for row in range(self.order):
            for col in range(self.order):
                self.agent.detectEnvironmentAndTakeAction(
                    self.terrain, self.order)


env = Environment(8)
printTerrain(env.terrain, env.order)
env.traverseTerrain()
