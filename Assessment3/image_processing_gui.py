import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

# Handles loading an image and converting it to OpenCV format
class ImageLoader:
    def __init__(self, canvas):
        self.canvas = canvas
        self.original_image = None
        self.tk_image = None
        self.cv_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.original_image = Image.open(file_path).resize((400, 300))
            self.tk_image = ImageTk.PhotoImage(self.original_image)
            pil_image = self.original_image.convert("RGB")
            self.cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            return True
        return False

# Allows cropping an image by drawing a rectangle on the canvas
class ImageCropper:
    def __init__(self, canvas, cropped_canvas):
        self.canvas = canvas
        self.cropped_canvas = cropped_canvas
        self.rect = None
        self.start_x = self.start_y = 0
        self.end_x = self.end_y = 0
        self.cropped_image = None

    def on_mouse_down(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.start_x, self.start_y,
            outline='red'
        )

    def on_mouse_drag(self, event):
        self.end_x, self.end_y = event.x, event.y
        self.canvas.coords(
            self.rect,
            self.start_x, self.start_y,
            self.end_x, self.end_y
        )

    def on_mouse_up(self, event, cv_image):
        self.end_x, self.end_y = event.x, event.y
        self.canvas.coords(
            self.rect,
            self.start_x, self.start_y,
            self.end_x, self.end_y
        )
        return self.crop_image(cv_image)

    def crop_image(self, cv_image):
        if cv_image is not None:
            x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
            x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
            cropped_cv = cv_image[y1:y2, x1:x2]
            if cropped_cv.size == 0:
                return None
            cropped_rgb = cv2.cvtColor(cropped_cv, cv2.COLOR_BGR2RGB)
            self.cropped_image = Image.fromarray(cropped_rgb)
            return self.cropped_image
        return None

# Handles resizing the cropped image and displaying it
class ImageResizer:
    def __init__(self, cropped_canvas):
        self.cropped_canvas = cropped_canvas
        self.cropped_tk_image = None

    def update_display(self, image, scale_percent):
        if image:
            width = int(image.width * scale_percent / 100)
            height = int(image.height * scale_percent / 100)
            width = max(1, width)
            height = max(1, height)
            resized = image.resize((width, height), Image.Resampling.LANCZOS)
            self.cropped_tk_image = ImageTk.PhotoImage(resized)
            self.cropped_canvas.delete("all")
            self.cropped_canvas.create_image(0, 0, anchor=tk.NW, image=self.cropped_tk_image)
            return resized
        return None

# Saves the cropped image to disk
class ImageSaver:
    def save_image(self, image):
        if image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )
            if file_path:
                image.save(file_path)
                return True
        return False

# Main application class for the GUI
class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🖼️ Image Processing GUI")

        # Managers for each functionality
        self.loader = ImageLoader(None)
        self.cropper = None
        self.resizer = None
        self.saver = ImageSaver()

        # State management
        self.undo_stack = []
        self.redo_stack = []
        self.current_cropped = None
        self.displayed_image = None

        # === UI Layout ===

        # Main top frame
        self.top_frame = ttk.Frame(master, padding=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Left panel for original image
        self.left_panel = ttk.LabelFrame(self.top_frame, text="Original Image", padding=5)
        self.left_panel.grid(row=0, column=0, sticky="nsew")

        # Right panel for cropped image
        self.right_panel = ttk.LabelFrame(self.top_frame, text="Cropped Image", padding=5)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        # Canvas for original image
        self.canvas = tk.Canvas(self.left_panel, width=400, height=300, bg="white", cursor="cross")
        self.canvas.pack()

        # Canvas for cropped image
        self.cropped_canvas = tk.Canvas(self.right_panel, width=400, height=300, bg="white")
        self.cropped_canvas.pack()

        # Inject canvas references into logic classes
        self.loader.canvas = self.canvas
        self.cropper = ImageCropper(self.canvas, self.cropped_canvas)
        self.resizer = ImageResizer(self.cropped_canvas)

        # Bottom frame for controls
        self.bottom_frame = ttk.Frame(master, padding=10)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Action buttons
        ttk.Button(self.bottom_frame, text="Load Image", command=self.load_image).grid(row=0, column=0, padx=5)
        ttk.Button(self.bottom_frame, text="Save Cropped Image", command=self.save_image).grid(row=0, column=1, padx=5)
        ttk.Button(self.bottom_frame, text="Undo", command=self.undo).grid(row=0, column=2, padx=5)
        ttk.Button(self.bottom_frame, text="Redo", command=self.redo).grid(row=0, column=3, padx=5)
        ttk.Button(self.bottom_frame, text="Reset", command=self.reset_canvases).grid(row=0, column=4, padx=5)

        # Resize slider
        self.slider_label = ttk.Label(self.bottom_frame, text="Resize (%)")
        self.slider_label.grid(row=0, column=5, padx=5, sticky='w')

        self.resize_slider = ttk.Scale(self.bottom_frame, from_=10, to=200, orient=tk.HORIZONTAL,
                                       command=self.on_slider_change)
        self.resize_slider.set(100)
        self.resize_slider.grid(row=0, column=6, padx=5, sticky='ew')
        self.bottom_frame.columnconfigure(6, weight=1)

        # Status bar for feedback
        self.status_label = ttk.Label(master, text="Welcome! Please load an image.", anchor="w")
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)

        # Bind mouse events for cropping
        self.canvas.bind("<ButtonPress-1>", self.cropper.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.cropper.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    # Load image and display it
    def load_image(self):
        if self.loader.load_image():
            self.reset_canvases()
            self.canvas.delete("all")
            self.displayed_image = self.loader.tk_image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.displayed_image)
            self.status_label.config(text="Image loaded successfully!")

    # Handle mouse up event to crop
    def on_mouse_up(self, event):
        cropped = self.cropper.on_mouse_up(event, self.loader.cv_image)
        if cropped:
            if self.current_cropped:
                self.undo_stack.append(self.current_cropped.copy())
            self.current_cropped = cropped
            self.resize_slider.set(100)
            self.resizer.update_display(self.current_cropped, 100)
            self.redo_stack.clear()
            self.status_label.config(text="Cropped image updated.")

    # Resize the cropped image
    def on_slider_change(self, value):
        if self.current_cropped:
            self.resizer.update_display(self.current_cropped, int(float(value)))

    # Save the resized image
    def save_image(self):
        if self.current_cropped:
            scale = int(self.resize_slider.get())
            width = int(self.current_cropped.width * scale / 100)
            height = int(self.current_cropped.height * scale / 100)
            resized = self.current_cropped.resize((width, height), Image.Resampling.LANCZOS)
            if self.saver.save_image(resized):
                self.status_label.config(text="Image saved successfully.")
            else:
                self.status_label.config(text="Save cancelled.")

    # Undo last crop
    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.current_cropped.copy())
            self.current_cropped = self.undo_stack.pop()
            self.resizer.update_display(self.current_cropped, self.resize_slider.get())
            self.status_label.config(text="Undo successful.")

    # Redo the undone crop
    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.current_cropped.copy())
            self.current_cropped = self.redo_stack.pop()
            self.resizer.update_display(self.current_cropped, self.resize_slider.get())
            self.status_label.config(text="Redo successful.")

    # Reset everything
    def reset_canvases(self):
        self.canvas.delete("all")
        self.cropped_canvas.delete("all")
        self.resize_slider.set(100)
        self.current_cropped = None
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.displayed_image = None
        self.status_label.config(text="Reset done.")

# Entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()