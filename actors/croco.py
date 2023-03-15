import pygame as pg
from positions.SpritePosition import *


class Croco(pg.sprite.Sprite):
    """
    Multiple crocodile possible
    """

    

    def __init__(self, game):
        self.game = game
        self.allPositions = self.generate()
        self.spritePosition = self.allPositions.get("C00")
        # self.sound=makeSound("sounds/Croco.wav")
        super().__init__(self.game.sprite_group)

    def update(self):
        pass
    
    def move(self):
        hasMoved = False
        if PyGame.clock() > self.timeOfNextFrame:  # We only animate our character every xx ms.
            self.timeOfNextFrame += 500
            if self.spritePosition.nextMove == None:
                self.game.hideSprite(self.spritePosition.sprite)
            else:
                hasMoved=True
                self.game.hideSprite(self.spritePosition.sprite)
                self.spritePosition = self.spritePosition.nextMove
            
            self.game.moveSprite(self.spritePosition.sprite,
                       self.spritePosition.x, self.spritePosition.y)
            self.game.showSprite(self.spritePosition.sprite)
        return hasMoved

    def generate(self):
        d = {}
        c = "Croco"
        d["C00"] = SpritePosition("C00", c)
        d["C01"] = SpritePosition("C01", c)
        d["C02"] = SpritePosition("C02", c)
        d["C03"] = SpritePosition("C03", c)
        d["C04"] = SpritePosition("C04", c)
        d["C05"] = SpritePosition("C05", c)
        d["C06"] = SpritePosition("C06", c)
        d["C07"] = SpritePosition("C07", c)
        d["C08"] = SpritePosition("C08", c)
        d["C09"] = SpritePosition("C09", c)
        d["C10"] = SpritePosition("C10", c)
        d["C11"] = SpritePosition("C11", c)
        d["C12"] = SpritePosition("C12", c)
        
        d["C00"].nextMove="C01"
        d["C01"].nextMove="C02"
        d["C02"].nextMove="C03"
        d["C02"].eaterName="C01"
        d["C03"].nextMove="C04"
        d["C04"].nextMove="C05"
        d["C05"].nextMove="C06"
        d["C06"].nextMove="C07"
        d["C07"].nextMove="C08"
        d["C08"].nextMove="C09"
        d["C09"].nextMove="C10"
        d["C09"].eaterName="C03"
        d["C10"].nextMove="C11"
        d["C11"].nextMove="C12"
        d["C12"].nextMove="C00"
     
        return d