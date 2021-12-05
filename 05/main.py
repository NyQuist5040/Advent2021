import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

n = len(L)

segments = np.zeros((n,4), np.int32) # columns of x1,y1,x2,y2

for i in range(n) :
    segments[i,:] = np.reshape([point.split(",") for point in L[i].split("->")], (1,4))

verticalSeg = segments[np.logical_or(segments[:,0]==segments[:,2], segments[:,1]==segments[:,3]), :]

map = np.zeros(( np.max(segments[:,[1,3]]) + 1, np.max(segments[:,[0,2]]) + 1 ), np.int32)

for i in range(verticalSeg.shape[0]) :
    seg = verticalSeg[i,:]
    xRange = range(min(seg[0], seg[2]), max(seg[0], seg[2]) + 1)
    yRange = range(min(seg[1], seg[3]), max(seg[1], seg[3]) + 1)
    map[yRange, xRange] += 1

### Question 1
print(np.sum(map >= 2))
