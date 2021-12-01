import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n")
f.close()

L = np.array(L).astype(int)
n = len(L)

isDesc = ( L[1:] - L[0:(n-1)] ) > 0

### Question 1
print(sum(isDesc))

sums = L[2:] + L[1:(n-1)] + L[0:(n-2)]
isSumDesc = ( sums[1:] - sums[0:(len(sums)-1)] ) > 0

### Question 2
print(sum(isSumDesc))
