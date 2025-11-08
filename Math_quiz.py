from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# === MAIN WINDOW ===
root = Tk()
root.title("Math Quiz")
root.geometry("900x500")
root.resizable(False, False)

# === LOAD IMAGES ===
# Placeholder for image loading, assuming 'P1.png', 'S1.png', etc., exist and are correct
try:
    bg_image = Image.open("P1.png").resize((900, 500))
    bg_photo = ImageTk.PhotoImage(bg_image)
    start_btn_img = ImageTk.PhotoImage(Image.open("S1.png").resize((300, 100)))
    rules_btn_img = ImageTk.PhotoImage(Image.open("R1.png").resize((300, 100)))
    back_btn_img = ImageTk.PhotoImage(Image.open("B1.png").resize((300, 100)))
    # It seems the images are already named correctly for the buttons based on the screenshot
    easy_btn_img = ImageTk.PhotoImage(Image.open("E1.png").resize((300, 100)))
    medium_btn_img = ImageTk.PhotoImage(Image.open("I1.png").resize((300, 100)))
    hard_btn_img = ImageTk.PhotoImage(Image.open("C1.png").resize((300, 100)))
    playagain_btn_img = ImageTk.PhotoImage(Image.open("B1.png").resize((300, 100)))
except Exception as e:
    # A simple fallback for testing if images are missing
    print(f"Image Error: {e}. Using dummy placeholders for buttons.")
    bg_photo = None # In a real app, you'd need a fallback color background
    
    # Create dummy images if the real ones fail to load for testing
    def create_dummy_img(text):
        dummy_img = Image.new('RGB', (300, 100), color='darkblue')
        from PIL import ImageDraw, ImageFont # Local import for dummy image creation
        d = ImageDraw.Draw(dummy_img)
        try:
            # Use a system font or default font if Arial isn't found
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()
        d.text((150, 50), text, fill='white', anchor='mm', font=font)
        return ImageTk.PhotoImage(dummy_img)

    start_btn_img = create_dummy_img("Start")
    rules_btn_img = create_dummy_img("Rules")
    back_btn_img = create_dummy_img("Back")
    easy_btn_img = create_dummy_img("Easy")
    medium_btn_img = create_dummy_img("Intermediate")
    hard_btn_img = create_dummy_img("Challenging")
    playagain_btn_img = create_dummy_img("Play Again")
    # If the background image is essential, you might need to stop the app or use a color.
    # For now, we'll continue with bg_photo being None if it failed.
    # messagebox.showerror("Image Error", f"Error loading images:\n{e}")
    # root.destroy()
    # exit()


# === GLOBAL VARIABLES ===
score = 0
question_num = 0
answer = 0
level = ""
attempt = 1

# === CONTAINER FOR FRAMES ===
container = Frame(root)
container.pack(fill="both", expand=True)

frames = {}

def create_frame(name):
    frame = Frame(container, width=900, height=500)
    frame.pack_propagate(False)
    frame.pack(fill="both", expand=True)
    
    # Use background image if loaded, otherwise use a default color
    if bg_photo:
        bg_label = Label(frame, image=bg_photo)
        bg_label.place(x=0, y=0)
    else:
        frame.config(bg="#87ceeb") # Sky Blue as a fallback
        
    frames[name] = frame
    return frame

def show_frame(name):
    for f in frames.values():
        f.pack_forget()
    frames[name].pack(fill="both", expand=True)

# === MAIN MENU ===
main_menu_frame = create_frame("main")
Button(main_menu_frame, image=start_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: show_frame("level")).place(x=300, y=250)
Button(main_menu_frame, image=rules_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: show_frame("rules")).place(x=300, y=380)

# === RULES FRAME ===
rules_frame = create_frame("rules")
Label(rules_frame, text="Rules", font=("Arial", 40, "bold"), bg="#add8e6").place(x=350, y=40)
rules_text = """1. There are 10 questions.
2. 10 points for 1st try.
3. 5 points for 2nd try.
4. Easy → 1 digit
5. Intermediate → 2 digits (may include negatives)
6. Hard → 3 digits (may include negatives)
"""
Label(rules_frame, text=rules_text, font=("Arial", 20), bg="#add8e6",
      justify="left").place(x=200, y=150)
Button(rules_frame, image=back_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: show_frame("main")).place(x=300, y=380)

# === LEVEL FRAME (MODIFIED) ===
level_frame = create_frame("level")
# Adjusted y-coordinate for the label to be lower for better visibility (e.g., y=100 -> y=150)
Label(level_frame, text="Select Difficulty", font=("Arial", 35, "bold"), bg="#add8e6").place(x=300, y=150)
# Adjusted y-coordinates for the buttons to be further apart and lower
Button(level_frame, image=easy_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: start_quiz("easy")).place(x=300, y=250)
Button(level_frame, image=medium_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: start_quiz("medium")).place(x=300, y=340)
Button(level_frame, image=hard_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: start_quiz("hard")).place(x=300, y=430)
# The original back button was at y=530 which is off-screen.
# I've commented out the original back button on the level screen for a cleaner 500-height layout.
# Button(level_frame, image=back_btn_img, borderwidth=0, highlightthickness=0,
#        command=lambda: show_frame("main")).place(x=300, y=530)


# === QUIZ FRAME ===
quiz_frame = create_frame("quiz")
score_label = Label(quiz_frame, text="Score: 0", font=("Arial", 22, "bold"), bg="#add8e6")
score_label.place(x=700, y=20)
question_label = Label(quiz_frame, text="", font=("Arial", 22, "bold"), bg="#add8e6")
question_label.place(x=330, y=100)
problem_label = Label(quiz_frame, text="", font=("Arial", 50, "bold"), bg="#add8e6")
problem_label.place(x=280, y=200)
entry = Entry(quiz_frame, font=("Arial", 30), width=8, justify="center")
entry.place(x=350, y=320)
submit_btn = Button(quiz_frame, text="Submit", font=("Arial", 22, "bold"),
                    command=lambda: check_answer())
submit_btn.place(x=370, y=400)

# === RESULTS FRAME ===
results_frame = create_frame("results")
Label(results_frame, text="Quiz Complete!", font=("Arial", 40, "bold"), bg="#add8e6").place(x=250, y=100)
score_result_label = Label(results_frame, text="", font=("Arial", 25), bg="#add8e6")
score_result_label.place(x=330, y=220)
grade_label = Label(results_frame, text="", font=("Arial", 25, "bold"), bg="#add8e6")
grade_label.place(x=360, y=280)
Button(results_frame, image=playagain_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: show_frame("main")).place(x=300, y=350)

# === QUIZ LOGIC ===
def random_numbers():
    if level == "easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "medium":
        return random.randint(-99, 99), random.randint(-99, 99)
    else:
        return random.randint(-999, 999), random.randint(-999, 999)

def operation():
    return random.choice(["+", "-"])

def start_quiz(chosen_level):
    global level, score, question_num
    level = chosen_level
    score = 0
    question_num = 0
    next_question()

def next_question():
    global num1, num2, op, answer, question_num, attempt
    question_num += 1
    attempt = 1
    if question_num > 10:
        show_results()
        return
    num1, num2 = random_numbers()
    op = operation()
    answer = num1 + num2 if op == "+" else num1 - num2
    question_label.config(text=f"Question {question_num}/10")
    problem_label.config(text=f"{num1} {op} {num2} =")
    entry.delete(0, END)
    score_label.config(text=f"Score: {score}")
    show_frame("quiz")

def check_answer():
    global score, attempt
    try:
        user_answer = int(entry.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number!")
        return
    if user_answer == answer:
        if attempt == 1:
            score += 10
        else:
            score += 5
        score_label.config(text=f"Score: {score}")
        messagebox.showinfo("Correct", "Good job!")
        next_question()
    else:
        if attempt == 1:
            attempt += 1
            messagebox.showinfo("Try again", "Not quite, try once more!")
        else:
            messagebox.showinfo("Wrong", f"Wrong again! The correct answer was {answer}.")
            next_question()

def show_results():
    score_result_label.config(text=f"Your Score: {score}/100")
    grade_label.config(text=f"Grade: {get_grade(score)}")
    show_frame("results")

def get_grade(score):
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "Try Again"

# === START APP ===
show_frame("main")
root.mainloop()