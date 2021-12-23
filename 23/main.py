from math import inf

class Burrow :
    def __init__(self, hallway, rooms, energy=0) :
        self._hallway = hallway
        self._rooms = rooms
        self._energy = energy

        # entrances to rooms as a hallway index
        self._entrances = {0: 2, 1: 4, 2: 6, 3: 8}
        #self._roomIndices = {2: 0, 4: 1, 6: 2, 8: 3}

        # room for each letter
        self._homes = {"A": 0, "B": 1, "C": 2, "D":3} 

        # energy per move
        self._consumptions = {"A": 1, "B": 10, "C": 100, "D":1000} 

    def __str__(self) :
        fullStr = "#############\n#"
        for case in self._hallway :
            if case is None :
                fullStr += "."
            else :
                fullStr += case

        fullStr += "#\n###"

        for room in self._rooms :
            if len(room) == 2 :
                fullStr += room[1] + "#"
            else :
                fullStr += ".#"

        fullStr += "##\n  #"

        for room in self._rooms :
            if len(room) >= 1 :
                fullStr += room[0] + "#"
            else :
                fullStr += ".#"

        fullStr += "  \n  #########\n"

        return fullStr

    def _isSorted(self) :
        hallwayEmpty = all(case is None for case in self._hallway)
        allHome = all(all(self._homes[letter]==i for letter in room) for i,room in enumerate(self._rooms))
        return ( hallwayEmpty and allHome )

    def sort(self, currentMin=inf) :
        if self._isSorted() :
            return self._energy, [str(self)]

        if self._energy > currentMin :
            #This path is already more expensive than the current min
            return inf, [str(self)]

        energyCost = inf
        pathway = []

        # All moves for letters in the hallway
        for i,letter in enumerate(self._hallway) :
            if letter is None :
                continue

            iHome = self._homes[letter]

            # Can't move to home if a non valid letter is there
            if any(inRoom != letter for inRoom in self._rooms[iHome]) :
                continue

            iEntrance = self._entrances[iHome]
            direction = (iEntrance > i) and -1 or 1

            # Check that the path between i and iEntrance is clear
            if all(a is None for a in self._hallway[iEntrance:i:direction]) :
                newHallway = self._hallway.copy()
                newHallway[i] = None

                newRooms = [room.copy() for room in self._rooms]
                newRooms[iHome].append(letter)

                stepsH = abs(iEntrance - i)
                stepsR = 2 - len(self._rooms[iHome])
                newEnergy = self._energy + self._consumptions[letter] * (stepsH + stepsR)

                newBurrow = Burrow(newHallway, newRooms, newEnergy)
                minEnergy, minPath = newBurrow.sort(energyCost)

                if minEnergy < energyCost :
                    energyCost = minEnergy
                    pathway = minPath

        # If we can get a letter to it's home, start with that (don't explore other possibilities)
        if energyCost < inf :
            return energyCost, [str(self)] + pathway

        # All moves for letters in rooms (nearest the entrance)
        for i, room in enumerate(self._rooms) :

            # empty room
            if len(room) == 0 :
                continue

            # all letters in this room are the good ones
            if all(self._homes[letter]==i for letter in room) :
                continue

            iRoom = self._entrances[i]
            for iEnd in range(11) :
                # iEnd can't be the index of an entrance
                if iEnd in [b for a,b in self._entrances.items()] :
                    continue

                direction = (iEnd > iRoom) and -1 or 1

                # the path from iRoom to iEnd must be clear
                if any(not a is None for a in self._hallway[iEnd:iRoom:direction]) :
                    continue

                newRooms = [r.copy() for r in self._rooms]

                letter = newRooms[i].pop()

                newHallway = self._hallway.copy()
                newHallway[iEnd] = letter

                stepsH = abs(iEnd - iRoom) + 1
                stepsR = 2 - len(room)
                newEnergy = self._energy + self._consumptions[letter] * (stepsH + stepsR)

                newBurrow = Burrow(newHallway, newRooms, newEnergy)
                minEnergy, minPath = newBurrow.sort(energyCost)

                if minEnergy < energyCost :
                    energyCost = minEnergy
                    pathway = minPath

        return energyCost, [str(self)] + pathway

### Example
#burrow = Burrow([None]*11, [["A", "B"], ["D", "C"], ["C", "B"], ["A","D"]])
### Input : too slow
#burrow = Burrow([None]*11, [["B", "A"], ["A", "C"], ["D", "B"], ["C","D"]])
### Easy example
#burrow = Burrow([None]*10 + ["A"], [["A"], ["C", "C"], ["B", "B"], ["D","D"]])
### My solution after a few step
burrow = Burrow([None]*3 + ["B", None, "C"] + [None]*5, [["B", "A"], ["A", "C"], [], ["D","D"]], 10540)
energy, path = burrow.sort(11342) #Manually found a solution for input
for b in path :
    print(b)

print(energy)
