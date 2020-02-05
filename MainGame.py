"""
Thanks :
http://pica-pic.com/donkey_kong_jr/
https://www.youtube.com/watch?v=K9CoOYqqVLU
http://www.github.com/stevepaget/pygame_functions
https://mamedev.emulab.it/haze/2017-new-focus/

"""

from pygame_functions import *
from MonkeyPosition import *
import pickle

WIDTH = 700
HEIGHT = 480
FPS = 10

screenSize(WIDTH, HEIGHT)
setBackgroundImage("img/EmptyScreen.png")
MONKEY_POSITIONS_FILE = "MonkeyPositions"
KEY_POSITIONS_FILE = "KeyPositions"
"""
Lower level = L
L0G : 0th position, ground level
L0H : 0th position, hanged
L1G : 1st position, ground level
L1J : 1st position, jump

L0H L1J L2H...
L0G L1G L2G...

Position of sprites are recorded using positionning_tool.py in a file named MonkeyPositions
"""


def getAllPositions(fileName):
    if os.path.isfile(fileName):
        with open(fileName, "rb") as positionFile:
            return pickle.Unpickler(positionFile).load()
    return {}


# Lower level
L0G = MonkeyPosition("L0G")
L0H = MonkeyPosition("L0H")
L1G = MonkeyPosition("L1G")
L1J = MonkeyPosition("L1J")
L2G = MonkeyPosition("L2G")
L2H = MonkeyPosition("L2H")
L3G = MonkeyPosition("L3G")
L3H = MonkeyPosition("L3H")
L4G = MonkeyPosition("L4G")
L4J = MonkeyPosition("L4J")
L5G = MonkeyPosition("L5G")
L5H = MonkeyPosition("L5H")

# Higher level
H0G = MonkeyPosition("H0G")
H1G = MonkeyPosition("H1G")
H1H = MonkeyPosition("H1H")
H2G = MonkeyPosition("H2G")
H2J = MonkeyPosition("H2J")
H3G = MonkeyPosition("H3G")
H3J = MonkeyPosition("H3J")
# Juming to the key
H4J = MonkeyPosition("H4J")
# Taking the key
H5T = MonkeyPosition("H5T")
# Opening the cage and win
H5O = MonkeyPosition("H5O")
H6W = MonkeyPosition("H6W")
# Fail to get the key and loose
H7F = MonkeyPosition("H7F")
H7L = MonkeyPosition("H7L")


# TODO : faire une méthode qui permet de saisir tous les mouvements d'un coup
# Lower level
L0G.setPositions(jump=L0H, right=L1G)
L0H.setPositions(down=L0G, right=L1J)
L1G.setPositions(jump=L1J, left=L0G, right=L2G)
L1J.setPositions(nextMove=L1G)
L2G.setPositions(jump=L2H, left=L2G, right=L3G)
L2H.setPositions(left=L1J, right=L3H, down=L2G)
L3G.setPositions(jump=L3H, left=L2G, right=L4G)
L3H.setPositions(left=L2H, right=L4J, down=L3G)
L4G.setPositions(jump=L4J, left=L3G, right=L5G)
L4J.setPositions(nextMove=L4G)
L5G.setPositions(jump=L5H, left=L4G)
L5H.setPositions(left=L4J, up=H0G, down=L5G)
# Higher level
H0G.setPositions(left=H1G, down=L5H)
H1G.setPositions(jump=H1H, left=H2G, right=H0G)
H1H.setPositions(down=H1G)
H2G.setPositions(jump=H2J, left=H3G, right=H1G)
H2J.setPositions(nextMove=H2G, left=H3G)
H3G.setPositions(jump=H3J, left=H7F, up=H4J)
H3J.setPositions(nextMove=H3G)
# Juming to the key
H4J.setPositions(nextMove=H5T)
# Taking the key
H5T.setPositions(nextMove=H5O)
# Opening the cage and win
H5O.setPositions(nextMove=H6W)
H6W.setPositions(nextMove=L0G)
# Fail to get the key and loose
H7F.setPositions(nextMove=H7L)
H7L.setPositions(nextMove=L0G)

K00 = SpritePosition("K00", "others")
K01 = SpritePosition("K01", "others")
K02 = SpritePosition("K02", "others")
K03 = SpritePosition("K03", "others")
K02B = SpritePosition("K02", "others")
K01B = SpritePosition("K01", "others")

K00.nextMove = K01
K01.nextMove = K02
K02.nextMove = K03
K03.nextMove = K02B
K02B.nextMove = K01B
K01B.nextMove = K00    

# Loading monkey sprites positions
monkey_positions = getAllPositions(MONKEY_POSITIONS_FILE)
key_positions = getAllPositions(KEY_POSITIONS_FILE)

# Monkey starts bottom left
currentMonkeyPosition = L0G  
currentMonkeySprite = currentMonkeyPosition.sprite
currentSpriteX = monkey_positions[currentMonkeyPosition.name][0]
currentSpriteY = monkey_positions[currentMonkeyPosition.name][1]
moveSprite(currentMonkeySprite, currentSpriteX, currentSpriteY)
showSprite(currentMonkeySprite)

# Key starts
currentKeyPosition = K00
currentKeySprite = currentKeyPosition.sprite
currentKeySpriteX = key_positions[currentKeyPosition.name][0]
currentKeySpriteY = key_positions[currentKeyPosition.name][1]
moveSprite(currentKeySprite, currentKeySpriteX, currentKeySpriteY)
showSprite(currentKeySprite)


while True:
    #Move key
    currentKeyPosition = currentKeyPosition.nextMove
    tick(10)
    killSprite(currentKeySprite)
    tick(FPS)

    if currentMonkeyPosition.nextMove != None:
        currentMonkeyPosition = currentMonkeyPosition.nextMove
        tick(2)
        killSprite(currentMonkeySprite)
    else:
        if keyPressed("space"):
            if currentMonkeyPosition.jumpMove != None:
                currentMonkeyPosition = currentMonkeyPosition.jumpMove
                killSprite(currentMonkeySprite)
        elif keyPressed("right"):
            if currentMonkeyPosition.rightMove != None:
                currentMonkeyPosition = currentMonkeyPosition.rightMove
                killSprite(currentMonkeySprite)
        elif keyPressed("left"):
            if currentMonkeyPosition.leftMove != None:
                currentMonkeyPosition = currentMonkeyPosition.leftMove
                killSprite(currentMonkeySprite)
        elif keyPressed("up"):
            if currentMonkeyPosition.upMove != None:
                currentMonkeyPosition = currentMonkeyPosition.upMove
                killSprite(currentMonkeySprite)
        elif keyPressed("down"):
            if currentMonkeyPosition.downMove != None:
                currentMonkeyPosition = currentMonkeyPosition.downMove
                killSprite(currentMonkeySprite)
        

    tick(FPS)
    # FIXME Do not display if no keypressed !

    currentMonkeySprite = currentMonkeyPosition.sprite
    currentSpriteX = monkey_positions[currentMonkeyPosition.name][0]
    currentSpriteY = monkey_positions[currentMonkeyPosition.name][1]
    moveSprite(currentMonkeySprite, currentSpriteX, currentSpriteY)
    showSprite(currentMonkeySprite)

    killSprite(currentKeySprite)
    currentKeySprite = currentKeyPosition.sprite
    currentKeySpriteX = key_positions[currentKeyPosition.name][0]
    currentKeySpriteY = key_positions[currentKeyPosition.name][1]
    moveSprite(currentKeySprite, currentKeySpriteX, currentKeySpriteY)
    showSprite(currentKeySprite)
