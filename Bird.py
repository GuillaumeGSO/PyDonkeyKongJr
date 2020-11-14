from pygame_functions import *
from SpritePosition import *


class Bird():
    """
    Bird crossing from left to right
    """

    def generate(self):
        d = {}
        b = "Bird"
        d["B00"] = SpritePosition("B00", b)
        d["B01"] = SpritePosition("B01", b)
        d["B02"] = SpritePosition("B02", b)
        d["B03"] = SpritePosition("B03", b)
        d["B04"] = SpritePosition("B04", b)
        d["B04"].eaterName="C02"
        d["B05"] = SpritePosition("B05", b)
        d["B06"] = SpritePosition("B06", b)
        d["B07"] = SpritePosition("B07", b)
        d["B00"].setPositions(nextMove=d["B01"])
        d["B01"].setPositions(nextMove=d["B02"])
        d["B02"].setPositions(nextMove=d["B03"])
        d["B03"].setPositions(nextMove=d["B04"])
        d["B04"].setPositions(nextMove=d["B05"])
        d["B05"].setPositions(nextMove=d["B06"])
        d["B06"].setPositions(nextMove=d["B07"])
        # Should disapear when reach the right
        d["B07"].setPositions(nextMove=d["B00"])
        return d

    def __init__(self):
        self.allPositions = self.generate()
        self.spritePosition = self.allPositions.get("B00")
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
