# Pygame template - skeleton for a new pygame project
from pygame_functions import *


WIDTH = 700
HEIGHT = 480
FPS = 30

screenSize(WIDTH, HEIGHT)
setBackgroundImage("EmptyScreen.png")

donkey = makeSprite("spriteMonkey01.png")
addSpriteImage(donkey, "spriteMonkey02.png")
GROUND = 390
groundlocations = [70, 140, 210, 270, 350, 430, 510, 590]

currentLocation = 0

moveSprite(donkey, groundlocations[currentLocation], GROUND)
showSprite(donkey)

while True:
    if keyPressed("right"):
        print("right {}".format(currentLocation))
        if currentLocation >= 0 and currentLocation < 7:
            currentLocation += 1
            moveSprite(donkey, groundlocations[currentLocation], GROUND)
            showSprite(donkey)
    if keyPressed("left"):
        print("left {}".format(currentLocation))
        if currentLocation > 0 and currentLocation < 7:
            currentLocation -= 1
            moveSprite(donkey, groundlocations[currentLocation], GROUND)
            showSprite(donkey)
    tick(10)
