import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import os
from tkinter import simpledialog, messagebox
from tkinter.simpledialog import askstring


# Create the main window
root = tk.Tk()
root.title("ShutDown App")
root.geometry('305x305')
style = Style()

# Disable resizing to remove the maximize button
root.resizable(False, False)

try:
    bg_img = Image.open("bg.jpg")  # First path
except:
    bg_img = Image.open("10_shutdown_app/bg.jpg")  # Fallback path

bg_img = bg_img.resize((305, 305))  # Resize image to fit the window
bg_img_tk = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window




def centered_messagebox(title, message, icon="info"):
    # Get the root window's position and size
    root.update_idletasks()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    # Calculate the messagebox position relative to the root window
    msgbox_width = 200  # Approximate width of the messagebox
    msgbox_height = 100  # Approximate height of the messagebox
    msgbox_x = root_x + (root_width // 2) - (msgbox_width // 2)
    msgbox_y = root_y + (root_height // 2) - (msgbox_height // 2)

    # Temporarily change the geometry of the messagebox
    root.geometry(f"+{msgbox_x}+{msgbox_y}")
    
    # Display messagebox based on the icon type
    if icon == "info":
        messagebox.showinfo(title, message)
    elif icon == "warning":
        messagebox.showwarning(title, message)
    elif icon == "error":
        messagebox.showerror(title, message)
    elif icon == "question":
        messagebox.askquestion(title, message)
    else:
        raise ValueError("Invalid icon type. Choose from 'info', 'warning', 'error', or 'question'.")

def Restart():
    blur_frame = blur_window()  # Apply blur to the window
    response = centered_messagebox("Confirmation", "Do you really want to restart your computer?", icon="question")
    if response:  # If user clicks Yes
        os.system("shutdown /r /t 1")
    else:  # If user clicks No
        unblur_window(blur_frame)
    

def Restart_with_Time():
    blur_frame = blur_window()  # Assuming blur_window() applies some blur effect to the root window
    time_units = ["seconds", "minutes", "hours"]

    # Create a new window for the unit selection
    select_window = tk.Toplevel(root)
    select_window.title("Select Unit")
    select_window.geometry("300x200")  # Set a fixed size for the window
    select_window.resizable(False, False)  # Disable resizing

    # Center the window on the screen
    screen_width = select_window.winfo_screenwidth()
    screen_height = select_window.winfo_screenheight()
    window_width = 300
    window_height = 200
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    select_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a StringVar to store the selected unit
    unit_var = tk.StringVar(value="Select Unit")  # Default value

    # Create the combobox (dropdown) for unit selection
    unit_combo = ttk.Combobox(select_window, values=time_units, state="readonly", textvariable=unit_var)
    unit_combo.place(relx=0.5, rely=0.4, anchor="center")  # Center the combobox in the window

    # Function to handle OK button click
    def on_ok_click():
        unit = unit_var.get()
        if unit == "Select Unit":
            messagebox.showinfo("Info", "Please select a valid time unit.")
            return
        select_window.destroy()  # Close the select window
        get_time(unit)

    # Function to handle Cancel button click
    def on_cancel_click():
        messagebox.showinfo("Info", "Selection canceled.")
        unblur_window(blur_frame)
        select_window.destroy()  # Close the select window

    # Create OK button
    ok_button = tk.Button(select_window, text="OK", command=on_ok_click)
    ok_button.place(relx=0.3, rely=0.7, anchor="center")

    # Create Cancel button
    cancel_button = tk.Button(select_window, text="Cancel", command=on_cancel_click)
    cancel_button.place(relx=0.7, rely=0.7, anchor="center")

    # Function to get the time based on the unit selected
    def get_time(unit):
        msg = f"Enter {unit}: "
        while True:
            try:
                message = askstring("Input", msg, parent=root)

                if message is None:  # If user cancels
                    unblur_window(blur_frame)
                    return

                # Handle unit-based time calculation
                if unit == "seconds":
                    time = int(message)
                elif unit == "minutes":
                    time = int(message) * 60
                elif unit == "hours":
                    time = int(message) * 3600

                response = centered_messagebox(
                    "Confirmation", 
                    f"Do you really want to restart your computer after: {message} {unit}?", 
                    icon="question"
                )
                if response:
                    os.system(f"shutdown /r /t {time}")
                else:
                    unblur_window(blur_frame)
                break
            except ValueError:
                msg = "Please enter a valid number: "
    

def LogOut():
    blur_frame = blur_window()  
    response = centered_messagebox("Confirmation", "Do you really want to Logout your computer?", icon="question")
    if response:  # If user clicks Yes
        os.system("shutdown -l")
    else:  # If user clicks No
        unblur_window(blur_frame)
    

def ShutDown():
    blur_frame = blur_window()  # Apply blur to the window
    response = centered_messagebox("Confirmation", "Do you really want to Shutdown your computer?", icon="question")
    if response:  # If user clicks Yes
        os.system("shutdown /s /t 1")
    else:  # If user clicks No
        unblur_window(blur_frame)
    
def blur_window():
    # Add a semi-transparent overlay to simulate a blur effect
    blur_frame = tk.Frame(root, bg="gray", width=root.winfo_width(), height=root.winfo_height())
    blur_frame.place(x=0, y=0, relwidth=1, relheight=1)
    blur_frame.attributes = {'alpha': 0.5}  # Adjust transparency if needed
    return blur_frame

def unblur_window(blur_frame):
    # Removes the blur effect by destroying the canvas overlay
    blur_frame.destroy()

button_options = {
    "font": ("Helvetica", 12, "italic"),
    "cursor": "hand2",
    "bg": "#f5f5f5",  # Light white background
    "activebackground": "skyblue",
    "relief": "ridge",
    "bd": 0,
    "width": 20,
    "height": 2
}

# Hover effects
def on_enter(event):
    # Get the current font and apply bold style on hover, keep the italic style
    current_font = event.widget.cget("font")
    font_name, font_size, *styles = current_font.split()  # Extract font name, size, and style(s)
    styles = set(styles)  # Convert list to a set to handle multiple styles
    styles.add("bold")  # Add bold to the set
    event.widget.config(bg="gray", highlightthickness=1.5, bd=1, font=(font_name, int(font_size), *styles))

def on_leave(event):
    # Restore the original font without bold, keeping italic
    current_font = event.widget.cget("font")
    font_name, font_size, *styles = current_font.split()  # Extract font name, size, and style(s)
    styles = set(styles)  # Convert list to a set to handle multiple styles
    styles.discard("bold")  # Remove bold if it exists
    event.widget.config(bg="#f5f5f5", highlightthickness=1, bd=0, font=(font_name, int(font_size), *styles))



# Set button font style
italic_font = ("Helvetica", 12, "italic")


# Add buttons directly to the main window with commands and hover effects
r = tk.Button(root, text="Restart", command=Restart, **button_options)
r.pack(pady=10)
r.bind("<Enter>", on_enter)
r.bind("<Leave>", on_leave)

rt = tk.Button(root, text="Restart With Time", command=Restart_with_Time, **button_options)
rt.pack(pady=10)
rt.bind("<Enter>", on_enter)
rt.bind("<Leave>", on_leave)

lg = tk.Button(root, text="LogOut", command=LogOut, **button_options)
lg.pack(pady=10)
lg.bind("<Enter>", on_enter)
lg.bind("<Leave>", on_leave)

st = tk.Button(root, text="ShutDown", command=ShutDown, **button_options)
st.pack(pady=10)
st.bind("<Enter>", on_enter)
st.bind("<Leave>", on_leave)


root.mainloop()