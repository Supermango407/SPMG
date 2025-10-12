from __future__ import annotations
import pygame
from pygame import Vector2


class Gameobject():
    """basic class with postion and drawing capabilities."""
    window:pygame.surface = None
    gameobjects:list[Gameobject] = []

    # static methods
    @staticmethod
    def static_start():
        """called at start of game."""
        for gameobject in Gameobject.gameobjects:
            gameobject.start()

    @staticmethod
    def static_update():
        """called once per frame."""
        for gameobject in Gameobject.gameobjects:
            gameobject.update()

    @staticmethod
    def static_event(event:pygame.event.Event):
        """called every pygame event."""
        for gameobject in Gameobject.gameobjects:
            if gameobject.listen:
                gameobject.event(event)

    # built in
    def __init__(self, position:Vector2, parrent:Gameobject=None, hidden:bool=False, listen:bool=False):
        """
            position: the local location relative to it's parrent.
            parrent: the gameobject atached to.
            hidden: if True the Gameobject won't be drawn.
            listen: if True the Gameobject event method will be called.
        """
        self.position = position
        self.parrent = parrent
        self.hidden = hidden
        self.listen = listen

        self.children:list[Gameobject] = []

        if parrent != None:
            parrent.children.append(self)

        Gameobject.gameobjects.append(self)
    
    # void methods
    def start(self) -> None:
        """called at start of game."""
        pass

    def update(self) -> None:
        """called once per frame."""
        if not self.hidden:
            self.draw()

    def draw(self) -> None:
        pass

    def event(self, event:pygame.event.Event):
        """called every pygame event if `self.listen` is True."""
        pass

    def set_position(self, new_postition:Vector2=None):
        """set the local position of `self`."""
        if new_postition == None:
            new_postition = self.position

        self.position = new_postition
        for child in self.children:
            child.set_position()

    # returning methods
    def global_position(self) -> Vector2:
        if self.parrent != None:
            return self.position + self.parrent.global_position()
        else:
            return self.position

