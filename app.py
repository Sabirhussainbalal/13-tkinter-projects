import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import os
import subprocess
from PIL import Image, ImageTk  # Importing PIL for image resizing

# List of images and corresponding project paths
image_paths = [
    ("1_email_validation/demo.PNG", "1_email_validation/app.py", "Email Validation"),
    ("2_qrcode/demo.PNG", "2_qrcode/app.py", "QR Code Generator"),
    ("3_converter/demo.PNG", "3_converter/app.py", "Converter"),
    ("4_speed_calculator/demo.PNG", "4_speed_calculator/app.py", "Speed Calculator"),
    ("5_google_translater/demo.PNG", "5_google_translater/app.py", "Google Translator"),
    ("6_digital_clock/demo.PNG", "6_digital_clock/app.py", "Digital Clock"),
    ("7_handwriter/demo.PNG", "7_handwriter/app.py", "Handwriting Recognition"),
    ("8_internet_speed/demo.PNG", "8_internet_speed/app.py", "Internet Speed Test"),
    ("9_blocking_sites/demo.PNG", "9_blocking_sites/app.py", "Blocking Sites"),
    ("10_shutdown_app/demo.PNG", "10_shutdown_app/app.py", "Shutdown App"),
    ("11_set_notification/demo.PNG", "11_set_notification/app.py", "Set Notification"),
    ("12_weather_app/demo.PNG", "12_weather_app/app.py", "Weather App"),
    ("13_user_nu_details/demo.PNG", "13_user_nu_details/app.py", "User Details"),
]

# Set the fixed image size (width and height)
IMAGE_WIDTH = 350
IMAGE_HEIGHT = 200

def open_project(project_path):
    if os.path.exists(project_path):
        try:
            # Try running the Python script
            subprocess.Popen(["python", project_path])
            messagebox.showinfo("Opened", f"Project {project_path} opened successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open {project_path}. Error: {str(e)}")
    else:
        messagebox.showerror("Error", f"Project {project_path} not found.")

def create_image_button(root, frame, image_path, project_path, title):
    # Open the image using PIL and resize it to fixed dimensions
    image = Image.open(image_path)
    image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))  # Resize to the fixed size
    img = ImageTk.PhotoImage(image)

    # Create a button with image and title, and center it inside the frame
    button = tk.Button(frame, image=img, text=title, compound="top", command=lambda: open_project(project_path))
    button.img = img  # Keep a reference to the image to avoid garbage collection
    button.config(width=IMAGE_WIDTH, height=IMAGE_HEIGHT + 30)  # Add height for text
    button.pack(pady=20, padx=10, anchor="center")  # Center the button and give padding

def create_app():
    root = tk.Tk()
    root.geometry("450x450")
    root.resizable(False, False)

    # Set the app background color (gray)
    root.configure(bg="#D3D3D3")

    label_title = tk.Label(root, text="13 Python Projects", font=("Helvetica", 16))
    label_title.pack(pady=10)
    label_short = tk.Label(root, text="Made with ❤️by Sabir", font=("Helvetica", 10))
    label_short.pack(pady=5)

    # Create a frame inside the root window with white background
    frame = tk.Frame(root, width=400, height=400, bg="white")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Create a canvas and a scrollbar
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a scrollable window inside the canvas
    scrollable_frame = tk.Frame(canvas, bg="white")  # White background for scrollable area
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Update the scrollable region
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Add image buttons to the frame
    for img_path, proj_path, title in image_paths:
        create_image_button(root, scrollable_frame, img_path, proj_path, title)

    root.mainloop()

create_app()
