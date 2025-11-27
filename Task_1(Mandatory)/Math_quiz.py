from tkinter import *
from PIL import Image, ImageTk
import random

# Global reference for the application icon
icon_photo_ref = None

#CUSTOM POP UP DIALOG
#This functions replace standard tkinter messagebox calls

def create_custom_dialog(title, message, type="info", callback_yes=None):    
    dialog = Toplevel(root)
    dialog.title(title)
    # Set the icon for the pop-up
    global icon_photo_ref
    if icon_photo_ref:
            # Apply the stored icon to window
            dialog.iconphoto(False, icon_photo_ref)
      
    # Calculate position to center the dialog over the main window
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    
    dialog_width = 350
    dialog_height = 180
    x = root_x + root_width // 2 - dialog_width // 2
    y = root_y + root_height // 2 - dialog_height // 2
    dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    # Set dialog as transient for root
    dialog.transient(root) 
    dialog.grab_set()      
    dialog.resizable(False, False)
    
    #colors and icon based on type
    if type == "warning":
        bg_color = "#F0AD4E" # Orange for warnings
        fg_color = "#333333"
        icon = "⚠️"
    elif type == "confirm":
        bg_color = "#5BC0DE" # Blue for confirmation
        fg_color = "white"
        icon = "❓"
    elif type == "wrong":
        bg_color = "#D9534F" # Red for wrong 
        fg_color = "white"
        icon = "❌"
    else: #correct
        bg_color = "#5CB85C" # Green for correct 
        fg_color = "white"
        icon = "✅"
        
    dialog.configure(bg=bg_color)
    
    # Message Label
    Label(
        dialog,
        text=f"{icon} {message}",
        bg=bg_color,
        fg=fg_color,
        font=("Arial", 12, "bold"),
        wraplength=dialog_width - 20,
        pady=15
    ).pack(padx=10)
# Adding the buttons according to the different situations
    button_frame = Frame(dialog, bg=bg_color)
    button_frame.pack(pady=10)
    
    if type == "confirm":
        # Yes Button
        Button(
            button_frame,
            text="Yes, Reset",
            command=lambda: [dialog.destroy(), callback_yes()],
            bg="#D9534F", fg="white",
            font=("Arial", 10, "bold"),
            relief="raised", padx=10, pady=5
        ).pack(side=LEFT, padx=10)
        
        # No Button
        Button(
            button_frame,
            text="No, Continue",
            command=dialog.destroy,
            bg="#292B2C", fg="white",
            font=("Arial", 10, "bold"),
            relief="raised", padx=10, pady=5
        ).pack(side=RIGHT, padx=10)
    else:
        # OK Button for warning
        Button(
            button_frame,
            text="OK",
            command=dialog.destroy,
            bg="#292B2C", fg="white",
            font=("Arial", 10, "bold"),
            relief="raised", padx=15, pady=5, width=8
        ).pack()

    #until the dialog is closed this won't run
    root.wait_window(dialog) 

# Main Page 
root = Tk()
root.title("Math Quiz")
root.geometry("600x500")
root.resizable(False, False)

# Adding Images for the separate bgs for each level and different pages
    # All images resized to fit the window or button size
bg_image = Image.open("Task_1(Mandatory)/bg.png").resize((600, 500))
bg_photo = ImageTk.PhotoImage(bg_image)
start_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/start.png").resize((200, 75)))
rules_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/rules.png").resize((200, 75)))
back_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/back.png").resize((200, 75)))
easy_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/easy.png").resize((200, 75)))
medium_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/intermidiate.png").resize((200, 75)))
hard_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/challenging.png").resize((200, 75)))
playagain_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/playagain.png").resize((200, 75)))
Start_Quiz_Img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/Start_Quiz.png").resize((200, 75)))
Submit_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/Submit.png").resize((125, 50)))
# Using a smaller image for the in-quiz back button 
small_back_btn_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/back.png").resize((150, 50)))
# Separate level backgrounds themed differently for each difficulty
easy_bg_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/easy_bg.png").resize((600, 500)))
medium_bg_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/medium_bg.png").resize((600, 500)))
hard_bg_img = ImageTk.PhotoImage(Image.open("Task_1(Mandatory)/hard_bg.png").resize((600, 500)))
    
#apply the icon photo
icon_photo_ref = ImageTk.PhotoImage(file="Task_1(Mandatory)/maths.ico")
root.iconphoto(False, icon_photo_ref)
    
# Variables used for quiz logic
score = 0
question_num = 0
answer = 0
level = ""
attempt = 1

# Creating the main container for all pages
container = Frame(root)
container.pack(fill="both", expand=True)
frames = {}

# Function to create each page
def create_frame(name):
    frame = Frame(container, width=600, height=500)
    frame.pack_propagate(False) 	# Stops resizing of frame
    frame.pack(fill="both", expand=True)

    # Set background image if available
    if bg_photo:
        bg_label = Label(frame, image=bg_photo)
        bg_label.place(x=0, y=0)
    else:
        frame.config(bg="#87ceeb") 
    
    frames[name] = frame
    return frame

# Function to switch between frames
def show_frame(name):
    for f in frames.values():
        f.pack_forget()
    frames[name].pack(fill="both", expand=True)

#MAIN MENU PAGE
main_menu_frame = create_frame("main")
Button(main_menu_frame, image=start_btn_img, borderwidth=0, highlightthickness=0,
        command=lambda: show_frame("level"), text="Start Quiz" if not start_btn_img else "").place(x=200, y=300)
Button(main_menu_frame, image=rules_btn_img, borderwidth=0, highlightthickness=0,
        command=lambda: show_frame("rules"), text="Rules" if not rules_btn_img else "").place(x=200, y=380)

#RULES PAGE
rules_frame = create_frame("rules")
Label(rules_frame, text="Rules", font=("Arial", 40, "bold"), bg="#217dc3").place(x=225, y=40)

#rules text
rules_text = """1. There are 10 questions.
2. 10 points for 1st try.
3. 5 points for 2nd try.
4. Easy → 1 digit
5. Intermediate → 2 digits (may include negatives)
6. Hard → 3 digits (may include negatives)
"""
Label(rules_frame, text=rules_text, font=("Arial", 16), bg="#217DC3", justify="left").place(x=65, y=150)

# Back button to return to main page
Button(rules_frame, image=back_btn_img, borderwidth=0, highlightthickness=0,
        command=lambda: show_frame("main"), text="Back" if not back_btn_img else "").place(x=200, y=380)

#LEVEL SELECTION PAGE 
level_frame = create_frame("level")

# Background inside the level frame
level_bg_label = Label(level_frame)
level_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Default background before selecting a level
if easy_bg_img:
    level_bg_label.config(image=easy_bg_img)
    level_bg_label.image = easy_bg_img # Keep reference

Label(level_frame, text="Select Difficulty", font=("Arial", 35, "bold"), bg="#add8e6").place(x=125, y=150)

# Buttons for each difficulty
Button(level_frame, image=easy_btn_img, borderwidth=0, highlightthickness=0,
        command=lambda: select_level("easy"), text="Easy" if not easy_btn_img else "").place(x=200, y=230)
Button(level_frame, image=medium_btn_img, borderwidth=0, highlightthickness=0,
        command=lambda: select_level("medium"), text="Medium" if not medium_btn_img else "").place(x=200, y=320)
Button(level_frame, image=hard_btn_img, borderwidth=0, highlightthickness=0,
        command=lambda: select_level("hard"), text="Hard" if not hard_btn_img else "").place(x=200, y=410)

#Back button at top-right
Button(level_frame, image=small_back_btn_img, borderwidth=0, highlightthickness=0,
        command=lambda: show_frame("main"), text="Back" if not small_back_btn_img else "").place(x=400, y=50)

#START QUIZ PAGE
start_frame = create_frame("start")

#Background for start frame changes based on difficulty
start_bg_label = Label(start_frame)
start_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

start_label = Label(start_frame, text="", font=("Arial", 30, "bold"), bg="#add8e6")
start_label.place(x=100, y=150)

#Button to begin quiz
Button(start_frame, image=Start_Quiz_Img, font=("Arial", 22), command=lambda: start_quiz(level), 
       text="Start Quiz" if not Start_Quiz_Img else "").place(x=200, y=250)

#Back button to return to level select
Button(start_frame, image=back_btn_img, font=("Arial", 22), command=lambda: show_frame("level"), 
       text="Back" if not back_btn_img else "").place(x=200, y=350)

#QUIZ PAGE
quiz_frame = create_frame("quiz")

#Background that changes accoding to the level 
quiz_bg_label = Label(quiz_frame)
quiz_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Score displayed at top-right
score_label = Label(quiz_frame, text="Score: 0", font=("Arial", 22, "bold"), bg="#add8e6")
score_label.place(x=400, y=20)

# Centered question and answer area
question_label = Label(quiz_frame, text="", font=("Arial", 22, "bold"), bg="#add8e6")
question_label.place(relx=0.5, y=100, anchor=CENTER)

problem_label = Label(quiz_frame, text="", font=("Arial", 50, "bold"), bg="#add8e6")
problem_label.place(relx=0.5, y=200, anchor=CENTER)

entry = Entry(quiz_frame, font=("Arial", 30), width=8, justify="center")
entry.place(relx=0.5, y=320, anchor=CENTER)

submit_btn = Button(quiz_frame, image=Submit_btn_img, justify="center", command=lambda: check_answer(),
                    text="Submit" if not Submit_btn_img else "")
submit_btn.place(relx=0.5, y=400, anchor=CENTER)

# Back button inside the quiz page
Button(quiz_frame, image=small_back_btn_img, borderwidth=0, highlightthickness=0,
        command=lambda: confirm_back(), text="Back" if not small_back_btn_img else "").place(x=25, y=25)

#RESULTS PAGE 
results_frame = create_frame("results")

#Background of results page uses easy background by default
results_bg_label = Label(results_frame, image=easy_bg_img)
results_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#Completion text
Label(results_frame, text="Quiz Complete!", font=("Arial", 40, "bold"), justify=CENTER, bg="#add8e6").place(x=100, y=100)

#Score and grade labels
score_result_label = Label(results_frame, text="", font=("Arial", 25), bg="#add8e6")
score_result_label.place(x=100, y=220)

grade_label = Label(results_frame, text="", font=("Arial", 25, "bold"), bg="#add8e6")
grade_label.place(x=100, y=280)

#Play again button
Button(results_frame, image=playagain_btn_img, borderwidth=0, highlightthickness=0,
        command=lambda: show_frame("main"), text="Play Again" if not playagain_btn_img else "").place(x=200, y=350)

#QUIZ LOGIC FUNCTIONS 

#Random numbers being generated based on difficulty 
def random_numbers():
    if level == "easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "medium":
        return random.randint(-99, 99), random.randint(-99, 99)
    else:
        return random.randint(-999, 999), random.randint(-999, 999)

#Randomly choose + or -
def operation():
    return random.choice(["+", "-"])

#Change backgrounds and move to "Start Quiz" page
def select_level(chosen_level):
    global level
    level = chosen_level

    # Update level selection background
    if level == "easy" and easy_bg_img:
        level_bg_label.config(image=easy_bg_img)
        start_bg_label.config(image=easy_bg_img)
        quiz_bg_label.config(image=easy_bg_img)
        results_bg_label.config(image=easy_bg_img)
    elif level == "medium" and medium_bg_img:
        level_bg_label.config(image=medium_bg_img)
        start_bg_label.config(image=medium_bg_img)
        quiz_bg_label.config(image=medium_bg_img)
        results_bg_label.config(image=medium_bg_img)
    elif level == "hard" and hard_bg_img:
        level_bg_label.config(image=hard_bg_img)
        start_bg_label.config(image=hard_bg_img)
        quiz_bg_label.config(image=hard_bg_img)
        results_bg_label.config(image=hard_bg_img)

    start_label.config(text=f"You selected {level.upper()}.\nStart the quiz?", justify="center")
    show_frame("start")

#Confirmation popup before exiting quiz
def reset_and_back_to_main():
    """Internal function to reset state after confirmation."""
    global score, question_num
    score = 0
    question_num = 0
    entry.delete(0, END)
    score_label.config(text=f"Score: 0")
    #Takes user back to the main start screen page 
    show_frame("main")

def confirm_back():
    #Uses custom Toplevel dialog for confirmation
    create_custom_dialog(
        "Confirm Exit", 
        "Are you sure you want to go back to the main menu? All quiz progress will be lost.", 
        type="confirm", 
        callback_yes=reset_and_back_to_main
    )

#Start quiz and apply level background
def start_quiz(chosen_level):
    global level, score, question_num
    level = chosen_level
    score = 0
    question_num = 0
    next_question()

#Generating and display each question
def next_question():
    global num1, num2, op, answer, question_num, attempt
    question_num += 1
    attempt = 1

    #After 10 questions show results
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

#Check if answer is correct and handle scoring
def check_answer():
    global score, attempt
    try:
        user_answer = int(entry.get())
    except ValueError:
        # Replaced messagebox.showwarning
        create_custom_dialog("Invalid Input", "Please enter a valid number!", type="warning")
        return
    
    if user_answer == answer:
        #Full points on first try, half on second
        score += 10 if attempt == 1 else 5
        score_label.config(text=f"Score: {score}")
        # Replaced messagebox
        create_custom_dialog("Correct!", "That's right! Moving to the next question.", type="info")
        next_question()
    else:
        if attempt == 1:
            attempt += 1
            # Replaced messagebox
            create_custom_dialog("Try again", "Not quite, try once more!", type="wrong")
        else:
            # Replaced messagebox
            create_custom_dialog("Wrong", f"Wrong again! The correct answer was {answer}.", type="wrong")
            next_question()

#Show the final results page
def show_results():
    score_result_label.config(text=f"Your Score: {score}/100")
    grade_label.config(text=f"Grade: {get_grade(score)}")
    show_frame("results")

#Basic grading function
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

#Start the app on main menu
show_frame("main")
root.mainloop()