import random


class State:

    def __init__(self, currentState, moveRequired=(-1, -1)):
        self.currentState = currentState
        self.nextStates = []
        self.moveRequired = moveRequired

    def printState(self):
        print(self.currentState)
        print("Move Required to reach:", self.moveRequired)


class GameTree:
    visitedStates = []

    def __init__(self, currentState, currentDominoes, otherDominoes):
        self.rootState = State(currentState)
        self.currentDominoes = currentDominoes
        self.otherDominoes = otherDominoes

    def makeTree(self):
        queue = []
        self.makeNextStates(
            self.rootState, self.currentDominoes, self.otherDominoes, queue)

        if(len(queue) > 2):
            queue.pop(-1)
        queue.pop(0)
        return queue

    def findAllPlayableDominoes(self, currentState, dominoes):
        left = currentState[0][0]
        right = currentState[-1][1]
        playableDominoes = []
        for domino in dominoes:
            if(left != right):
                if(domino[1] == left or domino[0] == right):
                    playableDominoes.append(domino)
                elif(domino[0] == left or domino[1] == right):
                    reverseDomino = (domino[1], domino[0])
                    playableDominoes.append(reverseDomino)
            else:
                if(domino[0] == left or domino[1] == left):
                    playableDominoes.append(domino)
        return playableDominoes

    def removeDominoFromSet(self, domino, dominoSet):
        reverseDomino = (domino[1], domino[0])
        if(domino in dominoSet):
            dominoSet.remove(domino)
        elif(reverseDomino in dominoSet):
            dominoSet.remove(reverseDomino)

    def makeNextStates(self, currentState, currentDominoes, otherDominoes, queue):
        if(len(otherDominoes) == 0):
            queue.extend([currentState.moveRequired, 1])
            return
        elif(len(currentDominoes) == 0):
            queue.extend([currentState.moveRequired, 0])
            return
        else:
            playableDominoes = self.findAllPlayableDominoes(
                currentState.currentState, currentDominoes)
            for domino in playableDominoes:
                self.addDominoesToState(domino, currentState, currentDominoes)
            queue.append(currentState.moveRequired)
            for state in currentState.nextStates:
                self.makeNextStates(state, currentDominoes,
                                    otherDominoes, queue)
                if(queue[-1] == 1 or queue[-1] == 0):
                    break

    def addDominoesToState(self, domino, state, dominoSet):
        left = state.currentState[0][0]
        right = state.currentState[-1][1]
        reverseDomino = (domino[1], domino[0])
        newState = state.currentState[:]
        if(left == domino[1]):
            newState.insert(0, domino)
        elif(left == reverseDomino[1]):
            newState.insert(0, reverseDomino)
        elif(right == domino[0]):
            newState.append(domino)
        else:
            newState.append(reverseDomino)
        self.removeDominoFromSet(domino, dominoSet)
        newState = State(newState, domino)
        state.nextStates.append(newState)


class Player:
    moveList = []

    def __init__(self, playerName):
        self.playername = playerName
        self.__dominoes = []

    def updateDominoes(self, newDomino):
        self.__dominoes.append(newDomino)

    def printDominoes(self):
        print(f"Domino set for Player: {self.playername}")
        for i in self.__dominoes:
            print(i, end=" ")
        print("\n")

    def findHighestDouble(self):
        for i in range(6, -1, -1):
            if(i, i) in self.__dominoes:
                return i
        return -1

    def removeDomino(self, domino):
        if domino in self.__dominoes:
            self.__dominoes.remove(domino)
            return
        reverseDomino = (domino[1], domino[0])
        if reverseDomino in self.__dominoes:
            self.__dominoes.remove(reverseDomino)

    def returnBestPlayableDomino(self, playableDominoes):
        bestDominoSum = -1
        bestDomino = (-1, 0)
        for domino in playableDominoes:
            currentDominoSum = domino[0]+domino[1]
            if(bestDominoSum < currentDominoSum):
                bestDominoSum = currentDominoSum
                bestDomino = domino
        self.removeDomino(bestDomino)
        return bestDomino

    def findBestDomino(self, left, right):
        playableDominoes = []
        for domino in self.__dominoes:
            if(left != right):
                if(domino[1] == left or domino[0] == right):
                    playableDominoes.append(domino)
                if(domino[0] == left or domino[1] == right):
                    reverseDomino = (domino[1], domino[0])
                    playableDominoes.append(reverseDomino)
            else:
                if(domino[0] == left or domino[1] == left):
                    playableDominoes.append(domino)
        bestDomino = self.returnBestPlayableDomino(playableDominoes)
        return bestDomino

    def chooseAMove(self, moveAI, moveAlgorithm):
        if(moveAI == moveAlgorithm):
            return moveAI
        else:
            if(moveAI[0] < 0):
                return moveAlgorithm
            elif(moveAlgorithm[0] < 0):
                return moveAI
            else:
                return moveAI

    def makeMove(self, currentState, otherDominoes):
        print(f"\n\n{self.playername} moves now")
        nextMove = (-1, 0)
        # if(len(self.moveList) == 0):
        yourDominoes = otherDominoes[:]
        myDominoes = self.returnDominoesLeft()[:]
        g = GameTree(currentState, myDominoes, yourDominoes)
        self.moveList = g.makeTree()
        if(len(self.moveList) > 0):
            nextMove = self.moveList.pop(0)
        print("AI Suggests:", nextMove)

        bestDomino = self.findBestDomino(
            currentState[0][0], currentState[-1][1])
        return nextMove

    def returnNoOfDominoesLeft(self):
        return len(self.__dominoes)

    def returnDominoesLeft(self):
        return self.__dominoes


class Dominoes:
    fullSet = []
    maxPlayer = Player("Max")
    minPlayer = Player("Min")
    numberOfDominoesPerPlayer = 8
    currentState = []
    maxPlaying = False
    maxMissed = False
    minMissed = False

    def makeFullSetOfDominoes(self):
        for i in range(7):
            for j in range(i, 7):
                domino = (i, j)
                self.fullSet.append(domino)

    def returnRandomDominoFromFullSet(self):
        randomDomino = random.choice(self.fullSet)
        self.fullSet.remove(randomDomino)
        return randomDomino

    def shuffleAndDistributeDominoes(self):
        for i in range(self.numberOfDominoesPerPlayer):
            self.minPlayer.updateDominoes(self.returnRandomDominoFromFullSet())
            self.maxPlayer.updateDominoes(self.returnRandomDominoFromFullSet())
        self.minPlayer.printDominoes()
        self.maxPlayer.printDominoes()
        self.decideFirstMove()

    def decideFirstMove(self):
        maxHighestDouble = self.maxPlayer.findHighestDouble()
        minHighestDouble = self.minPlayer.findHighestDouble()
        while(max(maxHighestDouble, minHighestDouble) < 0):
            self.shuffleAndDistributeDominoes()
        if(maxHighestDouble > minHighestDouble):
            self.maxPlaying = True
            print("Max got", maxHighestDouble, "and so Max goes first!")
            self.maxPlayer.removeDomino((maxHighestDouble, maxHighestDouble))
            self.updateCurrentState((maxHighestDouble, maxHighestDouble))
            self.maxPlaying = False
        else:
            print("Min got", minHighestDouble, "and so Min goes first!")
            self.minPlayer.removeDomino((minHighestDouble, minHighestDouble))
            self.updateCurrentState((minHighestDouble, minHighestDouble))
            self.maxPlaying = True

    def updateCurrentState(self, move):
        if(len(self.currentState) > 0):
            left = self.currentState[0][0]
            right = self.currentState[-1][1]
            if(left == move[1]):
                self.currentState.insert(0, move)
            elif(right == move[0]):
                self.currentState.append(move)
        else:
            self.currentState.append(move)

    def decidePlayer(self):
        if(self.maxPlaying):
            newMove = self.maxPlayer.makeMove(
                self.currentState, self.minPlayer.returnDominoesLeft())
            if(newMove[0] >= 0):
                print("Max player move:", newMove)
                self.maxPlayer.printDominoes()
                self.maxPlaying = False
                self.updateCurrentState(newMove)
                self.maxMissed = False
            else:
                print("Max is missing a Turn")
                self.maxMissed = True
                self.maxPlaying = False
        else:
            newMove = self.minPlayer.makeMove(
                self.currentState, self.maxPlayer.returnDominoesLeft())
            if(newMove[0] >= 0):
                print("Min player move:", newMove)
                self.minPlayer.printDominoes()
                self.maxPlaying = True
                self.updateCurrentState(newMove)
                self.minMissed = False
            else:
                print("Min is missing a Turn")
                self.minMissed = True
                self.maxPlaying = True

    def playGame(self):
        while(1):
            self.decidePlayer()
            print(self.currentState)
            if(self.minMissed and self.maxMissed):
                exit(1)
            if(self.minPlayer.returnNoOfDominoesLeft() == 0):
                print("Game Over. Min Wins!")
                exit(1)
            elif(self.maxPlayer.returnNoOfDominoesLeft() == 0):
                print("Game Over. Max Wins!")
                exit(1)


d = Dominoes()
d.makeFullSetOfDominoes()
d.shuffleAndDistributeDominoes()
d.playGame()
