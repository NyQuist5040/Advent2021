class Player :
    def __init__(self, position) :
        self._position = position
        self._score = 0

    def takeTurn(self, die, verbose=False) :
        self._position = (self._position + die.roll3() - 1)%10 + 1
        self._score += self._position
        if verbose :
            print(f"Player moved to space {self._position} for a total score of {self._score}")
        return self._score >= 1000

    def getScore(self) :
        return self._score

class DeterministicDie :
    def __init__(self) :
        self._face = 100
        self._numRolls = 0

    def roll(self) :
        self._face = (self._face)%100 + 1
        self._numRolls += 1
        return self._face

    def roll3(self) :
        sumRolls = 0
        for _ in range(3) :
            sumRolls += self.roll()
        return sumRolls

    def getNumRolls(self) :
        return self._numRolls

# Example
#player1 = Player(4)
#player2 = Player(8)
# Input
player1 = Player(4)
player2 = Player(2)

die = DeterministicDie()
while True :
    hasWon = player1.takeTurn(die, verbose=False)
    if hasWon :
        loser = player2
        break
    hasWon = player2.takeTurn(die)
    if hasWon :
        loser = player1
        break

### Question 1
print(loser.getScore() * die.getNumRolls())
