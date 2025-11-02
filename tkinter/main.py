import tkinter as tk
from PIL import ImageGrab, Image


def bind_all_children(widget:tk.Widget ,sequence:str, func:tk.Event):
    """recursively binds `tkinter.widget` and all of its children."""
    widget.bind(sequence, func)

    for child in widget.winfo_children():
        bind_all_children(child, sequence, func)


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
