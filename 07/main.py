import numpy as np

f = open("input.txt", "r")
L = f.read().split(",")
f.close()

crabs = np.array([int(k) for k in L])

middle = int(np.median(crabs))

### Question 1
print(np.sum(abs(crabs - middle)))

def fuel(x, crabs) :
    return np.sum((x-crabs)**2 + abs(x-crabs)) // 2

test = [fuel(x, crabs) for x in range(min(crabs), max(crabs))]

### Question 2
print(min(test))


