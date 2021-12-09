import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

map = np.ones((len(L)+2, len(L[0])+2), np.int32) * 9

for i in range(len(L)) :
    for j in range(len(L[i])) :
        map[i+1,j+1] = int(L[i][j])

isLowpoint = np.zeros(map.shape, np.bool)

for i in range(1, map.shape[0]-1) :
    for j in range(1, map.shape[1]-1) :
        isLowpoint[i,j] = map[i,j] < map[i+1,j] and map[i,j] < map[i-1,j] and \
                          map[i,j] < map[i,j+1] and map[i,j] < map[i,j-1]

### Question 1
print(np.sum(map[isLowpoint] + 1))

iLow, jLow = np.where(isLowpoint)

basinNumber = np.ones(map.shape, np.int32) * -1
basinSizes = np.zeros(len(iLow), np.int32)

def markBasin(point, num) :
    i, j = point
    basinNumber[i,j] = num
    if map[i,j] < map[i+1,j] and map[i+1,j] != 9 :
        markBasin((i+1, j), num)
    if map[i,j] < map[i-1,j] and map[i-1,j] != 9 :
        markBasin((i-1, j), num)
    if map[i,j] < map[i,j+1] and map[i,j+1] != 9 :
        markBasin((i, j+1), num)
    if map[i,j] < map[i,j-1] and map[i,j-1] != 9 :
        markBasin((i, j-1), num)

for i in range(len(iLow)) :
    markBasin((iLow[i], jLow[i]), i)
    basinSizes[i] = np.sum(basinNumber == i)

### Question 2
print(np.prod(sorted(basinSizes)[-3:]))
