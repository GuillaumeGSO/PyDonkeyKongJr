from pygame_functions import *
from SpritePosition import *


class Missed():
    """
    Errors during the game : 3 lives only
    """

    def generate(self):
        d = {}
        b = "Missed"
        d["M00"] = SpritePosition("M00", b)
        d["M01"] = SpritePosition("M01", b)
        d["M02"] = SpritePosition("M02", b)
        return d

    def __init__(self):
        self.allPositions = self.generate()
        self.spritePosition = [self.allPositions.get("M00"), 
        self.allPositions.get("M01"), self.allPositions.get("M02")]
        

    def update(self, num_error):
        spriteToAdd = self.spritePosition[num_error]
        moveSprite(spriteToAdd.sprite,
                   spriteToAdd.x, spriteToAdd.y)
        showSprite(spriteToAdd.sprite)