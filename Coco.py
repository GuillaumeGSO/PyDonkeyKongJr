from pygame_functions import *
from SpritePosition import *


class Coco():
    """
    The coconut falls when touched by monkey and respawn when monkey starts
    """

    def generate(self):
        d = {}
        c = "Coco"
        d["C00"] = SpritePosition("C00", c)
        d["C01"] = SpritePosition("C01", c)
        return d

    def __init__(self):
        self.allPositions = self.generate()
        self.spritePosition = self.allPositions.get("C00")
        self.frame = 0
        self.timeOfNextFrame = clock()

    def move(self):
        hasMoved = False
        if clock() > self.timeOfNextFrame:  # We only animate our character every xx ms.
            self.timeOfNextFrame += 500
            if self.spritePosition.nextMove == None:
                hideSprite(self.spritePosition.sprite)
            else:
                hasMoved=True
                hideSprite(self.spritePosition.sprite)
                self.spritePosition = self.spritePosition.nextMove
            
            moveSprite(self.spritePosition.sprite,
                       self.spritePosition.x, self.spritePosition.y)
            showSprite(self.spritePosition.sprite)
        return hasMoved

    def update(self):
        if self.move():
            updateDisplay()
