from PIL import Image
import numpy

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("//".join(sys.path[0].replace("\\", "/").split("/")[:-1]))

# import spmg_renderer.renderer as Renderer
from spmg_renderer.renderer import Renderer, ShaderVariable, ShaderVarTypes

if __name__ == '__main__':
    # default_image:Image = Image.open('C:\\Users\\music\\OneDrive\\Desktop\\398380651_337908712171077_6359366298681019352_n.jpg')
    # default_image:Image = Image.open('C:\\Users\\music\\OneDrive\\Desktop\\photos\\forest 3.jpg')
    # default_image:Image = Image.open('spmg_pygame/border.png')

    # resize image
    # image_scaler = max(1, default_image.size[0]/1024, default_image.size[1]/512)
    # default_image = default_image.resize((int(default_image.size[0]//image_scaler), int(default_image.size[1]//image_scaler)))
    
    renderer = Renderer(
        ["spmg_renderer/point_test.glsl", "spmg_renderer/invert_test.glsl"],
        texture_size=(512, 512),
        shader_vars=[[
            ShaderVariable(
                name="radius",
                data_type=ShaderVarTypes.INT,
                value=50
            ),
            ShaderVariable(
                name="points",
                data_type=ShaderVarTypes.IVEC2,
                array_size=3,
                array_buffer=2,
                value=[[0, 0], [256, 256], [512, 512]]
            ),
        ]]
    )

    print(renderer.get_shader_variable("points"))
    renderer.set_shader_variable("points", [[128, 384], [256, 256], [384, 128]])
    print(renderer.get_shader_variable("points"))
    
    renderer.run_shader()
    renderer.run_shader(1)
    # renderer.image.show()
    renderer.image.save("spmg_renderer/save.png")

    # new_image:Image = Renderer.run_shader(, "spmg_renderer/shader_test.glsl")
    # new_image.save("spmg_renderer/save.png")

    # default_image.close()
