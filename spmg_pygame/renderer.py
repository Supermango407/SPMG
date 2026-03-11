import pygame
from pygame import Vector2
from PIL import Image

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("//".join(sys.path[0].replace("\\", "/").split("/")[:-1]))

from spmg_pygame.gameobject import Gameobject

print('test')

class Canvas_Renderer(Gameobject):
    def __init__(self,
    position:Vector2=Vector2(0, 0),
    anchor:Vector2=Vector2(0, 0),
    relative_position:Vector2=Vector2(0, 0),
    size:Vector2=Vector2(0, 0),
    parent:Gameobject=None,
    hidden:bool=False,
    listen:bool=False
    ):
        super().__init__(position, anchor, relative_position, size, parent, hidden, listen)
        self.image = Image.new("RGBA", (int(self.size.x), int(self.size.y)), (255, 255, 255))
        self.surface = pygame.image.fromstring(
            self.image.tobytes(),
            self.image.size,
            self.image.mode
        )

    def draw(self):
        self.window.blit(self.surface, self.window_position)
        super().draw()