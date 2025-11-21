import tkinter as tk
import random
import os

# -----------------------------
# 1. Load jokes from file
# -----------------------------
file_path = "Task_2(Mandatory)/randomJokes.txt"

jokes = []
with open(file_path, "r") as f:
    for line in f:
        parts = line.strip().split("?", 1)
        if len(parts) == 2:
            jokes.append((parts[0] + "?", parts[1]))

# -----------------------------
# 2. GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Joke Assistant")
root.geometry("500x500")

# -----------------------------
# Background Image Placeholder
# -----------------------------
# You can later replace "bg.png" with your image file
try:
    bg_img = tk.PhotoImage(file="bg.png")
    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(relwidth=1, relheight=1)
except:
    root.config(bg="#e8d5ff")  # fallback lavender

# Container Frame (keeps everything centered)
container = tk.Frame(root, bg="#e8d5ff")
container.pack(expand=True)

# -----------------------------
# Labels
# -----------------------------
setup_label = tk.Label(
    container,
    text="Tap the button to begin!",
    bg="#e8d5ff",
    fg="#4b2a7f",
    font=("Arial", 14, "bold"),
    wraplength=460
)
setup_label.pack(pady=10)

punchline_label = tk.Label(
    container,
    text="",
    bg="#e8d5ff",
    fg="#6d3fc7",
    font=("Arial", 12),
    wraplength=460
)
punchline_label.pack(pady=10)

current_joke = None

# -----------------------------
# Placeholder: Laugh Sound
# -----------------------------
def play_laugh_sound():
    """
    Placeholder for sound.
    Add sound file later (ex: 'laugh.wav') using:
    
    import winsound
    winsound.PlaySound("laugh.wav", winsound.SND_FILENAME)
    """
    print("Laugh sound would play here!")  # temporary effect


# -----------------------------
# Button Functions
# -----------------------------
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
        play_laugh_sound()  # sound plays here

# -----------------------------
# Helper for Rounded Buttons
# -----------------------------
def make_button(text, command, color):
    return tk.Button(
        container,
        text=text,
        command=command,
        font=("Arial", 12, "bold"),
        bg=color,
        fg="black",
        relief="flat",
        width=20,
        height=1,
        padx=10,
        pady=6,
        bd=5
    )

# -----------------------------
# Buttons (Column layout)
# -----------------------------
btn1 = make_button("Alexa tell me a Joke", show_joke, "#c9b6ff")
btn1.pack(pady=5)

btn2 = make_button("Show Punchline", show_punchline, "#ffd86b")
btn2.pack(pady=5)

btn3 = make_button("Next Joke", show_joke, "#a6e1ff")
btn3.pack(pady=5)

btn4 = make_button("Quit", root.destroy, "#ff6b6b")
btn4.pack(pady=15)

# -----------------------------
# Run App
# -----------------------------
root.mainloop()
