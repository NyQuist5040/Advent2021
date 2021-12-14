import numpy as np

f = open("input.txt", "r")
pairs, folds = f.read().split("\n\n")
f.close()


### Initiate the paper
pairs = pairs.split("\n")
x = [0] * len(pairs)
y = [0] * len(pairs)
for i, pair in enumerate(pairs) :
    x[i], y[i] = (int(a) for a in pair.split(","))

paper = np.zeros((max(y)+1, max(x)+1), np.int32)

for i, j in zip(y, x) :
    paper[i, j] = 1

### initiate list of folds
folds = folds.split("\n")[:-1]
for i, f in enumerate(folds) :
    folds[i] = f[11:].split("=")
    folds[i][1] = int(folds[i][1])


def verticalFold(paper, n) :
    # Fold along y=n

    # ensure a fold along the middle
    diff = n * 2 + 1 - paper.shape[0]
    if diff > 0 :
        paper = np.pad(paper, ((0,diff), (0,0)))
    elif diff < 0 :
        paper = np.pad(paper, ((-diff,0), (0,0)))
        n += diff

    folded = np.logical_or(paper[:n,:], np.flipud(paper[(n+1):,:])).astype(np.int32)

    return folded

def horizontalFold(paper, n) :
    # Fold along x=n

    folded = np.rot90( verticalFold(np.rot90(paper), n) , 3)

    return folded

def applyFold(paper, fold) :
    if fold[0] == "x" :
        return horizontalFold(paper, fold[1])
    if fold[0] == "y" :
        return verticalFold(paper, fold[1])

def printPaper(paper) :
    printStr = ""
    for i in range(paper.shape[0]) :
        for j in range(paper.shape[1]) :
            if paper[i,j] :
                printStr += "#"
            else :
                printStr += "."
        printStr += "\n"
    print(printStr)

paper = applyFold(paper, folds[0])

### Question 1
print(np.sum(paper))

for f in folds[1:] :
    paper = applyFold(paper, f)

### Question 2
paper = np.fliplr(paper)
printPaper(paper)
