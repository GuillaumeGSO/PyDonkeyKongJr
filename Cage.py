from pygame_functions import *
from SpritePosition import *


class Cage():
    """
    The cage that disapear and the Mom's smile
    """

    def generate(self):
        d = {}
        b = "Cage"
        d["C00"] = SpritePosition("C00", b)
        d["C01"] = SpritePosition("C01", b)
        d["C02"] = SpritePosition("C02", b)
        # last before smile
        d["C03"] = SpritePosition("C03", b)
        # smiling Mom
        d["CSM"] = SpritePosition("CSM", b)
        return d

    def __init__(self):
        self.allPositions = self.generate()
        self.spritePosition = [self.allPositions.get("C00"),
                               self.allPositions.get("C01"),
                               self.allPositions.get("C02"),
                               self.allPositions.get("C03")]
        self.smilePostion = self.allPositions.get("CSM")

    def hide_cage(self, num_cage):
        print(num_cage)
        spriteToAdd = self.spritePosition[num_cage]
        moveSprite(spriteToAdd.sprite,
                   spriteToAdd.x, spriteToAdd.y)
        hideSprite(spriteToAdd.sprite)

    def restore_cages(self):
        for spriteToAdd in self.spritePosition:
            moveSprite(spriteToAdd.sprite,
                       spriteToAdd.x, spriteToAdd.y)
            showSprite(spriteToAdd.sprite)

    def hide_smile(self):
        hideSprite(self.smilePostion.sprite)

    def show_smile(self):
        moveSprite(self.smilePostion.sprite,
                   self.smilePostion.x, self.smilePostion.y)
        showSprite(self.smilePostion.sprite)
