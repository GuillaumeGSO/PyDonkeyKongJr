import pygame as pg

from positions.SpritePosition import *


class Player():
    """
    One and only one player.
    It should contains all of its different locations and sprites
    """

    def __init__(self, game):
        self.game = game
        self.isNewTurn = True
        self.all_positions = self.generate_positions()
        self.sprite_position = None
        self.playerMove = None
        # self.sound = makeSound("sounds/Monkey.wav")

    def update(self, playerMove):

        if self.startOfGame():
            return

        # TODO print("threat", pg.sprite.spritecollideany(
        #     self.spritePosition, self.game.threat_group))

        if playerMove == None:
            newPosition = self.all_positions.get(self.sprite_position.nextMove)
        elif playerMove == "JUMP":
            newPosition = self.all_positions.get(self.sprite_position.jumpMove)
        elif playerMove == "LEFT":
            newPosition = self.all_positions.get(self.sprite_position.leftMove)
        elif playerMove == "RIGHT":
            newPosition = self.all_positions.get(
                self.sprite_position.rightMove)
        elif playerMove == "UP":
            newPosition = self.all_positions.get(self.sprite_position.upMove)
        elif playerMove == "DOWN":
            newPosition = self.all_positions.get(self.sprite_position.downMove)

        temp = self.handleKey()
        if temp != None:
            newPosition = temp

        self.handleFall()

        if newPosition != None:
            self.sprite_position.kill()
            self.sprite_position = newPosition
            self.game.player_group.add(self.sprite_position)
            playerMove = None

    def startOfGame(self):
        if self.sprite_position == None:
            self.sprite_position = self.all_positions.get("L0G")

        if self.sprite_position.positionName == "L0G" and self.isNewTurn:
            self.game.init_objects()
            self.game.player_group.add(self.sprite_position)
            self.isNewTurn = False
            return True
        return False

    def handleKey(self):
        if (self.sprite_position.positionName == "H4J"):
            collider = pg.sprite.spritecollideany(
                self.sprite_position, self.game.cage_group)
            if collider != None and collider.positionName == "K03":
                self.game.catch_key()
                return self.all_positions.get("H5O")
            return self.all_positions.get("H7F")
        return None

    def handleFall(self):
        if self.sprite_position.positionName == "H7L":
            self.game.add_missed()
        self.isNewTurn = True

    def generate_positions(self):
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
        d["L0G"].jumpMove = "L0H"
        d["L0G"].rightMove = "L1G"

        d["L0H"].downMove = "L0G"
        d["L0H"].rightMove = "L1J"

        d["L1G"].jumpMove = "L1J"
        d["L1G"].leftMove = "L0G"
        d["L1G"].rightMove = "L2G"

        d["L1J"].nextMove = "L1G"

        d["L2G"].jumpMove = "L2H"
        d["L2G"].leftMove = "L1G"
        d["L2G"].rightMove = "L3G"

        d["L2H"].leftMove = "L1J"
        d["L2H"].rightMove = "L3H"
        d["L2H"].downMove = "L2G"

        d["L3G"].jumpMove = "L3H"
        d["L3G"].leftMove = "L2G"
        d["L3G"].rightMove = "L4G"

        d["L3H"].leftMove = "L2H"
        d["L3H"].rightMove = "L4J"
        d["L3H"].downMove = "L3G"

        d["L4G"].jumpMove = "L4J"
        d["L4G"].leftMove = "L3G"
        d["L4G"].rightMove = "L5G"

        d["L4J"].nextMove = "L4G"

        d["L5G"].jumpMove = "L5H"
        d["L5G"].leftMove = "L4G"

        d["L5H"].leftMove = "L4J"
        d["L5H"].upMove = "H0G"
        d["L5H"].downMove = "L5G"
        # Higher level
        d["H0G"].leftMove = "H1G"
        d["H0G"].downMove = "L5H"

        d["H1G"].jumpMove = "H1H"
        d["H1G"].leftMove = "H2G"
        d["H1G"].rightMove = "H0G"

        d["H1H"].downMove = "H1G"

        d["H2G"].jumpMove = "H2J"
        d["H2G"].leftMove = "H3G"
        d["H2G"].rightMove = "H1G"

        d["H2J"].nextMove = "H2G"
        d["H2J"].leftMove = "H3G"

        d["H3G"].jumpMove = "H3J"
        d["H3G"].leftMove = "H7F"
        d["H3G"].upMove = "H4J"
        d["H3G"].rightMove = "H2G"

        d["H3J"].nextMove = "H3G"

        # Taking the key
        d["H5T"].nextMove = "H5O"
        # Opening the cage and win
        d["H5O"].nextMove = "H6W"
        d["H6W"].nextMove = "L0G"
        # Fail to get the key and loose
        d["H7F"].nextMove = "H7L"
        d["H7L"].nextMove = "L0G"
        return d
