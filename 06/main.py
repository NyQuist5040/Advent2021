import sys

sys.setrecursionlimit(10000)

f = open("input.txt", "r")
L = [int(_) for _ in f.read().split(",")]
f.close()

class Fish :
    def __init__(self, timer=8, nextFish=None) :
        self._timer = timer
        self._nextFish = nextFish

    def insertFishNext(self, newFish) :
        newFish._nextFish = self._nextFish
        self._nextFish = newFish

    def insertFishEnd(self, newFish) :
        if self._nextFish is None :
            self._nextFish = newFish
        else :
            self._nextFish.insertFishEnd(newFish)

    def getListLength(self) :
        if self._nextFish is None :
            return 1
        else :
            return self._nextFish.getListLength() + 1

    def printFishTimers(self) :
        if self._nextFish is None :
            return str(self._timer) + "\n"
        else :
            return str(self._timer) + ", " + self._nextFish.printFishTimers()

    def newDay(self) :
        # last fish must be updated first so that new fishes are not
        if not self._nextFish is None :
            self._nextFish.newDay()

        if self._timer == 0 :
            self._timer = 6
            self.insertFishNext(Fish())
        else :
            self._timer -= 1


firstFish = Fish(timer = L[0])

for t in L[1:] :
    firstFish.insertFishEnd(Fish(timer = t))

for i in range(80) :
    firstFish.newDay()
    print(i, ":", firstFish.getListLength())

### Question 1
print(firstFish.getListLength())


