from tkinter import *
from datetime import datetime
import threading

# Create the main window
root = Tk()
root.title("Digital Clock")
root.geometry("380x150")
root.resizable(False, False)
root.config(bg="#2a2a2a")

def update_time():
    
    now = datetime.now()  # Get the current time
    current_time = now.strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
    current_date = now.strftime("%d")           # Day of the month
    am_pm_value = now.strftime("%p")            # AM or PM
    month_number = now.strftime("%m")           # Month Number
    x = f"{month_number}.{current_date}"
    day_name = now.strftime("%A")               # Day of the week
    y = f"{current_time[0:8]}"
    y = y.replace(":", " : ")
    # Update the labels with the current time and date
    am_pm.config(text=am_pm_value)  # Update the AM/PM label
    date_is.config(text=x)  # Update the date label
    day_is.config(text=day_name)  # Update the day label
    label1.config(text=y)  # Update the time label
    

    
    
time_text = {
    "font": ("Helvetica", 40, "bold"),
    "foreground": "red",
    "bg": "#2a2a2a",
}

bg = {
    "bg": "#2a2a2a",
}

# Create a label widget
am_pm = Label(root, text="")
am_pm.pack()
am_pm.config(font=("Arial", 7, "bold"), foreground="red", **bg)
am_pm.place(x=35, y=40)

label1 = Label(root, text="12 : 09 : 51", **time_text)
label1.pack()
label1.place(x=60, y=20)

day = Label(root, text="DAY", font=("Arial", 7), foreground="red", **bg)
day.place(x=83, y=80)

day_is = Label(root, text="MONDAY", font=("Arial", 12, "bold"), foreground="red", **bg)
day_is.pack()
day_is.place(x=65, y=100)

month = Label(root, text="MON", font=("Arial", 7), foreground="red", **bg)
month.place(x=260, y=80)

date = Label(root, text="DATE", font=("Arial", 7), foreground="red", **bg)
date.place(x=285, y=80)

date_is = Label(root, text="12.01", font=("Arial", 12, "bold"), foreground="red", **bg)
date_is.pack()
date_is.place(x=263, y=100)


made_by = Label(root, text="MADE BY Sabir", font=("Arial", 7, "bold"), foreground="red", **bg)
made_by.pack()
made_by.place(x=160, y=135)

def auto_translate():
    def worker():
        update_time()
        root.after(1, auto_translate)  # Schedule the next check in 5 seconds

    # Run translation in a separate thread
    threading.Thread(target=worker, daemon=True).start()

root.after(1, auto_translate)

# Run the application
root.mainloop()
