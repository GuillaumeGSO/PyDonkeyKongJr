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
FPS = 10

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

while True:
    p.update()  
    b.update()
    k.update()
    c.update()
    cc.update()
    tick(FPS)
   