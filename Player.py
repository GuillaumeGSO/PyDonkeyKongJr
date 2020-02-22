from pygame_functions import *
from SpritePosition import *


class Player():
    """
    One and only one player.
    It should contains all of its different locations and sprites
    """

    def generate(self):
        d = {}
        m = "Monkey"
        # Lower level
        d["L0G"] = SpritePosition("L0G", m)
        d["L0H"] = SpritePosition("L0H", m)
        d["L1G"] = SpritePosition("L1G", m)
        d["L1J"] = SpritePosition("L1J", m)
        d["L2G"] = SpritePosition("L2G", m)
        d["L2H"] = SpritePosition("L2H", m)
        d["L3G"] = SpritePosition("L3G", m)
        d["L3H"] = SpritePosition("L3H", m)
        d["L4G"] = SpritePosition("L4G", m)
        d["L4J"] = SpritePosition("L4J", m)
        d["L5G"] = SpritePosition("L5G", m)
        d["L5H"] = SpritePosition("L5H", m)
        d
        # Higher level
        d["H0G"] = SpritePosition("H0G", m)
        d["H1G"] = SpritePosition("H1G", m)
        d["H1H"] = SpritePosition("H1H", m)
        d["H2G"] = SpritePosition("H2G", m)
        d["H2J"] = SpritePosition("H2J", m)
        d["H3G"] = SpritePosition("H3G", m)
        d["H3J"] = SpritePosition("H3J", m)
        # Juming to the key
        d["H4J"] = SpritePosition("H4J", m)
        # Taking the key
        d["H5T"] = SpritePosition("H5T", m)
        # Opening the cage and win
        d["H5O"] = SpritePosition("H5O", m)
        d["H6W"] = SpritePosition("H6W", m)
        # Fail to get the key and loose
        d["H7F"] = SpritePosition("H7F", m)
        d["H7L"] = SpritePosition("H7L", m)

        # Updating of positions
        # Lower level
        d["L0G"].setPositions(jump=d["L0H"], right=d["L1G"])
        d["L0H"].setPositions(down=d["L0G"], right=d["L1J"])
        d["L1G"].setPositions(jump=d["L1J"], left=d["L0G"], right=d["L2G"])
        d["L1J"].setPositions(nextMove=d["L1G"])
        d["L2G"].setPositions(jump=d["L2H"], left=d["L1G"], right=d["L3G"])
        d["L2H"].setPositions(left=d["L1J"], right=d["L3H"], down=d["L2G"])
        d["L3G"].setPositions(jump=d["L3H"], left=d["L2G"], right=d["L4G"])
        d["L3H"].setPositions(left=d["L2H"], right=d["L4J"], down=d["L3G"])
        d["L4G"].setPositions(jump=d["L4J"], left=d["L3G"], right=d["L5G"])
        d["L4J"].setPositions(nextMove=d["L4G"])
        d["L5G"].setPositions(jump=d["L5H"], left=d["L4G"])
        d["L5H"].setPositions(left=d["L4J"], up=d["H0G"], down=d["L5G"])
        # Higher level
        d["H0G"].setPositions(left=d["H1G"], down=d["L5H"])
        d["H1G"].setPositions(jump=d["H1H"], left=d["H2G"], right=d["H0G"])
        d["H1H"].setPositions(down=d["H1G"])
        d["H2G"].setPositions(jump=d["H2J"], left=d["H3G"], right=d["H1G"])
        d["H2J"].setPositions(nextMove=d["H2G"], left=d["H3G"])
        d["H3G"].setPositions(jump=d["H3J"], left=d["H7F"], up=d["H4J"], right=d["H2G"])
        d["H3J"].setPositions(nextMove=d["H3G"])
        # Jumping to the key
        d["H4J"].setPositions(nextMove=d["H5T"])
        # Taking the key
        d["H5T"].setPositions(nextMove=d["H5O"])
        # Opening the cage and win
        d["H5O"].setPositions(nextMove=d["H6W"])
        d["H6W"].setPositions(nextMove=d["L0G"])
        # Fail to get the key and loose
        d["H7F"].setPositions(nextMove=d["H7L"])
        d["H7L"].setPositions(nextMove=d["L0G"])
        return d

    def __init__(self):
        self.allPositions = self.generate()
        self.spritePosition = self.allPositions.get("L0G")
        self.frame = 0
        self.timeOfNextFrame = clock()

    def move(self):
        hasMoved = False
        if clock() > self.timeOfNextFrame:  # We only animate our character every xx ms.
            self.timeOfNextFrame += 100
            if self.spritePosition.nextMove == None:
                hideSprite(self.spritePosition.sprite)
                if keyPressed("space"):
                    if self.spritePosition.jumpMove != None:
                        self.spritePosition = self.spritePosition.jumpMove
                        hasMoved=True
                elif keyPressed("right"):
                    if self.spritePosition.rightMove != None:
                        self.spritePosition = self.spritePosition.rightMove
                        hasMoved=True
                elif keyPressed("left"):
                    if self.spritePosition.leftMove != None:
                        self.spritePosition = self.spritePosition.leftMove
                        hasMoved=True
                elif keyPressed("up"):
                    if self.spritePosition.upMove != None:
                        self.spritePosition = self.spritePosition.upMove
                        hasMoved=True
                elif keyPressed("down"):
                    if self.spritePosition.downMove != None:
                        self.spritePosition = self.spritePosition.downMove
                        hasMoved=True
            else:
                hasMoved=True
                hideSprite(self.spritePosition.sprite)
                self.spritePosition = self.spritePosition.nextMove
            
            moveSprite(self.spritePosition.sprite,
                       self.spritePosition.x, self.spritePosition.y)
            showSprite(self.spritePosition.sprite)
        else:
            self.timeOfNextFrame = clock()
        return hasMoved

    def update(self):
        if self.move():
            updateDisplay()
