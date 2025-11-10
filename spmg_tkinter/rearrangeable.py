import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("//".join(sys.path[0].replace("\\", "/").split("/")[:-1]))

from spmg_tkinter.spmg_tkinter_main import bind_all_children, smooth_move_widget


class Rearrangeable(object):

    frame_dragging:tk.Frame = None
    """the current frame dragging"""
    widget_y_offset:int = 0
    """the y pos of mouse relative to where the frame was clicked"""
    start_index:int = 0
    """the index the frame dragging started in"""
    last_index:int = 0
    """the last index the frame was dragged through"""

    def __init__(self, parent:tk.Widget, frame_height:int=50, frame_padding:int=1, frame_bg_color="gray25", starting_frames:int=0):
        """
        `parent`: the tkinter parrent of `scrollable_frame`
        `frame_height`: the height of the inner frames
        `frame_padding`: the padding in between frames
        `frame_bg_color`: the color of the draggable frames
        `starting_frames`: the number of frames the `scrollable_frame`
        """
        self.parent = parent
        """the tkinter parrent of `scrollable_frame`"""
        self.frame_height = frame_height
        """the height of the inner frames"""
        self.frame_padding = frame_padding
        """the padding in between frames"""
        self.frame_bg_color = frame_bg_color
        """the color of the draggable frames"""
        self.starting_frames = starting_frames
        """the number of frames the `scrollable_frame`"""

        self.frames:list[tk.Frame] = []
        """list of all frames in `scrollable_frame`"""

        self.canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        """the canvas the `scrollable_frame` is placed in"""
        self.canvas.pack(side='left', fill='both', expand=True)

        self.scrollbar = tk.Scrollbar(self.parent, orient='vertical', command=self.canvas.yview)
        """the scrollbar for the `scrollable_frame`"""
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas)
        """the main frame the children frames are placed in"""
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(self.scrollable_frame_id, width=event.width))
        self.scrollable_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        bind_all_children(parent, "<ButtonRelease-1>", self.mouse_released)
        bind_all_children(parent, "<B1-Motion>", self.mouse_motion)
        bind_all_children(parent, "<MouseWheel>", self.on_mouse_wheel)

        for i in range(self.starting_frames):
            self.add_frame()

    def index_to_pos(self, index:int) -> int:
        """returns y pos of frame and `index`."""
        return index*(self.frame_height+self.frame_padding)+self.frame_padding

    def pos_to_index(self, y_pos:int) -> float:
        """gets nearest index to `y_pos`."""
        return (y_pos-self.frame_padding)/(self.frame_height+self.frame_padding)

    def add_frame(self, **start_data) -> tk.Frame:
        """
        creates new frames and adds it to window.
        `start_data`: data you can put into add frame, that will be passed to `create_frame`
            if you want to create frame with initial data.
        """
        height = self.index_to_pos(len(self.frames)+1)
        """new height of `scrollable_frame`"""
        y_pos = self.index_to_pos(len(self.frames))
        """y_pos of new frame"""

        # create draggable frame
        frame = tk.Frame(self.scrollable_frame, background=self.frame_bg_color)
        self.scrollable_frame.config(height=height)
        frame.place(x=0, y=y_pos, height=self.frame_height, relwidth=1)

        # call create_frame to fill frame with watever the user wants.
        self.create_frame(frame, **start_data)

        # bind unique events, event that treat what frame it happens to uniquely.
        bind_all_children(frame, "<Button-1>", lambda e: (self.frame_clicked(e, frame)))
        
        # bind universal events, event that are not realated to what frame it happens to.
        bind_all_children(frame, "<ButtonRelease-1>", self.mouse_released)
        bind_all_children(frame, "<B1-Motion>", self.mouse_motion)
        bind_all_children(frame, "<MouseWheel>", self.on_mouse_wheel)

        self.frames.append(frame)

        return frame

    def create_frame(self, frame:tk.Frame, **start_data) -> None:
        """creates the contents of the frame."""
        label = tk.Label(frame, text=F"{len(self.frames)}: Frame {len(self.frames)+1}", font=('Consolas', 24), fg='white', background='gray25')
        label.pack(side='left')

    def frame_moved(self, start_inded:int, end_index:int) -> None:
        """called after frame is moved."""
        print(F"started:{start_inded}, ended:{end_index}")

    def sort_frames(self):
        """organizes `frames` posision based of there index in `self.frames`."""
        for i, frame in enumerate(self.frames):
            frame.place(y=self.index_to_pos(i))

    def frame_clicked(self, event:tk.Event, frame:tk.Frame):
        if Rearrangeable.frame_dragging == None:
            # set global vars
            Rearrangeable.frame_dragging = frame
            Rearrangeable.widget_y_offset = -event.y

            index = round(self.pos_to_index(frame.winfo_y()))
            Rearrangeable.start_index = index
            Rearrangeable.last_index = index

            # make frame dragging render on top of other frames.
            frame.lift()

    def mouse_released(self, event:tk.Event):
        if Rearrangeable.frame_dragging != None:
            # sort frames to avoid overlapping errors
            self.sort_frames()

            # call frame moved for user to use however.
            self.frame_moved(
                Rearrangeable.start_index,
                max(0, min(len(self.frames)-1, Rearrangeable.last_index))
            )

            # reset global vars.
            Rearrangeable.frame_dragging = None
            Rearrangeable.widget_y_offset = 0
            Rearrangeable.start_index = 0
            Rearrangeable.last_index = 0

    def mouse_motion(self, event:tk.Event):
        if Rearrangeable.frame_dragging == event.widget:
            y_pos:int = event.y+Rearrangeable.frame_dragging.winfo_y()+Rearrangeable.widget_y_offset
            """the current y_pos of frame dragging."""
            Rearrangeable.frame_dragging.place(x=0, y=y_pos)
            
            index = self.pos_to_index(y_pos)
            """the non rounded index of frame dragging."""

            # if your in a new index frames need to be moved
            if abs(Rearrangeable.last_index-index) > 1:
                rounded_index = round(index)
                """the index frame dragging is currently at"""
                self.frame_endered_index(Rearrangeable.last_index, rounded_index)
                # update last index.
                Rearrangeable.last_index = rounded_index

    def frame_endered_index(self, old_index:int, new_index:int):
        """called when frame dragging enters new index."""
        total_frames = len(self.frames)
        # if dragging outside the `scrollable_frame` boundries, return.
        if old_index < 0 or new_index < 0 or old_index >= total_frames or new_index >= total_frames:
            return
        
        # whether frame dragging is moved up
        if old_index < new_index :
            dir_moving = -1
            """the directing the frames between are moving"""
            frames_between = self.frames[old_index+1:new_index+1]
            """the frames the index the dragging frame was and where it is now"""
        else:
            dir_moving = 1
            """the directing the frames between are moving"""
            frames_between = self.frames[new_index:old_index]
            """the frames the index the dragging frame was and where it is now"""

        for frame in frames_between:
            current_index = self.pos_to_index(int(frame.place_info()['y']))
            y_pos = self.index_to_pos(current_index+dir_moving)
            
            # smooth_move_widget(frame, 100 , y=y_pos)
            frame.place(y=y_pos)

        # remove frame dragging from its old index
        frame_moving = self.frames.pop(old_index)
        # add frame dragging to its new index
        self.frames.insert(new_index, frame_moving)

    def on_mouse_wheel(self, event:tk.Event):
        """called when mouse is scrolled on any of the frames."""
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

