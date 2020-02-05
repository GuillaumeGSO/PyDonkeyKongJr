from pygame_functions import *
from SpritePosition import *


class MonkeyPosition(SpritePosition):

    def __init__(self, name):
        SpritePosition.__init__(self, name, "monkey")
        self.rightMove = None
        self.leftMove = None
        self.upMove = None
        self.downMove = None
        self.jumpMove = None

    def setPositions(self, jump=None, up=None, down=None, left=None, right=None, nextMove=None):
        self.jumpMove = jump
        self.upMove = up
        self.downMove = down
        self.leftMove = left
        self.rightMove = right
        self.nextMove = nextMove
