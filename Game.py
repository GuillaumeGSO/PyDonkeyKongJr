from pygame_functions import *

from typing import  Protocol

class GameObject(Protocol):
    def update(self):
        """Updates the game."""

    def paint(self):
        """Paints the game."""

class Game(GameObject):
    def __init__(self, width: int, height: int, fps: int = 10 ):
        #WIDTH = 700
        #HEIGHT = 480
        #FPS = 10

        screenSize(self.width, self.height)
        setBackgroundImage("img/EmptyScreen.png")
        # setBackgroundImage("positions/FullScreen.png")

    def add_object(self, obj: GameObject):
        self.objects.append(obj)

    def remove_object(self, obj: GameObject):
        self.objects.remove(obj)

    def run(self):
        pass

    def update(self):
        """Updates the game."""
        for obj in self.objects:
            obj.update()

    def paint(self):
        """Paints the game."""
        #self.canvas.delete(tk.ALL)  # clear the screen
        #for obj in self.objects:
        #    obj.paint(self.canvas)