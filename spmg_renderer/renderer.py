import moderngl
import numpy
from PIL import Image
from dataclasses import dataclass

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("//".join(sys.path[0].replace("\\", "/").split("/")[:-1]))


@dataclass
class ShaderVariable(object):
    """for handling uniform variables in shaders."""
    name:str
    data_type:type
    value=None


class Renderer(object):
    """takes a image and runs compute shaders on it."""

    def __init__(self,
    shader_path:str,
    default_image:Image=None,
    size:tuple[int, int]=None,
    shader_vars:list[ShaderVariable]=[],
    group_size:tuple[int, int]=(1, 1),
    ):
        self.shader_path:str = shader_path
        """the path to the file the shader is in."""
        self.group_size:tuple[int, tuple] = group_size
        """the size of the groups in the shader."""
        self.shader_vars:dict[str, ShaderVariable] = {}
        """the uniform variables in shader."""

        for shader_var in shader_vars:
            if shader_var.value == None:
                shader_var.value = shader_var.data_type()
            self.shader_vars[shader_var.name] = shader_var

        with open(self.shader_path, 'r') as link:
            self.shader_text = link.read()
        
        # create/get image
        if default_image == None:
            if size == None:
                raise ValueError("either default image, or size needs a value")
            self.size = size
            self.image:Image = Image.new("RGBA", self.size, (255,)*4)
        else:
            self.image:Image = default_image.convert("RGBA")
            self.size = self.image.size
        
        self.context = moderngl.create_standalone_context(require=430)
        
        # create input texture
        self.input_texture = self.context.texture(
            self.size,
            components=4,
            data=self.image.tobytes(),
            dtype='u1'
        )
        self.input_texture.bind_to_image(unit=0, read=True, write=False)

        # create output texture
        self.output_texture = self.context.texture(
            self.size,
            components=4,
            dtype='u1'
        )
        self.output_texture.bind_to_image(unit=1, read=False, write=True)

        self.compute_shader = self.context.compute_shader(self.shader_text)
        
        # set the groups for the shader
        self.group_size = (int(self.size[0] // group_size[0]), int(self.size[1] // group_size[1]))

    def set_shader_variable(self, variable_name:str, value, shader:int=0):
        """set the uniform variable in shader"""
        self.shader_vars[variable_name].value = value
        shader_var = self.shader_vars[variable_name]
        self.compute_shader[self.shader_vars[variable_name].name] = shader_var.data_type(shader_var.value)

    
    def get_shader_var(self, variable_name:str, shader:int=0) -> ShaderVariable:
        """returns the value of shader variable."""
        return self.shader_vars[variable_name].value


    def run_shader(self):
        "runs shader."
        self.compute_shader.run(group_x=self.group_size[0], group_y=self.group_size[1])
        output_data = numpy.frombuffer(self.output_texture.read(), dtype=numpy.uint8).reshape(self.size[1], self.size[0], 4)
        self.image = Image.fromarray(output_data, "RGBA")

        self.input_texture.write(self.image.tobytes())


def run_shader(input_image:Image, shader_path:str, group_size:tuple[int, int]=(1, 1)) -> Image:
    """returns `input_image` after shader at `shader_path` is computed."""
    renderer = Renderer(shader_path=shader_path, default_image=input_image, group_size=group_size)
    renderer.run_shader()
    return renderer.image
