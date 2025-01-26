import tkinter as tk
from tkinter import ttk
import speedtest
import threading
from PIL import Image, ImageTk

def start_test():
    # Show "Testing..." message while the test is running
    download_label.config(text="Testing...", bg="gray")
    upload_label.config(text="Testing...", bg="gray")
    ping_label.config(text="Testing...", bg="gray")
    
    # Run the test in a separate thread to prevent UI freezing
    threading.Thread(target=run_speed_test).start()

def run_speed_test():
    start_button.config(text="Wait..")
    start_button.config(state="disabled")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download()
        upload_speed = st.upload()
        ping = st.results.ping

        # Update the labels with results
        download_label.config(
            text=f"Download Speed: {download_speed / 1_000_000:.2f} Mbps",
            bg="green",
            fg="white",
        )
        upload_label.config(
            text=f"Upload Speed: {upload_speed / 1_000_000:.2f} Mbps",
            bg="green",
            fg="white",
        )
        ping_label.config(
            text=f"Ping: {ping:.2f} ms", bg="green", fg="white"
        )
    except Exception as e:
        # Handle errors gracefully
        error_message = "Error: Could not fetch data"
        download_label.config(text=error_message, bg="red", fg="white")
        upload_label.config(text=error_message, bg="red", fg="white")
        ping_label.config(text=error_message, bg="red", fg="white")
    start_button.config(text="Start Test")
    start_button.config(state="enabled")

# Initialize tkinter window
root = tk.Tk()
root.geometry('400x400')
root.resizable(False, False)
root.title('Internet Speed Check')


try:
    bg_img = Image.open("bg.jpg")  # First path
except:
    bg_img = Image.open("8_internet_speed/bg.jpg")  # Fallback path

bg_img = bg_img.resize((400, 400))  # Resize image to fit the window
bg_img_tk = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window
bg_label.image = bg_img_tk  # Keep reference to avoid garbage collection


label = ttk.Label(root, text="Check your internet speed in just a click!", font=("Arial", 14))
label.pack(pady=10)

# Button style
style = ttk.Style()
style.configure(
    "TButton",
    font=("Arial", 12, "bold"),
    foreground="black",
    padding=(10, 20),
    borderwidth=2,
    cursor="hand2",
    relief="solid"
)
style.map(
    "TButton",
    background=[('active', '#45a049'), ('pressed', '#3e8e41')]
)

start_button = ttk.Button(root, text="Start Test", style="TButton", command=start_test)
start_button["cursor"] = "hand2"
start_button.pack(pady=20)

# Labels to show results
download_label = tk.Label(root, text="Download Speed", fg="dimgray", bg="gray", font=("Arial", 14), width=25, height=2, anchor="center")
download_label.pack(pady=10)

upload_label = tk.Label(root, text="Upload Speed", fg="dimgray", bg="gray", font=("Arial", 14), width=25, height=2, anchor="center")
upload_label.pack(pady=10)

ping_label = tk.Label(root, text="Ping", fg="dimgray", bg="gray", font=("Arial", 14), width=25, height=2, anchor="center")
ping_label.pack(pady=10)

root.mainloop()
