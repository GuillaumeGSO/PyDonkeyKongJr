import pygame as pg

from positions.SpritePosition import *


class Cage():
    """
    The cage that disapear and the Mom's smile
    """

    def __init__(self, game):
        self.game = game
        self.openedCage = 0
        self.all_positions = self.generate_positions()
        self.sprite_positions = [self.all_positions.get("C00"),
                                 self.all_positions.get("C01"),
                                 self.all_positions.get("C02"),
                                 self.all_positions.get("C03")]
        self.game.cage_group.add(self.sprite_positions)
        self.smile_postion = self.all_positions.get("CSM")

    def openCage(self):
        self.game.cage_group.remove(self.sprite_positions[self.openedCage])
        self.openedCage -= 1
        self.game.add_to_score(25)

    def update(self):
        pass

    # def hide_cage(self, num_cage):
    #     print(num_cage)
    #     spriteToAdd = self.spritePosition[num_cage]
    #     self.game.moveSprite(spriteToAdd.sprite,
    #                spriteToAdd.x, spriteToAdd.y)
    #     self.game.hideSprite(spriteToAdd.sprite)

    # def restore_cages(self):
    #     for spriteToAdd in self.spritePosition:
    #         self.game.moveSprite(spriteToAdd.sprite,
    #                    spriteToAdd.x, spriteToAdd.y)
    #         self.game.showSprite(spriteToAdd.sprite)

    # def hide_smile(self):
    #     self.game.hideSprite(self.smilePostion.sprite)

    # def show_smile(self):
    #     self.game.moveSprite(self.smilePostion.sprite,
    #                self.smilePostion.x, self.smilePostion.y)
    #     self.game.showSprite(self.smilePostion.sprite)

    def generate_positions(self):
        d = {}
        b = "Cage"
        d["C00"] = SpritePosition("C00", b)
        d["C01"] = SpritePosition("C01", b)
        d["C02"] = SpritePosition("C02", b)
        d["C03"] = SpritePosition("C03", b)
        # smiling Mom
        d["CSM"] = SpritePosition("CSM", b)
        return d
