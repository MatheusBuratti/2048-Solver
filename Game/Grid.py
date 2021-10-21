
from random import random
from math import floor

from Game.Tile import *
from Game.Point2D import *


class Grid:
    def __init__(self, size) -> None:
        self.size = size 
        self.cells = self.emptyGrid()

        # Stores the highest value tile formed
        self.highestValue = 2

    def emptyGrid(self) -> list:
        """Build a grid of the specified size"""
        cells = list()
        for x in range(0,self.size):
            row = list()
            cells.append(row)
            for y in range(0,self.size):
                row.append(None)
        return cells

    def fromState(self, state:list) -> list:
        """Returns a copy of a grid (state)"""
        cells = list()
        for x in range(0,self.size):
            row = cells[x] = []
            for y in range(0,self.size):
                tile = state[x][y]
                row.append(None if tile is None else Tile(Point2D(tile.x,tile.y),tile.value))

    def randomAvailableCell(self) -> Point2D:
        cells = self.availableCells()
        if len(cells) > 0:
            return cells[floor(random()*len(cells))]

    def availableCells(self) -> list:
        """Returns a list with all cells without tiles"""
        avCells = list()
        for cell in self.eachCell():
            if cell["tile"] is None:
                avCells.append(Point2D(cell["x"], cell["y"]))
        return avCells

    def eachCell(self) -> list:
        """Returns a list with all cells and tiles (if there is one in the cell)"""
        list = []
        for x in range(0,self.size): 
            for y in range(0,self.size):
                list.append({"x": x, "y": y, "tile": self.cells[x][y]})
        return list
        

    def cellsAvailable(self) -> bool:
        """Check if there are any cells available"""
        return True if len(self.availableCells()) > 0 else False

    def cellContent(self, position:Point2D) -> Tile:
        if self.withinBounds(position):
            return self.cells[position.x][position.y]
        return None

    def cellAvailable(self, position:Point2D) -> bool:
        """Check if a specific cell is available"""
        return True if self.cellContent(position) is None else False

    def insertTile(self,tile:Tile) -> None:
        """Inserts a tile at its position"""
        self.cells[tile.x][tile.y] = tile
        if tile.value > self.highestValue:
            self.highestValue = tile.value

    def removeTile(self,tile:Tile) -> None:
        self.cells[tile.x][tile.y] = None

    def withinBounds(self, position:Point2D) -> bool:
        """Checks if a position is inside the grid"""
        return position.x >= 0 and position.x < self.size and position.y >= 0 and position.y < self.size

