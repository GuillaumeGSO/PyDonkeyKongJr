import os
import pickle
import pygame as pg


class SpritePosition(pg.sprite.Sprite):

    def __init__(self, name, actorType):
        pg.sprite.Sprite.__init__(self)
        self.positionName = name
        self.actorType = actorType
        self.path = self.generatePath()
        self.image = self.loadImage(self.path)
        self.rect = self.image.get_rect()
        self.jumpMove = None
        self.upMove = None
        self.downMove = None
        self.leftMove = None
        self.rightMove = None
        self.nextMove = None
        self.eaterName = None

        self.dictPositions = self.getAllPositions(self.actorType)
        self.x = self.dictPositions.get(self.positionName)[0]
        self.y = self.dictPositions.get(self.positionName)[1]
        self.rect.x = self.x
        self.rect.y = self.y

    def generatePath(self):
        return "img/sprites/" + self.actorType + "/" + self.positionName + ".png"

    def update(self):
        if (self.nextMove != None):
            self.positionName = self.nextMove
            self.path = self.generatePath()
            self.image = self.loadImage(self.path)
            self.rect = self.image.get_rect()
            self.x = self.dictPositions.get(self.positionName)[0]
            self.y = self.dictPositions.get(self.positionName)[1]
            self.rect.x = self.x
            self.rect.y = self.y

    @staticmethod
    def getAllPositions(fileName):
        newFileName = "positions/" + fileName + "Positions"
        if os.path.isfile(newFileName):
            with open(newFileName, "rb") as positionFile:
                return pickle.Unpickler(positionFile).load()
        return {}

    @staticmethod
    def loadImage(fileName, useColorKey=False):
        if os.path.isfile(fileName):
            image = pg.image.load(fileName)
            image = image.convert_alpha()
            # Return the image
            return image
        else:
            raise Exception(
                f"Error loading image: {fileName} – Check filename and path ?")
