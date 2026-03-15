from typing import Union
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
    shader_paths:Union[str, list[str]],
    default_image:Image=None,
    size:tuple[int, int]=None,
    shader_vars:Union[list[ShaderVariable], list[list[ShaderVariable]]]=[],
    group_sizes:Union[tuple[int, int], list[tuple[int, int]]]=None,
    ):
        # set shader attributes to lists if there is only one
        if not type(shader_paths) is list:
            shader_paths = [shader_paths]
        if not type(group_sizes) is list:
            if group_sizes == None:
                # assume there are multiple shaders and
                # set the default values for all of them
                group_sizes = []
                for i in shader_paths:
                    group_sizes.append((1, 1))
            else:
                # assume there is only one shader and
                # set group sizes to be a list of sizes instead of just one
                group_sizes = [group_sizes]
        if len(shader_vars) > 0 and not type(shader_vars[0]) is list:
            shader_vars = [shader_vars]

        self.shader_paths:list[str] = shader_paths
        """list of paths to the files where the shaders are."""
        self.group_sizes:list[tuple[int, tuple]] = group_sizes
        """list of sizes for the shader groups."""
        self.shader_vars:list[dict[str, ShaderVariable]] = []
        """2D list for the uniform variables in shaders."""

        # set the shader variables
        for shader, varables in enumerate(shader_vars):
            self.shader_vars.append({})
            for shader_var in varables:
                if shader_var.value == None:
                    shader_var.value = shader_var.data_type()
                self.shader_vars[shader][shader_var.name] = shader_var

        self.shader_text = []
        for path in self.shader_paths:
            with open(path, 'r') as link:
                self.shader_text.append(link.read())
        
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

        self.compute_shaders = []
        for text in self.shader_text:
            self.compute_shaders.append(self.context.compute_shader(text))
        
        # set the groups for the shaders
        for shader, size in enumerate(self.group_sizes):
            self.group_sizes[shader] = (int(self.size[0] // size[0]), int(self.size[1] // size[1]))

    def set_shader_variable(self, variable_name:str, value, shader:int=0):
        """set the uniform variable in shader"""
        self.shader_vars[shader][variable_name].value = value
        shader_var:ShaderVariable = self.shader_vars[shader][variable_name]
        self.compute_shaders[shader][shader_var.name] = shader_var.data_type(shader_var.value)

    
    def get_shader_var(self, variable_name:str, shader:int=0) -> ShaderVariable:
        """returns the value of shader variable."""
        return self.shader_vars[shader][variable_name].value


    def run_shader(self, shader:int=0):
        "runs shader."
        self.compute_shaders[shader].run(group_x=self.group_sizes[shader][0], group_y=self.group_sizes[shader][1])
        output_data = numpy.frombuffer(self.output_texture.read(), dtype=numpy.uint8).reshape(self.size[1], self.size[0], 4)
        self.image = Image.fromarray(output_data, "RGBA")

        self.input_texture.write(self.image.tobytes())


def run_shader(input_image:Image, shader_path:str, group_size:tuple[int, int]=(1, 1)) -> Image:
    """returns `input_image` after shader at `shader_path` is computed."""
    renderer = Renderer(shader_paths=shader_path, default_image=input_image, group_sizes=group_size)
    renderer.run_shader()
    return renderer.image
