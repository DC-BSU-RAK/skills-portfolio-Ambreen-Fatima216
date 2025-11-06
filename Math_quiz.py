import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# --- FILE PATHS (update these to match your images) ---
BG_IMAGE_PATH = "P1.png"
START_BTN_PATH = "S1.png"
RULES_BTN_PATH = "R1.png"
EASY_BTN_PATH = "E1.png"
MODERATE_BTN_PATH = "I1.png"
ADVANCED_BTN_PATH = "C1.png"
BACK_BTN_PATH = "B1.png"


# --- SIZES ---
WIN_W, WIN_H = 1200, 1000
BTN_W, BTN_H = 300, 100


class MathsQuizApp:
    def __init__(self, root):
        self.root = root
        root.title("Maths Quiz")
        root.geometry(f"{WIN_W}x{WIN_H}")
        root.resizable(False, False)

        self.btn_images = {}
        self.load_images()

        # Create Canvas for BG
        self.canvas = tk.Canvas(root, width=WIN_W, height=WIN_H)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Frame for content
        self.content_frame = tk.Frame(self.canvas, bg='white', padx=50, pady=50)
        self.canvas.create_window(WIN_W // 2, WIN_H // 2, window=self.content_frame, anchor="center")

        # Quiz state variables
        self.score = 0
        self.question_count = 0
        self.current_answer = None
        self.attempt = 1
        self.level = None

        self.display_main_menu()

    def load_images(self):
        """Load and resize all required images"""
        try:
            img = Image.open(BG_IMAGE_PATH).resize((WIN_W, WIN_H), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(img)

            paths = {
                'start': START_BTN_PATH,
                'rules': RULES_BTN_PATH,
                'easy': EASY_BTN_PATH,
                'moderate': MODERATE_BTN_PATH,
                'advanced': ADVANCED_BTN_PATH,
                'back': BACK_BTN_PATH
            }

            for name, path in paths.items():
                img = Image.open(path).resize((BTN_W, BTN_H), Image.Resampling.LANCZOS)
                self.btn_images[name] = ImageTk.PhotoImage(img)

        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Image not found: {e}")
            self.root.destroy()

    def clear_frame(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    def create_img_btn(self, key, command, text=""):
        return tk.Button(
            self.content_frame,
            image=self.btn_images[key],
            command=command,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            compound="center",
            text=text,
            fg="white",
            font=('Arial', 20, 'bold')
        )

    # ------------------ MENUS ------------------
    def display_main_menu(self):
        self.clear_frame()
        tk.Label(self.content_frame, text="MATHS QUIZ", font=('Arial', 40, 'bold'), bg='white').pack(pady=40)
        self.create_img_btn('start', self.display_level_menu, "Start").pack(pady=20)
        self.create_img_btn('rules', self.display_rules, "Rules").pack(pady=20)

    def display_rules(self):
        self.clear_frame()
        tk.Label(self.content_frame, text="RULES", font=('Arial', 35, 'bold'), bg='white').pack(pady=20)
        rules = (
            "1. 10 questions per quiz.\n"
            "2. 10 points for correct 1st attempt.\n"
            "3. 5 points for correct 2nd attempt.\n"
            "4. Each level increases number size.\n"
        )
        tk.Label(self.content_frame, text=rules, font=('Arial', 16), bg='white', justify="left").pack(pady=20)
        self.create_img_btn('back', self.display_main_menu, "Back").pack(pady=20)

    def display_level_menu(self):
        self.clear_frame()
        tk.Label(self.content_frame, text="SELECT LEVEL", font=('Arial', 35, 'bold'), bg='white').pack(pady=20)

        tk.Label(self.content_frame, text="Easy: 1-digit numbers (Addition/Subtraction)", font=('Arial', 14), bg='white').pack()
        self.create_img_btn('easy', lambda: self.start_quiz('easy'), "Easy").pack(pady=10)

        tk.Label(self.content_frame, text="Moderate: 2-digit (Mixed Pos/Neg)", font=('Arial', 14), bg='white').pack()
        self.create_img_btn('moderate', lambda: self.start_quiz('moderate'), "Moderate").pack(pady=10)

        tk.Label(self.content_frame, text="Advanced: 3-digit (Mixed Pos/Neg)", font=('Arial', 14), bg='white').pack()
        self.create_img_btn('advanced', lambda: self.start_quiz('advanced'), "Advanced").pack(pady=10)

        self.create_img_btn('back', self.display_main_menu, "Back").pack(pady=20)

    # ------------------ QUIZ ------------------
    def start_quiz(self, level):
        self.level = level
        self.score = 0
        self.question_count = 0
        self.next_question()

    def randomInt(self):
        if self.level == 'easy':
            return random.randint(1, 9)
        elif self.level == 'moderate':
            return random.randint(-99, 99)
        else:
            return random.randint(-999, 999)

    def decideOperation(self):
        return random.choice(['+', '-'])

    def next_question(self):
        self.clear_frame()
        if self.question_count == 10:
            self.display_results()
            return

        self.num1 = self.randomInt()
        self.num2 = self.randomInt()
        self.operation = self.decideOperation()

        if self.operation == '+':
            self.current_answer = self.num1 + self.num2
        else:
            self.current_answer = self.num1 - self.num2

        self.question_count += 1
        self.attempt = 1

        tk.Label(self.content_frame, text=f"Question {self.question_count}/10", font=('Arial', 20, 'bold'), bg='white').pack(pady=20)
        tk.Label(self.content_frame, text=f"{self.num1} {self.operation} {self.num2} =", font=('Arial', 40, 'bold'), bg='white').pack(pady=20)

        self.answer_entry = tk.Entry(self.content_frame, font=('Arial', 24), justify='center')
        self.answer_entry.pack(pady=20)

        tk.Button(self.content_frame, text="Submit", font=('Arial', 20, 'bold'),
                  command=self.check_answer).pack(pady=20)

    def check_answer(self):
        try:
            user_ans = int(self.answer_entry.get())
        except ValueError:
            messagebox.showwarning("Error", "Please enter a valid number!")
            return

        if user_ans == self.current_answer:
            if self.attempt == 1:
                self.score += 10
            else:
                self.score += 5
            messagebox.showinfo("Correct!", "Good job!")
            self.next_question()
        else:
            if self.attempt == 1:
                self.attempt += 1
                messagebox.showwarning("Incorrect", "Try again!")
            else:
                messagebox.showerror("Wrong!", f"Wrong again! The correct answer was {self.current_answer}.")
                self.next_question()

    def display_results(self):
        self.clear_frame()
        grade = self.get_grade(self.score)

        tk.Label(self.content_frame, text="QUIZ COMPLETE!", font=('Arial', 35, 'bold'), bg='white').pack(pady=20)
        tk.Label(self.content_frame, text=f"Your score: {self.score}/100", font=('Arial', 25), bg='white').pack(pady=10)
        tk.Label(self.content_frame, text=f"Grade: {grade}", font=('Arial', 25, 'bold'), bg='white').pack(pady=10)

        self.create_img_btn('back', self.display_level_menu, "Play Again").pack(pady=30)

    def get_grade(self, score):
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


# ------------------ MAIN ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MathsQuizApp(root)
    root.mainloop()
