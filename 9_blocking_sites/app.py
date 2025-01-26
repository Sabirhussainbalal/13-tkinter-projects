import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk

# Dynamically determine the path based on the operating system
if os.name == 'nt':  # For Windows
    path = "C:\\Windows\\System32\\drivers\\etc\\hosts"
elif os.name == 'posix':  # For Unix-based systems (Mac, Linux)
    path = "/etc/hosts"
else:
    path = None  # Unsupported OS or unknown

block_sites = []

def process():
    global block_sites
    block_sites = []
    if path and os.path.exists(path):
        with open(path, "r+") as file:
            content = file.readlines()
            for line in content:
                if not line.strip().startswith("#") and line.strip():  # Ignore comments and empty lines
                    block_sites.append(line.strip().split()[1])  # Assuming the domain is in the second column
    else:
        messagebox.showerror("Error", "Hosts file path not found.")

def remove_line_from_file(path, line_to_remove):
    if path and os.path.exists(path):
        with open(path, "r") as file:
            lines = file.readlines()
        with open(path, "w") as file:
            for line in lines:
                if line.strip("\n") != line_to_remove:
                    file.write(line)

def block_site():
    site = site_entry.get()
    if not site:
        messagebox.showwarning("Input Error", "Please enter a site to block.")
        return
    
    process()
    if site in block_sites:
        messagebox.showinfo("Already Blocked", f"{site} is already blocked.")
    else:
        if path:
            with open(path, "a") as file:
                file.write(f"\n127.0.0.1 {site}")
            messagebox.showinfo("Site Blocked", f"{site} has been blocked.")
            process()
            update_blocked_sites()

    site_entry.delete(0, tk.END)

def unblock_site():
    site = site_entry.get()
    if not site:
        messagebox.showwarning("Input Error", "Please enter a site to unblock.")
        return
    
    process()
    if site in block_sites:
        line_to_remove = f"127.0.0.1 {site}"
        remove_line_from_file(path, line_to_remove)
        messagebox.showinfo("Site Unblocked", f"{site} has been unblocked.")
        process()
        update_blocked_sites()
    else:
        messagebox.showinfo("Not Blocked", f"{site} is not blocked.")

    site_entry.delete(0, tk.END)

def show_blocked_sites():
    process()
    if block_sites:
        blocked_sites_str = "\n".join(block_sites)
        messagebox.showinfo("Blocked Sites", f"Blocked Sites:\n{blocked_sites_str}")
    else:
        messagebox.showinfo("No Blocked Sites", "No sites are currently blocked.")

    site_entry.delete(0, tk.END)

def update_blocked_sites():
    blocked_sites_listbox.delete(0, tk.END)
    for site in block_sites:
        blocked_sites_listbox.insert(tk.END, site)

# Initialize the Tkinter window
root = tk.Tk()
root.title("Site Blocker")
root.geometry("400x300")
root.resizable(False, False)

try:
    bg_img = Image.open("bg.jpg")  # First path
except:
    bg_img = Image.open("9_blocking_sites/bg.jpg")  # Fallback path

bg_img = bg_img.resize((400, 300))  # Resize image to fit the window
bg_img_tk = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window
bg_label.image = bg_img_tk  # Keep reference to avoid garbage collection

# Create widgets
site_label = tk.Label(root, text="Enter site to block/unblock:")
site_label.pack(pady=5)

site_entry = tk.Entry(root, width=50)
site_entry.pack(pady=5)

block_button = tk.Button(root, text="Block Site", command=block_site)
block_button.pack(pady=5)

unblock_button = tk.Button(root, text="Unblock Site", command=unblock_site)
unblock_button.pack(pady=5)

view_button = tk.Button(root, text="View Blocked Sites", command=show_blocked_sites)
view_button.pack(pady=5)

blocked_sites_listbox = tk.Listbox(root, width=50, height=10)
blocked_sites_listbox.pack(pady=10)

# Run the initial processing to populate the blocked sites
process()

# Update the blocked sites listbox
update_blocked_sites()

# Run the Tkinter event loop
root.mainloop()
