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


class Canvas_Renderer(Gameobject):
    def __init__(self,
    shader_link:str,
    group_size=(32, 32),
    position:Vector2=Vector2(0, 0),
    anchor:Vector2=Vector2(0, 0),
    relative_position:Vector2=Vector2(0, 0),
    size:Vector2=Vector2(0, 0),
    parent:Gameobject=None,
    hidden:bool=False,
    listen:bool=False,
    default_image:Image=None
    ):
        super().__init__(position, anchor, relative_position, size, parent, hidden, listen)
        # get shader text from link
        self.shader_link = shader_link
        with open(self.shader_link, 'r') as link:
            self.shader_text = link.read()
        
        # create/get image
        if default_image == None:
            self.image:Image = Image.new("RGBA", (int(self.size.x), int(self.size.y)), (255, 255, 255, 255))
        else:
            self.image:Image = default_image
            self.set_size(Vector2(*self.image.size))
        
        self.context = moderngl.create_standalone_context(require=430)
        
        # create input texture
        self.input_texture = self.context.texture(
            (int(self.size.x), int(self.size.y)),
            components=4,
            data=self.image.tobytes(),
            dtype='u1'
        )
        self.input_texture.bind_to_image(unit=0, read=True, write=False)

        # create output texture
        self.output_texture = self.context.texture(
            (int(self.size.x), int(self.size.y)),
            components=4,
            dtype='u1'
        )
        self.output_texture.bind_to_image(unit=1, read=False, write=True)

        self.compute_shader = self.context.compute_shader(self.shader_text)
        
        # set the groups for the shader
        self.group_size = (int(self.size.x // group_size[0]), int(self.size.y // group_size[1]))

        image_bytes = self.image.tobytes()
        self.pygame_image = pygame.image.fromstring(
            image_bytes,
            self.image.size,
            self.image.mode
        )

        self.input_texture.write(image_bytes)

    def run_shader(self):
        """runs the shader, and updates the image."""
        self.compute_shader.run(group_x=self.group_size[0], group_y=self.group_size[1])
        output_data = numpy.frombuffer(self.output_texture.read(), dtype=numpy.uint8).reshape(int(self.size.x), int(self.size.y), 4)
        self.image = Image.fromarray(output_data, "RGBA")

        # update image surface
        self.pygame_image = pygame.image.fromstring(
            self.image.tobytes(),
            self.image.size,
            self.image.mode
        )

        self.input_texture.write(self.image.tobytes())

    def update(self):
        self.run_shader()
        super().update()

    def draw(self):
        self.window.blit(self.pygame_image, self.window_position)
        super().draw()
