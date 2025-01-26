import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from moviepy import VideoFileClip
from PIL import Image, ImageTk

# Function to convert video to audio
def convert_video_to_audio(video_path, output_folder, update_status):
    try:
        # Extract file name and extension
        filename = os.path.basename(video_path)
        file_name_without_extension = os.path.splitext(filename)[0]

        # Create an audio file name and check if it exists
        audio_filename = f"{file_name_without_extension}.mp3"
        audio_path = os.path.join(output_folder, audio_filename)

        counter = 1
        while os.path.exists(audio_path):
            audio_filename = f"{file_name_without_extension}_{counter}.mp3"
            audio_path = os.path.join(output_folder, audio_filename)
            counter += 1

        # Use `with` to ensure proper cleanup of resources
        with VideoFileClip(video_path) as video_clip:
            if video_clip.audio is None:
                raise ValueError("The selected video does not contain an audio track.")
            
            # Extract and write audio
            video_clip.audio.write_audiofile(audio_path, codec="libmp3lame")
        
        # Final update to the label
        update_status(f"Conversion Complete! Saved as: {os.path.basename(audio_path)}")
        return audio_path

    except Exception as e:
        update_status(f"Error: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to handle the video selection and conversion
def select_video():
    video_path = filedialog.askopenfilename(title="Select a video", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])

    if video_path:
        # Display converting message
        label_status.config(text="Converting... Please wait.")
        
        # Start the conversion in a separate thread to avoid blocking the GUI
        threading.Thread(target=convert_video, args=(video_path,)).start()

# Function to perform the conversion and update progress
def convert_video(video_path):
    try:
        # Get the output folder
        output_folder = os.path.dirname(video_path)
        
        # Start conversion and update status label
        convert_video_to_audio(video_path, output_folder, update_status)

    except Exception as e:
        label_status.config(text="Error during conversion.")
        messagebox.showerror("Error", str(e))

# Function to update the label from the worker thread using root.after() to ensure thread safety
def update_status(message):
    root.after(0, lambda: label_status.config(text=message))

# Create the main window
root = tk.Tk()
root.title("Video to Audio Converter")
root.geometry("500x300")
root.resizable(False, False)

# Set background image
try:
    bg_img = Image.open("bg.jpg")  # First path
except:
    bg_img = Image.open("3_converter/bg.jpg")  # Fallback path

bg_img = bg_img.resize((500, 300))  # Resize image to fit the window
bg_img_tk = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window
bg_label.image = bg_img_tk  # Keep reference to avoid garbage collection

# Add a label to show status
label_status = tk.Label(root, text="Select a video file to convert to audio.", width=50, height=3)
label_status.pack(pady=20)

# Add a button to select video file
btn_select_video = tk.Button(root, text="Select Video File", width=20, height=2, command=select_video)
btn_select_video.pack()

# Run the Tkinter event loop
root.mainloop()
