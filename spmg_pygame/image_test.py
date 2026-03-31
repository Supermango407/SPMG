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
from spmg_pygame.image import Image_Renderer

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
    
    # default_image = Image.open('C:\\Users\\music\\OneDrive\\Desktop\\398380651_337908712171077_6359366298681019352_n.jpg')
    new_image = Image.open('C:\\Users\\music\\OneDrive\\Desktop\\photos\\forest 3.jpg')
    default_image = Image.open('spmg_pygame/border.png')
    # default_image = Image.open('small_test.jpg')

    renderer = Image_Renderer(
        default_image,
        scaler=1,
        anchor=Vector2(0.5, 0.5),
        relative_position=Vector2(0.5, 0.5),
    )

    # resize image
    # image_scaler = max(1, default_image.size[0]/1024, default_image.size[1]/512)
    # default_image = default_image.resize((int(default_image.size[0]//image_scaler), int(default_image.size[1]//image_scaler)))
    
    # main loop
    running = True
    while running:
        window.fill((16, 16, 32))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print('run')
                renderer.set_image(new_image)
                renderer.set_scaler(2)
            else:
                Gameobject.static_event(event)
        
        Gameobject.static_update()
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
