import tkinter as tk 
from tkinter import simpledialog, messagebox, ttk 
import os 
import csv



# this code was developed using the ideas from the following youtube channel: forcodecoder
#file path & placeholder data
file_path = "task_3(mandatory & extention)/studentmarks.txt" 
# adjusted path for icon to ensure consistency across the application and dialogs
icon_path = "task_3(mandatory & extention)/student.ico" 
max_total_marks = 160 # maximum possible score is 160

# themes color for the page
color_dark_blue = "#004aad" 
color_light_blue = "#e0e6f0" 
color_heading_bg = "#2b7eac"  
color_text_primary = "white" 
color_text_secondary = "black" 


#base dialog class for reusability
class BaseDialog(tk.Toplevel):
    # a reusable base for custom toplevel dialogs
    def __init__(self, parent, title):
        super().__init__(parent)
        self.transient(parent) 
        self.title(title) 
        self.parent = parent 
        self.result = None
        
        #set the dialog icon to match the main app
        try:
            self.iconbitmap(icon_path) # attempts to set the window icon
        except Exception:
            pass
        
        # set colors and style for the dialog
        self.config(bg=color_dark_blue) 
        self.style = ttk.Style()
        
        # consistent style setup for all dialogs
        self.style.configure('tframe', background=color_dark_blue) 
        self.style.configure('tlabel', background=color_dark_blue, foreground=color_text_primary, font=('arial', 10, 'bold')) 
        self.style.configure('tentry', fieldbackground=color_light_blue, foreground=color_text_secondary, font=('arial', 10))
        self.style.map('tbutton', 
                       background=[('active', color_heading_bg), ('!disabled', color_light_blue)],
                       foreground=[('active', color_text_primary), ('!disabled', color_text_secondary)]) 
        self.style.configure('tbutton', font=('arial', 10, 'bold'))
        self.style.configure('tradiobutton', background=color_dark_blue, foreground=color_text_primary, font=('arial', 10)) 

        
        # center the dialog on screen
        self.update_idletasks() 
        w = self.winfo_reqwidth() 
        h = self.winfo_reqheight() 
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height() 
        x = parent.winfo_rootx() + (parent_w // 2) - (w // 2)
        y = parent.winfo_rooty() + (parent_h // 2) - (h // 2) 
        self.geometry(f"+{x}+{y}") 
        self.resizable(False, False) 

    def show(self):
        # displays the dialog and makes it modal
        self.grab_set() 
        self.wait_window(self)

    def ok(self, event=None):
        if not self.validate():
            # if validation fails, stop
            return
        self.withdraw() 
        self.update_idletasks()
        try:
            self.apply() 
        finally:
            self.cancel()

    def cancel(self, event=None):
        #window closing
        self.parent.focus_set() 
        self.destroy() 

    def validate(self):
        return True 

    def apply(self):
        pass 


# warning dialog
class MessageDialog(BaseDialog):
    # custom modal dialog for showing simple messages, warnings, or errors
    def __init__(self, parent, title, message, type='info'):
        super().__init__(parent, title) # calls the base dialog constructor
        self.type = type
        self.message = message
        
        # set specific icon and color based on type
        if type == 'error':
            icon_char = "❌"
            color = "#dc3545" # red
        elif type == 'warning':
            icon_char = "⚠️"
            color = "#ffc107" # yellow/orange
        elif type == 'success':
            icon_char = "✅"
            color = "#28a745" # green
        else: # info
            icon_char = "ℹ️"
            color = color_heading_bg # blue

        body = ttk.Frame(self, padding="20 15 20 15") # creates the main frame for content
        
        # icon/symbol
        ttk.Label(body, text=icon_char, 
                  foreground=color, 
                  background=color_dark_blue, 
                  font=('arial', 24, 'bold')).pack(pady=5) # displays the icon
        
        # message
        ttk.Label(body, text=message, 
                  font=('arial', 10), 
                  justify=tk.center).pack(pady=10) # displays the message

        body.pack(padx=10, pady=10)
        self.buttonbox() # adds the ok button
        self.show() # displays the dialog

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="ok", width=12, command=self.cancel, default="active") # ok button
        ok_button.pack(padx=10, pady=10)
        self.bind("<return>", self.cancel) # bind enter key
        self.bind("<escape>", self.cancel) # bind escape key
        box.pack(pady=5)

    def cancel(self, event=None):
        self.result = True # confirms user has seen the message
        super().cancel(event) # calls base cancel

# --- new: confirmation dialog (yes/no) (replaces messagebox.askyesno) ---
class ConfirmationDialog(BaseDialog):
    # custom modal dialog for asking yes/no questions
    def __init__(self, parent, title, message):
        super().__init>(parent, title) # calls the base dialog constructor
        self.result = False # default result is no

        body = ttk.Frame(self, padding="20 15 20 15")
        
        # question icon
        ttk.Label(body, text="❓", 
                  foreground=color_heading_bg, 
                  background=color_dark_blue, 
                  font=('arial', 24, 'bold')).pack(pady=5) # displays question icon
        
        # message
        ttk.Label(body, text=message, 
                  font=('arial', 10, 'bold'), 
                  justify=tk.center).pack(pady=10) # displays the question

        body.pack(padx=10, pady=10)
        self.buttonbox() # adds the yes/no buttons
        self.show() # displays the dialog

    def buttonbox(self):
        box = ttk.Frame(self)
        
        # yes button
        yes_button = ttk.Button(box, text="yes", width=12, command=self.on_yes, default="active")
        yes_button.pack(side="left", padx=10, pady=10)
        
        # no button
        no_button = ttk.Button(box, text="no", width=12, command=self.on_no)
        no_button.pack(side="left", padx=10, pady=10)

        self.bind("<return>", self.on_yes) # bind enter to yes
        self.bind("<escape>", self.on_no) # bind escape to no
        box.pack(pady=5)

    def on_yes(self, event=None):
        self.result = True # sets result to true
        self.cancel() # closes the dialog
        
    def on_no(self, event=None):
        self.result = False # sets result to false
        self.cancel() # closes the dialog
        
    def cancel(self, event=None):
        super().cancel(event) # calls base cancel


# --- 1. custom dialog for adding a student ---
class AddStudentDialog(BaseDialog):
    def __init__(self, parent, title):
        super().__init__(parent, title)
        
        body = ttk.Frame(self, padding="15 10 15 10")
        self.initial_focus = self.body(body) # creates the form fields
        body.pack(padx=10, pady=10)
        self.buttonbox() # adds the buttons

        if not self.initial_focus:
            self.initial_focus = self
        self.initial_focus.focus_set() # sets focus to the first entry
        
        self.show()

    def body(self, master):
        # create the dialog body with form fields
        ttk.Label(master, text="student code (4 digits, required):", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.code_entry = ttk.Entry(master, width=35) # entry for student code
        self.code_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="student name (full name):", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.name_entry = ttk.Entry(master, width=35) # entry for student name
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        # updated: changed 'coursework' to 'assessment'
        ttk.Label(master, text="assessment 1 mark (max 20):", anchor="w").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.c1_entry = ttk.Entry(master, width=35) # entry for assessment 1
        self.c1_entry.grid(row=2, column=1, padx=5, pady=5)

        # updated: changed 'coursework' to 'assessment'
        ttk.Label(master, text="assessment 2 mark (max 20):", anchor="w").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.c2_entry = ttk.Entry(master, width=35) # entry for assessment 2
        self.c2_entry.grid(row=3, column=1, padx=5, pady=5)

        # updated: changed 'coursework' to 'assessment'
        ttk.Label(master, text="assessment 3 mark (max 20):", anchor="w").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.c3_entry = ttk.Entry(master, width=35) # entry for assessment 3
        self.c3_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(master, text="examination mark (max 100):", anchor="w").grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.final_entry = ttk.Entry(master, width=35) # entry for final exam mark
        self.final_entry.grid(row=5, column=1, padx=5, pady=5)
        
        self.exam_entry = self.final_entry # alias for clarity in validation

        return self.code_entry # initial focus is the code entry

    def buttonbox(self):
        # add standard button box: ok and cancel
        box = ttk.Frame(self)

        w = ttk.Button(box, text="add student", width=12, command=self.ok, default="active") # add student button
        w.pack(side="left", padx=10, pady=10)
        w = ttk.Button(box, text="cancel", width=12, command=self.cancel) # cancel button
        w.pack(side="left", padx=10, pady=10)

        self.bind("<return>", self.ok)
        self.bind("<escape>", self.cancel)

        box.pack(pady=5)

    def validate(self):
        # validation logic for all input fields
        # 1. get raw string values
        code_str = self.code_entry.get().strip()
        name_str = self.name_entry.get().strip()
        a1_str = self.c1_entry.get().strip()
        a2_str = self.c2_entry.get().strip()
        a3_str = self.c3_entry.get().strip()
        final_str = self.final_entry.get().strip()

        # simple checks for empty fields
        if not code_str or not name_str:
            # updated: replaced messagebox with custom messagedialog
            MessageDialog(self, "validation error", "student code and name fields cannot be empty.", type='error')
            return False
            
        # check code format
        if len(code_str) != 4 or not code_str.isdigit():
            # updated: replaced messagebox with custom messagedialog
            MessageDialog(self, "validation error", "student code must be exactly 4 digits.", type='error')
            return False

        # mark checks
        marks_to_check = [
            (a1_str, 20, "assessment 1"), # a1 max 20
            (a2_str, 20, "assessment 2"), # a2 max 20
            (a3_str, 20, "assessment 3"), # a3 max 20
            (final_str, 100, "exam mark") # exam max 100
        ]
        
        self.validated_marks = [] # list to hold valid integer marks
        
        for mark_str, max_val, name in marks_to_check:
            try:
                mark = int(mark_str)
                if 0 <= mark <= max_val:
                    self.validated_marks.append(mark) # mark is valid
                else:
                    # updated: replaced messagebox with custom messagedialog
                    MessageDialog(self, "validation error", f"'{name}' must be a number between 0 and {max_val}.", type='error')
                    return False
            except ValueError:
                # updated: replaced messagebox with custom messagedialog
                MessageDialog(self, "validation error", f"'{name}' must be a whole number.", type='error')
                return False

        # all validation passed
        self.data_out = [
            code_str, 
            name_str, 
            *self.validated_marks # unpacks the validated marks
        ]
        return True # return true if input is valid

    def apply(self):
        self.result = self.data_out # sets the dialog result


# --- 2. custom dialog for searching (view/delete/update) ---
class SearchDialog(BaseDialog):
    def __init__(self, parent, title, prompt):
        super().__init>(parent, title) # calls base dialog constructor

        body = ttk.Frame(self, padding="15 10 15 10")
        # use tlabel style but override font size
        ttk.Label(body, text=prompt, anchor="w", font=('arial', 10)).pack(padx=5, pady=5, anchor='w') # displays the search prompt
        
        self.search_entry = ttk.Entry(body, width=40) # entry field for search term
        self.search_entry.pack(padx=5, pady=5)
        self.initial_focus = self.search_entry

        body.pack(padx=10, pady=10)
        self.buttonbox() # adds buttons
        self.initial_focus.focus_set()
        self.show()

    def buttonbox(self):
        box = ttk.Frame(self)
        ttk.Button(box, text="search/find", width=12, command=self.ok, default="active").pack(side="left", padx=10, pady=10) # search button
        ttk.Button(box, text="cancel", width=12, command=self.cancel).pack(side="left", padx=10, pady=10) # cancel button
        self.bind("<return>", self.ok)
        self.bind("<escape>", self.cancel)
        box.pack(pady=5)

    def ok(self, event=None):
        search_term = self.search_entry.get().strip() # gets the search term
        if not search_term:
            # updated: replaced messagebox with custom messagedialog
            MessageDialog(self, "input required", "please enter a student code or name.", type='warning')
            return
        self.result = search_term # sets the result
        self.cancel()


# --- 3. custom dialog for choosing update field ---
class UpdateChoiceDialog(BaseDialog):
    def __init__(self, parent, student_name):
        super().__init>(parent, f"update record for {student_name}") # calls base dialog constructor
        self.choice_var = tk.intvar(self) # variable to store radio button choice
        self.choice_var.set(0) # default no selection

        body = ttk.Frame(self, padding="15 10 15 10")
        ttk.Label(body, text=f"what field do you want to change for {student_name}?", font=('arial', 10, 'bold')).pack(pady=10)

        # updated: changed 'coursework' to 'assessment'
        options = [
            ("1: update name", 1),
            ("2: assessment mark 1 (max 20)", 2),
            ("3: assessment mark 2 (max 20)", 3),
            ("4: assessment mark 3 (max 20)", 4),
            ("5: examination mark (max 100)", 5)
        ]
        
        for text, value in options:
            ttk.Radiobutton(body, text=text, variable=self.choice_var, value=value, 
                            command=self.set_focus_ok).pack(anchor='w', padx=5, pady=2) # creates radio buttons

        body.pack(padx=10, pady=10)
        self.buttonbox()
        
        self.initial_focus = body
        self.initial_focus.focus_set()

        self.show()

    def set_focus_ok(self):
        # sets focus to ok button when a radio button is selected
        self.ok_button.focus_set()

    def buttonbox(self):
        box = ttk.Frame(self)
        self.ok_button = ttk.Button(box, text="select", width=12, command=self.ok, default="active") # select button
        self.ok_button.pack(side="left", padx=10, pady=10)
        ttk.Button(box, text="cancel", width=12, command=self.cancel).pack(side="left", padx=10, pady=10) # cancel button
        self.bind("<return>", self.ok)
        self.bind("<escape>", self.cancel)
        box.pack(pady=5)

    def ok(self, event=None):
        if self.choice_var.get() == 0:
            # updated: replaced messagebox with custom messagedialog
            MessageDialog(self, "selection required", "please select a field to update.", type='warning')
            return
        self.result = self.choice_var.get() # sets the choice as the result
        self.cancel()


# --- 4. custom dialog for mark input ---
class MarkInputDialog(BaseDialog):
    def __init__(self, parent, field_name, max_val):
        super().__init>(parent, f"update mark: {field_name}") # calls base dialog constructor
        self.max_val = max_val
        self.field_name = field_name

        body = ttk.Frame(self, padding="15 10 15 10")
        
        ttk.Label(body, text=f"enter new mark for {field_name} (max {max_val}):", 
                  font=('arial', 10)).pack(padx=5, pady=5, anchor='w') # mark prompt
        
        self.mark_entry = ttk.Entry(body, width=40) # mark entry field
        self.mark_entry.pack(padx=5, pady=5)
        self.initial_focus = self.mark_entry

        body.pack(padx=10, pady=10)
        self.buttonbox()
        self.initial_focus.focus_set()
        self.show()

    def buttonbox(self):
        box = ttk.Frame(self)
        ttk.Button(box, text="set mark", width=12, command=self.ok, default="active").pack(side="left", padx=10, pady=10) # set mark button
        ttk.Button(box, text="cancel", width=12, command=self.cancel).pack(side="left", padx=10, pady=10) # cancel button
        self.bind("<return>", self.ok)
        self.bind("<escape>", self.cancel)
        box.pack(pady=5)

    def ok(self, event=None):
        mark_str = self.mark_entry.get().strip() # gets the mark input
        
        if not mark_str:
            self.cancel() # treat empty input as cancel/no change
            return

        try:
            mark = int(mark_str)
            if 0 <= mark <= self.max_val:
                self.result = mark # sets the valid mark as result
                self.cancel()
            else:
                # updated: replaced messagebox with custom messagedialog
                MessageDialog(self, "validation error", f"mark must be a whole number between 0 and {self.max_val}!", type='warning')
        except ValueError:
            # updated: replaced messagebox with custom messagedialog
            MessageDialog(self, "validation error", "please enter a whole number!", type='warning')


# --- 5. custom dialog for text/name input (used for update name) ---
class TextInputDialog(BaseDialog):
    def __init__(self, parent, title, prompt, initial_value=""):
        super().__init>(parent, title) # calls base dialog constructor
        
        body = ttk.Frame(self, padding="15 10 15 10")
        
        ttk.Label(body, text=prompt, 
                  font=('arial', 10)).pack(padx=5, pady=5, anchor='w') # text prompt
        
        self.text_entry = ttk.Entry(body, width=40) # text entry field
        self.text_entry.insert(0, initial_value) # pre-fills with current value
        self.text_entry.pack(padx=5, pady=5)
        self.initial_focus = self.text_entry

        body.pack(padx=10, pady=10)
        self.buttonbox()
        self.initial_focus.focus_set()
        self.show()

    def buttonbox(self):
        box = ttk.Frame(self)
        ttk.Button(box, text="set name", width=12, command=self.ok, default="active").pack(side="left", padx=10, pady=10) # set name button
        ttk.Button(box, text="cancel", width=12, command=self.cancel).pack(side="left", padx=10, pady=10) # cancel button
        self.bind("<return>", self.ok)
        self.bind("<escape>", self.cancel)
        box.pack(pady=5)

    def ok(self, event=None):
        text_str = self.text_entry.get().strip() # gets the text input
        
        if not text_str:
            # updated: replaced messagebox with custom messagedialog
            MessageDialog(self, "input required", "please enter a name.", type='warning')
            return

        self.result = text_str # sets the text as result
        self.cancel()

# --- 6. custom dialog for save success (used by _save_data_to_file) ---
class SaveSuccessDialog(BaseDialog):
    # modern modal dialog for showing a successful save operation
    def __init__(self, parent):
        super().__init>(parent, "save successful") # calls base dialog constructor

        body = ttk.Frame(self, padding="20 15 20 15")
        
        # display the success message in a prominent style
        ttk.Label(body, text="✅ data saved successfully!", 
                  foreground="#28a745", # green color for success
                  background=color_dark_blue, 
                  font=('arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(body, text="all changes have been safely written to studentmarks.txt.", 
                  font=('arial', 10)).pack(pady=5)

        body.pack(padx=10, pady=10)
        self.buttonbox()
        self.show()

    def buttonbox(self):
        box = ttk.Frame(self)
        # use a single, clean "ok" button
        ok_button = ttk.Button(box, text="ok", width=12, command=self.ok, default="active")
        ok_button.pack(padx=10, pady=10)
        self.bind("<return>", self.ok)
        self.bind("<escape>", self.ok) # use ok for escape too for quick dismissal
        box.pack(pady=5)


# --- the main application class ---
class StudentManagerApp:
    def __init__(self, master):
        self.master = master # the main tkinter window
        master.title("student manager") # sets window title
        master.geometry("1000x650") # sets window size
        master.config(bg=color_dark_blue) # sets window background color

        self.student_data_list = [] # initializes the list to store student data
        self._load_data_from_file() # loads initial data from file

        # --- logo area (top left) ---
        logo_frame = tk.Frame(master, width=150, height=80, bg=color_dark_blue) # frame for the logo/title
        logo_frame.grid(row=0, column=0, sticky='nw', padx=10, pady=10)
        logo_frame.grid_propagate(False) 

        # placeholder for png image
        self.logo_placeholder = tk.Label(logo_frame, 
                                     text="     student\n     manager", # application title text
                                     fg="#ffffff", 
                                     bg=color_dark_blue, 
                                     font=("arial", 15, "bold"),
                                     relief=tk.flat,
                                     anchor="center")
        # the label is set to take up the full space of the logo_frame
        self.logo_placeholder.pack(expand=True, fill='both')

        # --- heading bar (top right) ---
        self.heading_frame = tk.Frame(master, height=80, bg=color_heading_bg) # frame for the main heading
        self.heading_frame.grid(row=0, column=1, sticky='new', padx=10, pady=10)
        self.heading_frame.grid_columnconfigure(0, weight=1) 
        self.heading_frame.grid_propagate(False)

        self.heading_label = tk.Label(self.heading_frame,
                                          text="all student records", # main heading text
                                          fg=color_text_primary,
                                          bg=color_heading_bg,
                                          font=("arial", 18, "bold")) 
        self.heading_label.pack(expand=True, padx=10, pady=10)
        
        # --- main layout grid setup ---
        master.grid_rowconfigure(1, weight=1) # makes row 1 expandable
        master.grid_columnconfigure(1, weight=1) # makes column 1 expandable

        # --- button sidebar (left column, row 1) ---
        self.button_frame = tk.Frame(master, width=150, bg=color_dark_blue, bd=1, relief=tk.ridge) # frame for the menu buttons
        self.button_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))
        self.button_frame.grid_propagate(False)

        # --- content area (right column, row 1) ---
        self._setup_content_area(master) # sets up the treeview and status box

        # --- making the menu buttons ---
        self._create_professional_buttons()
        
        # show initial data
        self._view_all_records() # displays all records on startup
        
    def _quit_app(self):
        # updated: function to confirm before quitting using custom dialog
        # replaced messagebox.askyesno with custom confirmationdialog
        dialog = ConfirmationDialog(self.master, "confirm exit", "are you sure you want to quit? any unsaved changes will be lost!")
        if dialog.result: 
            self.master.quit() # quits the application

    def _create_professional_buttons(self):
        # creates the menu buttons with professional, flat styling
        def create_graphic_button(text, command, row, btn_color="#4f79a1", text_color="white"): # helper function to create a button
            
            # use a slightly darker blue for active/hover state for contrast
            active_bg_color = color_heading_bg
            
            btn = tk.Button(self.button_frame, 
                            text=text, 
                            command=command, 
                            width=15, 
                            pady=10, 
                            bg=btn_color,
                            fg=text_color, 
                            relief=tk.flat, 
                            font=("arial", 10, "bold"),
                            activebackground=active_bg_color,
                            activeforeground=color_text_primary)
            btn.grid(row=row, column=0, padx=10, pady=5, sticky='ew')
            
            # add a slight border visually on hover for feedback
            btn.bind("<enter>", lambda e: e.widget.config(relief=tk.raised)) # hover effect
            btn.bind("<leave>", lambda e: e.widget.config(relief=tk.flat)) # unhover effect
            return btn
            
        # standard view buttons
        self.btn_all = create_graphic_button("view all records", self._view_all_records, 0)
        self.btn_one = create_graphic_button("find student", self._view_individual, 1)
        self.btn_high = create_graphic_button("highest scorer", self._show_highest, 3)
        self.btn_low = create_graphic_button("lowest scorer", self._show_lowest, 4)
        
        tk.Frame(self.button_frame, height=5, bg=color_dark_blue).grid(row=5, column=0) # separator frame
        
        # action buttons
        self.btn_add = create_graphic_button("add new student", self._add_student, 6, btn_color="#7823a5", text_color="white") 
        self.btn_update = create_graphic_button("update record", self._update_record, 7, btn_color="#1e9f1e", text_color="white") 
        self.btn_delete = create_graphic_button("delete record", self._delete_student, 8, btn_color="#faab00", text_color="white") 
        
        # save & quit
        self.btn_save = create_graphic_button("save changes", self._save_data_to_file, 10, btn_color=color_heading_bg, text_color="white") 
        # updated: changed command to the new _quit_app function
        self.btn_quit = create_graphic_button("quit", self._quit_app, 11, btn_color="#003d6c", text_color="white") 


    def _setup_content_area(self, master):
        # sets up the treeview (for tabular data) and the status text box (for messages/summaries)
        
        self.content_frame = tk.Frame(master, bg=color_dark_blue) # frame for content area
        self.content_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=(0, 10))
        self.content_frame.grid_rowconfigure(0, weight=1) 
        self.content_frame.grid_rowconfigure(1, weight=0) 
        self.content_frame.grid_columnconfigure(0, weight=1) 

        # 1. setup the treeview style for a cleaner look
        style = ttk.Style()
        style.theme_use("clam") # uses clam theme as base
        style.configure("treeview.heading", font=('arial', 10, 'bold'), background=color_heading_bg, foreground=color_text_primary)
        style.map("treeview.heading", background=[('active', color_heading_bg)])
        style.configure("treeview", background=color_light_blue, foreground=color_text_secondary, fieldbackground=color_light_blue, rowheight=25, borderwidth=0)
        style.map("treeview", background=[('selected', color_heading_bg)], foreground=[('selected', color_text_primary)])
        
        # 2. define columns
        columns = ('code', 'name', 'a1', 'a2', 'a3', 'final', 'total', 'percent', 'grade')
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', style="treeview") # the main table widget
        
        # 3. define headings and widths
        self.tree.heading('code', text='code', anchor='center')
        self.tree.heading('name', text='name', anchor='w')
        self.tree.heading('a1', text='a1', anchor='center')
        self.tree.heading('a2', text='a2', anchor='center')
        self.tree.heading('a3', text='a3', anchor='center')
        self.tree.heading('final', text='final', anchor='center')
        self.tree.heading('total', text='total', anchor='center')
        self.tree.heading('percent', text='%', anchor='center') 
        self.tree.heading('grade', text='grade', anchor='center')

        self.tree.column('code', width=80, stretch=tk.no, anchor='center')
        self.tree.column('name', width=150, anchor='w')
        self.tree.column('a1', width=60, stretch=tk.no, anchor='center') 
        self.tree.column('a2', width=60, stretch=tk.no, anchor='center') 
        self.tree.column('a3', width=60, stretch=tk.no, anchor='center') 
        self.tree.column('final', width=80, anchor='center')
        self.tree.column('total', width=80, anchor='center')
        self.tree.column('percent', width=80, anchor='center')
        self.tree.column('grade', width=80, stretch=tk.no, anchor='center')
        
        # 4. add scrollbar
        vsb = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree.yview) # vertical scrollbar
        self.tree.configure(yscrollcommand=vsb.set)
        
        # 5. place the treeview and scrollbar in the grid
        self.tree.grid(row=0, column=0, sticky='nsew') # places the table
        vsb.grid(row=0, column=1, sticky='ns') # places the scrollbar

        # 6. message/status text
        self.status_text = tk.Text(self.content_frame, height=8, wrap='word', bg=color_heading_bg, fg=color_text_primary, font=("arial", 10), relief=tk.flat) # text box for status messages
        self.status_text.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        self.status_text.insert(tk.end, "summary and individual record details will appear here...")
        self.status_text.config(state=tk.disabled) # make it read-only


    # --- 1. data handling functions ---
    
    def _load_data_from_file(self):
        # reads the student data from the file and puts it in our list
        self.student_data_list = [] 
        try:
            # check if file exists and has content before trying to read
            if not os.path.exists(file_path):
                # using placeholder data if the file is missing for a better demo experience
                placeholder_data = [
                    ['1345', 'john curry', 8, 15, 7, 45],
                    ['2345', 'sam sturtivant', 14, 15, 14, 77],
                    ['9876', 'lee scott', 17, 11, 16, 99],
                    ['3724', 'matt thompson', 19, 11, 15, 81],
                    ['1212', 'ron herrema', 14, 17, 18, 66],
                    ['8439', 'jake hobbs', 10, 11, 10, 43],
                    ['2344', 'jo hyde', 6, 15, 10, 55],
                    ['9384', 'gareth southgate', 5, 6, 8, 33],
                    ['8327', 'alan shearer', 20, 20, 20, 100],
                    ['2683', 'les ferdinand', 15, 17, 18, 92]
                ]
                self.student_data_list = placeholder_data # loads sample data
                # updated: replaced messagebox with custom messagedialog (warning)
                MessageDialog(self.master, "file missing", "the studentmarks.txt file was not found. initializing with sample data from the screenshot.", type='warning')
                return
                
            with open(file_path, 'r') as f:
                lines = f.readlines()
                if not lines or len(lines) < 2: # skips header line (count)
                    return 
                
                # we skip lines[0] which is the count
                for line in lines[1:]: 
                    clean_line = line.strip()
                    if not clean_line: continue
                    
                    parts = clean_line.split(',')
                    # the parts are [code, name, c1, c2, c3, exam] -> 6 parts
                    if len(parts) == 6:
                        try:
                            student_code = parts[0].strip()
                            name = parts[1].strip()
                            a1 = int(parts[2].strip())
                            a2 = int(parts[3].strip())
                            a3 = int(parts[4].strip())
                            final = int(parts[5].strip())
                            
                            self.student_data_list.append([student_code, name, a1, a2, a3, final]) # adds record to list
                        except ValueError:
                            # updated: replaced messagebox with custom messagedialog (warning)
                            MessageDialog(self.master, "data error", f"skipped bad data line with invalid marks: {clean_line}", type='warning')
                            
        except Exception as e:
            # updated: replaced messagebox with custom messagedialog (error)
            MessageDialog(self.master, "file read error", f"an error occurred while reading the file: {e}", type='error')

    def _save_data_to_file(self):
        # writes the current student list back into the file, including the new count
        try:
            # ensure the directory exists
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            
            with open(file_path, 'w', newline='') as f:
                # write the count first
                f.write(str(len(self.student_data_list)) + '\n') # writes the number of students
                
                writer = csv.writer(f)
                for student in self.student_data_list:
                    # student is already a list: [code, name, c1, c2, c3, exam]
                    writer.writerow(student) # writes each student record
            
            # this is already a modern dialog
            SaveSuccessDialog(self.master) # shows success dialog

        except Exception as e:
            # updated: replaced messagebox with custom messagedialog (error)
            MessageDialog(self.master, "save error", f"could not save file! error: {e}", type='error')

    # --- 2. calculation & formatting functions ---
    
    def _calculate_results(self, student_record):
        # takes a student's raw data and calculates their score, percent, and grade
        # the list is: [code, name, c1, c2, c3, exam]
        a1 = student_record[2]
        a2 = student_record[3]
        a3 = student_record[4]
        final = student_record[5]
        
        coursework_total = a1 + a2 + a3
        overall_total = coursework_total + final # calculates total marks
        
        overall_percent = (overall_total / max_total_marks) * 100 # calculates percentage
        
        grade = 'f' # default grade
        if overall_percent >= 70: grade = 'a'
        elif overall_percent >= 60: grade = 'b'
        elif overall_percent >= 50: grade = 'c'
        elif overall_percent >= 40: grade = 'd'
            
        return { # returns a dictionary of calculated results
            'code': student_record[0],
            'name': student_record[1],
            'a1': a1,
            'a2': a2,
            'a3': a3,
            'final': final,
            'total': overall_total,
            'percent': overall_percent,
            'grade': grade
        }
        
    def _insert_student_into_tree(self, results):
        # inserts a single student's calculated data into the treeview table
        self.tree.insert('', tk.end, values=( # inserts a new row
            results['code'],
            results['name'],
            f"{results['a1']}", 
            f"{results['a2']}", 
            f"{results['a3']}", 
            f"{results['final']}",
            f"{results['total']}",
            f"{results['percent']:.2f}",
            results['grade']
        ))

    def _clear_output(self, title):
        # clears the treeview table and the status box, then updates the heading
        self.heading_label.config(text=title) # updates the heading label
        
        # clear the treeview table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # clear the status text box
        self.status_text.config(state=tk.normal) # enables writing
        self.status_text.delete(1.0, tk.end) # deletes all content
        self.status_text.config(state=tk.disabled) # disables writing


    # --- 3. menu functionality ---
    
    # --- 1. view all student records (all records) ---
    def _view_all_records(self):
        # shows every student's results in the treeview and a summary in the status box
        self._clear_output("all student records") 
        
        total_percent_sum = 0
        
        if not self.student_data_list: # checks if list is empty
            self._write_status("the student list is currently empty! please use 'add new student' to add students.")
            return

        for student in self.student_data_list:
            results = self._calculate_results(student)
            self._insert_student_into_tree(results)
            total_percent_sum += results['percent']
            
        # summary calculation
        num_students = len(self.student_data_list)
        average_percent = total_percent_sum / num_students if num_students > 0 else 0

        summary = ( # formats the summary text
            f"--- class summary ---\n"
            f"total students in class: {num_students}\n"
            f"average percentage mark: {average_percent:.2f}%\n"
            f"maximum total mark possible: {max_total_marks}\n"
            f"---------------------"
        )
        self._write_status(summary) # displays the summary
        

    # --- 2. view individual student record (find student) ---
    def _view_individual(self):
        # lets the user search for one student and displays details in the status box
        dialog = SearchDialog(self.master, "find student record", 
                              "enter student name or student code to view their results:")
        search_term = dialog.result # gets the search term
        
        if not search_term: return 

        self._clear_output(f"viewing individual record: '{search_term}'")
        found_student = None

        for student in self.student_data_list:
            # match by code (index 0) or name (index 1, case-insensitive)
            if student[0] == search_term or student[1].lower() == search_term.lower():
                found_student = student
                break
        
        if found_student:
            results = self._calculate_results(found_student)
            
            # the individual marks c1, c2, c3 are in the raw student_record
            # updated: changed 'coursework' to 'assessment'
            output = ( # formats the individual student details
                f"record found for {results['name']} (code: {results['code']})\n"
                f"assessment marks: a1={found_student[2]}, a2={found_student[3]}, a3={found_student[4]}\n"
                f"assessment total: {results['a1']+results['a2']+results['a3']}/60 | exam mark: {results['final']}/100\n"
                f"overall total: {results['total']}/{max_total_marks} | final percentage: {results['percent']:.2f}% | final grade: {results['grade']}"
            )
            self._write_status(output)
            # inserts the single record into the table
            self._insert_student_into_tree(results)
        else:
            self._write_status(f"error: couldn't find a student with the name or code '{search_term}'.")


    # --- 3 & 4. highest/lowest score ---
    def _find_extreme_student(self, is_highest):
        # helper to find the student with the highest or lowest overall score
        action_text = "highest" if is_highest else "lowest"
        self._clear_output(f"student with {action_text} overall score")

        if not self.student_data_list:
            self._write_status("the student list is empty!")
            return

        best_student = None
        # initialize best_score to a value outside the possible range
        best_score = -1 if is_highest else max_total_marks + 1 

        for student in self.student_data_list:
            results = self._calculate_results(student)
            score = results['total']
            
            # logic to find extreme score (highest or lowest)
            if (is_highest and score > best_score) or (not is_highest and score < best_score):
                best_score = score
                best_student = results

        if best_student:
            output = ( # formats the result
                f"found {action_text} scorer: {best_student['name']} (code: {best_student['code']})\n"
                f"overall score: {best_student['total']}/{max_total_marks} | final percentage: {best_student['percent']:.2f}% | final grade: {best_student['grade']}\n"
                f"result displayed in the table above."
            )
            self._write_status(output)
            # display the result in the table too
            self._insert_student_into_tree(best_student)


    def _show_highest(self):
        self._find_extreme_student(is_highest=True) # calls helper to find highest

    def _show_lowest(self):
        self._find_extreme_student(is_highest=False) # calls helper to find lowest


    # --- 5. sort student records (ascending / descending) ---
    def _sort_records(self, reverse):
        # sorts the records by percentage and displays them in the treeview
        reverse_sort = reverse 
        
        students_with_percent = []
        for student in self.student_data_list:
            results = self._calculate_results(student)
            # store a tuple of (percent, raw_data_list)
            students_with_percent.append((results['percent'], student))
            
        # sort based on the percentage (index 0 of the tuple)
        students_with_percent.sort(key=lambda x: x[0], reverse=reverse_sort)
        
        self._clear_output(f"records sorted by percentage ({'descending' if reverse_sort else 'ascending'})")
        
        for percent, student_data in students_with_percent:
            results = self._calculate_results(student_data)
            self._insert_student_into_tree(results)
        
        self._write_status(f"table updated! showing {len(self.student_data_list)} students sorted by final percentage.")


    # --- 6. add a student record (add record) ---
    def _add_student(self):
        # opens a custom modal dialog to get new student details
        
        dialog = AddStudentDialog(self.master, "add new student record") # opens the add student dialog
        
        new_record = dialog.result

        if new_record:
            # check if student code already exists
            if any(new_record[0] == student[0] for student in self.student_data_list):
                 # updated: replaced messagebox with custom messagedialog (warning)
                 MessageDialog(self.master, "code exists", f"student code {new_record[0]} already exists!", type='warning')
                 return

            self.student_data_list.append(new_record) # adds the new record
            
            self._write_status(f"success! added new student: {new_record[1]}. remember to click 'save changes'!")
            self._view_all_records() # refresh the aesthetic table view
        else:
            self._write_status("adding new record cancelled by user.")


    # --- 7. delete a student record (delete record) ---
    def _delete_student(self):
        # finds a student and removes them from the list
        dialog = SearchDialog(self.master, "delete record", 
                              "enter student name or student code to delete:")
        search_term = dialog.result # gets search term
        
        if not search_term: return

        index_to_delete = -1
        deleted_name = ""

        for i, student in enumerate(self.student_data_list):
            if student[0] == search_term or student[1].lower() == search_term.lower():
                index_to_delete = i
                deleted_name = student[1]
                break
        
        if index_to_delete != -1:
            # updated: replaced messagebox.askyesno with custom confirmationdialog
            confirm_dialog = ConfirmationDialog(self.master, "confirm delete", f"are you sure you want to permanently delete {deleted_name}'s record?")
            if confirm_dialog.result: # if user confirms
                self.student_data_list.pop(index_to_delete) # removes the record
                self._write_status(f"successfully deleted record for {deleted_name}. remember to click 'save changes'!")
                self._view_all_records() # refreshes the view
            else:
                self._write_status(f"did not delete {deleted_name}.")
        else:
            self._write_status(f"couldn't find student '{search_term}' to delete.")


    # --- 8. update a students record (update record) ---
    def _update_record(self):
        # lets the user change a student's marks or name
        dialog = SearchDialog(self.master, "find record to update", 
                              "enter student name or student code to update:")
        search_term = dialog.result # gets search term

        if not search_term: return
        
        target_index = -1
        for i, student in enumerate(self.student_data_list):
            if student[0] == search_term or student[1].lower() == search_term.lower():
                target_index = i
                break
        
        if target_index == -1:
            self._write_status(f"couldn't find student '{search_term}' to update.")
            return

        student = self.student_data_list[target_index]
        current_name = student[1]
        
        choice_dialog = UpdateChoiceDialog(self.master, current_name) # opens dialog to choose field
        choice = choice_dialog.result

        if choice is None:
             self._write_status("update cancelled by user.")
             return
        
        if choice == 1:
            # using textinputdialog for name update
            name_dialog = TextInputDialog(self.master, "update student name", 
                                          f"enter new name for {current_name}:", initial_value=current_name)
            new_name = name_dialog.result
            
            if new_name: 
                student[1] = new_name # updates the name
                self._write_status(f"updated student name to {new_name}! remember to click 'save changes'!")
            else:
                self._write_status("name update cancelled or failed.")
            
        elif choice in [2, 3, 4, 5]:
            # mark index in list is choice + 0 (choice 2 maps to index 2, etc.)
            mark_index = choice + 0 
            max_val = 20 if choice < 5 else 100 # determines max mark
            # updated: changed 'assessment' (was coursework)
            field_name = ["", "name", "assessment 1", "assessment 2", "assessment 3", "final"][choice]
            
            # using custom dialog for mark input
            mark_dialog = MarkInputDialog(self.master, field_name, max_val)
            new_mark = mark_dialog.result

            if new_mark is not None:
                student[mark_index] = new_mark # updates the mark
                self._write_status(f"updated {field_name} for {student[1]} to {new_mark}! remember to click 'save changes'!")
            else:
                self._write_status("mark update cancelled or failed.")
        
        else:
            self._write_status("update cancelled.")
            return

        self._view_all_records() # show the updated table

    # --- utility to write to the status box ---
    def _write_status(self, text):
        # writes a message to the read-only status text box
        self.status_text.config(state=tk.normal) # enables writing
        self.status_text.delete(1.0, tk.end) # clears existing content
        self.status_text.insert(tk.end, text) # inserts new text
        self.status_text.config(state=tk.disabled) # disables writing

# --- start the whole program! ---
if __name__ == "__main__":
    root = tk.tk() # creates the main window

    # set window icon (best method for .ico)
    try:
        # use the constant defined at the top
        root.iconbitmap(icon_path) # sets the window icon
    except Exception as e:
        print("icon could not be loaded:", e)

    app = StudentManagerApp(root) # initializes the application class
    root.mainloop() # starts the tkinter event loop