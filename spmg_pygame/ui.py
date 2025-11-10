import pygame
from pygame import Vector2

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("//".join(sys.path[0].replace("\\", "/").split("/")[:-1]))

# import spmg_pygame.gameobject
from spmg_pygame.gameobject import Gameobject


class Text(Gameobject):
    """for displaying text to window"""

    def __init__(self,
    value:str,
    bg_color:tuple[int, int, int]=(0, 0, 0),
    **kwargs
    ):
        self.text_value = value
        """the str inside `Text`."""
        self.color = bg_color
        """the color of `Text`."""
        self.font = pygame.font.SysFont('Consolas', 30)
        """the font of `Text`."""

        self.text =  self.font.render(self.text_value, True, self.color)
        """the text renderer,"""

        super().__init__(**kwargs)

        self.set_size()

    def set_text(self, value:str):
        """sets value of text"""
        self.text_value = value
        self.text = self.font.render(self.text_value, True, self.color)
        
        # set position to realign after text width changes.
        self.set_size()

    def set_size(self, new_size=None) -> None:
        """set the size of `Gameobject`."""
        if new_size == None:
            new_size = Vector2(self.text.get_size())
        super().set_size(new_size)

    def set_color(self, color:tuple[int, int, int]):
         """sets color of text."""
         self.color = color
         self.text = self.font.render(self.text_value, True, self.color)

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
    """a clickable Gameobject with Text in it."""

    def __init__(
    self, onclick:callable,
    text_value:str="",
    text_color:tuple[int, int, int]=(0, 0, 0),
    bg_color:tuple[int, int, int]=(223, 223, 223),
    hover_bg_color:tuple[int, int, int]=(127, 127, 127),
    **kwargs
    ):
        self.onclick = onclick
        """called when button is clicked."""
        self.text_value = text_value
        """the str inside button."""
        self.text_color = text_color
        """the color of the text inside button."""
        self.bg_color = bg_color
        """the background color of button."""
        self.hover_bg_color = hover_bg_color
        """the background of button when button when mouse is over."""
        
        self.text:Text = Text(value=self.text_value, anchor=Vector2(0.5, 0.5), bg_color=self.text_color)
        """the text Gameobject."""

        super().__init__(listen=True, **kwargs)

        # move text to render infront of button.
        self.text.render_on_top(self.text)
        # have to set parrent after super().init is called
        self.text.set_parrent(self)
        # sets the size after text added
        self.set_size()
        
    def set_size(self, new_size=None, set_children=True):
        if self.text != None:
            self.text.set_size(new_size)
            new_size = self.text.size
        return super().set_size(new_size, set_children)
        
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

        super().draw()
      
    def hovering(self) -> bool:
        """whether the mouse is over button or not."""
        # the postion of the mouse relitive to the button
        relative_mouse = Gameobject.mouse_pos-self.window_position

        return relative_mouse.x >= 0 and relative_mouse.x <= self.size.x and relative_mouse.y >= 0 and relative_mouse.y <= self.size.y

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and self.hovering():
            self.onclick()

