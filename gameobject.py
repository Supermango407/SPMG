from __future__ import annotations
import pygame
from pygame import Vector2


class Gameobject():
    """basic class with postion and drawing capabilities."""
    window:pygame.surface = None
    gameobjects:list[Gameobject] = []

    # static methods
    @staticmethod
    def static_update():
        for gameobject in Gameobject.gameobjects:
            gameobject.update()

    # built in
    def __init__(self, position:Vector2, parrent:Gameobject=None, hidden=False):
        """
            position: the local location relative to it's parrent.
            parrent: the gameobject atached to.
            hidden: if True the Gameobject won't be drawn.
        """
        self.position = position
        self.parrent = parrent
        self.hidden = hidden

        Gameobject.gameobjects.append(self)
    
    # void methods
    def start(self) -> None:
        pass

    def update(self) -> None:
        if not self.hidden:
            self.draw()

    def draw(self) -> None:
        pass

    # returning methods
    def global_position(self) -> Vector2:
        if self.parrent != None:
            return self.position + self.parrent.global_position()
        else:
            return self.position

