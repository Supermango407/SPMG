import tkinter as tk
from tkinter.font import Font
import screeninfo
from rearrangeable import Rearrangeable

root = tk.Tk()

# set screen size
if len(screeninfo.get_monitors()) == 2: # two monitors
    root.geometry(f"800x600+{root.winfo_screenwidth()+250}+40")
else:
    root.geometry(f"800x600+250+40")

root.title("SPMG Test")
root.minsize(400, 400)
# root.state('zoomed')

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

r = Rearrangeable(main_frame, 50)

root.mainloop()
