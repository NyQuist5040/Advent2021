f = open("input.txt", "r")
L = [int(_) for _ in f.read().split(",")]
f.close()

fishPop = [0] * 9

for timer in L :
    fishPop[timer] += 1

def newDay() :
    tmp = fishPop[0]
    fishPop[0:-1] = fishPop[1:]
    fishPop[6] += tmp
    fishPop[8] = tmp

for _ in range(80) :
    newDay()

### Question 1
print(sum(fishPop))

for _ in range(256-80) :
    newDay()

### Question 2
print(sum(fishPop))
