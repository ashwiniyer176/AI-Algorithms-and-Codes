# Best First Search in an Undirected Graph
from collections import defaultdict


class Graph:
    # If no data structure is specified, the graph stores the values in the form of a list
    # Graphs is stored in the format {"Node Name":("Adjacent Node",Cost, Heuristic of Adjacent Node)}
    graph = defaultdict(list)
    closedNodes = []
    heuristic = defaultdict(int)

    def addEdge(self, node1, node2, cost, h1, h2):
        t1 = (node1, cost, h1)
        t2 = (node2, cost, h2)
        self.graph[node1].append(t2)
        self.graph[node2].append(t1)

    # Store Heuristic Values in a dictionary, which is later mapped to the graph
    def getHeuristicValues(self, numberOfNodes):
        print("Enter the Name and Heuristic Value for each Node:\n")
        for i in range(numberOfNodes):
            nodeName = input("Enter the Node Name: ")
            heuristic = int(input("Enter Heuristic Value:"))
            self.heuristic[nodeName] = heuristic

    def makeGraph(self, numberOfNodes):
        # Takes a node name and all the routes connected to the node
        print("Enter Node Names and Edges associated with it. \nGive the same name as for Heuristics(case-sensitive). \nEnter '.' to stop adding edges to current node:\n")
        for i in range(numberOfNodes):
            sourceNode = input("Enter current node name:")
            edge = ""
            while(edge != "."):
                edge = input(f"Enter node connected to {sourceNode}:")
                if(edge != "."):
                    cost = int(input("Enter cost: "))
                    # Mapping heuristic values from dictionary to the graph
                    source_H = self.heuristic[sourceNode]
                    edge_H = self.heuristic[edge]
                    self.addEdge(sourceNode, edge, cost, source_H, edge_H)
        print(self.graph)

    # Returns the node name of the smallest heuristic in the given list of tuples
    def findNextNode(self, queue):
        small = queue[0]
        for node in queue:
            if node[-1] < small[-1]:
                small = node
        return small[0]

    def BestFirstSearch(self, sourceNode, targetNode):
        if(sourceNode == targetNode):
            print(targetNode, " Found!")
            return

        else:
            print(sourceNode)
            self.closedNodes.append(sourceNode)
            queue = self.graph[sourceNode]
            nextNode = self.findNextNode(queue)
            self.BestFirstSearch(nextNode, targetNode)


g = Graph()
numberOfNodes = int(input("Enter number of Nodes: "))
g.getHeuristicValues(numberOfNodes)
g.makeGraph(numberOfNodes)
sourceNode = input("Enter Source Node:")
targetNode = input("Enter Target Node: ")
g.BestFirstSearch(sourceNode, targetNode)
