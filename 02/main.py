import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

steps = np.zeros([len(L), 2], np.int32)
for i in range(len(L)) :
    [direction, length] = L[i].split(" ")
    if direction == "forward" :
        steps[i, 0] = int(length)
    elif direction == "up" :
        steps[i, 1] = -int(length)
    elif direction == "down" :
        steps[i, 1] = int(length)

stepsTotal = np.sum(steps, 0)

### Question 1
print(stepsTotal[0] * stepsTotal[1])

### Question 2
aim = np.cumsum(steps[:,1])

newSteps = steps
newSteps[:,1] = newSteps[:,0] * aim

newStepsTotal = np.sum(newSteps, 0)
print(newStepsTotal[0] * newStepsTotal[1])
