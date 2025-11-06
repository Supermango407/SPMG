import pygame
from pygame import Vector2
import screeninfo
import os
from gameobject import Gameobject
from ui import Text, Button


if __name__ == '__main__':
    # move window to second monitor if it exsits
    if len(screeninfo.get_monitors()) == 2: # two monitors
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400,75)

    # initiate window
    pygame.init()
    pygame.display.set_caption("SPMG")

    # Set global vars
    window = pygame.display.set_mode((512, 512))
    clock = pygame.time.Clock()
    Gameobject.window = window
    Gameobject.static_start()
    
    text = Text("testing", position=Vector2(0, 10), anchor=Vector2(0.5, 0), relative_position=Vector2(0.5, 0))
    button = Button(lambda: print('click'), "next test", anchor=Vector2(0.5, 0.5), relative_position=Vector2(0.5, 0.5))
    button.set_position()

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
        pygame.draw.circle(window, (0, 255, 255), Vector2(window.get_size())*0.5, 8)
        pygame.draw.line(window, (0, 255, 255), Vector2(0, 0), Vector2(window.get_size()[0], 0), 4)
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
