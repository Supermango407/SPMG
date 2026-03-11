import pygame
from pygame import Vector2
import screeninfo
from PIL import Image

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("//".join(sys.path[0].replace("\\", "/").split("/")[:-1]))

from spmg_pygame.gameobject import Gameobject
from spmg_pygame.renderer import Canvas_Renderer


if __name__ == '__main__':
    # move window to second monitor if it exits
    if len(screeninfo.get_monitors()) == 2: # two monitors
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400,75)

    # initiate window
    pygame.init()
    pygame.display.set_caption("SPMG")

    # Set global vars
    window = pygame.display.set_mode((576, 576))
    clock = pygame.time.Clock()
    Gameobject.static_start(window)
    
    # default_image = Image.open('spmg_pygame/default_image.png')
    renderer = Canvas_Renderer(
        "spmg_pygame/shader_test.glsl",
        anchor=Vector2(0.5, 0.5),
        relative_position=Vector2(0.5, 0.5),
        size=Vector2(512, 512)
        # default_image=default_image
    )
    # default_image.close()

    # main loop
    running = True
    while running:
        window.fill((16, 16, 32))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print('run')
                renderer.run_shader()
            else:
                Gameobject.static_event(event)
        
        Gameobject.static_update()
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
