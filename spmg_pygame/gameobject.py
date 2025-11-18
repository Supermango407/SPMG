from __future__ import annotations
import pygame
from pygame import Vector2


class Gameobject():
    """basic class with postion and drawing capabilities."""
    
    window:pygame.Surface = None
    """the window Gameobjects are drawn to."""
    gameobjects:list[Gameobject] = []
    """a list of gameobjects sorted background to foreground."""
    mouse_pos:Vector2 = Vector2(0, 0)
    """the position of the mouse cursor"""

    # static methods
    @staticmethod
    def static_start(window:pygame.Surface=None):
        """called at start of game."""
        if window != None:
            Gameobject.window = window

        for gameobject in Gameobject.gameobjects:
            gameobject.start()

    @staticmethod
    def static_update():
        """called once per frame."""
        for gameobject in Gameobject.gameobjects:
            gameobject.update()

    @staticmethod
    def static_event(event:pygame.event.Event):
        """called for every pygame event."""
        if event.type == pygame.MOUSEMOTION:
            Gameobject.mouse_pos = pygame.mouse.get_pos()
        
        # reversed so that the gamobjects on top have click events before once beneath them
        for gameobject in reversed(Gameobject.gameobjects):
            if gameobject.listen:
                gameobject.event(event)

    # built in
    def __init__(self,
    position:Vector2=Vector2(0, 0),
    anchor:Vector2=Vector2(0, 0),
    relative_position:Vector2=Vector2(0, 0),
    size:Vector2=Vector2(0, 0), parent:Gameobject=None,
    hidden:bool=False,
    listen:bool=False
    ):
        self.position = position
        """the local location relative to it's parrent."""
        self.anchor = anchor
        """where in the Gameobject the point [0, 0] is located on a scale from 0-1."""
        self.relative_position = relative_position
        """where in the parrent gameobect is placed on a scale from 0-1."""
        self.size = size
        """the width and height of Gameobject."""
        self.parent = parent
        """the Gameobject atached to. defaults to window."""
        self.hidden = hidden
        """if True the Gameobject won't be drawn."""
        self.listen = listen
        """if True the Gameobject event method will be called."""
        
        self.parent = None
        """the Gameobject `self` is attached to."""
        if parent != None:
            self.set_parrent(parent)

        self.global_position = Vector2(0, 0)
        self.window_position = Vector2(0, 0)
        self.children:list[Gameobject] = []

        Gameobject.gameobjects.append(self)

        self.set_size()
        self.set_position()
    
    # void methods
    def start(self) -> None:
        """called at start of game."""
        pass

    def update(self) -> None:
        """called once per frame."""
        if not self.hidden:
            self.draw()

    def draw(self) -> None:
        """draws `self` to `Gameobject.window`."""
        pass

    def event(self, event:pygame.event.Event) -> None:
        """called every pygame event if `self.listen` is True."""
        pass

    def set_position(self, new_postition:Vector2=None, set_children:bool=True) -> None:
        """set `position` to `new_position`,
        then updates `global_position` and `window_position` of `self`.
        `set_children`: sets children's position if True."""
        if new_postition != None:
            self.position = new_postition

        self.global_position = self.get_global_position()
        self.window_position = self.get_window_position()

        if set_children:
            for child in self.children:
                child.set_position()

    def set_size(self, new_size:Vector2=None, set_children:bool=True) -> None:
        """set the size of `self`.
        `set_children`: sets children's position if True."""
        if new_size != None:
            self.size = new_size

        # set position to correct anchor
        self.set_position()

        # sets children's positions to correct children with relative_positions.
        if set_children:
            for child in self.children:
                child.set_position()

    def render_on_top(self, move_parrent:bool=True) -> None:
        """moves `self` to the top of the gameobjects for drawing.
        move_parrent: if True will move it's parrents to the top as well."""
        if not move_parrent or self.parent == None:
            Gameobject.gameobjects.remove(self)
            Gameobject.gameobjects.append(self)

            for child in self.children:
                child.render_on_top(move_parrent=False)
        else:
            self.parent.render_on_top(move_parrent=True)

    def set_parrent(self, new_parrent:Gameobject) -> None:
        """adds self to `new_parrents` children and
        removes current parrent if it exist."""
        if self.parent != None:
            self.parent.children.remove(self)
        self.parent = new_parrent
        self.parent.children.append(self)

    def destroy(self) -> None:
        """destroys gameobject."""
        Gameobject.gameobjects.remove(self)
        del(self)

    # returning methods
    def get_window_position(self) -> Vector2:
        """returns the window position of `self`.
        NOTE: it doesn't work if `self.global_position` it's updated."""
        return self.global_position - self.anchor.elementwise()*self.size

    def get_global_position(self) -> Vector2:
        """returns the global position of `self`."""
        position = self.position.copy()

        if self.parent != None:
            position += self.parent.window_position
            position += self.relative_position.elementwise()*self.parent.size
        else:
            position += self.relative_position.elementwise()*Gameobject.window.get_size()
        
        return position

