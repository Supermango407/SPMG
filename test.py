import pygame
from pygame import Vector2
import os
from gameobject import Gameobject
from collider import CircleCollider, RectCollider


class Circle(Gameobject):

    def __init__(self, position, radius:float, color:tuple[3]):
        """
            raduis: the size of the circle.
            color: the color of the circle.
        """
        super().__init__(position)
        self.radius = radius
        self.color = color
        self.collider = CircleCollider(parrent=self, hidden=False)

    def draw(self):
        pygame.draw.circle(Gameobject.window, self.color, self.global_position(), self.radius)


class Rect(Gameobject):
    def __init__(self, position, size:list[float, float], color:tuple[int, int, int]):
        """
            color: the color of the circle.
        """
        super().__init__(position)
        self.size = size
        self.color = color
        self.collider = RectCollider(parrent=self, hidden=False)

    def draw(self):
        pos = self.global_position()
        pygame.draw.rect(Gameobject.window, self.color, (pos.x, pos.y, self.size[0], self.size[1]))


circle = Circle(Vector2(150, 100), 50, (255, 255, 255))
rect = Rect(Vector2(250, 250), [150, 100], (255, 255, 255))


if __name__ == '__main__':
    # move window to second monitor
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400,75)

    # initiate window
    pygame.init()
    pygame.display.set_caption("Table Top")

    # Set global vars
    window = pygame.display.set_mode((512, 512))
    clock = pygame.time.Clock()
    Gameobject.window = window
    
    # main loop
    running = True
    while running:
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        Gameobject.static_update()

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
