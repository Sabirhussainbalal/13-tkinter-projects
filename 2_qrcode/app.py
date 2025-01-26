import tkinter as tk
from PIL import Image, ImageTk
import qrcode

# Function to generate the QR code
def generate_qr_code(text):
    qr = qrcode.make(text)
    qr_img = qr.convert('RGB')
    return qr_img

# Function to update the QR code in the UI
def update_qr_code():
    # Get the text from the entry box
    user_input = entry.get()

    # Generate QR code from the input
    qr_img = generate_qr_code(user_input)

    # Resize the QR code to fit inside the frame
    qr_img = qr_img.resize((250, 250))  # Resize to a fixed size
    qr_img_tk = ImageTk.PhotoImage(qr_img)

    # Update the QR code image in the label
    qr_code_label.config(image=qr_img_tk)
    qr_code_label.image = qr_img_tk

# Function to handle the input changes with a delay of 1 second
def on_key_release(event):
    # Cancel any existing scheduled update
    if hasattr(on_key_release, "scheduled"):
        root.after_cancel(on_key_release.scheduled)

    updated_msg.config(text="Updated", fg="green")
    on_key_release.scheduled = root.after(1000, update_qr_code)

# Function to download the QR code
def download_qr_code():
    user_input = entry.get()
    qr_img = generate_qr_code(user_input)
    updated_msg.config(text="QR code downloaded successfully!", fg="green")
    qr_img.save(f"{user_input}_qrcode.png")

# Function for button hover effect
def on_enter(event):
    download_button.config(bg="#4CAF50", fg="white")

def on_leave(event):
    download_button.config(bg="#f0f0f0", fg="black")

# Initialize the main window
root = tk.Tk()
root.title("QR Code Generator")
root.resizable(False, False)
root.geometry("400x600")  # Set size of the window

# Set background image
try:
    bg_img = Image.open("bg.jpg")  # First path
except:
    bg_img = Image.open("2_qrcode/bg.jpg")  # Fallback path

bg_img = bg_img.resize((400, 600))  # Resize image to fit the window
bg_img_tk = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window
bg_label.image = bg_img_tk  # Keep reference to avoid garbage collection

# Set logo image
try:
    logo_img = Image.open("logo.png")  # First path
except:
    logo_img = Image.open("2_qrcode/logo.png")  # Fallback path

logo_img = logo_img.resize((100, 100))  # Resize logo image
logo_img_tk = ImageTk.PhotoImage(logo_img)

logo_label = tk.Label(root, image=logo_img_tk, bg="white")
logo_label.pack(pady=20)

# Create an input box at the center
entry = tk.Entry(root, font=("Arial", 12), justify="center")
entry.pack(pady=20)

# Create a frame for the QR code display with fixed size
qr_code_frame = tk.Frame(root, width=250, height=250, bg="white")
qr_code_frame.pack(pady=20)

# Create a label inside the frame to display the QR code
# Initially, we show a placeholder image (like a blank image)
placeholder_img = Image.new("RGB", (250, 250), (255, 255, 255))  # Create a blank white image
placeholder_img_tk = ImageTk.PhotoImage(placeholder_img)
qr_code_label = tk.Label(qr_code_frame, image=placeholder_img_tk)
qr_code_label.pack(fill="both", expand=True)

# Bind the key release event to update QR code after 1 second
entry.bind("<KeyRelease>", on_key_release)

# Button to download the QR code
download_button = tk.Button(root, text="Download", font=("Arial", 12), command=download_qr_code, bg="#f0f0f0", bd=0)
download_button.pack(pady=10)
updated_msg = tk.Label(root, text="Made by Sabir!", font=("Arial", 10), padx=10, pady=20)
updated_msg.pack(padx=20, pady=20)
# Add hover effects for the button
download_button.bind("<Enter>", on_enter)
download_button.bind("<Leave>", on_leave)

# Start the Tkinter event loop
root.mainloop()
