from pygame_functions import *
from SpritePosition import *


class Key():
    """
    The key is moving back and forth...
    """

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

    def __init__(self):
        self.allPositions = self.generate()
        self.spritePosition = self.allPositions.get("K00")
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
