"""
Thanks :
http://pica-pic.com/donkey_kong_jr/
https://www.youtube.com/watch?v=K9CoOYqqVLU
http://www.github.com/stevepaget/pygame_functions
https://mamedev.emulab.it/haze/2017-new-focus/

"""

from pygame_functions import *
from Player import *
from Bird import *
from Key import *
from Croco import *
from Coco import *
from Missed import *


WIDTH = 700
HEIGHT = 480
FPS = 5

screenSize(WIDTH, HEIGHT)
setBackgroundImage("img/EmptyScreen.png")

"""
Position of sprites are recorded using positionning_tool.py in a file named xxxPositions
"""
setAutoUpdate(False)
p = Player()
b = Bird()
k = Key()
c = Croco()
cc = Coco()
m = Missed()
infoLabel = makeLabel("Score : ", 20, 500, 10, "black")
showLabel(infoLabel)

missed = 0

while missed < 3:
    p.update()
    b.update()
    k.update()
    c.update()
    cc.update()
    # if touching(p.spritePosition.sprite, c.spritePosition.sprite):
    #print("croco touching")
    # if touching(p.spritePosition.sprite, b.spritePosition.sprite):
    #print("bird touching")
    if p.spritePosition.name == "H2J" and cc.spritePosition.name == "C00":
        cc.spritePosition.nextMove = cc.allPositions["C01"]
    
    # If the coconut reach the bottom : hide it
    if cc.spritePosition.name == "C03":
        cc.hide()
    # If monkey is jumping to the key 
    if p.spritePosition.name == "H4J":
        if k.spritePosition.name == "K03":
            # Monkey grab the key
            p.spritePosition.nextMove = p.allPositions["H5T"]
            k.hide()
        else:
            # Monkey miss the key
            m.update(missed)
            missed += 1
            p.spritePosition.nextMove = p.allPositions["H7F"]
            #Monkey finish in the bush
            p.update()
            p.update()
    if p.spritePosition.name == "H7F":
        # Monkey miss the key
        m.update(missed)
        missed += 1
         #Monkey finish in the bush
        p.update()

    # If starting position : reset some stuff
    if p.spritePosition.name == "L0G":
        k.show()
        cc.init()

    tick(FPS)
changeLabel(infoLabel, "Game Over")
endWait()
