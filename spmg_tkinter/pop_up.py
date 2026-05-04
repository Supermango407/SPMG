import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
new_path = "//".join(sys.path[0].replace("\\", "/").split("/")[:-1])
if not new_path in sys.path:
    sys.path.append(new_path)


class PopUp(object):
    """the menu the pops up when mouse right clicks."""

    def __init__(self, root:tk.Tk, button_font:Font=None):
        self.root = root
        self.button_font = button_font
        self.frame = tk.Frame(self.root, background='gray12')
        
        self.root.bind("<Button-1>", lambda e: self.hide())
    
    def clear_frame(self):
        """deletes everything in `self.frame`."""
        for child in self.frame.winfo_children():
            child.pack_forget()

    def show(self, x, y):
        """shows the menu."""
        self.frame.place(anchor='nw', x=x-self.root.winfo_x()-9, y=y-self.root.winfo_y()-30)

    def hide(self):
        """hides the menu."""
        self.frame.place_forget()

    def add_button(self, label_text, on_clicked:callable):
        """adds button to `self.frame`."""
        button = tk.Button(
            self.frame,
            text=label_text,
            font=self.button_font,
            bg='gray10',
            fg='white',
            activebackground='gray8',
            activeforeground='white',
        )
        button.pack(pady=2, padx=2, fill='x')
        
        button.bind("<Enter>", lambda e: button.config(bg='gray14'))
        button.bind("<Leave>", lambda e: button.config(bg='gray10'))
        button.bind("<Button-1>", on_clicked)

    def open_menu(self, buttons:list[tuple[str, callable]], event:tk.Event):
        """something is right clicked.
        `buttons`: a list of tuples where the first element is the text on the button and 
        the second element is the function that runs when the button is clicked."""
        self.clear_frame()

        for label_text, on_clicked in buttons:
            self.add_button(label_text, on_clicked)

        self.show(event.x_root, event.y_root)