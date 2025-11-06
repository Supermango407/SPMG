import tkinter as tk

class DraggableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag_motion)

        # Store initial drag position
        self._drag_start_x = 0
        self._drag_start_y = 0

    def on_drag_start(self, event):
        # Record the initial click position relative to the frame
        print(event.x) 
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag_motion(self, event):
        # Calculate new position based on mouse movement and initial offset
        print(event.x)
        x = self.winfo_x() + (event.x - self._drag_start_x)
        y = self.winfo_y() + (event.y - self._drag_start_y)

        # Update the frame's position
        self.place(x=x, y=y)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")

    # Create a draggable frame
    draggable_frame = DraggableFrame(root, bg="lightblue", width= 150, height=100)
    draggable_frame.place(x=50, y=50)

    # Add a label inside the draggable frame
    label = tk.Label(draggable_frame, text="Drag me!", bg="lightgray")
    label.pack(expand=True, fill="both")

    root.mainloop()