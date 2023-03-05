# Pygame template - skeleton for a new pygame project
from pygame_functions import *
import glob
import pickle

WIDTH = 700
HEIGHT = 480
FPS = 120

screenSize(WIDTH, HEIGHT)
setBackgroundImage("positions/FullScreen.png")
"""
Setup below
"""
INCREMENT = 1
PREFIX = "Cage"


SPRITE_POSITIONS_FILE = PREFIX + "Positions"


def getAllPositions():
    if os.path.isfile(SPRITE_POSITIONS_FILE):
        with open(SPRITE_POSITIONS_FILE, "rb") as positionFile:
            return pickle.Unpickler(positionFile).load()
    return {}


def writePositionsFile(dictPosition):
    with open(SPRITE_POSITIONS_FILE, "wb") as positionFile:
        myPickler = pickle.Pickler(positionFile)
        myPickler.dump(dictPosition)


all_positions = getAllPositions()
print(all_positions)

for filepath in glob.iglob("img/sprites/" + PREFIX + "/*.png"):
    # Filenames are xxx.png thus 7 letters
    spriteName = filepath[-7:-4]
    print(spriteName)
    sprite = makeSprite(filepath)
    print(all_positions.get(spriteName))
    if all_positions.get(spriteName) == None:
        moveSprite(sprite, WIDTH / 2, HEIGHT / 2)
    else:
        moveSprite(sprite, all_positions.get(spriteName)
                   [0], all_positions.get(spriteName)[1])

    showSprite(sprite)

    position = True
    while position:
        if keyPressed("right"):
            moveSprite(sprite, sprite.rect.x + INCREMENT, sprite.rect.y)
        if keyPressed("left"):
            moveSprite(sprite, sprite.rect.x - INCREMENT, sprite.rect.y)
        if keyPressed("up"):
            moveSprite(sprite, sprite.rect.x, sprite.rect.y-INCREMENT)
        if keyPressed("down"):
            moveSprite(sprite, sprite.rect.x, sprite.rect.y+INCREMENT)
        if keyPressed("space"):
            print(sprite.rect.x, sprite.rect.y)
            all_positions[spriteName] = (sprite.rect.x, sprite.rect.y)
            position = False
        showSprite(sprite)
        tick(10)

    hideSprite(sprite)
writePositionsFile(all_positions)
print("End of positionning")
