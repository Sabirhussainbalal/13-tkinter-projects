import tkinter as tk
from PIL import Image, ImageTk
import os, random, requests, json
from datetime import datetime
from time import time
from pathlib import Path



# Variables
sentences_v = []
start_times = []
end_time = 0
sentence = ''
duration = 0
sentencess = []

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Typing Speed Checker")
    root.resizable(False, False)

    # Set fixed window size (optional)
    root.geometry("800x600")  # You can adjust this as per your preference
    try:
        bg_img = Image.open("bg.jpg")  # First path
    except:
        bg_img = Image.open("4_speed_calculator/bg.jpg")  # Fallback path

    bg_img = bg_img.resize((800, 600))  # Resize image to fit the window
    bg_img_tk = ImageTk.PhotoImage(bg_img)

    bg_label = tk.Label(root, image=bg_img_tk)
    bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to fill the window
    bg_label.image = bg_img_tk  # Keep reference to avoid garbage collection

    # Create a label widget
    label = tk.Label(root, text="Welcome to the Typing Speed Checker Game..", font=("Arial", 16, "bold"))
    label.place(relx=0.5, rely=0.03, anchor="center")
    # label.place_forget()

    subtitle = tk.Label(root, text="Let's get started! Try to beat the high score if you can.....", font=("Arial", 12, "bold"))
    subtitle.place(relx=0.5, rely=0.12, anchor="center")



    try:
        with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
    except:
        with open('4_speed_calculator/data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    
    
    for i in data['quotes']:  
        sentences_v.append(i['quote'])  



    

    # Create buttons (Start, Exit, Next)
    def on_hover_button(event, button, color):     
        button.config(bg=color)  # Change background color on hover

    def on_leave_button(event, button):
        button.config(bg="lightgray")  # Reset background color when not hovering

    def start_action():
        msg_label_func("green", "Game Started...")
        start_button.config(state="disabled")  # Disable Start button
        exit_button.config(state="normal")   # Enable Exit button
        done_button.config(state="normal")
        words_per_sc.place(relx=0, rely=0.20, anchor="w")
        Error.place(relx=0, rely=0.25, anchor="w")
        type_label.place(relx=0.20, rely=0.48, anchor="center")
        sen.place(relx=0.5, rely=0.55, anchor="center")
        entry.place(relx=0.5, rely=0.70, anchor="center")
        next_button.place(relx=0.43, rely=0.85, anchor="center")
        done_button.place(relx=0.55, rely=0.85, anchor="center")
        set_question()

    def next_action():
        next_button.config(state="disabled")
        set_question()
        done_button.config(state="normal")


    def exit_action():
        exit_button.config(state="disabled")  # Disable Exit button
        start_button.config(state="normal")   # Enable Start button
        next_button.config(state="disabled")  # Disable Next button
        done_button.config(state="disabled")


    # 1 step generate a sentence

    def get_random_sentence():
        entry.delete(0, tk.END)
        sentence = random.choice(sentences_v)
        sentencess.append(sentence)
        return sentence

    # 2 step compare sentence and user's input and count errors   
    def error(sentence, user_sen):  
        error_count = 0
        # Compare characters one by one up to the length of the shortest string
        for i in range(min(len(sentence), len(user_sen))):
            if sentence[i] != user_sen[i]:
                error_count += 1
        
        # If user_sen is shorter, count the extra characters in sentence as errors
        error_count += abs(len(sentence) - len(user_sen))
        
        error_count = error_count - 1
        if error_count == -1:
            error_count = 0
        sentencess = []
        start_times = []
        return error_count
    



    # 4 set question
    def set_question():
        sentence = get_random_sentence()
        start_time = time() 
        start_times.append(start_time)
        sen.config(text=f"{sentence}", fg="red")

    
    def done():
        tl_legn = len(start_times)
        start_time = start_times[tl_legn-1]
        start_time = int(start_time)
        end_time = time()
        end_time = int(end_time)
        duration = end_time - start_time
        done_button.config(state="disabled")
        user_sen = entry.get()   
        leng = len(sentencess)
        sentence =  sentencess[leng-1]   
        error_count =  error(sentence, user_sen)
        Error.config(text=f"Error count: {error_count}")
        word_count = len(user_sen.split()) 
        wps = word_count / duration if duration > 0 else 0  
        words_per_sc.config(text=f"Words per second: {wps:.2f}")
        next_button.config(state="normal")
        



            
        

    # Start Button
    start_button = tk.Button(root, text="Start", font=("Arial", 12, "bold"), bg="lightgray", command=start_action)
    start_button.place(relx=0.43, rely=0.26, anchor="center")

    # Exit Button
    exit_button = tk.Button(root, text="Exit", font=("Arial", 12, "bold"), bg="lightgray", command=exit_action, state="disabled")
    exit_button.place(relx=0.55, rely=0.26, anchor="center")

    # Next Button
    next_button = tk.Button(root, text="Next", font=("Arial", 12, "bold"), bg="lightgray", command=next_action, state="disabled")
    next_button.place_forget()


    done_button = tk.Button(root, text="Done", font=("Arial", 12, "bold"), bg="lightgray", command=done, state="disabled")
    done_button.place_forget()

    # Add hover effects for all buttons
    start_button.bind("<Enter>", lambda event, button=start_button: on_hover_button(event, button, "lightblue"))
    start_button.bind("<Leave>", lambda event, button=start_button: on_leave_button(event, button))
    start_button.config(cursor="hand2")

    exit_button.bind("<Enter>", lambda event, button=exit_button: on_hover_button(event, button, "lightblue"))
    exit_button.bind("<Leave>", lambda event, button=exit_button: on_leave_button(event, button))
    exit_button.config(cursor="hand2")

    next_button.bind("<Enter>", lambda event, button=next_button: on_hover_button(event, button, "lightblue"))
    next_button.bind("<Leave>", lambda event, button=next_button: on_leave_button(event, button))
    next_button.config(cursor="hand2")

    done_button.bind("<Enter>", lambda event, button=next_button: on_hover_button(event, button, "lightblue"))
    done_button.bind("<Leave>", lambda event, button=next_button: on_leave_button(event, button))
    done_button.config(cursor="hand2")
    
    # btn
    # Create a button with hover effect and animation


    # Update the rely positions of other labels to be closer to one another


    words_per_sc = tk.Label(root, text="Words per second: ...", fg="green", font=("Arial", 10, "bold"))
    words_per_sc.place_forget()

    Error = tk.Label(root, text="Error count: ...", font=("Arial", 10, "bold"), fg="black")
    Error.place_forget()



    scrollable_label = tk.Label(root,text="Made by Sabir..." , font=("Helvetica", 10, "bold"), fg="#2c3e50", wraplength=260)
    scrollable_label.place(relx=0.5, rely=0.97, anchor="center")


    type_label = tk.Label(root,text="Type the following sentence:" , font=("Helvetica", 10, "bold"), fg="#2c3e50", wraplength=260)
    type_label.place_forget()

    sen = tk.Label(root,text="..." , font=("Helvetica", 10), fg="black", wraplength=750)
    sen.place_forget()


    def msg_label_func(color, content):
        scrollable_label.config(fg=color, text=content)

    # msg_label_func("#ff5733", f"Status Warning:")

    # Create an entry (input) widget
    entry = tk.Entry(root, width=90)  # Replace x with the desired width for the entry widget
    entry.place_forget()
    

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()