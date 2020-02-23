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

continue_game = True

while continue_game:
    p.update()
    b.update()
    k.update()
    c.update()
    cc.update()
    # if touching(p.spritePosition.sprite, c.spritePosition.sprite):
    #print("croco touching")
    # if touching(p.spritePosition.sprite, b.spritePosition.sprite):
    #print("bird touching")
    if p.spritePosition.name=="H2J" and cc.spritePosition.name=="C00":
        cc.spritePosition.nextMove=cc.allPositions["C01"]
    if cc.spritePosition.name=="C03":
        cc.hide()
    if p.spritePosition.name=="H4J":
        if  k.spritePosition.name=="K03":
            print("got the key")
            p.spritePosition.nextMove=p.allPositions["H5T"]
            k.hide()
        else:
            print("missed the key")
            p.spritePosition.nextMove=p.allPositions["H7F"]
            k.show()
    if p.spritePosition.name=="L0G":
          k.show()
          cc.init()

    tick(FPS)
