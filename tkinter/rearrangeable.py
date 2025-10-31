import tkinter as tk
from tkinter.font import Font
from main import bind_all_children


class Rearrangeable(object):

    def __init__(self, parent:tk.Widget, starting_frames:int=0):
        self.parent = parent
        self.starting_frames = starting_frames
        self.frames:list[tk.Frame] = []

        self.canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)

        self.scrollbar = tk.Scrollbar(parent, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(self.scrollable_frame_id, width=event.width))
        self.scrollable_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        for i in range(self.starting_frames):
            self.add_frame(i)

        bind_all_children(parent, "<MouseWheel>", self.on_mouse_wheel)
        
    def add_frame(self, i:int=None) -> tk.Frame:
        """creates new frames and adds it to window."""
        frame = tk.Frame(self.scrollable_frame, background='gray25')
        frame.pack(side='top', fill='x', expand=True, pady=(0, 1))

        label = tk.Label(frame, text=F"{i}: Frames", font=('Consolas', 24), fg='white', background='gray25')
        label.pack(side='left')

        self.frames.append(frame)

        return frame

    def on_mouse_wheel(self, event:tk.Event):
        # print(event.delta)
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

