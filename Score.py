from Game import Game
from SpritePosition import *


class Score():
    """
    Display the score with sound
    """
    # https://pygame-zero.readthedocs.io/en/stable/index.html

    def __init__(self, game):
        self.score = 0
        self.scoreLabel = game.makeLabel(str(self.score), 80, 690, 0, "black")
        font = pygame.font.Font("fonts/Open 24 Display St.ttf", 80)
        self.scoreLabel.font = font
        self.scoreLabel.rect.topright = 690, 0
        self.sound = makeSound("sounds/Score.wav")
        game.showLabel(self.scoreLabel)
        game.changeLabel(self.scoreLabel, str(self.score))

    def addPoints(self, game, points):
        for i in range(points):
            self.score += 1
            game.changeLabel(self.scoreLabel, str(self.score))
            self.scoreLabel.rect.topright = 690, 0
            game.playSound(self.sound)
            game.pause(50)
