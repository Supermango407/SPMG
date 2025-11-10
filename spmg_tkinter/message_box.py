import tkinter as tk
from typing import Callable

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("//".join(sys.path[0].replace("\\", "/").split("/")[:-1]))

from spmg_tkinter.spmg_tkinter_main import IntEntry, FloatEntry


class MessageBox(object):
    """a window that opens up with a value input."""

    def __init__(self, root:tk.Widget, message:str, command:Callable, value_type:type=None, enter_text="Enter"):
        """
        `root`: the root screen the MessageBox appears in.
        `message`: the message at the top of message box.
        `value_type`: the value type of input.
        `enter_text`: the text of the enter button.
        """
        self.command = command
        self.value_type = value_type
        
        self.frame = tk.Frame(root, bg="gray85", borderwidth=4, relief="solid")
        self.frame.place(anchor='center', relx=0.5, rely=0.5)

        self.label = tk.Label(self.frame, text=message, font=("consolas", 18), bg="gray85")
        self.label.pack(side='top', fill='x')

        if self.value_type == str:
            self.input = tk.Entry(self.frame, font=("consolas", 18))
        elif self.value_type == int: 
            self.input = IntEntry(self.frame, font=("consolas", 18), width=8)
        elif self.value_type == float:  
            self.input = FloatEntry(self.frame, font=("consolas", 18), width=8)

        if hasattr(self, "input"):
            self.input.pack(side="bottom", pady=8)

        self.enter_button = tk.Button(self.frame, text=enter_text, command=lambda: self.submit(True), font=("consolas", 16), bg="gray90")
        self.enter_button.pack(side="left", padx=(2, 10), after=self.label, pady=2)

        self.cancel_button = tk.Button(self.frame, text="Cancel", command=lambda: self.submit(False), font=("consolas", 16), bg="gray90")
        self.cancel_button.pack(side="right", padx=(10, 2), after=self.label, pady=2)
        
    def submit(self, entered:bool):
        """
        called on button clicked.
        `entered`: True if entered clicked, False if cancel clicked.
        """
        if entered:
            if hasattr(self, "input"):
                value = self.input.get()
                if self.value_type == str:
                    self.command(value)
                if self.value_type == int or self.value_type == float:
                    self.command(None if value == '' else self.value_type(value))
            else:
                self.command(True)
        else:
            self.command(None)
