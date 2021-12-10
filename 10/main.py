f = open("input.txt", "r")
L = f.read().split("\n")[:-1]
f.close()

matches = { "(": ")",
            "[": "]",
            "{": "}",
            "<": ">"
}

def testLine(line) :
    bracketPile = []
    for char in line :
        if char in matches.keys() : #opening character
            bracketPile.append(char)
        elif len(bracketPile) == 0 : # no bracket to close
            return False, char
        elif matches[bracketPile[-1]] == char : # the character closes the opened bracket
                bracketPile.pop()
        else :
            return False, char
    # no bracket error detected
    closingStr = ""
    bracketPile.reverse()
    for char in bracketPile :
        closingStr += matches[char]

    return True, closingStr

numFails = { ")": 0,
             "]": 0,
             "}": 0,
             ">": 0
}

scoreFails = { ")": 3,
               "]": 57,
               "}": 1197,
               ">": 25137
}

scoreComplete = { ")": 1,
                  "]": 2,
                  "}": 3,
                  ">": 4
}

score1 = 0
listScore2 = []
for line in L :
    isCorrect, returnChar = testLine(line)
    if isCorrect :
        newScore = 0
        for char in returnChar :
            newScore = newScore * 5 + scoreComplete[char]
        listScore2.append(newScore)
    else :
        numFails[returnChar] += 1
        score1 += scoreFails[returnChar]

listScore2.sort()

### Question 1
print(score1)

### Question 2
print(listScore2)
print(listScore2[len(listScore2)//2])
