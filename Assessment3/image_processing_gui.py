import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processing GUI")

        self.original_image = None
        self.tk_image = None
        self.cropped_tk_image = None

        # Canvas for original image and cropping
        self.canvas = tk.Canvas(master, width=400, height=300, cursor="cross")
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # Canvas for cropped image
        self.cropped_canvas = tk.Canvas(master, width=400, height=300)
        self.cropped_canvas.pack(side=tk.RIGHT)

        self.load_button = tk.Button(master, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.BOTTOM)

        self.rect = None
        self.start_x = self.start_y = 0
        self.end_x = self.end_y = 0

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.original_image = Image.open(file_path).resize((400, 300))
            self.tk_image = ImageTk.PhotoImage(self.original_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.cropped_canvas.delete("all")  # Clear cropped canvas

    def on_mouse_down(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        self.end_x, self.end_y = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_mouse_up(self, event):
        self.end_x, self.end_y = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)
        self.crop_image()

    def crop_image(self):
        if self.original_image:
            x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
            x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
            # Crop using PIL
            cropped = self.original_image.crop((x1, y1, x2, y2))
            self.cropped_tk_image = ImageTk.PhotoImage(cropped)
            self.cropped_canvas.delete("all")
            self.cropped_canvas.create_image(0, 0, anchor=tk.NW, image=self.cropped_tk_image)
            self.cropped_canvas.image = self.cropped_tk_image  # Keep reference

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()