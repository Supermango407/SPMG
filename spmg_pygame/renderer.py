from typing import Union
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
from spmg_renderer.renderer import Renderer, ShaderVariable, ShaderVarTypes


class Canvas_Renderer(Gameobject):

    def __init__(self,
    shader_paths:Union[str, list[str]],
    default_image:Image=None,
    shader_vars:Union[list[ShaderVariable], list[list[ShaderVariable]]]=[],
    group_sizes:Union[tuple[int, int], list[tuple[int, int]]]=None,
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
            shader_paths=shader_paths,
            default_image=default_image,
            size=None if size == Vector2(0, 0) else (int(size.x), int(size.y)),
            shader_vars=shader_vars,
            group_sizes=group_sizes
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

    def set_shader_variable(self, variable_name:str, value, shader:int=0):
        """set the uniform variable in shader"""
        self.renderer.set_shader_variable(variable_name=variable_name, value=value, shader=shader)
    
    def get_shader_variable(self, variable_name:str, shader:int=0) -> ShaderVariable:
        """returns the value of shader variable."""
        return self.renderer.get_shader_variable(variable_name=variable_name, shader=shader)

    def update(self):
        self.run_shader()
        super().update()

    def draw(self):
        self.window.blit(self.pygame_image, self.window_position)
        super().draw()
