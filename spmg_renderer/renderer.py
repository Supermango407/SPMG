from typing import Union
import moderngl
import numpy
from PIL import Image
from dataclasses import dataclass
from enum import Enum

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("//".join(sys.path[0].replace("\\", "/").split("/")[:-1]))


@ dataclass
class ShaderVarType():
    glsl_type:str
    numbers:int
    python_type:type
    numpy_type:type


class ShaderVarTypes():
    BOOL = ShaderVarType("bool", 1, bool, numpy.bool)
    INT = ShaderVarType("int", 1, int, numpy.int32)
    UINT = ShaderVarType("uint", 1, int, numpy.uint32)
    FLOAT = ShaderVarType("float", 1, float, numpy.float32)
    DOUBLE = ShaderVarType("double", 1, float, numpy.float64)
    VEC2 = ShaderVarType("vec2", 2, tuple[float, float], numpy.float32)
    VEC3 = ShaderVarType("vec3", 3, tuple[float, float, float], numpy.float32)
    VEC4 = ShaderVarType("vec4", 4, tuple[float, float, float, float], numpy.float32)
    IVEC2 = ShaderVarType("ivec2", 2, tuple[int, int], numpy.int32)
    IVEC3 = ShaderVarType("ivec3", 3, tuple[int, int, int], numpy.int32)
    IVEC4 = ShaderVarType("ivec4", 4, tuple[int, int, int, int], numpy.int32)
    UVEC2 = ShaderVarType("uvec2", 2, tuple[int, int], numpy.uint32)
    UVEC3 = ShaderVarType("uvec3", 3, tuple[int, int, int], numpy.uint32)
    UVEC4 = ShaderVarType("uvec4", 4, tuple[int, int, int, int], numpy.uint32)
    BVEC2 = ShaderVarType("bvec2", 2, tuple[bool, bool], numpy.bool)
    BVEC3 = ShaderVarType("bvec3", 3, tuple[bool, bool, bool], numpy.bool)
    BVEC4 = ShaderVarType("bvec4", 4, tuple[bool, bool, bool, bool], numpy.bool)
    DVEC2 = ShaderVarType("dvec2", 2, tuple[float, float], numpy.float64)
    DVEC3 = ShaderVarType("dvec3", 3, tuple[float, float, float], numpy.float64)
    DVEC4 = ShaderVarType("dvec4", 4, tuple[float, float, float, float], numpy.float64)
    # TODO
    # MAT2 = 21
    # MAT3 = 22
    # MAT4 = 23


@dataclass
class ShaderVariable(object):
    """for handling uniform variables in shaders."""
    name:str
    """name of variable in shader."""
    data_type:ShaderVarType
    """the type of variable in shader."""
    array_buffer:Union[int, None] = None
    """the buffer index for an array. leave None if not an array."""
    array_size:Union[int, None] = None
    """the size for an array. leave None if not an array."""
    value:object=None
    """the value of variable."""


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
        self.array_buffers:list[dict[str, moderngl.Buffer]] = []
        """2D list for array vars, since they need a buffer to assign values."""

        self.shader_text = []
        for path in self.shader_paths:
            with open(path, 'r') as link:
                self.shader_text.append(link.read())
        
        # create/get image
        if default_image == None:
            if size == None:
                raise ValueError("either default image, or size needs a value")
            self.size = size
            self.image:Image = Image.new("RGBA", self.size, (255, 255, 255, 255))
        else:
            self.image:Image = default_image.convert("RGBA")
            self.size = self.image.size
        
        self.context = moderngl.create_standalone_context(require=430)
        
        shader_vars_to_set = []
        """a list of variables with default values to set after compute shader
        is create. format: [(`name`, `value`, `shader`), ...]"""
        # set the shader variables
        for shader, varables in enumerate(shader_vars):
            self.shader_vars.append({})
            self.array_buffers.append({})
            for shader_var in varables:
                if shader_var.array_buffer == None: # not an array
                    if shader_var.value == None: # no default value
                        shader_var.value = shader_var.data_type.python_type()
                    else:
                        shader_vars_to_set.append((shader_var.name, shader_var.value, shader))
                else: # is an array
                    if shader_var.value is None: # no default value
                        array = numpy.zeros([
                            shader_var.array_size,
                            shader_var.data_type.numbers
                        ])
                        shader_var.value = array
                    else:
                        shader_vars_to_set.append((shader_var.name, shader_var.value, shader))
                        array = numpy.array(
                            shader_var.value,
                            dtype=shader_var.data_type.numpy_type
                        )
                    self.array_buffers[shader][shader_var.name] = self.context.buffer(array.tobytes())
                    self.array_buffers[shader][shader_var.name].bind_to_storage_buffer(shader_var.array_buffer)

                self.shader_vars[shader][shader_var.name] = shader_var

        # create input texture
        self.input_texture = self.context.texture(
            self.size,
            components=4,
            data=self.image.tobytes(),
            dtype='f1'
        )
        self.input_texture.bind_to_image(unit=0, read=True, write=False)

        # create output texture
        self.output_texture = self.context.texture(
            self.size,
            components=4,
            dtype='f1'
        )
        self.output_texture.bind_to_image(unit=1, read=False, write=True)

        self.compute_shaders = []
        for text in self.shader_text:
            self.compute_shaders.append(self.context.compute_shader(text))

        # set the groups for the shaders
        for shader, size in enumerate(self.group_sizes):
            self.group_sizes[shader] = (int(self.size[0] // size[0]), int(self.size[1] // size[1]))

        # set default_values
        for name, value, shader in shader_vars_to_set:
            self.set_shader_variable(name, value, shader)

    def set_shader_variable(self, variable_name:str, value, shader:int=0):
        """set the uniform variable in shader"""
        self.shader_vars[shader][variable_name].value = value
        shader_var:ShaderVariable = self.shader_vars[shader][variable_name]
        if shader_var.array_buffer == None: # not an array
            self.compute_shaders[shader][shader_var.name] = shader_var.data_type.python_type(shader_var.value)
        else: # is an array
            array = numpy.array(
                shader_var.value,
                dtype=shader_var.data_type.numpy_type
            )
            self.array_buffers[shader][variable_name].write(array.tobytes())
    
    def get_shader_variable(self, variable_name:str, shader:int=0) -> ShaderVariable:
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
