import re
import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

def add(num1, num2) :
    num = "[" + num1 + "," + num2 + "]"

    while True :
        num, exploded = explode(num)
        if not exploded :
            num, splited = split(num)
            if not splited :
                break

    return num


def explode(num) :
    #Find the first 5 deep "["
    nOpen = 0
    iExplode = 0
    for i,char in enumerate(num) :
        if char == "[" :
            nOpen += 1
        elif char == "]" :
            nOpen -= 1

        if nOpen == 5 :
            iExplode = i
            break

    if iExplode == 0 : #Nothing to explode
        return num, False

    left, right = num[:iExplode], num[iExplode:]

    matchExplode = re.search(r"^\[\d+,\d+\]", right)
    toExplode = matchExplode.group()
    right = right[matchExplode.span()[1]:]

    lInt, rInt = toExplode[1:-1].split(',')
    lInt, rInt = int(lInt), int(rInt)

    matchLeftInt = re.search(r"\d+(?=[^\d]*$)", left)
    if not matchLeftInt is None :
        addedLeft = lInt + int(matchLeftInt.group())
        left = left[:matchLeftInt.span()[0]] + str(addedLeft) + left[matchLeftInt.span()[1]:]
    matchRightInt = re.search(r"\d+", right)
    if not matchRightInt is None :
        addedRight = rInt + int(matchRightInt.group())
        right = right[:matchRightInt.span()[0]] + str(addedRight) + right[matchRightInt.span()[1]:]

    num = left + "0" + right

    return num, True


def split(num) :
    matchSplit = re.search(r"\d\d+", num)
    if matchSplit is None :
        return num, False

    left, right = num[:matchSplit.span()[0]], num[matchSplit.span()[1]:]

    splitInt = int(matchSplit.group())
    lInt, rInt = splitInt//2, splitInt - splitInt//2

    num = left + "[" + str(lInt) + "," + str(rInt) + "]" + right

    return num, True


def magnitude(num) :
    while True :
        num, isReduced = reduceMagnitude(num)
        if not isReduced :
            break
    return int(num)


def reduceMagnitude(num) :
    # find a "[a,b]" couple
    couple = re.search(r"\[[^\[\]]+\]", num)
    if couple is None :
        return num, False

    lInt, rInt = couple.group()[1:-1].split(',')
    lInt, rInt = int(lInt), int(rInt)
    localMagnitude = 3*lInt + 2*rInt

    num = num[:couple.span()[0]] + str(localMagnitude) + num[couple.span()[1]:]

    return num, True


result = L[0]

for num in L[1:] :
    result = add(result, num)
print(result)

### Question 1
print(magnitude(result))

allMag = np.zeros((len(L), len(L)), np.int32)
for i, num1 in enumerate(L) :
    for j, num2 in enumerate(L) :
        if i == j :
            continue
        allMag[i,j] = magnitude(add(num1, num2))

### Question 2
print(np.max(allMag))
