import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n\n")
f.close()

drawList = [int(_) for _ in L[0].split(",")]

n = len(L) - 1

class BingoTable() :
    def __init__(self, table: np.array) :
        super(BingoTable, self).__init__()
        self.table = table
        self.called = np.zeros((5,5), np.int32)
        self.hasWon = False
        self.winningStep = -1
        self.winningNumber = 0

    def checkNumber(self, num) :
        for i in range(5) :
            for j in range(5) :
                if self.table[i,j] == num :
                    self.called[i,j] = 1

    def checkBingo(self) :
        return(any(np.sum(self.called, 0) == 5) or any(np.sum(self.called, 1) == 5))

    def score(self) :
        return(np.sum(self.table[self.called == 0]) * self.winningNumber)


tableList = []
for i in range(n) :
    newTable = np.reshape([int(_) for _ in L[i+1].split()], (5,5))
    tableList.append(BingoTable(newTable))

for step in range(len(drawList)) :
    number = drawList[step]
    for table in tableList :
        if table.hasWon :
            continue

        table.checkNumber(number)

        if table.checkBingo() :
            table.hasWon = True
            table.winningStep = step
            table.winningNumber = number


rankings = [table.winningStep for table in tableList]

winnerId = rankings.index(min(rankings))

### Question 1
print(tableList[winnerId].score())

loserId = rankings.index(max(rankings))

### Question 2
print(tableList[loserId].score())
