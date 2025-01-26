import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to generate and save the image with the entered text
def generate_image():
    text = entry.get()
    if not text:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return
    
    # Correct URL for the TTF file of the font
    font_url = "https://fonts.gstatic.com/s/italianno/v17/dg4n_p3sv6gCJkwzT6RXiJwo.woff2"
    
    # Download the font
    response = requests.get(font_url)
    if response.status_code != 200:
        messagebox.showerror("Font Error", "Failed to download the font.")
        return
    
    font_bytes = BytesIO(response.content)
    
    # Load the font
    font = ImageFont.truetype(font_bytes, size=40)
    
    # Create an image
    img = Image.new('RGB', (1200, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw the text on the image
    draw.text((50, 250), text, font=font, fill='black')
    
    # Save and display the output
    img.save("writing.png")
    img.show()
    
    # Inform the user the image has been saved
    messagebox.showinfo("Success", "Image saved as 'writing.png'.")

# Initialize the Tkinter window
root = tk.Tk()
root.geometry("400x200")
root.resizable(False, False)
root.title("Text to Image")
try:
    bg_img = Image.open("bg.jpg")  # First path
except:
    bg_img = Image.open("7_handwriter/bg.jpg")  # Fallback path

bg_img = bg_img.resize((400, 200))  # Resize image to fit the window
bg_img_tk = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window
bg_label.image = bg_img_tk  # Keep reference to avoid garbage collection


# Create the text input field
entry_label = tk.Label(root, text="Enter the text you want to write:")
entry_label.pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Create the button to generate the image
generate_button = tk.Button(root, text="Generate Image", command=generate_image)
generate_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
