from pygame_functions import *
from SpritePosition import *


class Score():
    """
    Display the score with sound
    """
    # https://pygame-zero.readthedocs.io/en/stable/index.html

    def __init__(self):
        self.score = 0
        self.scoreLabel = makeLabel(str(self.score), 80, 690, 0, "black")
        font = pygame.font.Font("fonts/Open 24 Display St.ttf", 80)
        self.scoreLabel.font = font
        self.scoreLabel.rect.topright = 690, 0
        self.sound = makeSound("sounds/Score.wav")
        showLabel(self.scoreLabel)
        changeLabel(self.scoreLabel, str(self.score))

    def addPoints(self, points):
        for i in range(points):
            self.score += 1
            changeLabel(self.scoreLabel, str(self.score))
            self.scoreLabel.rect.topright = 690, 0
            playSound(self.sound)
            pause(50)
