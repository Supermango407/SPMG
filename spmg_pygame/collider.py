from __future__ import annotations
import pygame
from pygame import Vector2
from enum import Enum

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from gameobject import Gameobject


class ColliderTypes(Enum):
    CIRCLE = 1
    RECT = 2


class Collider(Gameobject):
    """a class for dectecting overlapping events."""

    def __init__(self, position, parrent=None, hidden=True, listen=True, on_click:callable=None, on_release:callable=None, on_clicking:callable=None, on_right_click:callable=None, on_right_release:callable=None, on_right_clicking:callable=None, **kwargs):
        """
            `on_click`: called when mouse left button clicks over collider.
            `on_rlease`: called when mouse left button lets go over collider.
            `on_clicking`: called when mouse left button is down over collider.
            `on_right_click`: called when mouse right button clicks over collider.
            `on_right_rlease`: called when mouse right button lets go over collider.
            `on_right_clicking`: called when mouse rightq button is down over collider.
        """
        super().__init__(position=position, parrent=parrent, hidden=hidden, listen=listen, **kwargs)
        self.on_click = on_click
        self.on_release = on_release
        self.on_clicking = on_clicking
        self.on_right_click = on_right_click
        self.on_right_release = on_right_release
        self.on_right_clicking = on_right_clicking
    
    # void methods
    def update(self):
        if self.mouse_over():
            mouse_buttons_pressed = pygame.mouse.get_pressed()
            if self.on_clicking != None and mouse_buttons_pressed[0]:
                self.on_clicking()
            if self.on_right_clicking != None and mouse_buttons_pressed[2]:
                self.on_right_clicking()

        super().update()

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.on_click != None and self.mouse_over():
                    self.on_click()
            if event.button == 3:
                if self.on_right_click != None and self.mouse_over():
                    self.on_right_click()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.on_release != None and self.mouse_over():
                    self.on_release()
            if event.button == 3:
                if self.on_right_release != None and self.mouse_over():
                    self.on_right_release()
        super().event(event)
    
    def draw(self) -> None:
        pass

    # returning methods
    def point_over(self, pos:Vector2) -> bool:
        return False

    def mouse_over(self) -> bool:
        return self.point_over(Vector2(pygame.mouse.get_pos()))


class CircleCollider(Collider):

    def __init__(self, position=Vector2(0, 0), radius:float=None, border_width:float=2, parrent:Gameobject=None, hidden:bool=True, **kwargs):
        """
        raduis: the size of the collier.
            if raduis is None will default to parrents radius
        """
        super().__init__(position=position, parrent=parrent, hidden=hidden, **kwargs)
        if radius != None:
            self.radius = radius
        else:
            self.radius = parrent.radius
        
        self.border_width = border_width

    def point_over(self, point:Vector2):
        return (point-self.get_global_position()).magnitude() <= self.radius

    def draw(self):
        color = (255, 0, 0) if self.mouse_over() else (0, 255, 0)
        pos = self.get_global_position()
        pygame.draw.circle(Gameobject.window, color, pos, self.radius, self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x, pos.y-self.radius), Vector2(pos.x, pos.y+self.radius), self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x-self.radius, pos.y), Vector2(pos.x+self.radius, pos.y), self.border_width)


class RectCollider(Collider):

    def __init__(self, position=Vector2(0, 0), size:list[float, float]=None, border_width:float=2, parrent:Gameobject=None, hidden:bool=True, **kwargs):
        """
        size: the size of the collier.
            if size is None will default to parrents size
        """
        super().__init__(position=position, parrent=parrent, hidden=hidden, **kwargs)
        if size != None:
            self.size = size
        else:
            self.size = parrent.size

        self.border_width = border_width

    def point_over(self, point:Vector2):
        pos = self.get_global_position()
        return pos.x < point.x < pos.x+self.size[0] and pos.y < point.y < pos.y+self.size[1]

    def draw(self):
        color = (255, 0, 0) if self.mouse_over() else (0, 255, 0)
        pos = self.get_global_position()
        pygame.draw.rect(Gameobject.window, color, (pos.x, pos.y, self.size[0], self.size[1]), self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x+self.border_width, pos.y+self.border_width), Vector2(pos.x+self.size[0]-self.border_width, pos.y+self.size[1]-self.border_width), self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x+self.border_width, pos.y+self.size[1]-self.border_width), Vector2(pos.x+self.size[0]-self.border_width, pos.y+self.border_width), self.border_width)


collider_classes = {
    ColliderTypes.CIRCLE: CircleCollider,
    ColliderTypes.RECT: RectCollider,
}

