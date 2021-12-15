import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

riskMap = np.zeros((len(L), len(L[0])), np.int32)
for i, row in enumerate(L) :
    for j, num in enumerate(row) :
        riskMap[i,j] = int(num)

worthExploring = np.ones(riskMap.shape, np.int32)

def findExit(position: (int, int), worthExploring: np.array, riskMap: np.array) :
    i, j = position

    if i == riskMap.shape[0] - 1 and j == riskMap.shape[1] - 1 :
        return [position], riskMap[position] #path, danger

    # Recursive calls don't need to re-explore i,j or the neighbouring points
    newWorthExploring = worthExploring.copy()
    newWorthExploring[position] = 0
    for iPath, jPath in zip([0,0,1,-1], [1,-1,0,0]) :
        iNew = position[0] + iPath
        jNew = position[1] + jPath
        if iNew >= 0 and iNew < riskMap.shape[0] and jNew >= 0 and jNew < riskMap.shape[1] :
            newWorthExploring[iNew, jNew] = 0

    allPaths = []
    allDangers = []

    #for iPath, jPath in zip([0,0,1,-1], [1,-1,0,0]) :
    for iPath, jPath in zip([0,1], [1,0]) : #Only go Left/right
        iNew = position[0] + iPath
        jNew = position[1] + jPath
        if iNew >= 0 and iNew < riskMap.shape[0] and jNew >= 0 and jNew < riskMap.shape[1] \
                and worthExploring[iNew, jNew] :
            addPath, addDanger = findExit((iNew, jNew), newWorthExploring, riskMap)
            allPaths.append(addPath)
            allDangers.append(addDanger)

    if len(allDangers) == 0 : # No worthwhile path
        return [position], 99999 # huge danger so it is not selected

    danger = min(allDangers)
    path = allPaths[allDangers.index(danger)]

    return [position] + path, riskMap[position] + danger

### TOO SLOW
#path, danger = findExit((0,0), worthExploring, riskMap)
#print(path, danger-riskMap[0,0])


def minMap(riskMap) :
    minDangerMap = np.zeros(riskMap.shape, np.int32)
    m,n = riskMap.shape
    for i in range(m) :
        minDangerMap[i, n-1] = np.sum(riskMap[i:, n-1])
    for j in range(n) :
        minDangerMap[m-1, j] = np.sum(riskMap[m-1, j:])

    for i in range(m-2, -1, -1) :
        for j in range(n-2, -1, -1) :
            minDangerMap[i,j] = riskMap[i,j] + min(minDangerMap[i+1, j], minDangerMap[i, j+1])

    return minDangerMap

### Question 1
minDangerMap = minMap(riskMap)
print(minDangerMap[0,0] - riskMap[0,0])

largeRiskMap = [[None for _ in range(5)] for _ in range(5) ]
for i in range(5) :
    for j in range(5) :
        largeRiskMap[i][j] = (riskMap + i + j - 1) % 9 + 1
largeRiskMap = np.block(largeRiskMap)
print(largeRiskMap)

def minMapPropagation(riskMap) :
    minDangerMap = np.zeros(riskMap.shape, np.int32)
    m,n = riskMap.shape
    minDangerMap[m-1, n-1] = riskMap[m-1, n-1]

    while True :
        # Find the point on the border with minimal danger
        iMin, jMin = 0, 0
        valMin = 99999
        for i in range(m) :
            for j in range(n) :

                # Check that it has been explored
                if minDangerMap[i, j] == 0 :
                    continue

                onTheBorder = False
                for iPlus, jPlus in zip([0,0,1,-1], [1,-1,0,0]) :
                    iNew = i + iPlus
                    jNew = j + jPlus
                    if iNew >= 0 and iNew < m and jNew >= 0 and jNew < n \
                            and minDangerMap[iNew, jNew] == 0 :
                        onTheBorder = True
                        break # no need

                if not onTheBorder :
                    continue

                if minDangerMap[i, j] < valMin :
                    iMin, jMin = i, j
                    valMin = minDangerMap[i, j]

        # All non explored neighbours can be filled
        for iPlus, jPlus in zip([0,0,1,-1], [1,-1,0,0]) :
            iNew = iMin + iPlus
            jNew = jMin + jPlus
            if iNew >= 0 and iNew < m and jNew >= 0 and jNew < n \
                    and minDangerMap[iNew, jNew] == 0 :
                minDangerMap[iNew, jNew] = minDangerMap[iMin, jMin] + riskMap[iNew, jNew]

        # Check if all the map is filled
        print(np.sum(minDangerMap == 0))
        if np.sum(minDangerMap == 0) == 0 :
            break

    return minDangerMap

### Question 2
#largeMinDangerMap = minMap(largeRiskMap)
largeMinDangerMap = minMapPropagation(largeRiskMap)
#largeMinDangerMap = minMapPropagation(riskMap)
print(largeMinDangerMap[0,0] - largeRiskMap[0,0])
print(largeMinDangerMap)
