f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

class Node :
    def __init__(self, name) :
        self._name = name
        self._isBig = name[0].isupper()
        self._links = []

    def addLink(self, linkedNode) :
        self._links.append(linkedNode)

    def getName(self) :
        return self._name

    def getLinks(self) :
        return self._links

    def isBig(self) :
        return self._isBig

allNodes = {}
for line in L :
    l, r = line.split("-")
    for name in [l, r] :
        if not name in allNodes.keys() :
            allNodes[name] = Node(name)

    allNodes[l].addLink(allNodes[r])
    allNodes[r].addLink(allNodes[l])

def findEnd(startingPoint, visited) :
    visited.append(startingPoint.getName())

    if startingPoint.getName() == "end" :
        return [visited]

    pathways = []

    for node in startingPoint.getLinks() :
        exploreNode = node.isBig() or node.getName() not in visited
        if exploreNode :
            pathways = pathways + findEnd(node, visited.copy())

    return pathways

allPaths = findEnd(allNodes["start"], [])

### Question 1
print(len(allPaths))

def findEnd2(startingPoint, visited) :
    visited.append(startingPoint.getName())

    if startingPoint.getName() == "end" :
        return [visited]

    canVisitSecond = True
    visitedSmall = []
    for name in visited :
        if name[0].islower() :
            if name not in visitedSmall :
                visitedSmall.append(name)
            else :
                canVisitSecond = False

    pathways = []

    for node in startingPoint.getLinks() :
        exploreNode = node.isBig() or ( node.getName() not in visited ) or \
                      ( canVisitSecond and node.getName() != "start" )

        if exploreNode :
            pathways = pathways + findEnd2(node, visited.copy())

    return pathways

allPaths2 = findEnd2(allNodes["start"], [])

### Question 2
print(len(allPaths2))
