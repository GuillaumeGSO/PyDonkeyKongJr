"""
Thanks :
http://pica-pic.com/donkey_kong_jr/
https://www.youtube.com/watch?v=K9CoOYqqVLU
# http://www.github.com/stevepaget/pygame_functions
https://mamedev.emulab.it/haze/2017-new-focus/

"""

import pygame as pg
from settings import *
import sys
import os
from donkey_kong_jr import DonkeyKongJr

class App:

    def __init__(self):
        pg.init();
        pg.display.set_caption(SCREEN_NAME)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.bg = pg.image.load(os.path.join("img", "EmptyScreen.png")).convert()
        self.screen.blit(self.bg, [0,0])
        self.clock = pg.time.Clock()
        self.game = DonkeyKongJr(self)
        

    def update(self):
        self.game.update()
        self.clock.tick(FPS)

    def draw(self):
        self.game.draw()
        pg.display.flip()

    def check_events(self):
        self.game.playerMove = None
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.game.playerMove = "LEFT"
                elif event.key == pg.K_RIGHT:
                    self.game.playerMove = "RIGHT"
                elif event.key == pg.K_UP:
                    self.game.playerMove = "UP"
                elif event.key == pg.K_DOWN:
                    self.game.playerMove = "DOWN"
                elif event.key == pg.K_SPACE:
                    self.game.playerMove = "JUMP"

                
    

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
        



    # def runold(self):       
    #     game = PyGame()
    #     game.screenSize(WIDTH, HEIGHT)
    #     game.setBackgroundImage("img/EmptyScreen.png")

    #     """
    #     Position of sprites are recorded using positionning_tool.py in a file named xxxPositions
    #     """
    #     game.setAutoUpdate(False)
    #     sc = Score(game)
    #     p = Player(game)
    #     b = Bird(game)  # TODO a list of birds randomly added
    #     k = Key(game)
    #     c = Croco(game)  # TODO a list of crocodile randomly added
    #     cc = Coco(game)
    #     m = Missed(game)
    #     cage = Cage(game)

    #     missed = 0
    #     cages = 1


    #     cage.restore_cages()

    #     #TODO game logic should be in objects

    #     while missed < 3:
    #         p.update()
    #         b.update()
    #         k.update()
    #         c.update()
    #         cc.update()

    #         # If the monkey is touched
    #         if p.spritePosition.eaterName == c.spritePosition.name or p.spritePosition.eaterName == b.spritePosition.name:
    #             #m.update(missed)
    #             #missed += 1
    #             pass
            
    #         # If the coconut hit a crocodile
    #         if cc.visible and c.spritePosition.eaterName == cc.spritePosition.name:
    #             print("coco touch croco")
    #             sc.addPoints(game,3)
    #             if c.spritePosition.name == "C09":
    #                 print("coco touch lower croco")
    #                 sc.addPoints(game,3)
    #                 game.hideSprite(c.spritePosition.sprite)
    #             cc.init()
    #             cc.visible = False
            
    #         # If the coconut hit a bird
    #         if  cc.visible and c.spritePosition.eaterName == b.spritePosition.name:
    #             print("coco touched bird")
    #             sc.addPoints(game,6)
    #             game.hideSprite(c.spritePosition.sprite)
    #             cc.init()
    #             cc.visible = False
            
    #         # If the monkey touch the coconut, it falls
    #         if p.spritePosition.name == "H2J" and cc.spritePosition.name == "C00":
    #             cc.spritePosition.nextMove = cc.allPositions["C01"]

    #         # If the coconut reach the bottom : hide it
    #         if cc.visible and cc.spritePosition.name == "C03":
    #             cc.init()
    #             cc.visible = False
            

    #         # If monkey is jumping to the key
    #         if p.spritePosition.name == "H4J":
    #             if k.spritePosition.name == "K03":
    #                 # Monkey grab the key
    #                 p.spritePosition.nextMove = p.allPositions["H5T"]
    #                 sc.addPoints(random.randrange(5, 10))
    #                 cage.hide_cage(4-cages)
    #                 k.hide()
    #                 cages -= 1
    #                 if cages == 0:
    #                     #Mummy is free !
    #                     p.update()
    #                     p.update()
    #                     sc.addPoints(25)
    #                     cage.show_smile()
    #                     game.pause(1000)
    #             else:
    #                 # Monkey jump for the key
    #                 game.pause(300)
    #                 p.spritePosition.nextMove = p.allPositions["H7F"]
    #                 p.update()
                    
    #                 # Monkey miss the key
    #                 m.update(missed)
    #                 missed += 1
                    
    #                 # Monkey finish in the bush
    #                 p.update()
    #                 game.pause(300)
    #         # If monkey is falling...
    #         if p.spritePosition.name == "H7F":
    #             m.update(missed)
    #             missed += 1
    #             # Monkey finish in the bush
    #             game.pause(300)
    #             p.update()
    #             game.pause(300)

    #         # If starting position : reset some stuff
    #         if p.spritePosition.name == "L0G":
    #             k.show()
    #             cc.init()
    #             if cages == 0:
    #                 cages = 4
    #                 cage.hide_smile()
    #                 cage.restore_cages()

    #         game.tick(FPS)
    #     game.endWait()



if __name__ == "__main__":
    app = App()
    app.run()
