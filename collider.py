from __future__ import annotations
import pygame
from pygame import Vector2
from enum import Enum
from gameobject import Gameobject


class ColliderTypes(Enum):
    CIRCLE = 1
    RECT = 2


class Collider(Gameobject):
    """a class for dectecting overlapping events."""

    def __init__(self, position, parrent=None, hidden=True):
        super().__init__(position, parrent, hidden)
    
    # void methods
    def draw(self) -> None:
        pass

    # returning methods
    def point_over(self, pos:Vector2) -> bool:
        return False

    def mouse_over(self) -> bool:
        return self.point_over(Vector2(pygame.mouse.get_pos()))


class CircleCollider(Collider):

    def __init__(self, position=Vector2(0, 0), radius:float=None, border_width:float=2, parrent:Gameobject=None, hidden:bool=True):
        """
        raduis: the size of the collier.
            if raduis is None will default to parrents radius
        """
        super().__init__(position, parrent, hidden)
        if radius != None:
            self.radius = radius
        else:
            self.radius = parrent.radius
        
        self.border_width = border_width

    def point_over(self, point:Vector2):
        return (point-self.global_position()).magnitude() <= self.radius

    def draw(self):
        color = (255, 0, 0) if self.mouse_over() else (0, 255, 0)
        pos = self.global_position()
        pygame.draw.circle(Gameobject.window, color, pos, self.radius, self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x, pos.y-self.radius), Vector2(pos.x, pos.y+self.radius), self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x-self.radius, pos.y), Vector2(pos.x+self.radius, pos.y), self.border_width)


class RectCollider(Collider):

    def __init__(self, position=Vector2(0, 0), size:list[float, float]=None, border_width:float=2, parrent:Gameobject=None, hidden:bool=True):
        """
        size: the size of the collier.
            if size is None will default to parrents size
        """
        super().__init__(position, parrent, hidden)
        if size != None:
            self.size = size
        else:
            self.size = parrent.size

        self.border_width = border_width

    def point_over(self, point:Vector2):
        pos = self.global_position()
        return pos.x < point.x < pos.x+self.size[0] and pos.y < point.y < pos.y+self.size[1]

    def draw(self):
        color = (255, 0, 0) if self.mouse_over() else (0, 255, 0)
        pos = self.global_position()
        pygame.draw.rect(Gameobject.window, color, (pos.x, pos.y, self.size[0], self.size[1]), self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x+self.border_width, pos.y+self.border_width), Vector2(pos.x+self.size[0]-self.border_width, pos.y+self.size[1]-self.border_width), self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x+self.border_width, pos.y+self.size[1]-self.border_width), Vector2(pos.x+self.size[0]-self.border_width, pos.y+self.border_width), self.border_width)


collider_classes = {
    ColliderTypes.CIRCLE: CircleCollider,
    ColliderTypes.RECT: RectCollider,
}

