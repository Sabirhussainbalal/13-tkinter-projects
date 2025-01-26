import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# Initialize the Tkinter window
root = Tk()
root.geometry("500x400")
root.title("Phone Number Validator")
root.resizable(False, False)

# Set background image
try:
    bg_img = Image.open("bg.jpg")  # First path
except:
    bg_img = Image.open("13_user_nu_details/bg.jpg")  # Fallback path

bg_img = bg_img.resize((500, 400))  # Resize image to fit the window
bg_img_tk = ImageTk.PhotoImage(bg_img)

bg_label = Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window
bg_label.image = bg_img_tk  # Keep reference to avoid garbage collection

# Functions

def validate_phone():
    """Validate the phone number and display results."""
    number = phone_entry.get().strip()
    if not number:
        messagebox.showwarning("Input Error", "Please enter a phone number.")
        return

    try:
        phone_number = phonenumbers.parse(number, None)

        # Clear previous data
        result_text.delete("1.0", "end")

        # Start building the result string
        result = (
            f"Country Code: {phone_number.country_code}\n"
            f"National Number: {phone_number.national_number}\n"
        )

        # Validate the phone number
        is_valid = phonenumbers.is_valid_number(phone_number)
        if is_valid:
            carrier_name = carrier.name_for_number(phone_number, "en")
            location = geocoder.description_for_number(phone_number, "en")
            time_zones = timezone.time_zones_for_number(phone_number)

            result += (
                f"Carrier: {carrier_name}\n"
                f"Location: {location}\n"
                f"Time Zones: {', '.join(time_zones)}\n"
            )
        else:
            result += "This phone number is not valid.\n"

        # Animate result text
        animate_text(result)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def clear_data():
    """Clear the input and result fields."""
    phone_entry.delete(0, END)
    result_text.delete("1.0", "end")


def animate_text(text, index=0):
    """Animate text display in the result box."""
    if index < len(text):
        result_text.insert(END, text[index])
        root.after(50, animate_text, text, index + 1)

# UI Components

# Input Label and Entry
input_label = Label(root, text="Enter Phone Number:", font=("Arial", 12))
input_label.pack(pady=10)

phone_entry = Entry(root, font=("Arial", 14), justify="center", width=30)
phone_entry.pack(pady=5)

# Buttons Frame
button_frame = Frame(root)
button_frame.pack(pady=15)

validate_button = Button(
    button_frame, text="Validate", font=("Arial", 12), command=validate_phone, bg="lightblue", padx=10, pady=5
)
validate_button.grid(row=0, column=0, padx=10)

clear_button = Button(
    button_frame, text="Clear", font=("Arial", 12), command=clear_data, bg="lightcoral", padx=10, pady=5
)
clear_button.grid(row=0, column=1, padx=10)

# Result Text Box
result_label = Label(root, text="Results:", font=("Arial", 12))
result_label.pack(pady=10)

result_text = Text(root, font=("Arial", 12), width=50, height=10, wrap=WORD, state=NORMAL)
result_text.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
