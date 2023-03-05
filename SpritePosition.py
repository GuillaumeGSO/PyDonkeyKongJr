from pygame_functions import *
import pickle


class SpritePosition:

    def __init__(self, name, prefix=""):
        # Name must be the filename of a sprite
        self.name = name
        # Prefix should be both of img/sprites' subdirectory and prefix of a *Positions file
        if prefix != "":
            newPrefix = prefix + "/"
        self.sprite = makeSprite("img/sprites/" + newPrefix + name + ".png")
        # All the close positions
        self.jumpMove = None
        self.upMove = None
        self.downMove = None
        self.leftMove = None
        self.rightMove = None
        self.nextMove = None
        # Name of the sprite that can eat self 
        self.eaterName = None

        dictPositions = self.getAllPositions(prefix)
        self.x = 0
        self.y = 0
        if dictPositions!={}:
            self.x = dictPositions.get(name)[0]
            self.y = dictPositions.get(name)[1]


    def setPositions(self, jump=None, up=None, down=None, left=None, right=None, nextMove=None):
        self.jumpMove = jump
        self.upMove = up
        self.downMove = down
        self.leftMove = left
        self.rightMove = right
        self.nextMove = nextMove
    
    @staticmethod
    def getAllPositions(fileName):
        newFileName = "positions/" + fileName + "Positions"
        if os.path.isfile(newFileName):
            with open(newFileName, "rb") as positionFile:
                return pickle.Unpickler(positionFile).load()
        return {}
