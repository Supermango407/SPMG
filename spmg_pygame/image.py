import pygame
from pygame import Vector2
from PIL import Image

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
new_path = "//".join(sys.path[0].replace("\\", "/").split("/")[:-1])
if not new_path in sys.path:
    sys.path.append(new_path)

from spmg_pygame.gameobject import Gameobject


class Image_Renderer(Gameobject):

    def __init__(self,
    image:pygame.Surface|Image.Image,
    scaler:float = 1,
    position:Vector2=Vector2(0, 0),
    anchor:Vector2=Vector2(0, 0),
    relative_position:Vector2=Vector2(0, 0),
    parent:Gameobject=None,
    hidden:bool=False,
    listen:bool=False
    ):
        super().__init__(
            position=position,
            anchor=anchor,
            relative_position=relative_position,
            size=Vector2(0, 0),
            parent=parent,
            hidden=hidden,
            listen=listen
        )
        self.scaler = scaler
    
        # create pygame image
        if image != None:
            self.image:pygame.Surface = None
            self.set_image(image)

    def set_image(self, new_image:pygame.Surface|Image.Image):
        """sets `self.pil_image` and renders."""
        if isinstance(new_image, Image.Image):
            new_image = PIL_to_pygame(new_image)
        self.image:pygame.Surface = new_image
        self.render()

    def set_scaler(self, new_scaler:float):
        """sets `self.scaler` and renders."""
        self.scaler = new_scaler
        self.render()

    def render(self):
        """sets the image and resets size."""
        # raise error if image is too large
        size = self.image.get_size()
        pixel_count = size[0]*size[1]*self.scaler*self.scaler
        if pixel_count > 10000000:
            raise MemoryError(f"can't render image with size {pixel_count}")
        
        # resize image
        self.image = pygame.transform.scale(self.image, (
            self.image.get_size()[0]*self.scaler,
            self.image.get_size()[1]*self.scaler,
        ))

        self.set_size(Vector2(*self.image.get_size()))

    def draw(self):
        self.window.blit(self.image, self.window_position)


def PIL_to_pygame(image:Image.Image) -> pygame.Surface:
    """converts a PIL image to a pygame Image."""
    return pygame.image.fromstring(
        image.tobytes(),
        image.size,
        image.mode
    )

def pygame_to_PIL(pygame_image:pygame.surface):
    """converts a pygame image to a PIL Image."""
    return Image.frombytes(
        "RGBA",
        pygame_image.get_size(),
        pygame.image.tobytes(pygame_image, "RGBA")
    )
