from __future__ import annotations
import pygame
from pygame import Vector2
from enum import Enum
from gameobject import Gameobject


class ColliderTypes(Enum):
    CIRCLE = 1


class Collider(Gameobject):

    def __init__(self, position, parrent=None, hidden=True):
        super().__init__(position, parrent, hidden)
    
    # void methods
    def draw(self) -> None:
        pass

    # returning methods
    def point_over(self, pos:Vector2) -> bool:
        return False

    def mouse_over(self) -> bool:
        return self.point_over(pygame.mouse.get_pos())


class CircleCollider(Collider):

    def __init__(self, position=Vector2(0, 0), radius=None, border_width:float=2, parrent=None, hidden=True):
        super().__init__(position, parrent, hidden)
        if radius != None:
            self.radius = radius
        else:
            self.radius = parrent.radius
        self.border_width = border_width

    def point_over(self, pos):
        return (pos-self.global_position()).magnitude() <= self.radius

    def draw(self):
        color = (255, 0, 0) if self.mouse_over() else (0, 255, 0)
        pos = self.global_position()
        pygame.draw.circle(Gameobject.window, color, pos, self.radius, self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x, pos.y-self.radius), Vector2(pos.x, pos.y+self.radius), self.border_width)
        pygame.draw.line(Gameobject.window, color, Vector2(pos.x-self.radius, pos.y), Vector2(pos.x+self.radius, pos.y), self.border_width)


collider_classes = {
    ColliderTypes.CIRCLE: CircleCollider
}

