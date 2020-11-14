from pygame_functions import *
from SpritePosition import *


class Croco():
    """
    Multiple crocodile possible
    """

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
        
        d["C00"].setPositions(nextMove=d["C01"])
        d["C01"].setPositions(nextMove=d["C02"])
        d["C02"].setPositions(nextMove=d["C03"])
        d["C02"].eaterName="C01"
        d["C03"].setPositions(nextMove=d["C04"])
        d["C04"].setPositions(nextMove=d["C05"])
        d["C05"].setPositions(nextMove=d["C06"])
        d["C06"].setPositions(nextMove=d["C07"])
        d["C07"].setPositions(nextMove=d["C08"])
        d["C08"].setPositions(nextMove=d["C09"])
        d["C09"].setPositions(nextMove=d["C10"])
        d["C09"].eaterName="C03"
        d["C10"].setPositions(nextMove=d["C11"])
        d["C11"].setPositions(nextMove=d["C12"])
        d["C12"].setPositions(nextMove=d["C00"])
     
        return d

    def __init__(self):
        self.allPositions = self.generate()
        self.spritePosition = self.allPositions.get("C00")
        self.frame = 0
        self.timeOfNextFrame = clock()
        self.sound=makeSound("sounds/Croco.wav")

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
            playSound(self.sound)
