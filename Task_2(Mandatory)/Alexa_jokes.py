import tkinter as tk
import random
from PIL import Image, ImageTk
import os
import winsound

# Load jokes from file given in the resourses
file_path = "Task_2(Mandatory)/randomJokes.txt"
jokes = []
with open(file_path, "r") as f:
    for line in f:
        parts = line.strip().split("?", 1)
        if len(parts) == 2:
            jokes.append((parts[0] + "?", parts[1]))

# GUI Setup
AmbreenJokes = tk.Tk()
AmbreenJokes.title("😂Alexa Tell Me A Joke😂")
AmbreenJokes.geometry("500x500")
AmbreenJokes.resizable(False, False)
AmbreenJokes.iconphoto(False, ImageTk.PhotoImage(file="Task_2(Mandatory)/logo.ico"))

# Background Image
try:
    bg_img = tk.PhotoImage(file="Task_2(Mandatory)/bg2.png")
    bg_label = tk.Label(AmbreenJokes, image=bg_img)
    bg_label.place(relwidth=1, relheight=1)
except:
    AmbreenJokes.config(bg="#e8d5ff")

# Labels
setup_label = tk.Label(
    AmbreenJokes,
    text="Tap the button to begin!",
    bg="#e8d5ff",
    fg="#4b2a7f",
    font=("Arial", 14, "bold"),
    wraplength=460
)
setup_label.place(relx=0.5, y=70, anchor="center")

punchline_label = tk.Label(
    AmbreenJokes,
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

# Load Images for Buttons
img_joke = ImageTk.PhotoImage(file="Task_2(Mandatory)/ALEXA.png")
img_punchline = ImageTk.PhotoImage(file="Task_2(Mandatory)/SHOW.png")
img_next = ImageTk.PhotoImage(file="Task_2(Mandatory)/Next.png")
img_quit = ImageTk.PhotoImage(file="Task_2(Mandatory)/Quit.png")

# Buttons (Image Only)
btn1 = tk.Button(AmbreenJokes, image=img_joke, command=show_joke,
                 relief="flat", bd=0, highlightthickness=0)
btn1.place(relx=0.5, y=200, anchor="center")

btn2 = tk.Button(AmbreenJokes, image=img_punchline, command=show_punchline,
                 relief="flat", bd=0, highlightthickness=0)
btn2.place(relx=0.5, y=260, anchor="center")

btn3 = tk.Button(AmbreenJokes, image=img_next, command=show_joke,
                 relief="flat", bd=0, highlightthickness=0)
btn3.place(relx=0.5, y=320, anchor="center")

btn4 = tk.Button(AmbreenJokes, image=img_quit, command=AmbreenJokes.destroy,
                 relief="flat", bd=0, highlightthickness=0)
btn4.place(relx=0.5, y=380, anchor="center")

# Run App
AmbreenJokes.mainloop()
