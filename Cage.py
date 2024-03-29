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

    def __init__(self, game):
        self.game = game
        self.allPositions = self.generate()
        self.spritePosition = [self.allPositions.get("C00"),
                               self.allPositions.get("C01"),
                               self.allPositions.get("C02"),
                               self.allPositions.get("C03")]
        self.smilePostion = self.allPositions.get("CSM")

    def hide_cage(self, num_cage):
        print(num_cage)
        spriteToAdd = self.spritePosition[num_cage]
        self.game.moveSprite(spriteToAdd.sprite,
                   spriteToAdd.x, spriteToAdd.y)
        self.game.hideSprite(spriteToAdd.sprite)

    def restore_cages(self):
        for spriteToAdd in self.spritePosition:
            self.game.moveSprite(spriteToAdd.sprite,
                       spriteToAdd.x, spriteToAdd.y)
            self.game.showSprite(spriteToAdd.sprite)

    def hide_smile(self):
        self.game.hideSprite(self.smilePostion.sprite)

    def show_smile(self):
        self.game.moveSprite(self.smilePostion.sprite,
                   self.smilePostion.x, self.smilePostion.y)
        self.game.showSprite(self.smilePostion.sprite)
