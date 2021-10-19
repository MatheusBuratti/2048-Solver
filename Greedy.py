from GameManager import *

Game = GameManager(4)

Game.printGrid()

while not Game.isGameTerminated() and not Game.won:

    # Tries to match tiles
    matches = Game.allTileMatches()
    if matches:
        greedyMatch = matches.pop()
        for match in matches:
            if match["value"] > greedyMatch["value"]:
                greedyMatch = match
        Game.move(greedyMatch["direction"])
    else:
    # If there's no matches available just moves
        direction = 0
        moved = Game.move(direction)
        while not moved and direction < 4:
            direction+=1
            moved = Game.move(direction)
    Game.printGrid()
    print(end="\n\n\n")

print(Game.score)