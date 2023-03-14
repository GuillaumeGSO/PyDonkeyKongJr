# from pygame_functions import *
from positions.SpritePosition import *
import pygame as pg


class Bird():
    """
    Bird crossing from left to right high, from right to left lower
    """


    def __init__(self, game):
        print("INIT BIRD")
        self.game = game
        self.allPositions = self.generatePositions()
        self.spritePosition = None
        
           

    def update(self):
        print(self.game.sprite_group)
        if self.spritePosition == None:
            self.spritePosition = self.allPositions.get("B00")
        else:
            newPosition = self.allPositions.get(self.spritePosition.nextMove)
            self.game.sprite_group.remove(self.spritePosition)
            self.spritePosition.kill()
            if newPosition != None:
                self.spritePosition = newPosition
                self.spritePosition.update()
        self.game.sprite_group.add(self.spritePosition)
        print(self.game.sprite_group)
    
    def generatePositions(self):
        d = {}
        b = "Bird"
        d["B00"] = SpritePosition("B00", b)
        d["B01"] = SpritePosition("B01", b)
        d["B02"] = SpritePosition("B02", b)
        d["B03"] = SpritePosition("B03", b)
        d["B04"] = SpritePosition("B04", b)
        d["B05"] = SpritePosition("B05", b)
        d["B06"] = SpritePosition("B06", b)
        d["B07"] = SpritePosition("B07", b)

        d["B00"].nextMove="B01"
        d["B01"].nextMove="B02"
        d["B02"].nextMove="B03"
        d["B03"].nextMove="B04"
        d["B04"].nextMove="B05"
        d["B04"].eaterName="C02"
        d["B05"].nextMove="B06"
        d["B06"].nextMove="B07"
        d["B07"].nextMove="B00"
     
        return d