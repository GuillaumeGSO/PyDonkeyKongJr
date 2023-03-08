"""
Thanks :
http://pica-pic.com/donkey_kong_jr/
https://www.youtube.com/watch?v=K9CoOYqqVLU
http://www.github.com/stevepaget/pygame_functions
https://mamedev.emulab.it/haze/2017-new-focus/

"""

from pygame_functions import PyGame
from Player import *
from Bird import *
from Key import *
from Croco import *
from Coco import *
from Missed import *
from Cage import *
from Score import *
import random
from Settings import *

class Main:

    def run(self):       
        game = PyGame()
        game.screenSize(WIDTH, HEIGHT)
        game.setBackgroundImage("img/EmptyScreen.png")
        # setBackgroundImage("positions/FullScreen.png")

        """
        Position of sprites are recorded using positionning_tool.py in a file named xxxPositions
        """
        game.setAutoUpdate(False)
        sc = Score(game)
        p = Player(game)
        b = Bird(game)  # TODO a list of birds randomly added
        k = Key(game)
        c = Croco(game)  # TODO a list of crocodile randomly added
        cc = Coco(game)
        m = Missed(game)
        cage = Cage(game)

        missed = 0
        cages = 1


        cage.restore_cages()

        #TODO game logic should be in objects

        while missed < 3:
            p.update()
            b.update()
            k.update()
            c.update()
            cc.update()

            # If the monkey is touched
            if p.spritePosition.eaterName == c.spritePosition.name or p.spritePosition.eaterName == b.spritePosition.name:
                #m.update(missed)
                #missed += 1
                pass
            
            # If the coconut hit a crocodile
            if cc.visible and c.spritePosition.eaterName == cc.spritePosition.name:
                print("coco touch croco")
                sc.addPoints(game,3)
                if c.spritePosition.name == "C09":
                    print("coco touch lower croco")
                    sc.addPoints(game,3)
                    game.hideSprite(c.spritePosition.sprite)
                cc.init()
                cc.visible = False
            
            # If the coconut hit a bird
            if  cc.visible and c.spritePosition.eaterName == b.spritePosition.name:
                print("coco touched bird")
                sc.addPoints(game,6)
                game.hideSprite(c.spritePosition.sprite)
                cc.init()
                cc.visible = False
            
            # If the monkey touch the coconut, it falls
            if p.spritePosition.name == "H2J" and cc.spritePosition.name == "C00":
                cc.spritePosition.nextMove = cc.allPositions["C01"]

            # If the coconut reach the bottom : hide it
            if cc.visible and cc.spritePosition.name == "C03":
                cc.init()
                cc.visible = False
            

            # If monkey is jumping to the key
            if p.spritePosition.name == "H4J":
                if k.spritePosition.name == "K03":
                    # Monkey grab the key
                    p.spritePosition.nextMove = p.allPositions["H5T"]
                    sc.addPoints(game, random.randrange(5, 10))
                    cage.hide_cage(4-cages)
                    k.hide()
                    cages -= 1
                    if cages == 0:
                        #Mummy is free !
                        p.update()
                        p.update()
                        sc.addPoints(game,25)
                        cage.show_smile()
                        game.pause(1000)
                else:
                    # Monkey jump for the key
                    game.pause(300)
                    p.spritePosition.nextMove = p.allPositions["H7F"]
                    p.update()
                    
                    # Monkey miss the key
                    m.update(missed)
                    missed += 1
                    
                    # Monkey finish in the bush
                    p.update()
                    game.pause(300)
            # If monkey is falling...
            if p.spritePosition.name == "H7F":
                m.update(missed)
                missed += 1
                # Monkey finish in the bush
                game.pause(300)
                p.update()
                game.pause(300)

            # If starting position : reset some stuff
            if p.spritePosition.name == "L0G":
                k.show()
                cc.init()
                if cages == 0:
                    cages = 4
                    cage.hide_smile()
                    cage.restore_cages()

            game.tick(FPS)
        game.endWait()

def main():
    Main().run()

if __name__ == "__main__":
    main()
