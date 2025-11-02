import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
from main import bind_all_children, widget_image


class Rearrangeable(object):

    frame_dragging:tk.Frame = None
    widget_y_offset:int = 0

    def __init__(self, parent:tk.Widget, frame_height:int=50, frame_padding:int=1, starting_frames:int=0):
        self.parent = parent
        self.starting_frames = starting_frames
        self.frame_height = frame_height
        self.frame_padding = frame_padding
        self.frames:list[tk.Frame] = []

        self.canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)

        self.scrollbar = tk.Scrollbar(self.parent, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(self.scrollable_frame_id, width=event.width))
        self.scrollable_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        bind_all_children(parent, "<ButtonRelease-1>", self.mouse_released)
        bind_all_children(parent, "<B1-Motion>", self.mouse_motion)
        bind_all_children(parent, "<MouseWheel>", self.on_mouse_wheel)

        for i in range(self.starting_frames):
            self.add_frame(i)

    def add_frame(self, i:int=None) -> tk.Frame:
        """creates new frames and adds it to window."""
        frame = tk.Frame(self.scrollable_frame, background='gray25')
        height = (len(self.frames)+1)*(self.frame_height+self.frame_padding)+self.frame_padding
        self.scrollable_frame.config(height=height)
        y_pos = height-(self.frame_height+self.frame_padding)
        frame.place(x=0, y=y_pos, height=self.frame_height, relwidth=1)

        label = tk.Label(frame, text=F"Frame {i}", font=('Consolas', 24), fg='white', background='gray25')
        label.pack(side='left')

        bind_all_children(frame, "<Button-1>", lambda e: (self.frame_clicked(e, frame)))
        
        bind_all_children(frame, "<ButtonRelease-1>", self.mouse_released)
        bind_all_children(frame, "<B1-Motion>", self.mouse_motion)
        bind_all_children(frame, "<MouseWheel>", self.on_mouse_wheel)

        self.frames.append(frame)

        return frame

    def frame_clicked(self, event:tk.Event, frame:tk.Frame):
        if Rearrangeable.frame_dragging == None:
            Rearrangeable.frame_dragging = frame
            Rearrangeable.widget_y_offset = -event.y
            frame.lift()
    
    def mouse_released(self, event:tk.Event):
        Rearrangeable.frame_dragging = None
        Rearrangeable.widget_y_offset = 0

    def mouse_motion(self, event:tk.Event):
        if Rearrangeable.frame_dragging == event.widget:
            y_pos:int = event.y+Rearrangeable.frame_dragging.winfo_y()+Rearrangeable.widget_y_offset
            Rearrangeable.frame_dragging.place(x=0, y=y_pos)

    def on_mouse_wheel(self, event:tk.Event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

