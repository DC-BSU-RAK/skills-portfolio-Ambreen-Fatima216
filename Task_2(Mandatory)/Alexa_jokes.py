import tkinter as tk
import random
from PIL import Image, ImageTk
import os
import winsound
from tkinter import messagebox 

# Load jokes from file given in the resourses
file_path = "Task_2(Mandatory)/randomJokes.txt"
jokes = []
with open(file_path, "r") as f:
    for line in f:
        parts = line.strip().split("?", 1)
        if len(parts) == 2:
            jokes.append((parts[0] + "?", parts[1]))

# INSTRUCTIONS POP UP CLAASS
class InstructionDialog(tk.Toplevel):
    def __init__(self, parent, title, bg_image):
        super().__init__(parent)
        self.transient(parent) # Window on top of parent
        self.title(title)
        self.parent = parent
        
        #Set icon from parent
        try:
            self.iconphoto(False, parent.icon_photo) 
        except AttributeError:
            # Fallback if parent's icon_photo attribute isn't set
            pass

        # Set background image to match the main window
        self.bg_img = bg_image
        bg_label = tk.Label(self, image=self.bg_img)
        bg_label.place(relwidth=1, relheight=1)
        
        # Center the dialog on screen
        self.update_idletasks()
        w = 350 
        h = 300
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        x = parent.winfo_rootx() + (parent_w // 2) - (w // 2)
        y = parent.winfo_rooty() + (parent_h // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.resizable(False, False)
        
        #POP UP Dialog Content
        content_frame = tk.Frame(self, bg="#e8d5ff", bd=2, relief=tk.RIDGE)
        content_frame.pack(padx=20, pady=20, fill='both', expand=True)
        #welcome to the joke app pop up
        tk.Label(
            content_frame,
            text="Welcome to the Joke App! 😂",
            bg="#e8d5ff",
            fg="#4b2a7f",
            font=("Arial", 16, "bold")
        ).pack(pady=(15, 5))
        #instructions for the app
        tk.Label(
            content_frame,
            text="Instructions:",
            bg="#e8d5ff",
            fg="#6d3fc7",
            font=("Arial", 12, "underline")
        ).pack(pady=(5, 0))
        #Instructions content
        tk.Label(
            content_frame,
            text="1. Tap the ALEXA button to get a new joke setup.\n2. Tap SHOW to reveal the punchline and hear the laugh track.\n3. Tap NEXT to skip to the next joke.\n4. Tap QUIT to close the app.",
            bg="#e8d5ff",
            fg="#4b2a7f",
            font=("Arial", 9),
            justify=tk.LEFT,
            wraplength=300
        ).pack(padx=10, pady=(5, 10))
        #Instructions pop up button
        tk.Button(
            content_frame,
            text="Got It!",
            command=self.destroy,
            bg="#6d3fc7",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            bd=0,
            highlightthickness=0
        ).pack(pady=(5, 15))

        # Make the dialog modal
        self.grab_set()
        self.focus_set()
        self.wait_window(self)

#Quit Confirmation Dialog Class
class QuitConfirmationDialog(tk.Toplevel):
    def __init__(self, parent, title, bg_image):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.parent = parent
        self.result = False # Default result is No/Cancel

        try:
            self.iconphoto(False, parent.icon_photo)
        except AttributeError:
            pass

        self.bg_img = bg_image
        if self.bg_img:
            bg_label = tk.Label(self, image=self.bg_img)
            bg_label.place(relwidth=1, relheight=1)
        else:
            self.config(bg="#e8d5ff")
            
        self.update_idletasks()
        w = 380
        h = 180
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        x = parent.winfo_rootx() + (parent_w // 2) - (w // 2)
        y = parent.winfo_rooty() + (parent_h // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        #Doesnt allow to be resized
        self.resizable(False, False)

        # Dialog Content
        content_frame = tk.Frame(self, bg="#e8d5ff", bd=2, relief=tk.RIDGE)
        content_frame.pack(padx=20, pady=20, fill='both', expand=True)
        #Confirming if u want to quit app
        tk.Label(
            content_frame,
            text="⚠️ ARE YOU SURE YOU WANT TO QUIT?",
            bg="#e8d5ff",
            fg="#1b003c", # A warning red color
            font=("Arial", 12, "bold")
        ).pack(pady=(10, 10))

        # Button Box
        btn_frame = tk.Frame(content_frame, bg="#e8d5ff")
        btn_frame.pack(pady=5)
        #yes button
        tk.Button(
            btn_frame,
            text="Yes, Quit",
            command=self.on_yes,
            bg="#6d3fc7",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            bd=0,
            highlightthickness=0
        ).pack(side=tk.LEFT, padx=10)
        #No button
        tk.Button(
            btn_frame,
            text="No, Keep Joking",
            command=self.destroy,
            bg="#4b2a7f",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            bd=0,
            highlightthickness=0
        ).pack(side=tk.LEFT, padx=10)
        
        self.grab_set()
        self.focus_set()
        self.wait_window(self)

    def on_yes(self):
        self.result = True
        self.destroy()

#GUI Setup
AmbreenJokes = tk.Tk()
AmbreenJokes.title("😂Alexa Tell Me A Joke😂")
AmbreenJokes.geometry("500x500")
AmbreenJokes.resizable(False, False)

# Store the PhotoImage object for the icon so the Instruction Dialog can use it
try:
    AmbreenJokes.icon_photo = ImageTk.PhotoImage(file="Task_2(Mandatory)/logo.ico")
    AmbreenJokes.iconphoto(False, AmbreenJokes.icon_photo)
except Exception:
    AmbreenJokes.icon_photo = None

# Background Image
try:
    # Store the PhotoImage object 
    bg_img_raw = tk.PhotoImage(file="Task_2(Mandatory)/bg2.png")
    bg_img = bg_img_raw
    bg_label = tk.Label(AmbreenJokes, image=bg_img)
    bg_label.place(relwidth=1, relheight=1)
except:
    bg_img = None
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
        "Task_2(Mandatory)/laughtrack.wav",#laughter track to play on punchline
        winsound.SND_FILENAME | winsound.SND_ASYNC
    )

# Button Functions
def show_joke():
    global current_joke
    current_joke = random.choice(jokes)
    setup, _ = current_joke
    setup_label.config(text=setup)
    
    # Clear and hide the punchline label when a new joke is loaded
    punchline_label.config(text="")
    punchline_label.place_forget() 

def show_punchline():
    if current_joke:
        _, punch = current_joke
        punchline_label.config(text=punch)
        
        # Make the punchline label visible when the button is clicked
        punchline_label.place(relx=0.5, y=120, anchor="center") 
        
        play_laugh_sound()

# Quit Confirmation Function
def confirm_quit():
    if bg_img:
        dialog = QuitConfirmationDialog(AmbreenJokes, "Confirm Exit", bg_img)
        if dialog.result:
            AmbreenJokes.destroy()
    else:
        # Fallback if no image is loaded
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to quit the application?"):
            AmbreenJokes.destroy()


# Load Images for Buttons
img_joke = ImageTk.PhotoImage(file="Task_2(Mandatory)/ALEXA.png")
img_punchline = ImageTk.PhotoImage(file="Task_2(Mandatory)/SHOW.png")
img_next = ImageTk.PhotoImage(file="Task_2(Mandatory)/Next.png")
img_quit = ImageTk.PhotoImage(file="Task_2(Mandatory)/Quit.png")

# Buttons with the images
btn1 = tk.Button(AmbreenJokes, image=img_joke, command=show_joke,
                relief="flat", bd=0, highlightthickness=0)
btn1.place(relx=0.5, y=200, anchor="center")

btn2 = tk.Button(AmbreenJokes, image=img_punchline, command=show_punchline,
                relief="flat", bd=0, highlightthickness=0)
btn2.place(relx=0.5, y=260, anchor="center")

btn3 = tk.Button(AmbreenJokes, image=img_next, command=show_joke,
                relief="flat", bd=0, highlightthickness=0)
btn3.place(relx=0.5, y=320, anchor="center")

#Button 4 command to use the new confirm_quit function
btn4 = tk.Button(AmbreenJokes, image=img_quit, command=confirm_quit,
                relief="flat", bd=0, highlightthickness=0)
btn4.place(relx=0.5, y=380, anchor="center")

#Call the Instruction Dialog on application load
if bg_img:
    InstructionDialog(AmbreenJokes, "App Instructions", bg_img)

# Initially load a joke and hide the punchline label
show_joke()

# Run App
AmbreenJokes.mainloop()