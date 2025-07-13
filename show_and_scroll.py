import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk

# Read image and the coordinates of the boxes
idx = 9
image_path = f"./character{idx}/character{idx}_1.jpg"
excel_path = f"./character{idx}/character{idx}_boxes_location.xlsx"
character_boxes = pd.read_excel(excel_path, index_col=0).values.tolist()

# Creating the main GUI class
class CharacterViewer(tk.Tk):
    def __init__(self, image_path, boxes):
        super().__init__()
        self.title("Character Navigator")
        # Scale the image to fit the resolution of your display. Adjust the scale_factor based on your DPI settings
        self.scale_factor = 0.5
        orig_image = Image.open(image_path)
        scaled_width = int(orig_image.width * self.scale_factor)
        scaled_height = int(orig_image.height * self.scale_factor)
        self.image = orig_image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.geometry(f"{self.image.width}x{self.image.height}")

        self.canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
        self.canvas.pack()

        self.canvas_img = self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)
   
        self.boxes = [(int(x * self.scale_factor), int(y * self.scale_factor),
                       int(w * self.scale_factor), int(h * self.scale_factor)) for (x, y, w, h) in boxes]
 
        self.current_index = 0
        self.highlight = None

        self.bind("<Up>", self.prev_char)
        self.bind("<Down>", self.next_char)
        self.draw_box()

    def draw_box(self):
        print(f"{self.current_index} - {self.boxes[self.current_index]}")
        if self.highlight:
            self.canvas.delete(self.highlight)
        x, y, w, h = self.boxes[self.current_index]
        self.highlight = self.canvas.create_rectangle(
            x-w/4, y-h/4, x + 5*w/4, y + 5*h/4,
            outline='red', width=2
        )

    def prev_char(self, event=None):
        if self.current_index > 0:
            self.current_index -= 1
            self.draw_box()

    def next_char(self, event=None):
        if self.current_index < len(self.boxes) - 1:
            self.current_index += 1
            self.draw_box()

    def normalize_sort(self):
        pass

if __name__ == "__main__":
    app = CharacterViewer(image_path, character_boxes)
    app.mainloop()
