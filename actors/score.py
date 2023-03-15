import pygame as pg

from positions.SpritePosition import *


class Score():
    """
    Display the score with sound
    """

    def __init__(self, game):
        self.game = game
        self.score = 0
        # self.scoreLabel = self.game.makeLabel(
        #     str(self.score), 80, 690, 0, "black")
        font = pg.font.Font("fonts/Open 24 Display St.ttf", 80)
        # self.scoreLabel.font = font
        # self.scoreLabel.rect.topright = 690, 0
        # self.sound = makeSound("sounds/Score.wav")
        # self.game.showLabel(self.scoreLabel)
        # self.game.changeLabel(self.scoreLabel, str(self.score))

    def update(self):
        pass

    def addPoints(self, points):
        for i in range(points):
            self.score += 1
            self.game.changeLabel(self.scoreLabel, str(self.score))
            self.scoreLabel.rect.topright = 690, 0
            self.game.playSound(self.sound)
            self.game.pause(50)
