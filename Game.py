import pygame
import time

from GameManager import *

Game = GameManager(4)
Game.setup()

time.sleep(4)

while not Game.isGameTerminated():

    for row in Game.grid.cells:
        for cell in row:
            if cell is None:
                print("0",end=" ")
            else:
                print(cell.value,end=" ")
        print()
    print("----------")
    Game.move(0)
    time.sleep(2)