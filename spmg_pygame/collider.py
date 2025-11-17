from __future__ import annotations
import pygame
from pygame import Vector2
from enum import Enum

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("//".join(sys.path[0].replace("\\", "/").split("/")[:-1]))

from spmg_pygame.gameobject import Gameobject


class ColliderTypes(Enum):
    CIRCLE = 1
    RECT = 2


class Collider(Gameobject):
    """a class for dectecting overlapping events."""

    def __init__(self,
    hidden:bool=True,
    border_width:float=2,
    on_click:callable=None,
    on_release:callable=None,
    on_clicking:callable=None,
    on_right_click:callable=None,
    on_right_release:callable=None,
    on_right_clicking:callable=None,
    **kwargs
    ):
        super().__init__(hidden=hidden, listen=True, **kwargs)
        self.border_width = border_width
        """the the thickness border."""
        self.on_click = on_click
        """called when mouse left button clicks over collider."""
        self.on_release = on_release
        """called when mouse left button lets go over collider."""
        self.on_clicking = on_clicking
        """called when mouse left button is down over collider."""
        self.on_right_click = on_right_click
        """called when mouse right button clicks over collider."""
        self.on_right_release = on_right_release
        """called when mouse right button lets go over collider."""
        self.on_right_clicking = on_right_clicking
        """called when mouse rightq button is down over collider."""
    
    # void methods
    def update(self):
        if self.mouse_over():
            # call holding mouse events
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
        """whether a point is in colider."""
        return False

    def mouse_over(self) -> bool:
        """wheter mouse is over `self`."""
        return self.point_over(Vector2(pygame.mouse.get_pos()))


class CircleCollider(Collider):
    """a circular colider."""

    def __init__(self,
    radius:float=None,
    hidden:bool=True,
    **kwargs
    ):
        super().__init__(hidden=hidden, **kwargs)
        
        # default radius to parents raduis if radius is None.
        self.radius = None
        """raduis: the size of the collier."""
        if radius != None:
            self.radius = radius
        elif hasattr(self.parent, "radius") != None:
                self.radius = self.parent.radius

    def point_over(self, point:Vector2):
        return (point-self.get_global_position()).magnitude() <= self.radius

    def draw(self):
        color = (255, 0, 0) if self.mouse_over() else (0, 255, 0)
        pos = self.get_global_position()
        pygame.draw.circle(Gameobject.window, color, pos, self.radius, self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x, pos.y-self.radius), Vector2(pos.x, pos.y+self.radius), self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x-self.radius, pos.y), Vector2(pos.x+self.radius, pos.y), self.border_width)


class RectCollider(Collider):
    """a rectangle collider"""

    def __init__(self,
    hidden:bool=True,
    size:Vector2=None,
    **kwargs
    ):
        super().__init__(hidden=hidden, **kwargs)

        self.size = None
        """the size of the rect."""
        if size != None:
            self.size = size
        else:
            self.size = self.parent.size

    def point_over(self, point:Vector2):
        return self.window_position.x < point.x < self.window_position.x+self.size[0] and self.window_position.y < point.y < self.window_position.y+self.size[1]

    def draw(self):
        color = (255, 0, 0) if self.mouse_over() else (0, 255, 0)
        pygame.draw.rect(Gameobject.window, color, (self.window_position.x, self.window_position.y, self.size[0], self.size[1]), self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(self.window_position.x+self.border_width, self.window_position.y+self.border_width), Vector2(self.window_position.x+self.size[0]-self.border_width, self.window_position.y+self.size[1]-self.border_width), self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(self.window_position.x+self.border_width, self.window_position.y+self.size[1]-self.border_width), Vector2(self.window_position.x+self.size[0]-self.border_width, self.window_position.y+self.border_width), self.border_width)


collider_classes = {

    ColliderTypes.CIRCLE: CircleCollider,
    ColliderTypes.RECT: RectCollider,
}

