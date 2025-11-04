import tkinter as tk
import sys
from PIL import ImageGrab, Image
sys.path.append('../SPMG')
from spmg_math import lerp


class IntEntry(tk.Entry):
    @staticmethod
    def validate_numeric(input:str):
        return input.isdigit() or input == ""
    
    def __init__(self, master:tk.Widget, **kwargs):
        super().__init__(master, **kwargs)
        self.config(validate="key", validatecommand=(self.master.register(IntEntry.validate_numeric), '%P'))


class FloatEntry(tk.Entry):
    @staticmethod
    def validate_numeric(input:str):
        split_decimal = input.split('.')
        return input.isdigit() or input == "" or (len(split_decimal) == 2 and (split_decimal[0].isdecimal() or split_decimal[0] == "") and (split_decimal[1].isdecimal() or split_decimal[1] == ""))
    
    def __init__(self, master:tk.Widget, **kwargs):
        super().__init__(master, **kwargs)
        self.config(validate="key", validatecommand=(self.master.register(FloatEntry.validate_numeric), '%P'))


def bind_all_children(widget:tk.Widget ,sequence:str, func:tk.Event):
    """recursively binds `tkinter.widget` and all of its children."""
    widget.bind(sequence, func)

    for child in widget.winfo_children():
        bind_all_children(child, sequence, func)


def smooth_move_widget(widget:tk.Widget, durration:float, frame_rate:int=30, x:int=None, y:int=None, relx:float=None, rely:float=None):
    if durration > 0:

        delta_time = 1000/frame_rate
        step_fraction = delta_time/durration

        place_data = widget.place_info()
        if x == None:
            current_x = None
        else:
            start_x = int(place_data.get('x'))
            current_x = lerp(start_x, x, step_fraction)
        if y == None:
            current_y = None
        else:
            start_y = int(place_data.get('y'))
            current_y = lerp(start_y, y, step_fraction)
        if relx == None:
            current_relx = None
        else:
            start_relx = int(place_data.get('relx'))
            current_relx = lerp(start_relx, relx, step_fraction)
        if rely == None:
            current_rely = None
        else:
            start_rely = int(place_data.get('rely'))
            current_rely = lerp(start_rely, rely, step_fraction)

        print(y, rely)
        widget.place(x=current_x, y=current_y, relx=current_relx, rely=current_rely)
        widget.after(int(delta_time), lambda: smooth_move_widget(widget, durration-delta_time, frame_rate, x, y, relx, rely))
    else:
        print(y)
        widget.place(x=x, y=y, relx=relx, rely=rely)


# from https://stackoverflow.com/questions/46505982/is-there-a-way-to-clone-a-tkinter-widget
def clone_widget(widget:tk.Widget, master:tk.Widget=None) -> tk.Widget:
    """
    Create a cloned version of a widget

    Parameters
    ----------
    widget : tkinter widget
        tkinter widget that shall be cloned.
    master : tkinter widget, optional
        Master widget onto which cloned widget shall be placed. If None, same master of input widget will be used. The
        default is None.

    Returns
    -------
    cloned : tkinter widget
        Clone of input widget onto master widget.

    """

    # Get main info
    parent = master if master else widget.master
    cls = widget.__class__

    # Clone the widget configuration
    cfg = {key: widget.cget(key) for key in widget.configure()}
    cloned = cls(parent, **cfg)

    # Clone the widget's children
    for child in widget.winfo_children():
        child_cloned = clone_widget(child, master=cloned)
        if child.grid_info():
            grid_info = {k: v for k, v in child.grid_info().items() if k not in {'in'}}
            child_cloned.grid(**grid_info)
        elif child.place_info():
            place_info = {k: v for k, v in child.place_info().items() if k not in {'in'}}
            child_cloned.place(**place_info)
        else:
            pack_info = {k: v for k, v in child.pack_info().items() if k not in {'in'}}
            child_cloned.pack(**pack_info)

    return cloned


def widget_image(widget:tk.Widget) -> Image:
    """returns Image of widget."""
    widget.update_idletasks() # Ensures the widget and its children are fully rendered

    x = widget.winfo_x() + widget.winfo_rootx()
    y = widget.winfo_y() + widget.winfo_rooty()
    width = widget.winfo_width()
    height = widget.winfo_height()
    
    image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    return image
