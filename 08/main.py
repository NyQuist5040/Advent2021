import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

trueEncoding = { 0: "abcefg",
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
            if len(code) == len(trueEncoding[easyDig]) :
                numEasy += 1

### Question 1
print(numEasy)

def getEncoding(pattern) :
    encoding = {}
    # Find easy digits
    for digit in easyDigits :
        for code in pattern :
            if len(code) == len(trueEncoding[digit]) :
                encoding[digit] = code
    # Find number 3
    for code in pattern :
        if len(code) == 5 :
            if encoding[1][0] in set(code) and encoding[1][1] in set(code) :
                encoding[3] = code
    # Find numbers 9, 6, and 0
    for code in pattern :
        if len(code) == 6 :
            if encoding[1][0] in set(code) and encoding[1][1] in set(code) :
                # either 9 or 0
                if all([letter in set(code) for letter in encoding[4]]) :
                    encoding[9] = code
                else :
                    encoding[0] = code
            else :
                encoding[6] = code
    # Find topLeft segment
    for letter in "abcdefg" :
        if letter in set(encoding[9]) and not letter in set(encoding[3]) :
            topLeft = letter
    # Find numbers 5 and 2
    for code in pattern :
        if len(code) == 5 and code != encoding[3] :
            if topLeft in set(code) :
                encoding[5] = code
            else :
                encoding[2] = code

    return encoding

def decode(output, pattern) :
    encoding = getEncoding(pattern)
    decoded = ""
    for code in output :
        for i in range(10) :
            if sorted(list(code)) == sorted(list(encoding[i])) :
                decoded += str(i)
    return int(decoded)

test = getEncoding(patterns[0])

sumCodes = 0
for i in range(len(patterns)) :
    sumCodes += decode(outputs[i], patterns[i])

### Question 2
print(sumCodes)
