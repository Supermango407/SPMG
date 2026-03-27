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
    numpy_string:str


class ShaderVarTypes():
    BOOL = ShaderVarType("bool", 1, bool, numpy.bool, "b1")
    INT = ShaderVarType("int", 1, int, numpy.int32, "f4")
    UINT = ShaderVarType("uint", 1, int, numpy.uint32, "f4")
    FLOAT = ShaderVarType("float", 1, float, numpy.float32, "f4")
    DOUBLE = ShaderVarType("double", 1, float, numpy.float64, "f8")
    VEC2 = ShaderVarType("vec2", 2, tuple[float, float], numpy.float32, "f4")
    VEC3 = ShaderVarType("vec3", 3, tuple[float, float, float], numpy.float32, "f4")
    VEC4 = ShaderVarType("vec4", 4, tuple[float, float, float, float], numpy.float32, "f4")
    IVEC2 = ShaderVarType("ivec2", 2, tuple[int, int], numpy.int32, "f4")
    IVEC3 = ShaderVarType("ivec3", 3, tuple[int, int, int], numpy.int32, "f4")
    IVEC4 = ShaderVarType("ivec4", 4, tuple[int, int, int, int], numpy.int32, "f4")
    UVEC2 = ShaderVarType("uvec2", 2, tuple[int, int], numpy.uint32, "f4")
    UVEC3 = ShaderVarType("uvec3", 3, tuple[int, int, int], numpy.uint32, "f4")
    UVEC4 = ShaderVarType("uvec4", 4, tuple[int, int, int, int], numpy.uint32, "f4")
    BVEC2 = ShaderVarType("bvec2", 2, tuple[bool, bool], numpy.bool, "b1")
    BVEC3 = ShaderVarType("bvec3", 3, tuple[bool, bool, bool], numpy.bool, "b1")
    BVEC4 = ShaderVarType("bvec4", 4, tuple[bool, bool, bool, bool], numpy.bool, "b1")
    DVEC2 = ShaderVarType("dvec2", 2, tuple[float, float], numpy.float64, "f8")
    DVEC3 = ShaderVarType("dvec3", 3, tuple[float, float, float], numpy.float64, "f8")
    DVEC4 = ShaderVarType("dvec4", 4, tuple[float, float, float, float], numpy.float64, "f8")
    IMAGE = ShaderVarType("image2D", 1, Image, numpy.ndarray, "f1")
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
    buffers:dict[int, moderngl.Buffer] = {}
    context:moderngl.Context = None

    def __init__(self,
    shader_paths:Union[str, list[str]],
    texture_default_value:Image=None,
    texture_size:tuple[int, int]=None,
    default_color: tuple[int, int, int, int]=(255, 255, 255, 255),
    shader_vars:Union[list[ShaderVariable], list[list[ShaderVariable]]]=[],
    group_sizes:Union[tuple[int, int], list[tuple[int, int]]]=None,
    texture_type:ShaderVariable=ShaderVarTypes.IMAGE,
    start_buffer:int=0
    ):
        # set shader attributes to lists if there is only one
        if not type(shader_paths) is list:
            shader_paths = [shader_paths]
        if not type(group_sizes) is list:
            if group_sizes is None:
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

        self.texture_type:ShaderVariable = texture_type
        """the type of the input and output textures"""
        
        # add context if it doesn't exist
        if Renderer.context is None:
            Renderer.context = moderngl.create_standalone_context(require=430)
        
        # create/get input texture value
        if texture_default_value is None:
            if texture_size is None:
                raise ValueError("either default image, or size needs a value")
            self.texture_size = texture_size
            if self.texture_type is ShaderVarTypes.IMAGE: # is an image
                self.input_texture_bytes:Union[Image.Image, numpy.ndarray] = Image.new("RGBA", self.texture_size, default_color).tobytes()
            else:
                self.input_texture_bytes:Union[Image.Image, numpy.ndarray] = numpy.full((self.texture_size[1], self.texture_size[0], 4), default_color, dtype=self.texture_type.numpy_type).tobytes()
        else:
            if self.texture_type is ShaderVarTypes.IMAGE: # is an image
                self.input_texture_bytes = texture_default_value.convert("RGBA").tobytes()
                self.texture_size = texture_default_value.size
            else: # is an array
                self.input_texture_bytes:Union[Image.Image, numpy.ndarray] = numpy.array(texture_default_value, dtype=self.texture_type.numpy_type).tobytes()
                self.texture_size = (len(texture_default_value), 1)

        # create input texture
        self.input_texture = Renderer.context.texture(
            self.texture_size,
            components=4,
            data=self.input_texture_bytes,
            dtype=self.texture_type.numpy_string
        )
        self.input_texture.bind_to_image(unit=start_buffer)
        Renderer.buffers[start_buffer] = self.input_texture

        # # create output texture
        self.output_texture = Renderer.context.texture(
            self.texture_size,
            components=4,
            dtype=self.texture_type.numpy_string
        )
        self.output_texture.bind_to_image(unit=start_buffer+1)
        Renderer.buffers[start_buffer+1] = self.output_texture

        # get shader text
        self.shader_text = []
        for path in self.shader_paths:
            with open(path, 'r') as link:
                self.shader_text.append(link.read())
        
        shader_vars_to_set = []
        """a list of variables with default values to set after compute shader
        is create. format: [(`name`, `value`, `shader`), ...]"""
        # set the shader variables
        for shader, varables in enumerate(shader_vars):
            # create dict with input and output textures
            self.shader_vars.append({})

            for shader_var in varables:
                if shader_var.array_buffer is None: # not an array or image
                    if shader_var.value is None: # no default value
                        shader_var.value = shader_var.data_type.python_type()
                    else:
                        shader_vars_to_set.append((shader_var.name, shader_var.value, shader))
                elif shader_var.array_size is None: # is an image
                    if Renderer.buffers.get(shader_var.array_buffer) is None: # buffer doesn't exist yet
                        if shader_var.value is None: # no default value
                            raise(ValueError("image variables need a default value"))
                        elif type(shader_var.value) is not Image.Image: # default value is not an image
                            raise(ValueError("image variables need a default value of type Image"))
                        # create image texture
                        var_image:Image = shader_var.value
                        Renderer.buffers[shader_var.array_buffer] = Renderer.context.texture(
                            var_image.size,
                            components=4,
                            data=var_image.tobytes(),
                            dtype='f1'
                        )
                        Renderer.buffers[shader_var.array_buffer].bind_to_image(unit=shader_var.array_buffer)
                    else:
                        shader_var.value = Image.frombytes("RGBA", shader_var.value.size, Renderer.buffers[shader_var.array_buffer].read())
                else: # is an array
                    if Renderer.buffers.get(shader_var.array_buffer) is None: # buffer doesn't exist yet
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
                        Renderer.buffers[shader_var.array_buffer] = Renderer.context.buffer(array.tobytes())
                        Renderer.buffers[shader_var.array_buffer].bind_to_storage_buffer(shader_var.array_buffer)
                    else:
                        shader_var.value = numpy.frombuffer(Renderer.buffers[shader_var.array_buffer].read(), dtype=shader_var.data_type.numpy_type).reshape(-1, shader_var.data_type.numbers)
                    
                self.shader_vars[shader][shader_var.name] = shader_var

        self.compute_shaders = []
        for text in self.shader_text:
            self.compute_shaders.append(Renderer.context.compute_shader(text))

        # set the groups for the shaders
        for shader, group_size in enumerate(self.group_sizes):
            self.group_sizes[shader] = (int(self.texture_size[0] // group_size[0]), int(self.texture_size[1] // group_size[1]))

        # set default_values
        for name, var_image, shader in shader_vars_to_set:
            self.set_shader_variable(name, var_image, shader)

    def set_shader_variable(self, variable_name:str, value, shader:int=0):
        """set the uniform variable in shader"""
        self.shader_vars[shader][variable_name].value = value
        shader_var:ShaderVariable = self.shader_vars[shader][variable_name]
        if shader_var.array_buffer is None: # not an array
            self.compute_shaders[shader][shader_var.name] = shader_var.data_type.python_type(shader_var.value)
        elif shader_var.array_size is None: # is an image
            var_image:Image = shader_var.value
            Renderer.buffers[shader_var.array_buffer].write(var_image.tobytes())
        else: # is an array
            array = numpy.array(
                shader_var.value,
                dtype=shader_var.data_type.numpy_type
            )
            Renderer.buffers[shader_var.array_buffer].write(array.tobytes())
    
    def get_shader_variable(self, variable_name:str, shader:int=0) -> any:
        """returns the value of shader variable."""
        shader_var:ShaderVariable = self.shader_vars[shader][variable_name]
        if shader_var.array_buffer is None: # not an array or image
            return self.shader_vars[shader][variable_name].value
        elif shader_var.array_size is None: # is an image
            bytes = Renderer.buffers[shader_var.array_buffer].read()
            array = numpy.frombuffer(bytes, dtype='f4')
            return Image.frombytes("RGBA", shader_var.value.size, array)
        else: # is an array
            bytes = Renderer.buffers[shader_var.array_buffer].read()
            array = numpy.frombuffer(bytes, dtype="f4").reshape(-1, shader_var.data_type.numbers)
            value = []
            for i in list(array):
                value.append(shader_var.data_type.python_type(i))
            return value

    def run_shader(self, shader:int=0):
        "runs shader."
        self.compute_shaders[shader].run(group_x=self.group_sizes[shader][0], group_y=self.group_sizes[shader][1])
        
        if self.texture_type == ShaderVarTypes.IMAGE: # is an image
            output_data = numpy.frombuffer(self.output_texture.read(), dtype=numpy.uint8).reshape(self.texture_size[1], self.texture_size[0], 4)
            self.input_texture_bytes = Image.fromarray(output_data, "RGBA").tobytes()
        else: # is an array
            output_data = numpy.frombuffer(self.output_texture.read(), dtype=numpy.float32).reshape(self.texture_size[1], self.texture_size[0], 4)
            self.input_texture_bytes = output_data.tobytes()
        
        
        self.input_texture.write(self.input_texture_bytes)
        Renderer.context.finish()


def run_shader(input_image:Image, shader_path:str, group_size:tuple[int, int]=(1, 1)) -> Image:
    """returns `input_image` after shader at `shader_path` is computed."""
    renderer = Renderer(shader_paths=shader_path, texture_default_value=input_image, group_sizes=group_size)
    renderer.run_shader()
    return renderer.input_texture_bytes
