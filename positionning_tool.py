# Pygame template - skeleton for a new pygame project

import glob
import os
import pickle
from settings import *

from pygame_functions import *



class PositioningTool:
    """
    This tools is showing a screenshot of the game with original sprites.
    All the sprites will appear one by one
    Use keys to adjust sprites to original and save in positions files
    """

    def run(self):
        tool = PyGame()
        tool.screenSize(WIDTH, HEIGHT)
        tool.setBackgroundImage("positions/FullScreen.png")

        """
        Setup below
        """
        INCREMENT = 1
        ALL_PREFIX = ["Bird","Cage", "Coco", "Croco", "Key", "Missed", "Monkey"]


        for prefix in ALL_PREFIX:
            positionFileName = prefix + "Positions"
            all_positions = PositioningTool.getAllPositions(positionFileName)
            print(all_positions)

            for filepath in glob.iglob("img/sprites/" + prefix + "/*.png"):
                # Filenames are xxx.png thus 7 letters
                spriteName = filepath[-7:-4]
                print(spriteName)
                sprite = makeSprite(filepath)
                print(all_positions.get(spriteName))
                if all_positions.get(spriteName) == None:
                    tool.moveSprite(sprite, WIDTH / 2, HEIGHT / 2)
                else:
                    tool.moveSprite(sprite, all_positions.get(spriteName)
                            [0], all_positions.get(spriteName)[1])

                tool.showSprite(sprite)

                position = True
                while position:
                    if tool.keyPressed("right"):
                        tool.moveSprite(sprite, sprite.rect.x + INCREMENT, sprite.rect.y)
                    if tool.keyPressed("left"):
                        tool.moveSprite(sprite, sprite.rect.x - INCREMENT, sprite.rect.y)
                    if tool.keyPressed("up"):
                        tool.moveSprite(sprite, sprite.rect.x, sprite.rect.y-INCREMENT)
                    if tool.keyPressed("down"):
                        tool.moveSprite(sprite, sprite.rect.x, sprite.rect.y+INCREMENT)
                    if tool.keyPressed("space"):
                        print(sprite.rect.x, sprite.rect.y)
                        all_positions[spriteName] = (sprite.rect.x, sprite.rect.y)
                        position = False
                    tool.showSprite(sprite)
                    tool.tick(10)

                tool.hideSprite(sprite)
            PositioningTool.writePositionInFile(all_positions, positionFileName)
        print("End of positionning")

    @staticmethod
    def getAllPositions(spritePositionFile):
        if os.path.isfile(spritePositionFile):
            with open(spritePositionFile, "rb") as positionFile:
                return pickle.Unpickler(positionFile).load()
        return {}

    @staticmethod
    def writePositionInFile(dictPosition, spritePositionFile):
        with open(spritePositionFile, "wb") as positionFile:
            myPickler = pickle.Pickler(positionFile)
            #myPickler.dump(dictPosition)

def main():
    PositioningTool().run()

if __name__ == "__main__":
    main()