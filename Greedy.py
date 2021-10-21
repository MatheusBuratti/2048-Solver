from typing import Match
from Game.GameManager import *

Game = GameManager(4)

highestScore = 0
highestTileValue = 0

for i in range(0,100):
    while not Game.isGameTerminated():
        greedyPlay = None

        # Checks if there are tile matches available
        possiblePlays = Game.allTileMatches()
        if possiblePlays:

            for match in possiblePlays:
                if greedyPlay is None or match["value"] > greedyPlay["value"]:
                    greedyPlay = match

            Game.move(greedyPlay["direction"])

        # If there's no matches available, tries to move in the order 0 1 2 3 until it moves
        else:

            direction = 0
            moved = Game.move(direction)
            # Game.move returns a boolean whether it was possible to move or not
            while not moved and direction < 4:
                direction+=1
                moved = Game.move(direction)

    if Game.score > highestScore:highestScore = Game.score
    if Game.grid.highestValue > highestTileValue: highestTileValue = Game.grid.highestValue

    Game.restart()

print(highestScore)
print(highestTileValue)
