import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import csv



# This code was developed using the ideas from the following youtube Channel: ForCodeCoder
# This part handles where the data file
FILE_PATH = "Task_3(Mandatory & Extention)/studentMarks.txt"
# This is where the app icon is saved
ICON_PATH = "Task_3(Mandatory & Extention)/Student.ico" 
MAX_TOTAL_MARKS = 160 # There are 3 course marks out of 20 and 1 exam mark out of 100, which adds up to 160

# THEMES COLOR FOR THE PAGE - this is for making the app look good
COLOR_DARK_BLUE = "#004AAD" # The main color for the background, a dark blue
COLOR_LIGHT_BLUE = "#E0E6F0"  # The color for the content boxes, a light grey-blue
COLOR_HEADING_BG = "#2B7EAC"  # The color for the top bar and highlights
COLOR_TEXT_PRIMARY = "white"
COLOR_TEXT_SECONDARY = "black"


# This is the main class for all the little pop-up windows (dialogs)
class BaseDialog(tk.Toplevel):
    """This is the main box class for making pop-up windows."""
    def __init__(self, parent, title):
        super().__init__(parent)
        self.transient(parent) # The pop-up window stays on top of the main window
        self.title(title)
        self.parent = parent
        self.result = None
        
        # Try to put the student icon on the pop-up window too
        try:
            self.iconbitmap(ICON_PATH)
        except Exception:
            pass # If the icon file is gone, just skip this part
        
        # Set all the colors and look for the pop-up window
        self.config(bg=COLOR_DARK_BLUE)
        self.style = ttk.Style()
        
        # This sets a consistent look for all the pop-up boxes
        self.style.configure('TFrame', background=COLOR_DARK_BLUE)
        self.style.configure('TLabel', background=COLOR_DARK_BLUE, foreground=COLOR_TEXT_PRIMARY, font=('Arial', 10, 'bold'))
        self.style.configure('TEntry', fieldbackground=COLOR_LIGHT_BLUE, foreground=COLOR_TEXT_SECONDARY, font=('Arial', 10))
        self.style.map('TButton', 
                       background=[('active', COLOR_HEADING_BG), ('!disabled', COLOR_LIGHT_BLUE)],
                       foreground=[('active', COLOR_TEXT_PRIMARY), ('!disabled', COLOR_TEXT_SECONDARY)])
        self.style.configure('TButton', font=('Arial', 10, 'bold'))
        self.style.configure('TRadiobutton', background=COLOR_DARK_BLUE, foreground=COLOR_TEXT_PRIMARY, font=('Arial', 10))

        
        # This code tries to put the little window right in the middle of the big window
        self.update_idletasks()
        w = self.winfo_reqwidth() # Get how wide the pop-up window is
        h = self.winfo_reqheight() # Get how tall the pop-up window is
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        x = parent.winfo_rootx() + (parent_w // 2) - (w // 2)
        y = parent.winfo_rooty() + (parent_h // 2) - (h // 2)
        self.geometry(f"+{x}+{y}")
        self.resizable(False, False) # Can't change the size of the pop-up window

    def show(self):
        """This function makes the pop-up window appear and makes sure you have to click it first."""
        self.grab_set()
        self.wait_window(self)

    def ok(self, event=None):
        # Stop if the user put in bad info
        if not self.validate():
            # The validation function handles the error message
            return
        self.withdraw()
        self.update_idletasks()
        try:
            self.apply()
        finally:
            self.cancel() # Close the window after trying to apply changes

    def cancel(self, event=None):
        self.parent.focus_set() # Go back to the main window
        self.destroy() # Close this pop-up window

    def validate(self):
        return True # The default rule is that it's okay

    def apply(self):
        pass # The default thing to do is nothing


# This is a custom pop-up box for showing simple messages, like an error or a warning
class MessageDialog(BaseDialog):
    """This is the pop-up box for showing a message, warning, or error."""
    def __init__(self, parent, title, message, type='info'):
        super().__init__(parent, title)
        self.type = type
        self.message = message
        
        # Change the symbol and color based on what type of message it is
        if type == 'error':
            icon_char = "❌"
            color = "#dc3545" # Red for error
        elif type == 'warning':
            icon_char = "⚠️"
            color = "#ffc107" # Yellow for warning
        elif type == 'success':
            icon_char = "✅"
            color = "#28a745" # Green for success
        else: # info
            icon_char = "ℹ️"
            color = COLOR_HEADING_BG # Blue for information

        body = ttk.Frame(self, padding="20 15 20 15")
        
        # Show the Icon/Symbol
        ttk.Label(body, text=icon_char, 
                  foreground=color, 
                  background=COLOR_DARK_BLUE, 
                  font=('Arial', 24, 'bold')).pack(pady=5)
        
        # Show the Message
        ttk.Label(body, text=message, 
                  font=('Arial', 10), 
                  justify=tk.CENTER).pack(pady=10)

        body.pack(padx=10, pady=10)
        self.buttonbox() # Add the OK button
        self.show()

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=12, command=self.cancel, default="active")
        ok_button.pack(padx=10, pady=10)
        self.bind("<Return>", self.cancel) # Press Enter to close
        self.bind("<Escape>", self.cancel) # Press Escape to close
        box.pack(pady=5)

    def cancel(self, event=None):
        self.result = True # Save that the user saw the message
        super().cancel(event)

# This is a pop-up box for asking Yes/No questions
class ConfirmationDialog(BaseDialog):
    """This is the pop-up box for asking 'Are you sure?'"""
    def __init__(self, parent, title, message):
        super().__init__(parent, title)
        self.result = False # The default answer is No

        body = ttk.Frame(self, padding="20 15 20 15")
        
        # Show the Question Mark Icon
        ttk.Label(body, text="❓", 
                  foreground=COLOR_HEADING_BG, 
                  background=COLOR_DARK_BLUE, 
                  font=('Arial', 24, 'bold')).pack(pady=5)
        
        # Show the Question Message
        ttk.Label(body, text=message, 
                  font=('Arial', 10, 'bold'), 
                  justify=tk.CENTER).pack(pady=10)

        body.pack(padx=10, pady=10)
        self.buttonbox() # Add the Yes/No buttons
        self.show()

    def buttonbox(self):
        box = ttk.Frame(self)
        
        # Yes Button
        yes_button = ttk.Button(box, text="Yes", width=12, command=self.on_yes, default="active")
        yes_button.pack(side="left", padx=10, pady=10)
        
        # No Button
        no_button = ttk.Button(box, text="No", width=12, command=self.on_no)
        no_button.pack(side="left", padx=10, pady=10)

        self.bind("<Return>", self.on_yes) # Enter key presses Yes
        self.bind("<Escape>", self.on_no) # Escape key presses No
        box.pack(pady=5)

    def on_yes(self, event=None):
        self.result = True # Set the answer to True
        self.cancel()
        
    def on_no(self, event=None):
        self.result = False # Set the answer to False
        self.cancel()
        
    def cancel(self, event=None):
        super().cancel(event)


#Custom Pop-up Box for Adding a Student
class AddStudentDialog(BaseDialog):
    def __init__(self, parent, title):
        super().__init__(parent, title)
        
        body = ttk.Frame(self, padding="15 10 15 10")
        self.initial_focus = self.body(body) # Build the input fields
        body.pack(padx=10, pady=10)
        self.buttonbox() # Add the buttons

        if not self.initial_focus:
            self.initial_focus = self
        self.initial_focus.focus_set()
        
        self.show()

    def body(self, master):
        """This makes all the input fields for the student info."""
        ttk.Label(master, text="Student Code (4 digits, required):", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.code_entry = ttk.Entry(master, width=35)
        self.code_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="Student Name (Full Name):", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.name_entry = ttk.Entry(master, width=35)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Get the mark for Assessment 1
        ttk.Label(master, text="Assessment 1 Mark (max 20):", anchor="w").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.c1_entry = ttk.Entry(master, width=35)
        self.c1_entry.grid(row=2, column=1, padx=5, pady=5)

        # Get the mark for Assessment 2
        ttk.Label(master, text="Assessment 2 Mark (max 20):", anchor="w").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.c2_entry = ttk.Entry(master, width=35)
        self.c2_entry.grid(row=3, column=1, padx=5, pady=5)

        # Get the mark for Assessment 3
        ttk.Label(master, text="Assessment 3 Mark (max 20):", anchor="w").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.c3_entry = ttk.Entry(master, width=35)
        self.c3_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(master, text="Examination Mark (max 100):", anchor="w").grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.Final_entry = ttk.Entry(master, width=35)
        self.Final_entry.grid(row=5, column=1, padx=5, pady=5)
        
        self.exam_entry = self.Final_entry
        return self.code_entry 

    def buttonbox(self):
        """Add the OK and Cancel buttons."""
        box = ttk.Frame(self)

        w = ttk.Button(box, text="Add Student", width=12, command=self.ok, default="active")
        w.pack(side="left", padx=10, pady=10)
        w = ttk.Button(box, text="Cancel", width=12, command=self.cancel)
        w.pack(side="left", padx=10, pady=10)

        self.bind("<Return>", self.ok) # Enter key presses Add Student
        self.bind("<Escape>", self.cancel) # Escape key presses Cancel

        box.pack(pady=5)

    def validate(self):
        # 1. First, grab all the text the user typed in
        code_str = self.code_entry.get().strip()
        name_str = self.name_entry.get().strip()
        A1_str = self.c1_entry.get().strip()
        A2_str = self.c2_entry.get().strip()
        A3_str = self.c3_entry.get().strip()
        Final_str = self.Final_entry.get().strip() # This is the exam mark

        # Check if the code or name boxes are empty
        if not code_str or not name_str:
            MessageDialog(self, "Validation Error", "You must fill in the Student Code and Name boxes.", type='error')
            return False
            
        # Check if the code is 4 numbers
        if len(code_str) != 4 or not code_str.isdigit():
            MessageDialog(self, "Validation Error", "The Student Code has to be exactly 4 numbers.", type='error')
            return False

        # This list holds all the mark boxes we need to check
        marks_to_check = [
            (A1_str, 20, "Assessment 1"), 
            (A2_str, 20, "Assessment 2"), 
            (A3_str, 20, "Assessment 3"), 
            (Final_str, 100, "Exam Mark")
        ]
        
        self.validated_marks = []
        
        # Loop through each mark to make sure it's a valid number
        for mark_str, max_val, name in marks_to_check:
            try:
                mark = int(mark_str)
                # Check if the mark is between 0 and the max value
                if 0 <= mark <= max_val:
                    self.validated_marks.append(mark)
                else:
                    MessageDialog(self, "Validation Error", f"'{name}' must be a number between 0 and {max_val}.", type='error')
                    return False
            except ValueError:
                # If the user typed letters instead of numbers
                MessageDialog(self, "Validation Error", f"'{name}' must be a whole number.", type='error')
                return False

        # If everything passes, save the data to send back
        self.data_out = [
            code_str, 
            name_str, 
            *self.validated_marks
        ]
        return True # It passed all the checks

    def apply(self):
        self.result = self.data_out # Set the result to the student info


#Custom Pop-up for Searching 
class SearchDialog(BaseDialog):
    def __init__(self, parent, title, prompt):
        super().__init__(parent, title)

        body = ttk.Frame(self, padding="15 10 15 10")
        # Ask the user what to search for
        ttk.Label(body, text=prompt, anchor="w", font=('Arial', 10)).pack(padx=5, pady=5, anchor='w') 
        
        self.search_entry = ttk.Entry(body, width=40)
        self.search_entry.pack(padx=5, pady=5)
        self.initial_focus = self.search_entry

        body.pack(padx=10, pady=10)
        self.buttonbox()
        self.initial_focus.focus_set()
        self.show()

    def buttonbox(self):
        box = ttk.Frame(self)
        ttk.Button(box, text="Search/Find", width=12, command=self.ok, default="active").pack(side="left", padx=10, pady=10)
        ttk.Button(box, text="Cancel", width=12, command=self.cancel).pack(side="left", padx=10, pady=10)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack(pady=5)

    def ok(self, event=None):
        search_term = self.search_entry.get().strip()
        if not search_term:
            # Tell the user they need to type something
            MessageDialog(self, "Input Required", "You must enter a student code or name.", type='warning')
            return
        self.result = search_term # Save the thing they searched for
        self.cancel()


#Custom Pop-up for Choosing Update Field
class UpdateChoiceDialog(BaseDialog):
    def __init__(self, parent, student_name):
        super().__init__(parent, f"Update Record for {student_name}")
        self.choice_var = tk.IntVar(self)
        self.choice_var.set(0) # Start with nothing selected

        body = ttk.Frame(self, padding="15 10 15 10")
        ttk.Label(body, text=f"What do you want to change for {student_name}?", font=('Arial', 10, 'bold')).pack(pady=10)

        # List all the options the user can change
        options = [
            ("1: Update Name", 1),
            ("2: Assessment Mark 1 (max 20)", 2),
            ("3: Assessment Mark 2 (max 20)", 3),
            ("4: Assessment Mark 3 (max 20)", 4),
            ("5: Examination Mark (max 100)", 5)
        ]
        
        # Make a radio button for each option
        for text, value in options:
            ttk.Radiobutton(body, text=text, variable=self.choice_var, value=value, 
                            command=self.set_focus_ok).pack(anchor='w', padx=5, pady=2)

        body.pack(padx=10, pady=10)
        self.buttonbox()
        
        self.initial_focus = body
        self.initial_focus.focus_set()

        self.show()

    def set_focus_ok(self):
        # Move the focus to the Select button when an option is clicked
        self.ok_button.focus_set()

    def buttonbox(self):
        box = ttk.Frame(self)
        self.ok_button = ttk.Button(box, text="Select", width=12, command=self.ok, default="active")
        self.ok_button.pack(side="left", padx=10, pady=10)
        ttk.Button(box, text="Cancel", width=12, command=self.cancel).pack(side="left", padx=10, pady=10)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack(pady=5)

    def ok(self, event=None):
        if self.choice_var.get() == 0:
            # Tell the user they must pick one
            MessageDialog(self, "Selection Required", "Please click on a field you want to change.", type='warning')
            return
        self.result = self.choice_var.get() # Save the number of the choice
        self.cancel()


# --- 4. Custom Pop-up for Mark Input ---
class MarkInputDialog(BaseDialog):
    def __init__(self, parent, field_name, max_val):
        super().__init__(parent, f"Update Mark: {field_name}")
        self.max_val = max_val # The biggest number allowed for this mark
        self.field_name = field_name

        body = ttk.Frame(self, padding="15 10 15 10")
        
        # Ask the user for the new mark
        ttk.Label(body, text=f"Enter NEW mark for {field_name} (max {max_val}):", 
                  font=('Arial', 10)).pack(padx=5, pady=5, anchor='w')
        
        self.mark_entry = ttk.Entry(body, width=40)
        self.mark_entry.pack(padx=5, pady=5)
        self.initial_focus = self.mark_entry

        body.pack(padx=10, pady=10)
        self.buttonbox()
        self.initial_focus.focus_set()
        self.show()

    def buttonbox(self):
        box = ttk.Frame(self)
        ttk.Button(box, text="Set Mark", width=12, command=self.ok, default="active").pack(side="left", padx=10, pady=10)
        ttk.Button(box, text="Cancel", width=12, command=self.cancel).pack(side="left", padx=10, pady=10)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack(pady=5)

    def ok(self, event=None):
        mark_str = self.mark_entry.get().strip()
        
        if not mark_str:
            self.cancel() # If they didn't type anything, just close the box
            return

        try:
            mark = int(mark_str)
            # Check if the mark is good 
            if 0 <= mark <= self.max_val:
                self.result = mark
                self.cancel()
            else:
                # If the number is too big or too small
                MessageDialog(self, "Validation Error", f"Mark must be a whole number between 0 and {self.max_val}!", type='warning')
        except ValueError:
            # If they typed letters instead of numbers
            MessageDialog(self, "Validation Error", "Please enter a whole number!", type='warning')


#Custom Pop-up for Text/Name Input
class TextInputDialog(BaseDialog):
    def __init__(self, parent, title, prompt, initial_value=""):
        super().__init__(parent, title)
        
        body = ttk.Frame(self, padding="15 10 15 10")
        
        ttk.Label(body, text=prompt, 
                  font=('Arial', 10)).pack(padx=5, pady=5, anchor='w')
        
        self.text_entry = ttk.Entry(body, width=40)
        self.text_entry.insert(0, initial_value) # Put the old name in the box
        self.text_entry.pack(padx=5, pady=5)
        self.initial_focus = self.text_entry

        body.pack(padx=10, pady=10)
        self.buttonbox()
        self.initial_focus.focus_set()
        self.show()

    def buttonbox(self):
        box = ttk.Frame(self)
        ttk.Button(box, text="Set Name", width=12, command=self.ok, default="active").pack(side="left", padx=10, pady=10)
        ttk.Button(box, text="Cancel", width=12, command=self.cancel).pack(side="left", padx=10, pady=10)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack(pady=5)

    def ok(self, event=None):
        text_str = self.text_entry.get().strip()
        
        if not text_str:
            # Tell the user they need to type something
            MessageDialog(self, "Input Required", "Please enter a name.", type='warning')
            return

        self.result = text_str # Save the new name
        self.cancel()

#Custom Pop-up for Save Success
class SaveSuccessDialog(BaseDialog):
    """This pop-up says 'yay, it saved correctly'."""
    def __init__(self, parent):
        super().__init__(parent, "Save Successful")

        body = ttk.Frame(self, padding="20 15 20 15")
        
        # This is the big success message
        ttk.Label(body, text="✅ Data Saved Successfully!", 
                  foreground="#28a745", # Green color
                  background=COLOR_DARK_BLUE, 
                  font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(body, text="All changes have been safely written to studentMarks.txt.", 
                  font=('Arial', 10)).pack(pady=5)

        body.pack(padx=10, pady=10)
        self.buttonbox()
        self.show()

    def buttonbox(self):
        box = ttk.Frame(self)
        # Just one OK button
        ok_button = ttk.Button(box, text="OK", width=12, command=self.ok, default="active")
        ok_button.pack(padx=10, pady=10)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok) 
        box.pack(pady=5)


#The Main Application Class
class StudentManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Student Manager") # The title of the main window
        master.geometry("1000x650") # Set the starting size of the window
        master.config(bg=COLOR_DARK_BLUE) # Set the main background color

        self.student_data_list = [] # This list will hold all the student info
        self._load_data_from_file() # Load the data when the program starts

        #Logo Area
        logo_frame = tk.Frame(master, width=150, height=80, bg=COLOR_DARK_BLUE)
        logo_frame.grid(row=0, column=0, sticky='nw', padx=10, pady=10)
        logo_frame.grid_propagate(False) # Stop the frame from changing size

        # This is the label that acts like a logo
        self.logo_placeholder = tk.Label(logo_frame, 
                                     text="     STUDENT\n     MANAGER", # The text for the logo
                                     fg="#FFFFFF", 
                                     bg=COLOR_DARK_BLUE, 
                                     font=("Arial", 15, "bold"),
                                     relief=tk.FLAT,
                                     anchor="center")
        # Make the label fill up the whole logo space
        self.logo_placeholder.pack(expand=True, fill='both')

        # --- Heading Bar (Top Right) ---
        self.heading_frame = tk.Frame(master, height=80, bg=COLOR_HEADING_BG)
        self.heading_frame.grid(row=0, column=1, sticky='new', padx=10, pady=10)
        self.heading_frame.grid_columnconfigure(0, weight=1) # Make sure the column can grow
        self.heading_frame.grid_propagate(False)

        self.heading_label = tk.Label(self.heading_frame,
                                          text="ALL STUDENT RECORDS", # What the label says at the top
                                          fg=COLOR_TEXT_PRIMARY,
                                          bg=COLOR_HEADING_BG,
                                          font=("Arial", 18, "bold")) 
        self.heading_label.pack(expand=True, padx=10, pady=10)
        
        #Main Layout Grid Setup
        master.grid_rowconfigure(1, weight=1) 
        master.grid_columnconfigure(1, weight=1) 

        #Button Sidebar 
        self.button_frame = tk.Frame(master, width=150, bg=COLOR_DARK_BLUE, bd=1, relief=tk.RIDGE)
        self.button_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))
        self.button_frame.grid_propagate(False)

        #Content Area 
        self._setup_content_area(master)

        # Making the Menu Buttons
        self._create_professional_buttons()
        
        # Show all the data when the app first loads
        self._view_all_records()
        
    def _quit_app(self):
        """This function asks the user if they really want to close the app."""
        # Use the custom pop-up box to ask Yes/No
        dialog = ConfirmationDialog(self.master, "Confirm Exit", "Are you sure you want to quit? Any unsaved changes will be lost!")
        if dialog.result: # If the user clicked Yes
            self.master.quit()

    def _create_professional_buttons(self):
        #This function makes all the buttons on the left sidebar

        def create_graphic_button(text, command, row, btn_color="#4F79A1", text_color="white"):  
            #This little function makes one button with a cool, flat look 
            # The color when the mouse is over the button
            active_bg_color = COLOR_HEADING_BG
            
            btn = tk.Button(self.button_frame, 
                            text=text, 
                            command=command, 
                            width=15, 
                            pady=10, 
                            bg=btn_color,
                            fg=text_color, 
                            relief=tk.FLAT, # Flat look
                            font=("Arial", 10, "bold"),
                            activebackground=active_bg_color,
                            activeforeground=COLOR_TEXT_PRIMARY)
            btn.grid(row=row, column=0, padx=10, pady=5, sticky='ew')
            
            # Make the button look raised a bit when the mouse hovers over it
            btn.bind("<Enter>", lambda e: e.widget.config(relief=tk.RAISED))
            btn.bind("<Leave>", lambda e: e.widget.config(relief=tk.FLAT))
            return btn
            
        # Make the standard viewing buttons
        self.btn_all = create_graphic_button("View All Records", self._view_all_records, 0)
        self.btn_one = create_graphic_button("Find Student", self._view_individual, 1)
        self.btn_high = create_graphic_button("Highest Scorer", self._show_highest, 3)
        self.btn_low = create_graphic_button("Lowest Scorer", self._show_lowest, 4)
        
        # A little space between button groups
        tk.Frame(self.button_frame, height=5, bg=COLOR_DARK_BLUE).grid(row=5, column=0)
        
        # Make the action buttons 
        self.btn_add = create_graphic_button("Add New Student", self._add_student, 6, btn_color="#7823a5", text_color="white") 
        self.btn_update = create_graphic_button("Update Record", self._update_record, 7, btn_color="#1E9F1E", text_color="white") 
        self.btn_delete = create_graphic_button("Delete Record", self._delete_student, 8, btn_color="#faab00", text_color="white") 
        
        # Save and Quit buttons
        self.btn_save = create_graphic_button("Save Changes", self._save_data_to_file, 10, btn_color=COLOR_HEADING_BG, text_color="white") 
        self.btn_quit = create_graphic_button("QUIT", self._quit_app, 11, btn_color="#003D6C", text_color="white") 


    def _setup_content_area(self, master):
        """This sets up the table (Treeview) and the message box (Status)."""
        
        self.content_frame = tk.Frame(master, bg=COLOR_DARK_BLUE)
        self.content_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=(0, 10))
        self.content_frame.grid_rowconfigure(0, weight=0) # Row 0 is for the sort buttons 
        self.content_frame.grid_rowconfigure(1, weight=1) # Row 1 is for the big table 
        self.content_frame.grid_rowconfigure(2, weight=0) # Row 2 is for the message box 
        self.content_frame.grid_columnconfigure(0, weight=1) # Column 0 can grow
        
        # This frame holds the sort buttons
        self.sort_frame = tk.Frame(self.content_frame, bg=COLOR_DARK_BLUE)
        self.sort_frame.grid(row=0, column=0, sticky='ew', columnspan=2, pady=(0, 5))
        
        # 1. Setup the style for the table to make it look clean
        style = ttk.Style()
        style.theme_use("clam") 
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background=COLOR_HEADING_BG, foreground=COLOR_TEXT_PRIMARY)
        style.map("Treeview.Heading", background=[('active', COLOR_HEADING_BG)])
        style.configure("Treeview", background=COLOR_LIGHT_BLUE, foreground=COLOR_TEXT_SECONDARY, fieldbackground=COLOR_LIGHT_BLUE, rowheight=25, borderwidth=0)
        style.map("Treeview", background=[('selected', COLOR_HEADING_BG)], foreground=[('selected', COLOR_TEXT_PRIMARY)])
        
        # 2. Tell the table what columns it has
        columns = ('code', 'name', 'A1', 'A2', 'A3', 'Final', 'total', 'percent', 'grade')
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', style="Treeview")
        
        # 3. Set the column titles and how wide they are
        self.tree.heading('code', text='Code', anchor='center')
        self.tree.heading('name', text='Name', anchor='w')
        self.tree.heading('A1', text='A1', anchor='center')
        self.tree.heading('A2', text='A2', anchor='center')
        self.tree.heading('A3', text='A3', anchor='center')
        self.tree.heading('Final', text='Final', anchor='center')
        self.tree.heading('total', text='Total', anchor='center')
        self.tree.heading('percent', text='%', anchor='center') 
        self.tree.heading('grade', text='Grade', anchor='center')

        self.tree.column('code', width=80, stretch=tk.NO, anchor='center')
        self.tree.column('name', width=150, anchor='w')
        self.tree.column('A1', width=60, stretch=tk.NO, anchor='center') 
        self.tree.column('A2', width=60, stretch=tk.NO, anchor='center') 
        self.tree.column('A3', width=60, stretch=tk.NO, anchor='center') 
        self.tree.column('Final', width=80, anchor='center')
        self.tree.column('total', width=80, anchor='center')
        self.tree.column('percent', width=80, anchor='center')
        self.tree.column('grade', width=80, stretch=tk.NO, anchor='center')
        
        # 4. Add the scrollbar for the table
        vsb = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # 5. Put the table and the scrollbar in the correct spot
        self.tree.grid(row=1, column=0, sticky='nsew')
        vsb.grid(row=1, column=1, sticky='ns')

        # 6. This is the box for messages and summaries
        self.status_text = tk.Text(self.content_frame, height=8, wrap='word', bg=COLOR_HEADING_BG, fg=COLOR_TEXT_PRIMARY, font=("Arial", 10), relief=tk.FLAT) 
        self.status_text.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        self.status_text.insert(tk.END, "Summary and individual record details will appear here...")
        self.status_text.config(state=tk.DISABLED) 

    # This function makes the ascending and descending sort buttons
    def _create_sort_buttons(self):
        """This makes the sort buttons for the 'View All' screen."""
        # Clear out any old buttons first
        for widget in self.sort_frame.winfo_children():
            widget.destroy()

        # Add a little title next to the buttons
        ttk.Label(self.sort_frame, text="Sort By Final Percentage:", 
                  background=COLOR_DARK_BLUE, 
                  foreground=COLOR_TEXT_PRIMARY, 
                  font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(5, 10), pady=2)

        # Make the Ascending button (lowest score first)
        ttk.Button(self.sort_frame, 
                   text="Ascending ▲", 
                   command=lambda: self._sort_records(reverse=False), 
                   width=15, 
                   style='TButton').pack(side=tk.LEFT, padx=5, pady=2)

        # Make the Descending button (highest score first)
        ttk.Button(self.sort_frame, 
                   text="Descending ▼", 
                   command=lambda: self._sort_records(reverse=True), 
                   width=15, 
                   style='TButton').pack(side=tk.LEFT, padx=5, pady=2)


    #FUNCTIONS THAT READ AND WRITE THE DATA FILE
    
    def _load_data_from_file(self):
        """This function reads the student data from the text file."""
        self.student_data_list = [] # Start with an empty list
        try:
            # Check if the file is missing
            if not os.path.exists(FILE_PATH):
                # If it's missing, use some fake student data so the app still works
                placeholder_data = [
                    ['1345', 'John Curry', 8, 15, 7, 45],
                    ['2345', 'Sam Sturtivant', 14, 15, 14, 77],
                    ['9876', 'Lee Scott', 17, 11, 16, 99],
                    ['3724', 'Matt Thompson', 19, 11, 15, 81],
                    ['1212', 'Ron Herrema', 14, 17, 18, 66],
                    ['8439', 'Jake Hobbs', 10, 11, 10, 43],
                    ['2344', 'Jo Hyde', 6, 15, 10, 55],
                    ['9384', 'Gareth Southgate', 5, 6, 8, 33],
                    ['8327', 'Alan Shearer', 20, 20, 20, 100],
                    ['2683', 'Les Ferdinand', 15, 17, 18, 92]
                ]
                self.student_data_list = placeholder_data
                # Tell the user we are using fake data
                MessageDialog(self.master, "File Missing", "The studentMarks.txt file was not found. Using sample data instead.", type='warning')
                return
                
            with open(FILE_PATH, 'r') as f:
                lines = f.readlines()
                if not lines or len(lines) < 2: # Check if the file is basically empty
                    return 
                
                # Skip the first line, which is just the count of students
                for line in lines[1:]: 
                    clean_line = line.strip()
                    if not clean_line: continue # Skip empty lines
                    
                    parts = clean_line.split(',')
                    if len(parts) == 6:
                        try:
                            student_code = parts[0].strip()
                            name = parts[1].strip()
                            A1 = int(parts[2].strip())
                            A2 = int(parts[3].strip())
                            A3 = int(parts[4].strip())
                            Final = int(parts[5].strip())
                            
                            self.student_data_list.append([student_code, name, A1, A2, A3, Final])
                        except ValueError:
                            # If one of the marks wasn't a number
                            MessageDialog(self.master, "Data Error", f"Skipped bad data line with invalid marks: {clean_line}", type='warning')
                            
        except Exception as e:
            # If something really bad happened while opening the file
            MessageDialog(self.master, "File Read Error", f"Something went wrong while reading the file: {e}", type='error')

    def _save_data_to_file(self):
        """This function writes all the current student data back to the text file."""
        try:
            # Make sure the folder for the file exists
            os.makedirs(os.path.dirname(FILE_PATH) or '.', exist_ok=True)
            
            with open(FILE_PATH, 'w', newline='') as f:
                # Write the total number of students first
                f.write(str(len(self.student_data_list)) + '\n')
                
                writer = csv.writer(f)
                # Go through the list and write each student's line
                for student in self.student_data_list:
                    writer.writerow(student) 
            
            # Show the success pop-up box
            SaveSuccessDialog(self.master)

        except Exception as e:
            # If the file couldn't be saved for some reason
            MessageDialog(self.master, "Save Error", f"The file couldn't be saved! Error: {e}", type='error')

    #FUNCTIONS THAT DO MATH AND FORMATTING
    
    def _calculate_results(self, student_record):
        """This takes a student's marks and figures out their total score, percent, and letter grade."""
        # The list is: [Code, Name, A1, A2, A3, Final]
        A1 = student_record[2]
        A2 = student_record[3]
        A3 = student_record[4]
        Final = student_record[5]
        
        coursework_total = A1 + A2 + A3
        overall_total = coursework_total + Final # Add course marks and exam mark
        
        # Calculate the final percentage
        overall_percent = (overall_total / MAX_TOTAL_MARKS) * 100
        
        # Figure out the letter grade
        grade = 'F'
        if overall_percent >= 70: grade = 'A'
        elif overall_percent >= 60: grade = 'B'
        elif overall_percent >= 50: grade = 'C'
        elif overall_percent >= 40: grade = 'D'
            
        # Send back a dictionary of all the results
        return {
            'code': student_record[0],
            'name': student_record[1],
            'A1': A1,
            'A2': A2,
            'A3': A3,
            'Final': Final,
            'total': overall_total,
            'percent': overall_percent,
            'grade': grade
        }
        
    def _insert_student_into_tree(self, results):
        """This function puts one student's results into the table."""
        self.tree.insert('', tk.END, values=(
            results['code'],
            results['name'],
            f"{results['A1']}", 
            f"{results['A2']}", 
            f"{results['A3']}", 
            f"{results['Final']}",
            f"{results['total']}",
            f"{results['percent']:.2f}",
            results['grade']
        ))

    def _clear_output(self, title):
        """This function clears the table and the message box, and updates the title at the top."""
        self.heading_label.config(text=title)
        
        # Clear all the rows from the table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Clear the message box at the bottom
        self.status_text.config(state=tk.NORMAL) # Turn on editing
        self.status_text.delete(1.0, tk.END) # Delete all the text
        self.status_text.config(state=tk.DISABLED) # Turn off editing


    #THE MAIN APP BUTTON FUNCTIONS 
    
    #View all student records 
    def _view_all_records(self):
        """This shows every student in the main table and a summary below."""
        self._clear_output("ALL STUDENT RECORDS") # Clear everything and set the title
        
        # Make sure the sort buttons are there
        self._create_sort_buttons()

        total_percent_sum = 0
        
        if not self.student_data_list:
            self._write_status("The student list is totally empty! Use 'Add New Student' to put someone in.")
            return

        # Go through every student
        for student in self.student_data_list:
            results = self._calculate_results(student)
            self._insert_student_into_tree(results)
            total_percent_sum += results['percent']
            
        # Calculate the summary stuff
        num_students = len(self.student_data_list)
        average_percent = total_percent_sum / num_students if num_students > 0 else 0

        # Write the class summary in the message box
        summary = (
            f"--- CLASS SUMMARY ---\n"
            f"Total Students in Class: {num_students}\n"
            f"Average Percentage Mark: {average_percent:.2f}%\n"
            f"Maximum Total Mark Possible: {MAX_TOTAL_MARKS}\n"
            f"---------------------"
        )
        self._write_status(summary)
        

    #View individual student record
    def _view_individual(self):
        """This lets you search for one student and shows their details."""
        # Ask the user for the name or code
        dialog = SearchDialog(self.master, "Find Student Record", 
                              "Type in the Student Name OR Student Code to see their results:")
        search_term = dialog.result
        
        if not search_term: return # Stop if the user cancelled 

        self._clear_output(f"VIEWING INDIVIDUAL RECORD: '{search_term}'")
        
        # Remove the sort buttons because we are only looking at one student
        for widget in self.sort_frame.winfo_children():
            widget.destroy()
            
        found_student = None

        # Look for the student
        for student in self.student_data_list:
            # Check by Code OR Name (ignoring capital letters for the name)
            if student[0] == search_term or student[1].lower() == search_term.lower():
                found_student = student
                break
        
        if found_student:
            results = self._calculate_results(found_student)
            
            # Create a nice message with all the details
            output = (
                f"RECORD FOUND for {results['name']} (Code: {results['code']})\n"
                f"Assessment Marks: A1={found_student[2]}, A2={found_student[3]}, A3={found_student[4]}\n"
                f"Assessment Total: {results['A1']+results['A2']+results['A3']}/60 | Exam Mark: {results['Final']}/100\n"
                f"Overall Total: {results['total']}/{MAX_TOTAL_MARKS} | Final Percentage: {results['percent']:.2f}% | Final Grade: {results['grade']}"
            )
            self._write_status(output)
            # Show the one student in the table too
            self._insert_student_into_tree(results)
        else:
            self._write_status(f"Error: Couldn't find a student named or coded '{search_term}'.")


    #Highest/Lowest Score
    def _find_extreme_student(self, is_highest):
        """This helper function finds the student with the best or worst score."""
        action_text = "HIGHEST" if is_highest else "LOWEST"
        self._clear_output(f"STUDENT WITH {action_text} OVERALL SCORE")
        
        # Remove the sort buttons
        for widget in self.sort_frame.winfo_children():
            widget.destroy()

        if not self.student_data_list:
            self._write_status("The student list is empty!")
            return

        best_student = None
        # Start with a score that is impossible to beat for the best/worst
        best_score = -1 if is_highest else MAX_TOTAL_MARKS + 1 

        # Go through all the students
        for student in self.student_data_list:
            results = self._calculate_results(student)
            score = results['total']
            
            # Check if this student is the new best/worst
            if (is_highest and score > best_score) or (not is_highest and score < best_score):
                best_score = score
                best_student = results

        if best_student:
            # Write the result in the message box
            output = (
                f"FOUND {action_text} SCORER: {best_student['name']} (Code: {best_student['code']})\n"
                f"Overall Score: {best_student['total']}/{MAX_TOTAL_MARKS} | Final Percentage: {best_student['percent']:.2f}% | Final Grade: {best_student['grade']}\n"
                f"Result displayed in the table above."
            )
            self._write_status(output)
            # Put the result in the table too
            self._insert_student_into_tree(best_student)


    def _show_highest(self):
        self._find_extreme_student(is_highest=True) # Find the highest score

    def _show_lowest(self):
        self._find_extreme_student(is_highest=False) # Find the lowest score


    #Sort student records
    def _sort_records(self, reverse):
        """This function sorts the students by their final percentage and shows the new list."""
        reverse_sort = reverse # True means descending (highest first), False means ascending (lowest first)
        
        students_with_percent = []
        # Calculate the percentage for everyone and save it with their data
        for student in self.student_data_list:
            results = self._calculate_results(student)
            # Save it as a pair: (percentage, raw data)
            students_with_percent.append((results['percent'], student))
            
        # Sort the list based on the percentage
        students_with_percent.sort(key=lambda x: x[0], reverse=reverse_sort)
        
        # Clear the screen and update the title
        self._clear_output(f"RECORDS SORTED BY PERCENTAGE ({'DESCENDING' if reverse_sort else 'ASCENDING'})")
        
        # Put the sort buttons back
        self._create_sort_buttons() 
        
        # Put all the students back into the table in the new sorted order
        for percent, student_data in students_with_percent:
            results = self._calculate_results(student_data)
            self._insert_student_into_tree(results)
        
        self._write_status(f"Table updated! Showing {len(self.student_data_list)} students sorted by final percentage.")


    #Add a student record
    def _add_student(self):
        """This opens the pop-up box to get the new student's information."""
        
        dialog = AddStudentDialog(self.master, "Add New Student Record")
        
        new_record = dialog.result # Get the info the user typed in

        if new_record:
            # Check if that student code is already in the list
            if any(new_record[0] == student[0] for student in self.student_data_list):
                 # Tell the user if the code is a duplicate
                 MessageDialog(self.master, "Code Exists", f"Student code {new_record[0]} already exists! Pick a new one.", type='warning')
                 return

            self.student_data_list.append(new_record) # Add the new student to the list
            
            self._write_status(f"YAY! You added a new student: {new_record[1]}. Make sure to click 'Save Changes'!")
            self._view_all_records() # Refresh the table to show the new student
        else:
            self._write_status("Adding a new record was cancelled by the user.")


    # --- 7. Delete a student record (DELETE RECORD) ---
    def _delete_student(self):
        """This lets you find a student and remove them from the list."""
        # Ask the user what to search for
        dialog = SearchDialog(self.master, "Delete Record", 
                              "Type in the Student Name OR Student Code to DELETE:")
        search_term = dialog.result
        
        if not search_term: return # Stop if the user cancelled

        index_to_delete = -1
        deleted_name = ""

        # Find the student's spot in the list
        for i, student in enumerate(self.student_data_list):
            if student[0] == search_term or student[1].lower() == search_term.lower():
                index_to_delete = i
                deleted_name = student[1]
                break
        
        if index_to_delete != -1:
            # Ask the user one more time if they are sure they want to delete
            confirm_dialog = ConfirmationDialog(self.master, "Confirm Delete", f"Are you sure you want to PERMANENTLY DELETE {deleted_name}'s record?")
            if confirm_dialog.result:
                self.student_data_list.pop(index_to_delete) # Remove the student from the list
                self._write_status(f"Record for {deleted_name} has been deleted. Don't forget to click 'Save Changes'!")
                self._view_all_records() # Refresh the table
            else:
                self._write_status(f"Did not delete {deleted_name}.")
        else:
            self._write_status(f"Couldn't find student '{search_term}' to delete.")


    # --- 8. Update a students record (UPDATE RECORD) ---
    def _update_record(self):
        """This lets the user change a student's name or marks."""
        # Ask the user what student to find
        dialog = SearchDialog(self.master, "Find Record to Update", 
                              "Type in the Student Name OR Student Code to UPDATE:")
        search_term = dialog.result

        if not search_term: return
        
        target_index = -1
        # Find the student's spot in the list
        for i, student in enumerate(self.student_data_list):
            if student[0] == search_term or student[1].lower() == search_term.lower():
                target_index = i
                break
        
        if target_index == -1:
            self._write_status(f"Couldn't find student '{search_term}' to update.")
            return

        student = self.student_data_list[target_index]
        current_name = student[1]
        
        # Ask the user what part of the record they want to change
        choice_dialog = UpdateChoiceDialog(self.master, current_name)
        choice = choice_dialog.result

        if choice is None:
             self._write_status("The update was cancelled.")
             return
        
        if choice == 1:
            # If they chose to update the name
            name_dialog = TextInputDialog(self.master, "Update Student Name", 
                                          f"Enter NEW name for {current_name}:", initial_value=current_name)
            new_name = name_dialog.result
            
            if new_name: 
                student[1] = new_name # Change the name in the list
                self._write_status(f"Student name changed to {new_name}! Remember to click 'Save Changes'!")
            else:
                self._write_status("The name update was cancelled or failed.")
            
        elif choice in [2, 3, 4, 5]:
            # If they chose to update a mark
            # The mark's spot in the list is the same as the choice number
            mark_index = choice + 0 
            # Set the max score (20 for assessment, 100 for final exam)
            max_val = 20 if choice < 5 else 100
            # Get the name of the mark (e.g., "Assessment 1")
            field_name = ["", "Name", "Assessment 1", "Assessment 2", "Assessment 3", "Final"][choice]
            
            # Open the box to get the new mark
            mark_dialog = MarkInputDialog(self.master, field_name, max_val)
            new_mark = mark_dialog.result

            if new_mark is not None:
                student[mark_index] = new_mark # Update the mark in the list
                self._write_status(f"Updated {field_name} for {student[1]} to {new_mark}! Remember to click 'Save Changes'!")
            else:
                self._write_status("The mark update was cancelled or failed.")
        
        else:
            self._write_status("Update cancelled.")
            return

        self._view_all_records() # Show the updated table

    #Utility to write to the Status Box
    def _write_status(self, text):
        """This function writes a message into the message box at the bottom."""
        self.status_text.config(state=tk.NORMAL) # Turn on editing
        self.status_text.delete(1.0, tk.END) # Clear old text
        self.status_text.insert(tk.END, text) # Put in the new text
        self.status_text.config(state=tk.DISABLED) # Turn off editing

#Start the whole program
if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(ICON_PATH) 
    app = StudentManagerApp(root)
    root.mainloop()