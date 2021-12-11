import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

energy = np.zeros((len(L), len(L[0])), np.int32)
for i, line in enumerate(L) :
    for j, char in enumerate(line) :
        energy[i, j] = int(char)

def simulateStep(energy) :
    newFlashes = 0

    energy += 1

    while True :

        iFlashes, jFlashes = np.where(energy > 9)
        newFlashes += len(iFlashes)

        if len(iFlashes) == 0 :
            break

        for i, j in zip(iFlashes, jFlashes) :
            iStart = max(i-1, 0)
            iEnd = min(i+2, energy.shape[0])
            jStart = max(j-1, 0)
            jEnd = min(j+2, energy.shape[1])

            energy[iStart:iEnd, jStart:jEnd] += 1

            energy[i, j] = -999 # so it won't flash again

    energy[energy < 0] = 0

    return energy, newFlashes

nFlashes = 0

for _ in range(100) :
    energy, newFlashes = simulateStep(energy)
    nFlashes += newFlashes

### Question 1
print(nFlashes)

nSteps = 100
while True :
    nSteps += 1
    energy, newFlashes = simulateStep(energy)
    if newFlashes == energy.shape[0] * energy.shape[1] :
        break

### Question 2
print(nSteps)
