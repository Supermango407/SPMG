from __future__ import annotations
import pygame
from pygame import Vector2

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("\\".join(current_dir.split("\\")[:-1]))

from spmg_math import lerp


class Gameobject():
    """basic class with postion and drawing capabilities."""
    window:pygame.Surface = None
    anchors:dict[Gameobject] = {}
    gameobjects:list[Gameobject] = []
    mouse_pos:Vector2 = Vector2(0, 0)

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
        if event.type == pygame.MOUSEMOTION:
            Gameobject.mouse_pos = pygame.mouse.get_pos()
        # reversed so that the gamobjects on top have click events before once beneath them
        for gameobject in reversed(Gameobject.gameobjects):
            if gameobject.listen:
                gameobject.event(event)

    # built in
    def __init__(self, position:Vector2=Vector2(0, 0), anchor:Vector2=Vector2(0, 0), relative_position:Vector2=Vector2(0, 0), size:Vector2=Vector2(0, 0), parrent:Gameobject=None, hidden:bool=False, listen:bool=False):
        f"""
            `position`: the local location relative to it's parrent.
            `anchor`: where in the Gameobject the point [0, 0] is located on a scale from 0-1.
            `relative_position`: where in the parrent gameobect is placed on a scale from 0-1.
            `size`: the width and height of Gameobject.
            `parrent`: the Gameobject atached to. defaults to window.
            `hidden`: if True the Gameobject won't be drawn.
            `listen`: if True the Gameobject event method will be called.
        """
        self.position = position
        self.anchor = anchor
        self.relative_position = relative_position
        self.size = size
        self.parrent = parrent
        self.hidden = hidden
        self.listen = listen

        if parrent != None:
            parrent.children.append(self)

        self.global_position = Vector2(0, 0)
        self.window_position = Vector2(0, 0)
        self.children:list[Gameobject] = []

        self.set_position()

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
        if new_postition != None:
            self.position = new_postition

        self.global_position = self.get_global_position()
        self.window_position = self.get_window_position()

        # print(type(self), self.position, self.global_position, self.window_position)

        for child in self.children:
            child.set_position()

    def set_size(self, new_size:Vector2=None):
        """set the size of `self`."""
        if new_size != None:
            self.size = new_size

        # set children location to correct any children with relative_positions.
        for child in self.children:
            child.set_position()

    def render_on_top(self, move_parrent:bool=True):
        """
            moves `self` to the top of the gameobjects for drawing.
            move_parrent: if True will move it's parrents to the top as well.
        """
        if not move_parrent or self.parrent == None:
            Gameobject.gameobjects.remove(self)
            Gameobject.gameobjects.append(self)

            for child in self.children:
                child.render_on_top(move_parrent=False)
        else:
            self.parrent.render_on_top(move_parrent=True)

    # returning methods
    def get_window_position(self):
        return self.global_position - self.anchor.elementwise()*self.size

    def get_global_position(self) -> Vector2:
        position = self.position.copy()

        if self.parrent != None:
            position += self.parrent.get_global_position()
            position += self.relative_position.elementwise()*self.parrent.size
        else:
            position += self.relative_position.elementwise()*Gameobject.window.get_size()
        
        return position
