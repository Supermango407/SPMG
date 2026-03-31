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
new_path = "//".join(sys.path[0].replace("\\", "/").split("/")[:-1])
if not new_path in sys.path:
    sys.path.append(new_path)

from spmg_pygame.gameobject import Gameobject
from spmg_pygame.image import Image_Renderer, pygame_to_PIL
from spmg_renderer.renderer import Renderer, ShaderVariable, ShaderVarTypes, ShaderVarType


class Canvas_Renderer(Image_Renderer):
    
    @ staticmethod
    def array_to_image_bytes(texture_array:numpy.ndarray):
        """converts numpy array from `Renderer` to image bytes."""
        return (texture_array*255).astype('uint8').tobytes()

    def __init__(self,
    shader_paths:Union[str, list[str]],
    texture_default_value:Image=None,
    texture_size:tuple[int, int]=None,
    default_color: tuple[int, int, int, int]=(255, 255, 255, 255),
    shader_vars:Union[list[ShaderVariable], list[list[ShaderVariable]]]=[],
    group_sizes:Union[tuple[int, int], list[tuple[int, int]]]=None,
    texture_type:ShaderVarType=ShaderVarTypes.IMAGE,
    start_buffer:int=0,
    scaler:float = 1,
    position:Vector2=Vector2(0, 0),
    anchor:Vector2=Vector2(0, 0),
    relative_position:Vector2=Vector2(0, 0),
    parent:Gameobject=None,
    hidden:bool=False,
    listen:bool=False
    ):
        # scale image down if necessary
        if scaler < 1 and isinstance(texture_default_value, Image.Image):
            texture_default_value = texture_default_value.resize((
                int(texture_default_value.size[0]*scaler),
                int(texture_default_value.size[1]*scaler)
            ), resample=Image.BOX)
            scaler=1
    
        # create renderer
        self.renderer = Renderer(
            shader_paths=shader_paths,
            texture_default_value=texture_default_value,
            texture_size=texture_size,
            default_color=default_color,
            shader_vars=shader_vars,
            group_sizes=group_sizes,
            texture_type=texture_type,
            start_buffer=start_buffer
        )

        # set the scaler so `get_pygame_image` doesn't cause an error
        self.scaler=scaler

        super().__init__(
            image=self.get_pygame_image(),
            scaler=scaler,
            position=position,
            anchor=anchor,
            relative_position=relative_position,
            parent=parent,
            hidden=hidden,
            listen=listen
        )
        self.set_position()

    def run_shader(self, shader:int=0):
        """runs the shader, and updates the image."""
        self.renderer.run_shader(shader)

        self.update_image(False)
    
    def update_image(self, update_array=True):
        """set `self.image` to the texture.
        `update_array: if False wont waste time refetching array."""
        if update_array:
            self.renderer.input_texture_array = self.renderer.get_texture_array(self.renderer.input_texture)

        self.image = self.get_pygame_image()
        self.render()

    def set_shader_variable(self, variable_name:str, value, shader:int=0):
        """set the uniform variable in shader"""
        self.renderer.set_shader_variable(variable_name=variable_name, value=value, shader=shader)
    
    def get_shader_variable(self, variable_name:str, shader:int=0) -> ShaderVariable:
        """returns the value of shader variable."""
        return self.renderer.get_shader_variable(variable_name=variable_name, shader=shader)

    def get_pygame_image(self):
        """generates pygame image from `self.renderer`"""
        return pygame.image.fromstring(
            self.array_to_image_bytes(self.renderer.input_texture_array),
            self.renderer.texture_size,
            "RGBA"
        )

    def draw(self):
        self.window.blit(self.image, self.window_position)
        super().draw()
