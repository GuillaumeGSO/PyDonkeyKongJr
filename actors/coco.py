import pygame as pg

from positions.SpritePosition import *


class Coco():
    """
    The coconut falls when touched by monkey and respawn when monkey starts
    """

    def __init__(self, game):
        self.game = game
        self.allPositions = self.generate()
        self.spritePosition = self.allPositions.get("C00")
        self.visible = True

    def update(self):
        pass

    # def move(self):
    #     hasMoved = False
    #     if PyGame.clock() > self.timeOfNextFrame:  # We only animate our character every xx ms.
    #         self.timeOfNextFrame += 500
    #         if self.spritePosition.nextMove == None:
    #             print("coco last move", self.spritePosition.y)
    #             self.hide()
    #         else:
    #             hasMoved=True
    #             print("coco next move", self.spritePosition.y)
    #             self.game.hideSprite(self.spritePosition.sprite)
    #             self.spritePosition = self.spritePosition.nextMove

    #         self.game.moveSprite(self.spritePosition.sprite,
    #                    self.spritePosition.x, self.spritePosition.y)
    #         self.game.showSprite(self.spritePosition.sprite)
    #     return hasMoved

    # def hide(self):
    #     # self.game.hideSprite(self.spritePosition.sprite)
    #     # visible = False
    #     pass

    # def show(self):
    #     self.game.showSprite(self.spritePosition.sprite)
    #     visible = True

    def init(self):
        self.spritePosition = self.allPositions.get("C00")
        self.allPositions.get("C00").setPositions(nextMove=None)
        self.show()

    def generate(self):
        d = {}
        c = "Coco"
        d["C00"] = SpritePosition("C00", c)
        d["C01"] = SpritePosition("C01", c)
        d["C02"] = SpritePosition("C02", c)
        d["C03"] = SpritePosition("C03", c)
        # No next move in position 0 : not falling without being touched
        d["C01"].nextMove = "C02"
        d["C02"].nextMove = "C03"
        return d
