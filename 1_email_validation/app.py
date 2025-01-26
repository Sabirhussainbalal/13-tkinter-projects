from PIL import Image, ImageTk
import tkinter as tk

# Function to validate the email
def validate_email(email):
    if len(email) < 6:
        return "Email must be at least 6 characters long.", "red"
    if not email[0].isalpha():
        return "Email must start with a letter.", "red"
    if "@" not in email or email.count("@") != 1:
        return "Email must contain exactly one '@' symbol.", "red"
    
    after_at = email.split("@")[1]
    before_at = email.split("@")[0]

    if len(before_at) < 3:
        return "Username must be at least 3 characters long.", "red"

    if "." not in after_at or after_at.count(".") != 1 or after_at[0] == ".":
        return "Invalid domain part.", "red"
    if "." in before_at and before_at.count(".") == 1 and before_at[-1] == ".":
        return "Please enter a valid email address.", "red"
    
    # Check for valid characters
    for char in email:
        if char not in "@.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            return "Invalid characters in email address.", "red"
    
    return "Email is valid.", "green"

# Function to update the message after input
def on_submit():
    user_input = entry.get()
    message, color = validate_email(user_input)
    message_label.config(text=message, fg=color)

# Initialize the main window
root = tk.Tk()
root.title("Email Validator")
root.geometry("400x400")  # Set size of the window

try:
    bg_img = Image.open("bg.jpg")  # First path
except:
    bg_img = Image.open("1_email_validation/bg.jpg")  # Fallback path

# Resize the background image
bg_img = bg_img.resize((400, 400))  # Resize image to fit the window

# Convert to Tkinter-compatible image
bg_img_tk = ImageTk.PhotoImage(bg_img)

# Set the background image in the label
bg_label = tk.Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window

# Keep a reference to the image to avoid garbage collection
bg_label.image = bg_img_tk

# Set favorite logo (replace with the actual logo path)
logo_img = bg_img  # Replace with your logo image path
logo_img = logo_img.resize((100, 100))  # Resize logo image
logo_img_tk = ImageTk.PhotoImage(logo_img)

logo_label = tk.Label(root, image=logo_img_tk, bg="white")
logo_label.pack(pady=20)

# Create an input box at the center
entry = tk.Entry(root, font=("Arial", 12), justify="center")
entry.pack(pady=20)

# Button to submit input and update message
submit_button = tk.Button(root, text="Check", font=("Arial", 12), command=on_submit)
submit_button.pack(pady=10)

# Label to display the message after input
message_label = tk.Label(root, text="", font=("Arial", 10), fg="black", wraplength=300)
message_label.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
