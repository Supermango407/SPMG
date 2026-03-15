import pygame
from pygame import Vector2
from PIL import Image
import moderngl
import numpy

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("//".join(sys.path[0].replace("\\", "/").split("/")[:-1]))

from spmg_pygame.gameobject import Gameobject
from spmg_renderer.renderer import Renderer


class Canvas_Renderer(Gameobject):

    def __init__(self,
    shader_path:str,
    group_size=(32, 32),
    default_image:Image=None,
    position:Vector2=Vector2(0, 0),
    anchor:Vector2=Vector2(0, 0),
    relative_position:Vector2=Vector2(0, 0),
    size:Vector2=Vector2(0, 0),
    parent:Gameobject=None,
    hidden:bool=False,
    listen:bool=False
    ):
        super().__init__(position, anchor, relative_position, size, parent, hidden, listen)
    
        # create renderer
        self.renderer = Renderer(
            shader_paths=shader_path,
            default_image=default_image,
            size=None if size == Vector2(0, 0) else (size.x, size.y),
            group_sizes=group_size
        )

        # create pygame image
        self.pygame_image = pygame.image.fromstring(
            self.renderer.image.tobytes(),
            self.renderer.image.size,
            self.renderer.image.mode,
        )

        self.set_size(self.pygame_image.get_size())

    def run_shader(self, shader:int=0):
        """runs the shader, and updates the image."""
        self.renderer.run_shader(shader)

        # update pygame image
        self.pygame_image = pygame.image.fromstring(
            self.renderer.image.tobytes(),
            self.renderer.image.size,
            self.renderer.image.mode
        )

    def update(self):
        self.run_shader()
        super().update()

    def draw(self):
        self.window.blit(self.pygame_image, self.window_position)
        super().draw()
