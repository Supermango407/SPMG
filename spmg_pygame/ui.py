import pygame
from pygame import Vector2

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from gameobject import Gameobject


class Text(Gameobject):
    """for displaying text to window"""

    def __init__(self, value:str, position:Vector2=Vector2(0, 0), anchor:Vector2=Vector2(0, 0), relative_position:Vector2=Vector2(0, 0), parrent:Gameobject=None, color:tuple[int, int, int]=(0, 0, 0)):
        """
        `value`: the text that will be on the screen
        `position`: the location of the sprite onscreen.
        `anchor`: where the board is placed on the screen eg:
            top_left, top, top_right, left, center, right, bottom_left, bottom, bottom_right.
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
        `color`: the color of the text
        """
        self.value = value
        self.color = color
        self.font = pygame.font.SysFont('Consolas', 30)

        self.text =  self.font.render(self.value, True, color)
        
        super().__init__(position=position, anchor=anchor, relative_position=relative_position, parrent=parrent, size=Vector2(self.text.get_size()))

    def set_text(self, value:str):
        """sets value of text"""
        self.value = value
        self.text = self.font.render(self.value, True, self.color)
        
        # set position to realign after text width changes.
        self.set_position()
        self.set_size()

    def set_size(self, new_size=None):
        if new_size == None:
            new_size = self.text.get_size()
        super().set_size(new_size)

    def set_color(self, color:tuple[int, int, int]):
         """sets color of text"""
         self.color = color
         self.text = self.font.render(self.value, True, self.color)

    def draw(self):
        """write text on screen."""
        rect = (
            self.window_position.x,
            self.window_position.y,
            self.size.x,
            self.size.y,
        )
        Gameobject.window.blit(self.text, rect)

        super().draw()


class Button(Gameobject):
    
    """class for button Widget."""


    def __init__(self, onclick:callable, text_value:str="", position:Vector2=Vector2(0, 0), anchor:Vector2=Vector2(0, 0), relative_position:Vector2=Vector2(0, 0), text_color:tuple[int, int, int]=(0, 0, 0), bg_color:tuple[int, int, int]=(223, 223, 223), hover_bg_color:tuple[int, int, int]=(127, 127, 127), parrent:Gameobject=None, **kwargs):
        """
        `onclick`: what to do when the button is clicked.
        `text_value`: the text of the button.
        `text_color`: the color of the text.
        `bg_color`: the color of the background, when mouse isn't over button.
        `hover_bg_color: the color of the background, when mouse is over button.
        `position`: the location of the sprite onscreen.
        `anchor`: where the board is placed on the screen eg:
            top_left, top, top_right, left, center, right, bottom_left, bottom, bottom_right.
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
        """
        self.onclick = onclick
        self.text_value = text_value
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color
        
        super().__init__(position=position, anchor=anchor, relative_position=relative_position, parrent=parrent, listen=True)
        
        self.text:Text = Text(value=self.text_value, anchor=Vector2(0.5, 0.5), parrent=self, color=text_color)
        self.set_position()
        self.set_size()
        
    def set_size(self, new_size = None):
        if new_size == None and self.text != None:
            new_size = self.text.size
        return super().set_size(new_size)
        
    def draw(self):
        # draw background
        pygame.draw.rect(
            self.window,
            self.hover_bg_color if self.hovering() else self.bg_color,
            (
                self.window_position.x,
                self.window_position.y,
                self.size.x,
                self.size.y
            )
        )

        # draw text
        # self.text.draw()
        super().draw()
      
    def hovering(self) -> bool:
        """whethere the mouse is over button or not."""
        # the postion of the mouse relitive to the button
        relative_mouse = Gameobject.mouse_pos-self.window_position

        return relative_mouse.x >= 0 and relative_mouse.x <= self.size.x and relative_mouse.y >= 0 and relative_mouse.y <= self.size.y

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and self.hovering():
            self.onclick()

