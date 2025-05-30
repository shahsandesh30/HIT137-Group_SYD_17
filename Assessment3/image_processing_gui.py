import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

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
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            
            # Convert to OpenCV format
            pil_image = self.original_image.convert("RGB")
            self.cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            return True
        return False

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

class ImageResizer:
    def __init__(self, cropped_canvas):
        self.cropped_canvas = cropped_canvas
        self.cropped_tk_image = None

    def update_display(self, image, scale_percent):
        #resize and display image
        if not image:
            return None
        
        # calculate new dimensions based on scale percentage
        new_width = max(1, int(image.width * scale_percent / 100))
        new_height = max(1, int(image.height * scale_percent / 100))

        # resize the image
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # convert to PhotoImage for display
        self.cropped_tk_image = ImageTk.PhotoImage(resized_image)

        # clear the cropped canvas and display the resized image
        self.cropped_canvas.delete("all")
        self.cropped_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.cropped_tk_image
        )

        return resized_image
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

class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processing GUI")

        # Create main canvas and cropped canvas
        self.canvas = tk.Canvas(master, width=400, height=300, cursor="cross")
        self.canvas.pack(side=tk.LEFT)

        self.cropped_canvas = tk.Canvas(master, width=400, height=300)
        self.cropped_canvas.pack(side=tk.RIGHT)

        # Initialize components/canvases
        self.loader = ImageLoader(self.canvas)
        self.cropper = ImageCropper(self.canvas, self.cropped_canvas)
        self.resizer = ImageResizer(self.cropped_canvas)
        self.saver = ImageSaver()

        # Create control frame for buttons and slider
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        #   Add buttons for loading,saving and resetting images
        self.load_button = tk.Button(
            self.control_frame, 
            text="Load Image", 
            command=self.load_image
        )
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = tk.Button(
            self.control_frame, 
            text="Save Cropped Image", 
            command=self.save_image
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(
            self.control_frame, text="Reset", command=self.reset_canvases
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Add slider for resizing cropped images
        self.resize_slider = tk.Scale(
            self.control_frame, 
            from_=10, to=200,
            orient=tk.HORIZONTAL, 
            label="Resize (%)",
            command=self.on_slider_change
        )
        self.resize_slider.set(100)
        self.resize_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Binding mouse events for cropping
        self.canvas.bind("<ButtonPress-1>", self.cropper.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.cropper.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # Initialize current cropped image
        self.current_cropped = None

    def load_image(self):
        if self.loader.load_image():
            self.cropped_canvas.delete("all")

    def on_mouse_up(self, event):
        self.current_cropped = self.cropper.on_mouse_up(event, self.loader.cv_image)
        if self.current_cropped:
            self.resize_slider.set(100)
            self.resizer.update_display(self.current_cropped, 100)

    def on_slider_change(self, value):
        if self.current_cropped:
            self.resizer.update_display(self.current_cropped, int(value))

    def save_image(self):
        if self.current_cropped:
            scale = int(self.resize_slider.get())
            width = int(self.current_cropped.width * scale / 100)
            height = int(self.current_cropped.height * scale / 100)
            resized = self.current_cropped.resize(
                (width, height), 
                Image.Resampling.LANCZOS
            )
            self.saver.save_image(resized)
    def reset_canvases(self):
        """Clear both canvases and reset the slider."""
        self.canvas.delete("all")
        self.cropped_canvas.delete("all")
        self.resize_slider.set(100)
        self.current_cropped = None
    
   
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()