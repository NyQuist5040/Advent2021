import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

n = len(L)
d = len(L[0])

for i in range(n) :
    L[i] = [int(e) for e in L[i]]

A = np.array(L)

gammaBin = (np.sum(A, 0) >= n/2).astype(int)
epsilonBin = 1 - gammaBin

gammaBin = ''.join(gammaBin.astype(str))
epsilonBin = ''.join(epsilonBin.astype(str))

gamma = int(gammaBin, 2)
epsilon = int(epsilonBin, 2)

### Question 1
print(gamma * epsilon)

Aoxy = A
for i in range(d) :
    majorityOxy = ( np.sum(Aoxy[:, i]) >= Aoxy.shape[0]/2 ).astype(int)
    Aoxy = Aoxy[Aoxy[:,i] == majorityOxy]
    if Aoxy.shape[0] == 1 :
        break

ACO2 = A
for i in range(d) :
    majorityCO2 = ( np.sum(ACO2[:, i]) >= ACO2.shape[0]/2 ).astype(int)
    ACO2 = ACO2[ACO2[:,i] == 1 - majorityCO2]
    if ACO2.shape[0] == 1 :
        break

oxygen = int(''.join(Aoxy[0].astype(str)), 2)
CO2 = int(''.join(ACO2[0].astype(str)), 2)

### Question 2
print(oxygen * CO2)
