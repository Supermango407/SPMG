import tkinter as tk
from tkinter.font import Font
import screeninfo

# adds the current path to ovoid import errors
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("//".join(sys.path[0].replace("\\", "/").split("/")[:-1]))

from rearrangeable import Rearrangeable
from message_box import MessageBox
from spmg_tkinter_main import IntEntry, clone_widget, widget_image, smooth_move_widget


root = tk.Tk()

# set screen size
if len(screeninfo.get_monitors()) == 2: # two monitors
    root.geometry(f"800x600+{root.winfo_screenwidth()+250}+40")
else:
    root.geometry(f"800x600+250+40")

root.title("SPMG Test")
root.minsize(400, 400)
# root.state('zoomed')

header = tk.Frame(root, bg="steel blue", height=50)
header.pack(side="top", fill="x")

header_label = tk.Label(header, text='Header', bg='steel blue', font=("Consolas", 24), justify="center")
header_label.place(anchor="center", relx=0.5, rely=0.5)

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

font=Font(family="Consolas", size=24, weight="normal")

# frames:list[tk.Frame] = []
# for i in range(20):
#     frame = tk.Frame(main_frame)
#     frame.pack(side="top", fill="x", expand=True)
#     label = tk.Label(frame, text=F"{i}: Frame", font=font)
#     label.pack(side="left")
#     frames.append(frame)

r = Rearrangeable(main_frame, frame_height=50, starting_frames=20)
# Rearrangeable.set_root(root)


def clone_header(e):
    new_header = clone_widget(header)
    new_header.pack(side="top", fill='x', after=header)


def save_header_image(e):
    image = widget_image(header)
    image.save("widget_screenshot.png")


def move_frame(e):
    r.frames[0].lift()
    smooth_move_widget(r.frames[0], 1000, y=100)
    # r.frames[0].place(y=10)


def open_message(e):
    MessageBox(root, "are you sure you want to delete that.", print_type, None)


def print_type(value):
    print(f"{type(value)}: {value}")


root.bind_all("<space>", open_message)

root.mainloop()
