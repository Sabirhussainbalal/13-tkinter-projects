from tkinter import *
import requests
from datetime import datetime
from PIL import Image, ImageTk

# Initialize Window
root = Tk()
root.geometry("400x400")
root.title("Weather App")
root.resizable(False, False)

# Set background image
try:
    bg_img = Image.open("bg.jpg")  # First path
except:
    bg_img = Image.open("12_weather_app/bg.jpg")  # Fallback path

bg_img = bg_img.resize((400, 400))  # Resize image to fit the window
bg_img_tk = ImageTk.PhotoImage(bg_img)

bg_label = Label(root, image=bg_img_tk)
bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window
bg_label.image = bg_img_tk  # Keep reference to avoid garbage collection

# Function to format time for location
def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()

city_value = StringVar()

# Function to fetch and display weather with animation
def showWeather():
    api_key = "4a2f54b5a80504c313ba85fb833ca93b"  # Replace with your actual API key
    city_name = city_value.get().strip()
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    response = requests.get(weather_url)
    weather_info = response.json()

    # Clear existing text
    tfield.delete("1.0", "end")

    if weather_info.get('cod') == 200:  # Valid response
        kelvin = 273
        temp = int(weather_info['main']['temp'] - kelvin)
        feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
        pressure = weather_info['main']['pressure']
        humidity = weather_info['main']['humidity']
        wind_speed = weather_info['wind']['speed'] * 3.6
        sunrise = weather_info['sys']['sunrise']
        sunset = weather_info['sys']['sunset']
        timezone = weather_info['timezone']
        cloudy = weather_info['clouds']['all']
        description = weather_info['weather'][0]['description']

        sunrise_time = time_format_for_location(sunrise + timezone)
        sunset_time = time_format_for_location(sunset + timezone)

        weather = (
            f"Weather of: {city_name}\n"
            f"Temperature (Celsius): {temp}\u00b0\n"
            f"Feels like in (Celsius): {feels_like_temp}\u00b0\n"
            f"Pressure: {pressure} hPa\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed:.2f} km/h\n"
            f"Sunrise at {sunrise_time} and Sunset at {sunset_time}\n"
            f"Cloud: {cloudy}%\n"
            f"Info: {description.capitalize()}"
        )
    else:
        weather = f"Weather for '{city_name}' not found! Kindly enter a valid city name!"

    # Animate text
    animate_text(weather)

# Animation function
def animate_text(text, index=0):
    if index < len(text):
        tfield.insert(END, text[index])
        root.after(50, animate_text, text, index + 1)

# Function to clear the text field
def clearText():
    tfield.delete("1.0", "end")

# Hover effects for the buttons
def on_enter(e, btn):
    btn.config(bg="teal", fg="white")

def on_leave(e, btn):
    btn.config(bg="lightblue", fg="black")

# Interface
city_head = Label(root, text='Enter City Name', font='Arial 12 bold')
city_head.pack(pady=10)

inp_city = Entry(root, textvariable=city_value, width=24, font='Arial 14 bold', justify='center')
inp_city.pack(pady=5)

# Button frame for alignment
button_frame = Frame(root)
button_frame.pack(pady=10)

# Check Weather Button
check_button = Button(
    button_frame, command=showWeather, text="Check Weather", font="Arial 10",
    bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5
)
check_button.grid(row=0, column=0, padx=5)
check_button.bind("<Enter>", lambda e: on_enter(e, check_button))
check_button.bind("<Leave>", lambda e: on_leave(e, check_button))

# Clear Button
clear_button = Button(
    button_frame, command=clearText, text="Clear Data", font="Arial 10",
    bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5
)
clear_button.grid(row=0, column=1, padx=5)
clear_button.bind("<Enter>", lambda e: on_enter(e, clear_button))
clear_button.bind("<Leave>", lambda e: on_leave(e, clear_button))

weather_now = Label(root, text="The Weather is:", font='Arial 12 bold')
weather_now.pack(pady=10)

tfield = Text(root, width=46, height=10, font="Arial 10", wrap=WORD)
tfield.pack(pady=5)

# Run the app
root.mainloop()