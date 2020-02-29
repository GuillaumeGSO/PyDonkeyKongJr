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
from Cage import *
from Score import *
import random


WIDTH = 700
HEIGHT = 480
FPS = 6

screenSize(WIDTH, HEIGHT)
setBackgroundImage("img/EmptyScreen.png")
# setBackgroundImage("positions/FullScreen.png")

"""
Position of sprites are recorded using positionning_tool.py in a file named xxxPositions
"""
setAutoUpdate(False)
sc = Score()
p = Player()
b = Bird()  # TODO a list of birds randomly added
k = Key()
c = Croco()  # TODO a list of crocodile randomly added
cc = Coco()
m = Missed()
cage = Cage()

missed = 0
cages = 4


cage.restore_cages()

while missed < 3:
    p.update()
    b.update()
    k.update()
    c.update()
    cc.update()
    
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
            sc.addPoints(random.randrange(5, 10))
            cage.hide_cage(4-cages)
            cages -= 1
            if cages == 0:
                sc.addPoints(25)
                cage.show_smile()
                p.update()
                p.update()
                pause(1000)
        else:
            # Monkey miss the key
            m.update(missed)
            missed += 1
            p.spritePosition.nextMove = p.allPositions["H7F"]
            # Monkey finish in the bush
            pause(300)
            p.update()
            pause(300)
            p.update()
            pause(300)
    # If monkey is falling...
    if p.spritePosition.name == "H7F":
        m.update(missed)
        missed += 1
        # Monkey finish in the bush
        pause(300)
        p.update()
        pause(300)

    # If starting position : reset some stuff
    if p.spritePosition.name == "L0G":
        k.show()
        cc.init()
        if cages == 0:
            cages = 4
            cage.hide_smile()
            cage.restore_cages()

    tick(FPS)
endWait()
