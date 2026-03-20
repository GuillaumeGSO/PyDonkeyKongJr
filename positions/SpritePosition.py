import json
import os
import pygame as pg


class SpritePosition(pg.sprite.Sprite):

    def __init__(self, name, actorType):
        pg.sprite.Sprite.__init__(self)
        self.position_name = name
        self.actor_type = actorType
        self.path = self.generate_path()
        self.image = self.load_image(self.path)
        self.rect = self.image.get_rect()
        self.jump_move = None
        self.up_move = None
        self.down_move = None
        self.left_move = None
        self.right_move = None
        self.next_move = None
        self.eater_name = None

        self.dict_positions = self.get_all_positions(self.actor_type)
        self.x = self.dict_positions.get(self.position_name)[0]
        self.y = self.dict_positions.get(self.position_name)[1]
        self.rect.x = self.x
        self.rect.y = self.y

    def generate_path(self):
        return "img/sprites/" + self.actor_type + "/" + self.position_name + ".png"

    def update(self):
        if self.next_move is not None:
            self.position_name = self.next_move
            self.path = self.generate_path()
            self.image = self.load_image(self.path)
            self.rect = self.image.get_rect()
            self.x = self.dict_positions.get(self.position_name)[0]
            self.y = self.dict_positions.get(self.position_name)[1]
            self.rect.x = self.x
            self.rect.y = self.y

    @staticmethod
    def get_all_positions(file_name):
        json_path = "positions/" + file_name + "Positions.json"
        if os.path.isfile(json_path):
            with open(json_path, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def load_image(fileName, useColorKey=False):
        if os.path.isfile(fileName):
            image = pg.image.load(fileName)
            image = image.convert_alpha()
            # Return the image
            return image
        else:
            raise Exception(
                f"Error loading image: {fileName} – Check filename and path ?")
