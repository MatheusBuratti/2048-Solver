from math import nextafter
from random import random

from Grid import *
from Tile import *
from Point2D import *

class GameManager:
    def __init__(self,size) -> None:
        self.size = size
        self.startTiles = 2
    
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
        for cell in self.grid.allCells():
            tile = cell["tile"]
            if tile is not None:
                tile.mergedFrom = None
                tile.savePosition()
                
    def moveTile(self, tile: Tile, cell:Point2D) -> None:
        """Move a tile and its representation"""
        self.grid.cells[tile.x][tile.y] = None
        self.grid.cells[cell.x][cell.y] = tile
        tile.updatePosition(cell)

    def move(self, direction: int) -> None:

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
                        farthest,next = self.findFarthestPosition(cell,vector)
                        next = self.grid.cellContent(next)

                        if next is not None and next.value == tile.value and next.mergedFrom is None:
                            merged = Tile(next, tile.value*2)
                            merged.mergedFrom = [tile, next]

                            self.grid.insertTile(merged)
                            self.grid.removeTile(tile)

                            tile.updatePosition(next)

                            self.score += merged.value

                            if merged.value == 2048:
                                self.won = True
                            else:
                                self.moveTile(tile, farthest)

                        if self.positionsEqual(cell, tile):
                            moved = True
                            
            if moved:
                self.addRandomTile()

                if not self.movesAvailable():
                    self.over = True


    
    def getVector(self, direction:int) -> Point2D:
        """Get the vector representing the chosen direction"""
        map = {
            0: Point2D(0,-1), # Up
            1: Point2D(1,0),  # Right
            2: Point2D(0,1),  # Down
            3: Point2D(-1,0)} # Left

        return map[direction]

    def buildTransversals(self, vector:Point2D):
        transversals = { "x": [], "y": []}
        for pos in range(0,self.size):
            transversals["x"].append(pos)
            transversals["y"].append(pos)

        if vector.x == 1: 
            transversals["x"] = transversals["x"].reverse()
        if vector.y == 1: 
            transversals["y"] = transversals["y"].reverse()
    
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
        for x in range(0,self.size):
            for y in range(0,self.size):
                tile = self.grid.cellContent(Point2D(x,y))
                if tile is not None:
                    if y+1 < self.size:
                        nextCell = self.grid.cellContent(Point2D(x,y+1))
                        if nextCell is not None and nextCell.value == tile.value:
                            matches.append((tile,nextCell))
                            


    def positionsEqual(self, first:Point2D, second:Point2D) -> bool:
        return first.x == second.x and first.y == second.y

