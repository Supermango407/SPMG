from __future__ import annotations
import pygame
from pygame import Vector2
from gameobject import Gameobject
import collider
from collider import Collider

currently_dragging:Gameobject = None
dragging_offset:Vector2 = Vector2(0, 0)
start_dragging = Vector2(0, 0)

def draggable(gameobject:Gameobject, collider:Collider=None) -> Gameobject:
    """decorator to make `Gameojbects` dragable."""
    if collider != None:
        gameobject.collider = collider
    

    # save original method
    og_event = gameobject.event
    # define new method
    def event(self:Gameobject, event:pygame.event.Event):
        global currently_dragging
        global dragging_offset
        global start_dragging

        if event.type == pygame.MOUSEBUTTONDOWN:
            if currently_dragging == None and self.collider.mouse_over(): # clicks `self`
                self.render_on_top()
                currently_dragging = self
                dragging_offset = self.get_global_position() - Vector2(pygame.mouse.get_pos())
                start_dragging = self.get_global_position()
                self.started_dragging()
        elif event.type == pygame.MOUSEBUTTONUP and currently_dragging is self: # lets go of `self`
                self.stopped_dragging(start_dragging, self.get_global_position())
                currently_dragging = None
                dragging_offset = Vector2(0, 0)
                start_dragging = Vector2(0, 0)
        
        # call original method
        og_event(self, event)
    # set old method to new method
    gameobject.event = event


    # save original method
    og_update = gameobject.update
    # define new method
    def update(self:Gameobject):
        if currently_dragging is self:
            self.set_position(Vector2(pygame.mouse.get_pos())+dragging_offset)
        
        # call original method
        og_update(self)
    # set old method to new method
    gameobject.update = update

    if not hasattr(gameobject, "started_dragging"):
        def started_dragging(self:Gameobject):
            pass
        gameobject.started_dragging = started_dragging

    if not hasattr(gameobject, "stopped_dragging"):
        def stopped_dragging(self:Gameobject, start:Vector2, end:Vector2):
            pass
        gameobject.stopped_dragging = stopped_dragging

    return gameobject
