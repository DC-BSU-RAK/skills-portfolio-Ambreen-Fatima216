import tkinter as tk
from tkinter import PhotoImage
import random
import os

# --- 1. Pretend Setup: Create a super simple joke file for the program to use ---

file_path = "A1 - Resources/randomJokes.txt"

if not os.path.exists(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write("Why did the chicken cross the road?To get to the other side.\n")
        f.write("What do you call a fake noodle?An impasta.\n")
        f.write("What happens if you boil a clown?You get a laughing stock.\n")


# --- 2. The Main Program ---

class MySillyJokeApp:
    def __init__(self, master):
        self.master = master
        master.title("My Super Silly Joke App! 🤪")
        master.geometry("500x500")

        # ---- SIMPLE PURPLE BACKGROUND ----
        master.config(bg="#a060ff")   # light purple

        # --- Smiley Icon ---
        smiley_data = (
            'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+g'
            'yfykAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3ggQCwYgQyI7qAAAADhJ'
            'REFUOMt1kjFuwzAIRO/g/w9cO8jS+d7S0pIeQAg1QOqIExg2sZ2sUoE3C21d+48G'
            'gQ/8I5zR1hQAAAAASUVORK5CYII='
        )
        self.smiley_icon = PhotoImage(data=smiley_data)
        master.iconphoto(False, self.smiley_icon)

        # --- Load Jokes ---
        self.jokes = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('?', 1)
                if len(parts) == 2:
                    self.jokes.append((parts[0].strip() + '?', parts[1].strip()))

        self.current_joke = None

        # --- Setup Text Label ---
        self.setup_label = tk.Label(
            master,
            text="Tap the button to get started!",
            wraplength=450,
            font=("Comic Sans MS", 14, "bold"),
            bg="white",
            fg="black"
        )
        self.setup_label.pack(pady=(30, 10), padx=20)

        # --- Punchline Label ---
        self.punchline_label = tk.Label(
            master,
            text="",
            wraplength=450,
            font=("Comic Sans MS", 12),
            bg="white",
            fg="purple"
        )
        self.punchline_label.pack(pady=(5, 20), padx=20)

        # --- Buttons ---
        button_frame = tk.Frame(master, bg="#a060ff")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Alexa tell me a Joke",
            command=self.show_joke_setup,
            font=("Comic Sans MS", 10),
            bg="lime",
            activebackground="green"
        ).pack(side=tk.LEFT, padx=5)

        self.punchline_button = tk.Button(
            button_frame,
            text="Show Punchline",
            command=self.show_punchline,
            state=tk.DISABLED,
            font=("Comic Sans MS", 10),
            bg="yellow",
            activebackground="gold"
        )
        self.punchline_button.pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Next Joke",
            command=self.show_joke_setup,
            font=("Comic Sans MS", 10),
            bg="cyan",
            activebackground="blue"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            master,
            text="Quit",
            command=master.quit,
            font=("Comic Sans MS", 10),
            bg="red",
            fg="white"
        ).pack(pady=10)

    # --- Button Functions ---

    def show_joke_setup(self):
        if not self.jokes:
            self.setup_label.config(text="Uh oh! No jokes loaded! 😢")
            self.punchline_label.config(text="")
            self.punchline_button.config(state=tk.DISABLED)
            return

        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke

        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.punchline_button.config(state=tk.NORMAL)

    def show_punchline(self):
        if self.current_joke:
            _, punchline = self.current_joke
            self.punchline_label.config(text=punchline)
            self.punchline_button.config(state=tk.DISABLED)


# --- Starting the App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MySillyJokeApp(root)
    root.mainloop()
