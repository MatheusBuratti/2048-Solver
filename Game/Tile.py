from Game.Point2D import *

class Tile:
    def __init__(self, position: Point2D, value:int = 2) -> None:
        self.x = position.x
        self.y = position.y
        self.value = value

        self.previousPosition = None
        self.mergedFrom = None

    def savePosition(self) -> None:
        self.previousPosition = Point2D(self.x,self.y)

    def updatePosition(self, position:Point2D) -> None:
        self.x = position.x
        self.y = position.y
