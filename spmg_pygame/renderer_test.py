import pygame
from pygame import Vector2
import screeninfo
from PIL import Image

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
new_path = "//".join(sys.path[0].replace("\\", "/").split("/")[:-1])
if not new_path in sys.path:
    sys.path.append(new_path)


from spmg_pygame.gameobject import Gameobject
from spmg_pygame.renderer import Canvas_Renderer, ShaderVariable, ShaderVarTypes
from spmg_renderer.renderer import run_shader


if __name__ == '__main__':
    # move window to second monitor if it exits
    if len(screeninfo.get_monitors()) == 2: # two monitors
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400,75)

    # initiate window
    pygame.init()
    pygame.display.set_caption("SPMG")

    # Set global vars
    # window = pygame.display.set_mode((576, 576))
    window = pygame.display.set_mode((1056, 544))
    clock = pygame.time.Clock()
    Gameobject.static_start(window)
    
    default_image = Image.open('C:\\Users\\music\\OneDrive\\Desktop\\398380651_337908712171077_6359366298681019352_n.jpg')
    # default_image = Image.open('C:\\Users\\music\\OneDrive\\Desktop\\photos\\forest 3.jpg')
    # default_image = Image.open('spmg_pygame/border.png')
    # default_image = Image.open('small_test.jpg')

    # resize image
    # image_scaler = max(1, default_image.size[0]/1024, default_image.size[1]/512)
    # default_image = default_image.resize((int(default_image.size[0]//image_scaler), int(default_image.size[1]//image_scaler)))
    
    # func_test_img = run_shader(default_image, "spmg_renderer/invert_test.glsl")
    # func_test_img.save("func_test.png")

    # img_var = Image.new("RGBA", (20, 10), (0, 0, 0, 255))

    renderer = Canvas_Renderer(
        ["spmg_pygame/shader_test.glsl", "spmg_renderer/invert_test.glsl"],
        anchor=Vector2(0.5, 0.5),
        scaler=0.25,
        relative_position=Vector2(0.5, 0.5),
        group_sizes=[(1, 1), (1, 1)],
        # size=Vector2(512, 512),
        # default_color=(0, 255, 255, 255),
        texture_default_value=default_image,
        shader_vars=[
            [
                ShaderVariable(
                    name="offset",
                    data_type=ShaderVarTypes.FLOAT,
                    # value= 0.00390625*16 # 1/256
                ),
            ],
            # [
            #     ShaderVariable(
            #         name="ImageVar",
            #         data_type=ShaderVarTypes.IMAGE,
            #         array_buffer=3,
            #         value=img_var
            #     ),
            # ]
        ]
    )
    
    default_image.close()
    # renderer.run_shader(1)
    # renderer.get_shader_variable("ImageVar", 1).save('test.png')


    class Drawer(Gameobject):

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

        def draw(self):
            pygame.draw.circle(self.window, (0, 255, 0), self.global_position, 25)


    # drawer = Drawer(
    #     position=Vector2(50, 0),
    #     relative_position=Vector2(0.5, 0.5),
    #     anchor=Vector2(0.5, 0.5),
    #     parent=renderer,
    #     size=renderer.size
    # )
    

    def update():
        renderer.run_shader(0)


    # main loop
    running = True
    while running:
        window.fill((16, 16, 32))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print('run')
                renderer.run_shader(1)
                old_value = renderer.get_shader_variable("offset", 0)
                renderer.set_shader_variable("offset", old_value*-1, 0)
            else:
                Gameobject.static_event(event)
        
        update()
        Gameobject.static_update()
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
