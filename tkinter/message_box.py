import tkinter as tk
from main import IntEntry, FloatEntry


class MessageBox(object):

    def __init__(self, root:tk.Widget, message:str, value_type=None, enter_text="Enter"):
        """
        `root`: the root screen the MessageBox appears in.
        `message`: the message at the top of message box.
        `value_type`: the value type of input.
        `enter_text`: the text of the enter button.
        """
        self.frame = tk.Frame(root, bg="gray85", borderwidth=4, relief="solid")
        self.frame.place(anchor='center', relx=0.5, rely=0.5)

        self.label = tk.Label(self.frame, text=message, font=("consolas", 18), bg="gray85")
        self.label.pack(side='top', fill='x')

        self.enter_button = tk.Button(self.frame, text=enter_text, font=("consolas", 16), bg="gray90")
        self.enter_button.pack(side="left", padx=(2, 10), pady=2)

        self.cancel_button = tk.Button(self.frame, text="Cancel", font=("consolas", 16), bg="gray90")
        self.cancel_button.pack(side="right", padx=(10, 2), pady=2)
        
        if value_type == str:
            self.input = tk.Entry(self.frame, font=("consolas", 18))
        elif value_type == int: 
            self.input = IntEntry(self.frame, font=("consolas", 18), width=8)
        elif value_type == float: 
            self.input = FloatEntry(self.frame, font=("consolas", 18), width=8)

        if hasattr(self, "input"):
            self.input.pack(side="bottom", pady=8)

