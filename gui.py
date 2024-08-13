import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from color_matcher import ColorMatcher


class ColorMatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Matcher")

        self.image = None
        self.matched_image = None
        self.image_path = None
        self.display_image_resized = None
        self.threshold = 10
        self.exact = True
        self.padding = 0

        self.setup_ui()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="grey")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        open_button = tk.Button(self.control_frame, text="Open Image", command=self.open_image)
        open_button.pack(pady=10)

        self.threshold_entry = tk.Entry(self.control_frame)
        self.threshold_entry.insert(0, "Threshold: 10")
        self.threshold_entry.pack(pady=5)

        self.exact_var = tk.BooleanVar(value=True)
        exact_check = tk.Checkbutton(self.control_frame, text="Exact Match", variable=self.exact_var)
        exact_check.pack(pady=5)

        self.padding_entry = tk.Entry(self.control_frame)
        self.padding_entry.insert(0, "Padding: 0")
        self.padding_entry.pack(pady=5)

        apply_button = tk.Button(self.control_frame, text="Apply Settings", command=self.apply_settings)
        apply_button.pack(pady=10)

        save_button = tk.Button(self.control_frame, text="Save Image", command=self.save_image)
        save_button.pack(pady=10)

    def open_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not self.image_path:
            return

        self.image = Image.open(self.image_path)
        self.matched_image = Image.open(self.image_path)
        self.display_resized_image()

    def apply_settings(self):
        try:
            threshold_text = self.threshold_entry.get().replace("Threshold: ", "")
            self.threshold = float(threshold_text)

            padding_text = self.padding_entry.get().replace("Padding: ", "")
            self.padding = int(padding_text)

            self.exact = self.exact_var.get()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for threshold and padding.")

    def display_resized_image(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        scale = min(canvas_width / self.matched_image.width, canvas_height / self.matched_image.height)

        resized_width = int(self.matched_image.width * scale)
        resized_height = int(self.matched_image.height * scale)
        self.display_image_resized = self.matched_image.resize((resized_width, resized_height))

        self.tk_image = ImageTk.PhotoImage(self.display_image_resized)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_canvas_click(self, event):
        if self.image is None:
            return

        scale_x = self.image.width / self.display_image_resized.width
        scale_y = self.image.height / self.display_image_resized.height
        x = int(event.x * scale_x)
        y = int(event.y * scale_y)

        matcher = ColorMatcher(self.image)

        self.matched_image = matcher.match((x, y), self.threshold, self.exact, self.padding)
        self.display_resized_image()

    def save_image(self):
        if self.image is None:
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg")])
        if save_path:
            self.image.save(save_path)


def run_gui():
    root = tk.Tk()
    ColorMatcherApp(root)
    root.mainloop()
