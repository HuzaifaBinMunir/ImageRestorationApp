import tkinter as tk
from tkinter import filedialog, messagebox, LabelFrame, Label
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageRestorationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Restoration App")
        self.root.geometry("800x400")
        
        # Initialize variables to store images
        self.degraded_image = None
        self.restored_image = None

        # Create a frame for controls on the left side
        control_frame = LabelFrame(root, text="Controls", padx=10, pady=10)
        control_frame.place(x=20, y=50, width=200, height=200)

        # Load Degraded Image Button
        load_button = tk.Button(control_frame, text="Load Degraded Image", command=self.load_image, width=18)
        load_button.grid(row=0, column=0, padx=5, pady=5)

        # Apply Restoration Button
        restore_button = tk.Button(control_frame, text="Apply Restoration", command=self.restore_image, width=18)
        restore_button.grid(row=1, column=0, padx=5, pady=5)

        # Save Result Button
        save_button = tk.Button(control_frame, text="Save Result", command=self.save_result, width=18)
        save_button.grid(row=2, column=0, padx=5, pady=5)

        # Label for degraded image
        degraded_label = Label(root, text="Degraded Image", font=("Arial", 12, "bold"))
        degraded_label.place(x=250, y=30)

        # Label for restored image
        restored_label = Label(root, text="Restored Image", font=("Arial", 12, "bold"))
        restored_label.place(x=500, y=30)

        # Canvas for displaying images
        self.canvas1 = tk.Canvas(root, width=250, height=250, bg="gray")
        self.canvas1.place(x=250, y=70)

        self.canvas2 = tk.Canvas(root, width=250, height=250, bg="gray")
        self.canvas2.place(x=500, y=70)

    def load_image(self):
        # Load degraded image
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.bmp")])
        if not file_path:
            return  # User canceled

        self.degraded_image = cv2.imread(file_path)
        self.display_image(self.degraded_image, self.canvas1, title="Degraded Image")

    def display_image(self, image, canvas, title=""):
        # Convert OpenCV image to PIL format for Tkinter compatibility
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        pil_image = pil_image.resize((250, 250))  # Resize for better viewing
        img_tk = ImageTk.PhotoImage(pil_image)

        # Display image in canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk  # Keep a reference to avoid garbage collection
        canvas.create_text(125, 230, text=title, fill="white")

    def restore_image(self):
        if self.degraded_image is None:
            messagebox.showerror("Error", "Please load a degraded image first.")
            return

        # Apply restoration algorithm (simple example with median filtering)
        grayscale_image = cv2.cvtColor(self.degraded_image, cv2.COLOR_BGR2GRAY)
        restored_image = cv2.medianBlur(grayscale_image, 3)

        self.restored_image = restored_image
        self.display_image(cv2.cvtColor(restored_image, cv2.COLOR_GRAY2BGR), self.canvas2, title="Restored Image")

    def save_result(self):
        if self.restored_image is None:
            messagebox.showerror("Error", "No restored image to save. Please apply restoration first.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")])
        if not file_path:
            return  # User canceled

        cv2.imwrite(file_path, self.restored_image)
        messagebox.showinfo("Success", "Restored image saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRestorationGUI(root)
    root.mainloop()
