from pygame_functions import *


class SpritePosition:

    def __init__(self, name, prefix=""):
        self.name = name
        if prefix != "":
            newPrefix = prefix + "/"
        self.sprite = makeSprite("img/sprites/" + newPrefix + name + ".png")
        self.nextMove = None
