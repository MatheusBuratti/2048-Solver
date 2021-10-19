from math import nextafter
from random import random

from Grid import *
from Tile import *
from Point2D import *

class GameManager:
    def __init__(self,size) -> None:
        self.size = size
        self.startTiles = 2
        
        self.setup()
    
    def setup(self) -> None:
        """Set up the game"""
        self.grid = Grid(self.size)
        self.score = 0
        self.over = False
        self.won = False

        self.addStartTiles()

    def restart(self) -> None:
        """Restarts the game"""
        self.setup()

    def isGameTerminated(self) -> bool:
        """Returns true if the game is lost"""
        return self.over

    def addStartTiles(self) -> None:
        """Set up the initial tiles to start the game with"""
        for i in range(0,self.startTiles):
            self.addRandomTile()

    def addRandomTile(self) -> None:
        """Adds a tile in a random position"""
        if self.grid.cellsAvailable():
            value = 2 if random() < 0.9 else 4
            tile = Tile(self.grid.randomAvailableCell(),value)
            self.grid.insertTile(tile)

    def prepareTiles(self) -> None:
        """Save all tile positions and remove merger info"""
        for cell in self.grid.eachCell():
            tile = cell["tile"]
            if tile is not None:
                tile.mergedFrom = None
                tile.savePosition()
                
    def moveTile(self, tile: Tile, cell:Point2D) -> None:
        """Move a tile and its representation"""
        self.grid.cells[tile.x][tile.y] = None
        self.grid.cells[cell.x][cell.y] = tile
        tile.updatePosition(cell)

    def move(self, direction: int) -> bool:
        """Moves tiles on the grid in the specified direction"""
        if not self.isGameTerminated():
            vector = self.getVector(direction)
            transversals = self.buildTransversals(vector)
            moved = False

            self.prepareTiles()

            for x in transversals["x"]:
                for y in transversals["y"]:
                    cell = Point2D(x,y)
                    tile = self.grid.cellContent(cell)

                    if tile is not None:
                        farthest,next = self.findFarthestPosition(cell, vector)
                        nextTile = self.grid.cellContent(next)

                        if nextTile is not None and nextTile.value == tile.value and nextTile.mergedFrom is None:
                            merged = Tile(next, tile.value*2)
                            merged.mergedFrom = [tile, nextTile]

                            self.grid.insertTile(merged)
                            self.grid.removeTile(tile)

                            tile.updatePosition(next)

                            self.score += merged.value

                            if merged.value == 2048:
                                self.won = True

                        else:
                            self.moveTile(tile, farthest)

                        if not self.positionsEqual(cell, tile):
                            # Tile moved from its original cell
                            moved = True
                            
            if moved:
                self.addRandomTile()

                if not self.movesAvailable():
                    self.over = True
            return moved
    
    def getVector(self, direction:int) -> Point2D:
        """Get the vector representing the chosen direction"""
        map = {
            0: Point2D(0,-1),
            1: Point2D(1,0), 
            2: Point2D(0,1), 
            3: Point2D(-1,0)}

        return map[direction]

    def buildTransversals(self, vector:Point2D):
        """Build a list of positions to transverse in the right order"""
        transversals = { "x": [], "y": []}

        for pos in range(0, self.size):
            transversals["x"].append(pos)
            transversals["y"].append(pos)

        if vector.x == 1: 
            transversals["x"] = reversed(transversals["x"])
        if vector.y == 1: 
            transversals["y"] = reversed(transversals["y"])
    
        return transversals

    def findFarthestPosition(self, cell:Point2D, vector:Point2D):
        previous = cell

        cell = Point2D(previous.x + vector.x, previous.y + vector.y)

        while self.grid.withinBounds(cell) and self.grid.cellAvailable(cell):
            previous = cell
            cell = Point2D(previous.x + vector.x, previous.y + vector.y)

        return previous, cell

    def movesAvailable(self) -> bool:
        return self.grid.cellsAvailable() or self.tileMatchesAvailable()

    def tileMatchesAvailable(self) -> bool:
        for x in range(0,self.size):
            for y in range(0,self.size):
                tile = self.grid.cellContent(Point2D(x,y))
                if tile is not None:
                    for direction in range(0,4):
                        vector = self.getVector(direction)
                        cell = Point2D(x + vector.x, y + vector.y)

                        other = self.grid.cellContent(cell)
                        if other is not None and other.value == tile.value:
                            return True

    def allTileMatches(self) -> list:
        matches = list()
        for cells in self.grid.cells:
            for tile in cells:
                if tile is not None:
                    for direction in range(0,2):
                        vector = self.getVector(direction)
                        farthest, next = self.findFarthestPosition(Point2D(tile.x,tile.y),vector)
                        next = self.grid.cellContent(next)
                        if next is not None and next.value == tile.value:
                            matches.append({"value": tile.value, "direction": direction})
        return matches


                            

    def positionsEqual(self, first:Point2D, second:Point2D) -> bool:
        return first.x == second.x and first.y == second.y

    def printGrid(self):
        for cells in self.grid.cells:
            for cell in cells:
                if cell is None:
                    print("0", end = " ")
                else:
                    print(cell.value, end = " ")
            print()

