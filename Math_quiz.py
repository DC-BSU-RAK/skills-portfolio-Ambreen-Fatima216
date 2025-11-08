from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# main window
root = Tk()
root.title("Math Quiz")
root.geometry("1200x1000")
root.resizable(False, False)

# load background image
bg_image = Image.open("P1.png").resize((1200, 1000))
bg_photo = ImageTk.PhotoImage(bg_image)

# button images
start_btn_img = ImageTk.PhotoImage(Image.open("S1.png").resize((300, 100)))
rules_btn_img = ImageTk.PhotoImage(Image.open("R1.png").resize((300, 100)))
back_btn_img = ImageTk.PhotoImage(Image.open("B1.png").resize((300, 100)))
easy_btn_img = ImageTk.PhotoImage(Image.open("E1.png").resize((300, 100)))
medium_btn_img = ImageTk.PhotoImage(Image.open("I1.png").resize((300, 100)))
hard_btn_img = ImageTk.PhotoImage(Image.open("C1.png").resize((300, 100)))
playagain_btn_img = ImageTk.PhotoImage(Image.open("B1.png").resize((300, 100)))

# globals
score = 0
question_num = 0
answer = 0
level = ""
attempt = 1
entry = None

# container for all frames
container = Frame(root)
container.pack(fill="both", expand=True)

frames = {}

def create_frame(name):
    frame = Frame(container, width=1200, height=1000)
    frame.pack_propagate(False)
    frame.pack(fill="both", expand=True)
    bg_label = Label(frame, image=bg_photo)
    bg_label.place(x=0, y=0)
    frames[name] = frame
    return frame

def show_frame(name):
    for f in frames.values():
        f.pack_forget()
    frames[name].pack(fill="both", expand=True)

# === MAIN MENU ===
main_menu_frame = create_frame("main")

Button(main_menu_frame, image=start_btn_img, borderwidth=0, highlightthickness=0, command=lambda: show_frame("level")).place(x=450, y=500)
Button(main_menu_frame, image=rules_btn_img, borderwidth=0, highlightthickness=0, command=lambda: show_frame("rules")).place(x=450, y=630)

# === RULES FRAME ===
rules_frame = create_frame("rules")
Label(rules_frame, text="Rules", font=("Arial", 40, "bold"), bg="#add8e6").place(x=530, y=200)
rules_text = """1. There are 10 questions.
2. 10 points for 1st try.
3. 5 points for 2nd try.
4. Easy → 1 digit
5. Intermediate → 2 digits (may include negatives)
6. Hard → 3 digits (may include negatives)
"""
Label(rules_frame, text=rules_text, font=("Arial", 20), bg="#add8e6", justify="left").place(x=430, y=300)
Button(rules_frame, image=back_btn_img, borderwidth=0, highlightthickness=0, command=lambda: show_frame("main")).place(x=450, y=700)

# === LEVEL FRAME ===
level_frame = create_frame("level")
Label(level_frame, text="Select Difficulty", font=("Arial", 35, "bold"), bg="#add8e6").place(x=440, y=300)
Button(level_frame, image=easy_btn_img, borderwidth=0, highlightthickness=0, command=lambda: start_quiz("easy")).place(x=450, y=400)
Button(level_frame, image=medium_btn_img, borderwidth=0, highlightthickness=0, command=lambda: start_quiz("medium")).place(x=450, y=520)
Button(level_frame, image=hard_btn_img, borderwidth=0, highlightthickness=0, command=lambda: start_quiz("hard")).place(x=450, y=640)
Button(level_frame, image=back_btn_img, borderwidth=0, highlightthickness=0, command=lambda: show_frame("main")).place(x=450, y=760)

# === QUIZ FRAME ===
quiz_frame = create_frame("quiz")
score_label = Label(quiz_frame, text="Score: 0", font=("Arial", 22, "bold"), bg="#add8e6")
score_label.place(x=950, y=40)
question_label = Label(quiz_frame, text="", font=("Arial", 22, "bold"), bg="#add8e6")
question_label.place(x=480, y=200)
problem_label = Label(quiz_frame, text="", font=("Arial", 50, "bold"), bg="#add8e6")
problem_label.place(x=450, y=300)
entry = Entry(quiz_frame, font=("Arial", 30), width=8, justify="center")
entry.place(x=500, y=400)
submit_btn = Button(quiz_frame, text="Submit", font=("Arial", 22, "bold"), command=lambda: check_answer())
submit_btn.place(x=520, y=480)

# === RESULTS FRAME ===
results_frame = create_frame("results")
Label(results_frame, text="Quiz Complete!", font=("Arial", 40, "bold"), bg="#add8e6").place(x=460, y=300)
score_result_label = Label(results_frame, text="", font=("Arial", 25), bg="#add8e6")
score_result_label.place(x=500, y=400)
grade_label = Label(results_frame, text="", font=("Arial", 25, "bold"), bg="#add8e6")
grade_label.place(x=530, y=460)
Button(results_frame, image=playagain_btn_img, borderwidth=0, highlightthickness=0, command=lambda: show_frame("main")).place(x=450, y=560)

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
            messagebox.showinfo("Wrong", f"Wrong again! Correct answer was {answer}.")
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

show_frame("main")
root.mainloop()
