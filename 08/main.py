import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

encoding = { 0: "abcefg",
             1: "cf",
             2: "acdeg",
             3: "acdfg",
             4: "bcdf",
             5: "abdfg",
             6: "abdefg",
             7: "acf",
             8: "abcdefg",
             9: "abcdfg"
}

easyDigits = [1, 4, 7, 8]

patterns = []
outputs = []
for row in L :
    [pat, out] = row.split(" | ")
    patterns.append(pat.split(" "))
    outputs.append(out.split(" "))

numEasy = 0
for row in outputs :
    for code in row :
        for easyDig in easyDigits :
            if len(code) == len(encoding[easyDig]) :
                numEasy += 1

### Question 1
print(numEasy)
