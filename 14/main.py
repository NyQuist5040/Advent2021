f = open("input.txt", "r")
start, rules = f.read().split("\n\n")
f.close()

rules = rules.split("\n")[:-1]
inserts = {}
for r in rules :
    match, add = r.split(" -> ")
    inserts[match] = add

steps = [list(start)]

for _ in range(10) :
    n = len(steps[-1]) * 2 -1
    newStep = [" "] * n
    newStep[0:n:2] = steps[-1]

    for i in range(1, n-1, 2) :
        newStep[i] = inserts[newStep[i-1] + newStep[i+1]]

    steps.append(newStep)

lastStep = steps[-1]

occurences = {}
for letter in set(lastStep) :
    occurences[letter] = sum([l == letter for l in lastStep])

### Question 1
nOccurences = [a for _,a in occurences.items()]
print(max(nOccurences) - min(nOccurences))

nLinks = [{}]
for k in inserts.keys() :
    nLinks[0][k] = 0
for i in range(len(start) - 1) :
    nLinks[0][start[i] + start[i+1]] += 1


for _ in range(40) :

    newLinks = {}
    for k in inserts.keys() :
        newLinks[k] = 0

    for link, n in nLinks[-1].items() :
        newLinks[link[0] + inserts[link]] += n
        newLinks[inserts[link] + link[1]] += n

    nLinks.append(newLinks)


occurences = {}
for letter in set([a for _,a in inserts.items()]) :
    occurences[letter] = 0

for link, n in nLinks[-1].items() :
    occurences[link[0]] += n
    occurences[link[1]] += n

occurences[start[0]] += 1
occurences[start[-1]] += 1

for k in occurences :
    occurences[k] = occurences[k]//2

### Question 2
nOccurences = [a for _,a in occurences.items()]
print(max(nOccurences) - min(nOccurences))

