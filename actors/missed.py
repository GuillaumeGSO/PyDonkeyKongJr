import pygame as pg

from positions.SpritePosition import *


class Missed():
    """
    Errors during the game : 3 lives only
    """

    def __init__(self, game):
        self.game = game
        self.allPositions = self.generatePositions()
        self.spritePosition: SpritePosition = None
        # self.sound = makeSound("sounds/Missed.wav")

    def miss(self, number):
        self.spritePosition = self.allPositions.get("M0" + str(number))
        self.game.info_group.add(self.spritePosition)

    def update(self):
        pass
        # if self.spritePosition == None:
        #     self.spritePosition = self.allPositions.get("M00")
        #     return
        # newPosition = self.allPositions.get(self.spritePosition.nextMove)
        # self.spritePosition.kill()
        # if newPosition != None:
        #     self.spritePosition = newPosition
        # self.game.info_group.add(self.spritePosition)

    # def update(self, num_error):
    #     spriteToAdd = self.spritePosition[num_error]
    #     self.game.moveSprite(spriteToAdd.sprite,
    #                spriteToAdd.x, spriteToAdd.y)
    #     self.game.playSound(self.sound)
    #     for i in range(5):
    #         self.game.showSprite(spriteToAdd.sprite)
    #         self.game.pause(150)
    #         self.game.hideSprite(spriteToAdd.sprite)
    #         self.game.pause(150)
    #     self.game.showSprite(spriteToAdd.sprite)

    def generatePositions(self):
        d = {}
        b = "Missed"
        d["M00"] = SpritePosition("M00", b)
        d["M01"] = SpritePosition("M01", b)
        d["M02"] = SpritePosition("M02", b)
        return d
