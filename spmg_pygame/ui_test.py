import pygame
from pygame import Vector2
import screeninfo
import os
from gameobject import Gameobject, center_anchor
from ui import Text, Button


if __name__ == '__main__':
    # move window to second monitor if it exsits
    if len(screeninfo.get_monitors()) == 2: # two monitors
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400,75)

    # initiate window
    pygame.init()
    pygame.display.set_caption("SPMG")

    text = Text("testing")
    button = Button(lambda: print('click'), "next test", parrent=center_anchor)

    # Set global vars
    window = pygame.display.set_mode((512, 512))
    clock = pygame.time.Clock()
    Gameobject.window = window
    Gameobject.static_start()
    
    # main loop
    running = True
    while running:
        window.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                Gameobject.static_event(event)
        
        Gameobject.static_update()
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
