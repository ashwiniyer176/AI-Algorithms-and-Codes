from collections import defaultdict


class myGraph:
    # To init the graph with a given number of cities
    def __init__(self, numberOfVertices):
        self.numberOfVertices = numberOfVertices
        self.graph = defaultdict(list)

    # To make the graph as the user requires
    def make_myGraph(self, numberOfRoutes):
        for i in range(numberOfRoutes):
            node1 = int(input("Enter City 1: "))
            node2 = int(input("Enter City 2: "))
            g.addEdgeToGraph(node1, node2)

    # To add paths between the given cities
    def addEdgeToGraph(self, node1, node2):
        self.graph[node1].append(node2)

    # To show how the graph is structured
    def print_myGraph(self):
        print(self.graph)

    # The function that performs DLS recursively
    def depthLimitedSearch(self, source, destination, depthLimit, route):

        if (source == destination):  # If we have reached the required city
            return True

        if(depthLimit <= 0):  # If we hit the limit before reaching our city
            return False

        # Checking the neighbours of the current node
        for neighbour in self.graph[source]:
            print("Source: ", source, " Neighbour: ",
                  neighbour, "Depth Limit:", depthLimit)
            route.add(source)

            # Recursively searches neighbours of the source
            # until the depth limit is reached, or the destination is reached
            if(self.depthLimitedSearch(neighbour, destination, depthLimit-1, route)):

                return True
        return False

    def IterativeDeepeningSearch(self, source, destination, depthLimit, numberofCities):
        for newLimit in range(1, depthLimit):
            route = set()
            # print(source, destination, newLimit)
            if(self.depthLimitedSearch(source, destination, newLimit, route)):
                print(route)
                return True
        return False


if __name__ == "__main__":
    numberofCities = int(input("Enter number of Cities: "))
    numberOfRoutes = int(input("Enter number of Routes: "))
    source = int(input("Where do I start from?(City Number):"))
    destination = source
    depthLimit = numberofCities
    g = myGraph(numberofCities)

    g.make_myGraph(numberOfRoutes)
    g.print_myGraph()
    if (g.IterativeDeepeningSearch(source, destination, depthLimit, numberofCities) == True):
        print(source, " is part of a cycle")
    else:
        print(source, " is not part of a cycle")
