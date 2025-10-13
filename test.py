import pygame
from pygame import Vector2
import os
from gameobject import Gameobject
from collider import CircleCollider, RectCollider
from draggable import draggable


@draggable
class Circle(Gameobject):

    def __init__(self, position, radius:float, color:tuple[3]):
        """
            raduis: the size of the circle.
            color: the color of the circle.
        """
        super().__init__(position, listen=True)
        self.radius = radius
        self.color = color
        self.collider = CircleCollider(
            parrent=self,
            hidden=False,
            on_click=self.click,
            on_release=self.release,
            on_right_click=self.right_click,
            on_right_release=self.right_release,
            on_clicking=self.clicking,
            on_right_clicking=self.right_clicking
        )

    def draw(self):
        pygame.draw.circle(Gameobject.window, self.color, self.global_position(), self.radius)

    def click(self):
        print('circle clicked')

    def release(self):
        print('circle released')
    
    def right_click(self):
        print('circle right clicked')

    def right_release(self):
        print('circle right released')

    def clicking(self):
        print('circle clicking')
        
    def right_clicking(self):
        print('circle right clicking')

    # def started_dragging(self):
        # print('started', self)
    
    def stopped_dragging(self, start:Vector2, end:Vector2):
        # print('stopped', start, end, self)
        self.set_position(start)
    
    # def update(self):
    #     super().update()
    #     self.set_position(self.position+Vector2(1, 0))


@draggable
class Rect(Gameobject):
    def __init__(self, position, size:list[float, float], color:tuple[int, int, int]):
        """
            color: the color of the circle.
        """
        super().__init__(position, listen=True)
        self.size = size
        self.color = color
        self.collider = RectCollider(parrent=self, hidden=False)

    def draw(self):
        pos = self.global_position()
        pygame.draw.rect(Gameobject.window, self.color, (pos.x, pos.y, self.size[0], self.size[1]))

    # def started_dragging(self):
    #     print('started', self)
    
    # def stopped_dragging(self, start:Vector2, end:Vector2):
    #     print('stopped', start, end, self)

    # def update(self):
    #     super().update()
    #     self.set_position(self.position+Vector2(0, -1))


circle = Circle(Vector2(150, 100), 50, (255, 255, 255))
rect = Rect(Vector2(250, 250), [150, 100], (255, 255, 255))


if __name__ == '__main__':
    # move window to second monitor
    # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400,75)

    # initiate window
    pygame.init()
    pygame.display.set_caption("SPMG")

    # Set global vars
    window = pygame.display.set_mode((512, 512))
    clock = pygame.time.Clock()
    Gameobject.window = window
    Gameobject.static_start()
    
    # main loop
    running = True
    while running:
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                Gameobject.static_event(event)
        
        Gameobject.static_update()
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
