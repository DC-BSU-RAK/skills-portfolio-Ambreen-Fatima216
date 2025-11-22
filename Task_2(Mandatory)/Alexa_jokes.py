import tkinter as tk
import random
from PIL import Image, ImageTk
import os
import winsound


#Load jokes from file
file_path = "Task_2(Mandatory)/randomJokes.txt"

jokes = []
with open(file_path, "r") as f:
    for line in f:
        parts = line.strip().split("?", 1)
        if len(parts) == 2:
            jokes.append((parts[0] + "?", parts[1]))

#GUI Setup
root = tk.Tk()
root.title("Joke Assistant")
root.geometry("500x500")
root.resizable(False, False)
root.iconphoto(False, ImageTk.PhotoImage(file="Task_2(Mandatory)/logo.ico"))

#Background Image
try:
    bg_img = tk.PhotoImage(file="Task_2(Mandatory)/bg2.png")
    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(relwidth=1, relheight=1)
except:
    root.config(bg="#e8d5ff")

# Labels 
setup_label = tk.Label(
    root,
    text="Tap the button to begin!",
    bg="#e8d5ff",
    fg="#4b2a7f",
    font=("Arial", 14, "bold"),
    wraplength=460
)
setup_label.place(relx=0.5, y=70, anchor="center")

punchline_label = tk.Label(
    root,
    text="",
    bg="#e8d5ff",
    fg="#6d3fc7",
    font=("Arial", 12),
    wraplength=460
)
punchline_label.place(relx=0.5, y=120, anchor="center")
current_joke = None

# Laugh Sound
def play_laugh_sound():
    winsound.PlaySound(
        "Task_2(Mandatory)/laughtrack.wav",
        winsound.SND_FILENAME | winsound.SND_ASYNC
    )

# Button Functions
def show_joke():
    global current_joke
    current_joke = random.choice(jokes)
    setup, _ = current_joke
    setup_label.config(text=setup)
    punchline_label.config(text="")

def show_punchline():
    if current_joke:
        _, punch = current_joke
        punchline_label.config(text=punch)
        play_laugh_sound()

# Button Maker
def make_button(text, command, color):
    return tk.Button(
        root,
        text=text,
        command=command,
        font=("Arial", 12, "bold"),
        bg=color,
        fg="black",
        relief="flat",
        width=20,
        height=1
    )

# Buttons Centered 

btn1 = make_button("Alexa tell me a Joke", show_joke, "#c9b6ff")
btn1.place(relx=0.5, y=200, anchor="center")

btn2 = make_button("Show Punchline", show_punchline, "#ffd86b")
btn2.place(relx=0.5, y=250, anchor="center")

btn3 = make_button("Next Joke", show_joke, "#a6e1ff")
btn3.place(relx=0.5, y=300, anchor="center")

btn4 = make_button("Quit", root.destroy, "#ff6b6b")
btn4.place(relx=0.5, y=360, anchor="center")

# Run App
root.mainloop()
