import numpy as np
from math import inf

with open("input.txt") as f :
    L = f.read().split("\n")[:-1]

class RebootStep :
    def __init__(self, string) :
        onOff, ranges = string.split(" ")

        self._turnIt = int(onOff == "on")

        xRange, yRange, zRange = ranges.split(",")
        self._xRange = tuple(int(x) for x in xRange.split("=")[1].split(".."))
        self._yRange = tuple(int(y) for y in yRange.split("=")[1].split(".."))
        self._zRange = tuple(int(z) for z in zRange.split("=")[1].split(".."))

        self._isInit = all([abs(a) <= 50 for a in self._xRange + self._yRange + self._zRange])

    def __str__(self) :
        return f"{self._turnIt} : x={self._xRange}, y={self._yRange}, z={self._zRange}"

    def isInit(self) :
        return self._isInit

    def getxRange(self) :
        return self._xRange

    def getyRange(self) :
        return self._yRange

    def getzRange(self) :
        return self._zRange

    def getturnIt(self) :
        return self._turnIt

class Reactor :
    def __init__(self) :
        self._grid = np.zeros((101, 101, 101), np.int32)
        self._xShift = -50

    def __str__(self) :
        return str(self._grid)

    def _xtoi(self, x) :
        return x - self._xShift

    def applyStep(self, step) :
        self._grid[self._xtoi(step.getxRange()[0]):(self._xtoi(step.getxRange()[1])+1),\
                   self._xtoi(step.getyRange()[0]):(self._xtoi(step.getyRange()[1])+1),\
                   self._xtoi(step.getzRange()[0]):(self._xtoi(step.getzRange()[1])+1)]\
                = step.getturnIt()

    def numOn(self) :
        return np.sum(self._grid)


class ReactorTree :
    def __init__(self, xRange, yRange, zRange, value) :
        self._xRange = xRange
        self._yRange = yRange
        self._zRange = zRange

        self._value = value

        self._children = []

    def applyStep(self, step) :

        # If this cell is not at the end of the tree, propagate the call
        if len(self._children) > 0 :
            for child in self._children :
                child.applyStep(step)
            return None

        # restrict the step's range tot the tree cell
        xCut = (max(self._xRange[0], step.getxRange()[0]), min(self._xRange[1], step.getxRange()[1]))
        yCut = (max(self._yRange[0], step.getyRange()[0]), min(self._yRange[1], step.getyRange()[1]))
        zCut = (max(self._zRange[0], step.getzRange()[0]), min(self._zRange[1], step.getzRange()[1]))

        if xCut[0] > xCut[1] or yCut[0] > yCut[1] or zCut[0] > zCut[1] :
            # The step does not overlap this tree cell
            return None

        if step.getturnIt() == self._value :
            # The step will not change the value of the cell
            return None

        for i, (xStart, xEnd) in enumerate(zip([self._xRange[0], xCut[0], xCut[1]+1], \
                                               [xCut[0]-1, xCut[1], self._xRange[1]])) :
            if xStart > xEnd : # 0 length slice
                continue

            # left and right slices
            if i != 1 :
                self._children.append(ReactorTree((xStart, xEnd), self._yRange, self._zRange, self._value))
                continue

            # Middle slice
            for j, (yStart, yEnd) in enumerate(zip([self._yRange[0], yCut[0], yCut[1]+1], \
                                                   [yCut[0]-1, yCut[1], self._yRange[1]])) :
                if yStart > yEnd : # 0 length slice
                    continue

                # top and bottom slices
                if j != 1 :
                    self._children.append(ReactorTree((xStart, xEnd), (yStart, yEnd), self._zRange, self._value))
                    continue

                # Middle slice
                for k, (zStart, zEnd) in enumerate(zip([self._zRange[0], zCut[0], zCut[1]+1], \
                                                       [zCut[0]-1, zCut[1], self._zRange[1]])) :
                    if zStart > zEnd : # 0 length slice
                        continue

                    # left and right slices
                    if k != 1 :
                        self._children.append(ReactorTree((xStart, xEnd), (yStart, yEnd), (zStart, zEnd), self._value))
                        continue

                    # Middle slice
                    self._children.append(ReactorTree((xStart, xEnd), (yStart, yEnd), (zStart, zEnd), step.getturnIt()))

    def numOn(self) :
        if len(self._children) == 0 :
            if self._value == 0 :
                return 0
            else :
                return (self._xRange[1] - self._xRange[0] + 1) * \
                       (self._yRange[1] - self._yRange[0] + 1) * \
                       (self._zRange[1] - self._zRange[0] + 1)

        return sum(child.numOn() for child in self._children)


bootingSteps = []
for elt in L :
    bootingSteps.append(RebootStep(elt))

reactor = Reactor()

for step in bootingSteps :
    if step.isInit() :
        reactor.applyStep(step)

### Question 1
print(reactor.numOn())

reactor = ReactorTree((-inf, inf), (-inf, inf), (-inf, inf), 0)

for step in bootingSteps :
    reactor.applyStep(step)

### Question 2
print(reactor.numOn())
