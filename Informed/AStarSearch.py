# Uniform Cost Search in Weighted Directed Graph
from collections import defaultdict


class Graph:
    # The graph stores the values in the form of a list
    graph = defaultdict(list)
    heuristicValues = defaultdict(int)
    visitedNodes = list()
    openNodes = []
    path = list()
    pathList = defaultdict(list)
    rootNode = ""

    def makeGraph(self, numberOfNodes):
        print("\nMaking the graph:")
        for i in range(numberOfNodes):
            sourceNode = input("Enter current node name:")
            edge = ""
            while(edge != "."):
                edge = input(f"Enter node connected to {sourceNode}:")
                if(edge != "."):
                    cost = int(input("Enter cost:"))
                    self.addEdge(sourceNode, edge, cost)
        print(self.graph)

    def getHeuristicValues(self, numberOfNodes):
        print("Enter the Name and Heuristic Value for each Node:\n")
        for i in range(numberOfNodes):
            print(i)
            nodeName = input("Enter the Node Name: ")
            heuristic = int(input("Enter Heuristic Value:"))
            self.heuristicValues[nodeName] = heuristic

    def AStarSearch(self, numberOfNodes, sourceNode, targetNode):
        small = 0
        while(1):
            costofPath = self.getPath(sourceNode, targetNode, 0)
            self.pathList[costofPath] = self.path
            self.path = []
            if(small == 0 or small > costofPath):
                small = costofPath
            print(self.pathList)
            print("Visited Nodes = ", self.visitedNodes)
            if(not self.isOpenNodeAccessible()):
                break
        print("Smallest Path = ", self.pathList[small])

    def getPath(self, sourceNode, targetNode, currentCost):
        if(sourceNode == targetNode):
            print(targetNode, currentCost)
            self.path.append(targetNode)
            return currentCost
        else:
            print(sourceNode, currentCost)
            self.updateOpenNodes(sourceNode)
            nextNode = self.findNextNode(sourceNode, currentCost)
            currentCost += nextNode[-1]
            self.addToVisitedNodes(sourceNode)
            self.addToPath(sourceNode)
            return self.getPath(nextNode[0], targetNode, currentCost)

    def updateOpenNodes(self, sourceNode):
        if(sourceNode not in self.visitedNodes or sourceNode != self.rootNode):
            for node in self.graph[sourceNode]:
                if(node not in self.openNodes):
                    self.openNodes.append(node)
        print("Open Nodes Updated = ", self.openNodes)

    def findNextNode(self, sourceNode, currentCost):
        small = (sourceNode, 0)
        for node in self.openNodes:
            if node in self.graph[sourceNode]:
                if(small[-1] == 0 or self.findEstimatedCost(currentCost, small) > self.findEstimatedCost(currentCost, node)):
                    small = node
        self.openNodes.remove(small)
        print("Open Nodes = ", self.openNodes, "\nSmall= ", small)
        print("Small cost=", self.findEstimatedCost(currentCost, small))
        return small

    def findEstimatedCost(self, currentCost, node):
        name = node[0]
        pathCost = node[1]
        heuristic = self.heuristicValues[name]
        estimatedCost = currentCost+heuristic+pathCost
        return estimatedCost

    def isOpenNodeAccessible(self):
        for x in self.openNodes:
            if x in self.graph[self.rootNode]:
                return True
        return False

    def addEdge(self, currentNode, edgeNode, cost):
        t1 = (edgeNode, cost)
        self.graph[currentNode].append(t1)

    def addToPath(self, node):
        if(node != self.rootNode):
            self.path.append(node)

    def addToVisitedNodes(self, node):
        if(node not in self.visitedNodes):
            self.visitedNodes.append(node)


g = Graph()

numberOfNodes = int(input("Enter number of nodes: "))
g.getHeuristicValues(numberOfNodes)
g.makeGraph(numberOfNodes)
sourceNode = input("Enter Source Node:")
targetNode = input("Enter target node: ")
g.rootNode = sourceNode
g.AStarSearch(numberOfNodes, sourceNode, targetNode)
