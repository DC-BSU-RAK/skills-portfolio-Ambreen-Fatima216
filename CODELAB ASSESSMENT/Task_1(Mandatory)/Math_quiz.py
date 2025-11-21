from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Main Page 
root = Tk()
root.title("Math Quiz")
root.geometry("600x500")
root.resizable(False, False)

# Images
# Images
try:
    bg_image = Image.open("Task_1(Mandatory)/bg.png").resize((600, 500))
    bg_photo = ImageTk.PhotoImage(bg_image)
    start_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/start.png").resize((200, 75)))
    rules_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/rules.png").resize((200, 75)))
    back_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/back.png").resize((200, 75)))
    easy_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/easy.png").resize((200, 75)))
    medium_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/intermidiate.png").resize((200, 75)))
    hard_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/challenging.png").resize((200, 75)))
    playagain_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/playagain.png").resize((200, 75)))
    easy_bg_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/easy_bg.png").resize((600, 500)))
    medium_bg_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/medium_bg.png").resize((600, 500)))
    hard_bg_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/hard_bg.png").resize((600, 500)))

except:
    bg_photo = easy_bg_img = medium_bg_img = hard_bg_img = None
    def create_dummy_img(text):
        dummy_img = Image.new('RGB', (300, 100), color='darkblue')
        from PIL import ImageDraw, ImageFont
        d = ImageDraw.Draw(dummy_img)
        try: font = ImageFont.truetype("arial.ttf", 40)
        except: font = ImageFont.load_default()
        d.text((150,50), text, fill='white', anchor='mm', font=font)
        return ImageTk.PhotoImage(dummy_img)
    
    start_btn_img = create_dummy_img("Start")
    rules_btn_img = create_dummy_img("Rules")
    back_btn_img = create_dummy_img("Back")
    easy_btn_img = create_dummy_img("Easy")
    medium_btn_img = create_dummy_img("Intermediate")
    hard_btn_img = create_dummy_img("Challenging")
    playagain_btn_img = create_dummy_img("Play Again")

# Variables
score = 0
question_num = 0
answer = 0
level = ""
attempt = 1

# Container
container = Frame(root)
container.pack(fill="both", expand=True)
frames = {}

def create_frame(name):
    frame = Frame(container, width=600, height=500)
    frame.pack_propagate(False)
    frame.pack(fill="both", expand=True)
    if bg_photo:
        bg_label = Label(frame, image=bg_photo)
        bg_label.place(x=0, y=0)
    else:
        frame.config(bg="#87ceeb")
    frames[name] = frame
    return frame

def show_frame(name):
    for f in frames.values():
        f.pack_forget()
    frames[name].pack(fill="both", expand=True)

# Main Menu
main_menu_frame = create_frame("main")
Button(main_menu_frame, image=start_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: show_frame("level")).place(x=200, y=300)
Button(main_menu_frame, image=rules_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: show_frame("rules")).place(x=200, y=380)

# Rules Frame
rules_frame = create_frame("rules")
Label(rules_frame, text="Rules", font=("Arial", 40, "bold"), bg="#217dc3").place(x=225, y=40)
rules_text = """1. There are 10 questions.
2. 10 points for 1st try.
3. 5 points for 2nd try.
4. Easy → 1 digit
5. Intermediate → 2 digits (may include negatives)
6. Hard → 3 digits (may include negatives)
"""
Label(rules_frame, text=rules_text, font=("Arial", 16), bg="#217DC3", justify="left").place(x=65, y=150)
Button(rules_frame, image=back_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: show_frame("main")).place(x=200, y=380)

# Level Selection Frame
level_frame = create_frame("level")
level_bg_label = Label(level_frame)
level_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Default background
if easy_bg_img:
    level_bg_label.config(image=easy_bg_img)
    level_bg_label.image = easy_bg_img

Label(level_frame, text="Select Difficulty", font=("Arial", 35, "bold"), bg="#add8e6").place(x=125, y=150)
Button(level_frame, image=easy_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: select_level("easy")).place(x=200, y=230)
Button(level_frame, image=medium_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: select_level("medium")).place(x=200, y=320)
Button(level_frame, image=hard_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: select_level("hard")).place(x=200, y=410)
Button(level_frame, image=back_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: show_frame("main")).place(x=200, y=100)

# Start Quiz Frame
start_frame = create_frame("start")
start_bg_label = Label(start_frame)
start_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
start_label = Label(start_frame, text="", font=("Arial", 30, "bold"), bg="#add8e6")
start_label.place(x=100, y=150)
Button(start_frame, text="Start Quiz", font=("Arial", 22), command=lambda: start_quiz(level)).place(x=150, y=250)
Button(start_frame, text="Back", font=("Arial", 22), command=lambda: show_frame("level")).place(x=350, y=250)

# Quiz Frame
quiz_frame = create_frame("quiz")
quiz_bg_label = Label(quiz_frame)
quiz_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
score_label = Label(quiz_frame, text="Score: 0", font=("Arial", 22, "bold"), bg="#add8e6")
score_label.place(x=400, y=20)
question_label = Label(quiz_frame, text="", font=("Arial", 22, "bold"), bg="#add8e6")
question_label.place(x=150, y=100)
problem_label = Label(quiz_frame, text="", font=("Arial", 50, "bold"), bg="#add8e6")
problem_label.place(x=150, y=200)
entry = Entry(quiz_frame, font=("Arial", 30), width=8, justify="center")
entry.place(x=200, y=320)
submit_btn = Button(quiz_frame, text="Submit", font=("Arial", 22, "bold"), command=lambda: check_answer())
submit_btn.place(x=220, y=400)

# Results Frame
results_frame = create_frame("results")
Label(results_frame, text="Quiz Complete!", font=("Arial", 40, "bold"), bg="#add8e6").place(x=150, y=100)
score_result_label = Label(results_frame, text="", font=("Arial", 25), bg="#add8e6")
score_result_label.place(x=200, y=220)
grade_label = Label(results_frame, text="", font=("Arial", 25, "bold"), bg="#add8e6")
grade_label.place(x=230, y=280)
Button(results_frame, image=playagain_btn_img, borderwidth=0, highlightthickness=0,
       command=lambda: show_frame("main")).place(x=200, y=350)

# Quiz Logic
def random_numbers():
    if level == "easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "medium":
        return random.randint(-99, 99), random.randint(-99, 99)
    else:
        return random.randint(-999, 999), random.randint(-999, 999)

def operation():
    return random.choice(["+", "-"])

# Select level and go to start quiz frame
def select_level(chosen_level):
    global level
    level = chosen_level
    # Update level selection frame background to selected level
    if level == "easy" and easy_bg_img:
        level_bg_label.config(image=easy_bg_img)
        level_bg_label.image = easy_bg_img
    elif level == "medium" and medium_bg_img:
        level_bg_label.config(image=medium_bg_img)
        level_bg_label.image = medium_bg_img
    elif level == "hard" and hard_bg_img:
        level_bg_label.config(image=hard_bg_img)
        level_bg_label.image = hard_bg_img

    # Set start frame background the same as selected level
    if level == "easy" and easy_bg_img:
        start_bg_label.config(image=easy_bg_img)
        start_bg_label.image = easy_bg_img
    elif level == "medium" and medium_bg_img:
        start_bg_label.config(image=medium_bg_img)
        start_bg_label.image = medium_bg_img
    elif level == "hard" and hard_bg_img:
        start_bg_label.config(image=hard_bg_img)
        start_bg_label.image = hard_bg_img

    start_label.config(text=f"You selected {level.upper()}.\nStart the quiz?")
    show_frame("start")

def start_quiz(chosen_level):
    global level, score, question_num
    level = chosen_level
    score = 0
    question_num = 0

    # Set quiz background same as level
    if level == "easy" and easy_bg_img:
        quiz_bg_label.config(image=easy_bg_img)
        quiz_bg_label.image = easy_bg_img
    elif level == "medium" and medium_bg_img:
        quiz_bg_label.config(image=medium_bg_img)
        quiz_bg_label.image = medium_bg_img
    elif level == "hard" and hard_bg_img:
        quiz_bg_label.config(image=hard_bg_img)
        quiz_bg_label.image = hard_bg_img

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

show_frame("main")
root.mainloop()
