import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from googletrans import Translator, LANGUAGES
from tkinter import font
import threading

# Create the main window
root = tk.Tk()
root.title("Translator App")
root.geometry("600x500")
root.resizable(False, False)
try:
    bg_img = Image.open("bg.jpg")  # First path
except:
    bg_img = Image.open("5_google_translater/bg.jpg")  # Fallback path

bg_img = bg_img.resize((600, 500))  # Resize image to fit the window
bg_img_tk = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window
bg_label.image = bg_img_tk  # Keep reference to avoid garbage collection

# Initialize the translator
translator = Translator()

# List of available languages
list_of_languages = list(LANGUAGES.values())

def translate_text():
    while True:
        try:
            text = input1.get("1.0", "end-1c").strip()  # Get and strip any extra spaces
            if not text:  # Check if the input text is empty
                input2.delete("1.0", "end")
                error_label.config(text="Please enter text to translate.")
                return

            src_lang = combo_box.get()
            if src_lang == "":  # If no source language selected, auto-detect
                src_lang = "auto"

            
            dest_lang = combo_box2.get()
            translation = translator.translate(text, src=src_lang, dest=dest_lang)

            # Clear and update the translated text area
            input2.delete("1.0", "end")
            input2.insert("1.0", translation.text)
            error_label.config(text="")  # Clear error label if successful

            

        except Exception as e:
            error_label.config(text=f"Error: {str(e)}")  # Display any errors
def auto_translate():
    def worker():
        translate_text()
        root.after(5000, auto_translate)  # Schedule the next check in 5 seconds

    # Run translation in a separate thread
    threading.Thread(target=worker, daemon=True).start()


# Configure grid layout for centering widgets with minimal spacing
root.grid_rowconfigure(0, weight=0)  # Title
root.grid_rowconfigure(1, weight=0)  # Short label 1
root.grid_rowconfigure(1, weight=0)  # Input 1
root.grid_rowconfigure(3, weight=0)  # Combo and Button
root.grid_rowconfigure(4, weight=0)  # Short label 2
root.grid_rowconfigure(5, weight=0)  # Input 2
root.grid_columnconfigure(0, weight=1)

# Title Label
title_label = tk.Label(root, text="Google Translator Using Python", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, sticky="n", pady=15)

# Short label in the center
short_label1 = tk.Label(root, text="Text to Translate:", font=("Arial", 10, "bold"))
short_label1.grid(row=1, column=0, pady=10)

combo_box = ttk.Combobox(root, values=list_of_languages, width=20, height=15)
combo_box.grid(row=2, pady=0)
combo_box.place(x=58, y=93)

# Input for the first short label
input1 = tk.Text(root, height=7, width=60)
input1.grid(row=3, column=0, pady=15)

# Combo Box and button next to each other

short_label2 = tk.Label(root, text="Translated Text:", font=("Arial", 10, "bold"))
short_label2.grid(row=5, column=0, pady=10)


combo_box2 = ttk.Combobox(root, values=list_of_languages, width=20, height=15)
combo_box2.grid(row=6, column=0, pady=0)  # Second combo box below the button
combo_box2.place(x=58, y=280)
combo_box2.set("English")

# Two short labels


# Input for the second short label
input2 = tk.Text(root, height=7, width=60)
input2.grid(row=7, column=0, pady=15)

error_label = tk.Label(root, text="...", font=("Arial", 10, "bold"), fg="red")
error_label.grid(row=8, column=0, pady=15)

root.after(5000, auto_translate)

# Run the Tkinter event loop
root.mainloop()
