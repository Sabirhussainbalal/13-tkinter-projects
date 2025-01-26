import tkinter as tk
from tkinter import messagebox
from plyer import notification
import time
import threading
from tkcalendar import Calendar
from datetime import datetime, timedelta
from PIL import Image, ImageTk

# Function to send notifications at the specified time
def send_notification_at_time(title, message, notification_time, status_label):
    # Wait until the scheduled notification time
    while datetime.now() < notification_time:
        time.sleep(1)  # Check every second
    
    # Send the notification
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Time the notification stays on screen
    )
    
    # Update the status label on the GUI
    status_label.config(text=f"Notification sent at {notification_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
# Function to start the notification process in a separate thread
def start_notifications():
    title = title_entry.get()
    message = message_entry.get()

    # Get the selected date and time from the calendar and entry fields
    selected_date = calendar.get_date()
    selected_time = time_entry.get()

    try:
        # Combine the date and time into a single datetime object
        notification_time_str = f"{selected_date} {selected_time}"
        notification_time = datetime.strptime(notification_time_str, "%m/%d/%y %H:%M")
        
        if notification_time < datetime.now():
            raise ValueError("Selected time must be in the future.")
    except ValueError as e:
        messagebox.showerror("Invalid Input", f"Error with date/time: {e}. Please select a future time.")
        return

    # Update status in the GUI before starting the notifications
    status_label.config(text="Notifications are running...")

    # Start the notification function in a new thread to prevent the GUI from freezing
    threading.Thread(target=send_notification_at_time, args=(title, message, notification_time, status_label), daemon=True).start()

# Initialize the Tkinter window
root = tk.Tk()
root.title("Notification Scheduler")
root.geometry("500x550")

# Disable resizing to remove the maximize button
root.resizable(False, False)

try:
    bg_img = Image.open("bg.jpg")  # First path
except:
    bg_img = Image.open("11_set_notification/bg.jpg")  # Fallback path

bg_img = bg_img.resize((500, 550))  # Resize image to fit the window
bg_img_tk = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window

# Create widgets for title, message, and interval input
title_label = tk.Label(root, text="Notification Title:")
title_label.pack(pady=5)
title_entry = tk.Entry(root, width=40)
title_entry.pack(pady=5)

message_label = tk.Label(root, text="Notification Message:")
message_label.pack(pady=5)
message_entry = tk.Entry(root, width=40)
message_entry.pack(pady=5)

# Create a calendar widget to select the date
calendar_label = tk.Label(root, text="Select the date:")
calendar_label.pack(pady=5)
calendar = Calendar(root, selectmode='day', date_pattern='mm/dd/yy')
calendar.pack(pady=5)

# Create an entry widget for the user to enter time (HH:MM)
time_label = tk.Label(root, text="Enter time (HH:MM):")
time_label.pack(pady=5)
time_entry = tk.Entry(root, width=20)
time_entry.pack(pady=5)

# Create a button to start the notifications
start_button = tk.Button(root, text="Start Notifications", command=start_notifications)
start_button.pack(pady=20)

# Create a label to display the status of the notifications
status_label = tk.Label(root, text="Notification status will appear here.", fg="blue")
status_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
