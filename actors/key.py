import pygame as pg
from positions.SpritePosition import *


class Key():
    """
    The key is moving back and forth...
    """

    

    def __init__(self, game):
        self.game = game
        self.allPositions = self.generate()
        self.spritePosition = self.allPositions.get("K00")
     

    def update(self):
        pass
    
    # def move(self):
    #     hasMoved = False
    #     if self.visible:
    #         if PyGame.clock() > self.timeOfNextFrame:  # We only animate our character every xx ms.
    #             self.timeOfNextFrame += 500
    #             if self.spritePosition.nextMove == None:
    #                 self.game.hideSprite(self.spritePosition.sprite)
    #             else:
    #                 hasMoved=True
    #                 self.game.hideSprite(self.spritePosition.sprite)
    #                 self.spritePosition = self.spritePosition.nextMove
                
    #             self.game.moveSprite(self.spritePosition.sprite,
    #                     self.spritePosition.x, self.spritePosition.y)
    #             self.game.showSprite(self.spritePosition.sprite)
    #     return hasMoved

  
    
    # def hide(self):
    #     self.visible=False
    #     self.game.hideSprite(self.spritePosition.sprite)

    # def show(self):
    #     self.visible=True
    #     self.game.showSprite(self.spritePosition.sprite)

    def generate(self):
        d = {}
        k = "Key"
        d["K00"] = SpritePosition("K00", k)
        d["K01"] = SpritePosition("K01", k)
        d["K02"] = SpritePosition("K02", k)
        d["K03"] = SpritePosition("K03", k)
        d["K02b"] = SpritePosition("K02", k)
        d["K01b"] = SpritePosition("K01", k)
        
        d["K00"].setPositions(nextMove=d["K01"])
        d["K01"].setPositions(nextMove=d["K02"])
        d["K02"].setPositions(nextMove=d["K03"])
        d["K03"].setPositions(nextMove=d["K02b"])
        d["K02b"].setPositions(nextMove=d["K01b"])
        d["K01b"].setPositions(nextMove=d["K00"])
        return d
