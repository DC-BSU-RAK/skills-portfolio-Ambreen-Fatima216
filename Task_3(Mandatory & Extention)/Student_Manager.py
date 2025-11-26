import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import os
import csv


#This code was developed using the ideas from the following youtube Channel: ForCodeCoder
# --- File Path & Placeholder Data ---
FILE_PATH = "Task_3(Mandatory & Extention)/studentMarks.txt"
MAX_TOTAL_MARKS = 160 # 3 course marks out of 20 each and 1 exam mark out of 100 is 160

# THEMES COLOR FOR THE PAG
COLOR_DARK_BLUE = "#004AAD"      # Main background color
COLOR_LIGHT_BLUE = "#E0E6F0"     # Content background 
COLOR_HEADING_BG = "#2B7EAC"     # Slightly lighter blue for the heading bar 
COLOR_TEXT_PRIMARY = "white"
COLOR_TEXT_SECONDARY = "black"


#Custom Modal Dialog for Adding a Student 
class AddStudentDialog(tk.Toplevel):
    """A custom, modal Toplevel dialog for collecting all student input in one go."""
    def __init__(self, parent, title):
        super().__init__(parent)
        self.transient(parent) # Window will stay on top of parent
        self.title(title)
        self.parent = parent
        self.result = None
        
        # Set colors and style for the dialog
        self.config(bg=COLOR_DARK_BLUE)
        self.style = ttk.Style()
        self.style.configure('TFrame', background=COLOR_DARK_BLUE)
        self.style.configure('TLabel', background=COLOR_DARK_BLUE, foreground=COLOR_TEXT_PRIMARY, font=('Arial', 10, 'bold'))
        self.style.configure('TEntry', fieldbackground=COLOR_LIGHT_BLUE, foreground=COLOR_TEXT_SECONDARY)
        self.style.map('TButton', background=[('active', COLOR_HEADING_BG), ('!disabled', COLOR_LIGHT_BLUE)])
        self.style.configure('TButton', font=('Arial', 10, 'bold'), foreground=COLOR_TEXT_SECONDARY)

        # Center the dialog on screen
        self.geometry(f"+{parent.winfo_rootx()+150}+{parent.winfo_rooty()+100}")
        self.resizable(False, False)

        # Create content frame
        body = ttk.Frame(self, padding="15 10 15 10")
        self.initial_focus = self.body(body)
        body.pack(padx=10, pady=10)

        self.buttonbox()
        
        # Make it modal
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.initial_focus.focus_set()
        
        # Wait until the window is destroyed
        self.wait_window(self)

    def body(self, master):
        """Create the dialog body."""
        
        ttk.Label(master, text="Student Code (4 digits, required):", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.code_entry = ttk.Entry(master, width=35)
        self.code_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="Student Name (Full Name):", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.name_entry = ttk.Entry(master, width=35)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(master, text="Coursework 1 Mark (max 20):", anchor="w").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.c1_entry = ttk.Entry(master, width=35)
        self.c1_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(master, text="Coursework 2 Mark (max 20):", anchor="w").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.c2_entry = ttk.Entry(master, width=35)
        self.c2_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(master, text="Coursework 3 Mark (max 20):", anchor="w").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.c3_entry = ttk.Entry(master, width=35)
        self.c3_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(master, text="Examination Mark (max 100):", anchor="w").grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.exam_entry = ttk.Entry(master, width=35)
        self.exam_entry.grid(row=5, column=1, padx=5, pady=5)

        return self.code_entry # Initial focus

    def buttonbox(self):
        """Add standard button box: OK and Cancel."""
        box = ttk.Frame(self)

        w = ttk.Button(box, text="Add Student", width=12, command=self.ok, default="active")
        w.pack(side="left", padx=10, pady=10)
        w = ttk.Button(box, text="Cancel", width=12, command=self.cancel)
        w.pack(side="left", padx=10, pady=10)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(pady=5)

    def ok(self, event=None):
        if not self.validate():
            # If validation fails, focus remains on the dialog
            return

        self.withdraw()
        self.update_idletasks()
        
        try:
            self.apply()
        finally:
            self.cancel() # Always close the dialog whether apply succeeded or not

    def cancel(self, event=None):
        # Put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        # 1. Get raw string values
        code_str = self.code_entry.get().strip()
        name_str = self.name_entry.get().strip()
        c1_str = self.c1_entry.get().strip()
        c2_str = self.c2_entry.get().strip()
        c3_str = self.c3_entry.get().strip()
        exam_str = self.exam_entry.get().strip()

        # Simple checks
        if not code_str or not name_str:
            messagebox.showerror("Validation Error", "Student Code and Name fields cannot be empty.")
            return False
            
        if len(code_str) != 4 or not code_str.isdigit():
            messagebox.showerror("Validation Error", "Student Code must be exactly 4 digits.")
            return False

        # Mark checks
        marks_to_check = [
            (c1_str, 20, "Coursework 1"),
            (c2_str, 20, "Coursework 2"),
            (c3_str, 20, "Coursework 3"),
            (exam_str, 100, "Exam Mark")
        ]
        
        self.validated_marks = []
        
        for mark_str, max_val, name in marks_to_check:
            try:
                mark = int(mark_str)
                if 0 <= mark <= max_val:
                    self.validated_marks.append(mark)
                else:
                    messagebox.showerror("Validation Error", f"'{name}' must be a number between 0 and {max_val}.")
                    return False
            except ValueError:
                messagebox.showerror("Validation Error", f"'{name}' must be a whole number.")
                return False

        # All validation passed
        self.data_out = [
            code_str, 
            name_str, 
            *self.validated_marks
        ]
        return True # Return True if input is valid

    def apply(self):
        # This function is called if validation succeeds
        self.result = self.data_out


# --- The Main Application Class (The Big Boss of our program) ---
class StudentManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("💻 The Super Awesome Student Manager!")
        master.geometry("1000x650") # Made the window slightly bigger for the table
        master.config(bg=COLOR_DARK_BLUE) 

        self.student_data_list = []
        self._load_data_from_file() 

        # --- A place for the Logo (Top Left Circle) ---
        logo_frame = tk.Frame(master, width=150, height=80, bg=COLOR_DARK_BLUE)
        logo_frame.grid(row=0, column=0, sticky='nw', padx=10, pady=10)
        logo_frame.grid_propagate(False) 

        logo_image_label = tk.Label(logo_frame, 
                                    text="[UNIVERSITY\nLOGO HERE]", 
                                    fg=COLOR_TEXT_PRIMARY, 
                                    bg=COLOR_DARK_BLUE, 
                                    font=("Arial", 10, "bold"),
                                    relief='solid', bd=2, highlightthickness=0,
                                    width=10, height=5)
        logo_image_label.place(relx=0.5, rely=0.5, anchor='center')

        # --- Heading Bar (Top Right) ---
        self.heading_frame = tk.Frame(master, height=80, bg=COLOR_HEADING_BG)
        self.heading_frame.grid(row=0, column=1, sticky='new', padx=10, pady=10)
        self.heading_frame.grid_columnconfigure(0, weight=1) 
        self.heading_frame.grid_propagate(False)

        self.heading_label = tk.Label(self.heading_frame,
                                      text="AESTHETIC STUDENT DATA DISPLAY",
                                      fg=COLOR_TEXT_PRIMARY,
                                      bg=COLOR_HEADING_BG,
                                      font=("Arial", 16, "bold"))
        self.heading_label.pack(expand=True, padx=10, pady=10)
        
        # --- Main Layout Grid Setup ---
        master.grid_rowconfigure(1, weight=1)    
        master.grid_columnconfigure(1, weight=1) 

        # --- Button Sidebar (Left Column, Row 1) ---
        self.button_frame = tk.Frame(master, width=150, bg=COLOR_DARK_BLUE)
        self.button_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))
        self.button_frame.grid_propagate(False)

        # --- Content Area (Right Column, Row 1) ---
        self._setup_content_area(master)

        # --- Making the Menu Buttons (Our Control Panel!) ---
        def create_button(text, command, row):
            btn = tk.Button(self.button_frame, 
                            text=text, 
                            command=command, 
                            width=15, 
                            pady=8, 
                            bg=COLOR_LIGHT_BLUE,
                            fg=COLOR_TEXT_SECONDARY, 
                            relief=tk.RAISED,
                            font=("Arial", 10, "bold"))
            btn.grid(row=row, column=0, padx=10, pady=5, sticky='ew')
            return btn
            
        # 1. View all
        self.btn_all = create_button("ALL RECORDS", self._view_all_records, 0)
        # 2. View Individual (Now uses the status box)
        self.btn_one = create_button("ONE RECORD", self._view_individual, 1)
        # 3. Highest Score (Now uses the status box)
        self.btn_high = create_button("HIGHEST SCORE", self._show_highest, 2)
        # 4. Lowest Score (Now uses the status box)
        self.btn_low = create_button("LOWEST SCORE", self._show_lowest, 3)
        
        # --- Separator/Space ---
        tk.Frame(self.button_frame, height=5, bg=COLOR_DARK_BLUE).grid(row=4, column=0)
        
        # 6. Add Student
        self.btn_add = create_button("ADD RECORD", self._add_student, 5)
        # 8. Update Record
        self.btn_update = create_button("UPDATE RECORD", self._update_record, 6)
        # 7. Delete Student 
        self.btn_delete = create_button("DELETE RECORD", self._delete_student, 7)
        
        # 5. Sort Records - NOW TWO BUTTONS!
        create_button("SORT ASCENDING", lambda: self._sort_records(reverse=False), 8) 
        create_button("SORT DESCENDING", lambda: self._sort_records(reverse=True), 9)  
        
        # --- Separator/Space (Shifted down) ---
        tk.Frame(self.button_frame, height=10, bg=COLOR_DARK_BLUE).grid(row=10, column=0)
        
        # Save Button (Shifted down)
        self.btn_save = create_button("SAVE CHANGES", self._save_data_to_file, 11)
        
        # Quit Button (Shifted down)
        self.btn_quit = create_button("QUIT", master.quit, 12)
        self.btn_quit.config(bg="#003D6C", fg="white") 
        
        # Show initial data
        self._view_all_records()


    def _setup_content_area(self, master):
        """Sets up the Treeview (for tabular data) and the status Text box (for messages/summaries)."""
        
        self.content_frame = tk.Frame(master, bg=COLOR_DARK_BLUE)
        self.content_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=(0, 10))
        self.content_frame.grid_rowconfigure(0, weight=1) # Treeview row expands
        self.content_frame.grid_rowconfigure(1, weight=0) # Message row fixed height
        self.content_frame.grid_columnconfigure(0, weight=1) # Treeview/Message column expands

        # 1. Setup the Treeview Style for a cleaner look
        style = ttk.Style()
        style.theme_use("clam") # 'clam' theme looks modern
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background=COLOR_HEADING_BG, foreground=COLOR_TEXT_PRIMARY)
        style.configure("Treeview", background=COLOR_LIGHT_BLUE, foreground=COLOR_TEXT_SECONDARY, fieldbackground=COLOR_LIGHT_BLUE, rowheight=25)
        
        # 2. Define Columns
        columns = ('code', 'name', 'coursework', 'exam', 'total', 'percent', 'grade')
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', style="Treeview")
        
        # 3. Define Headings and Widths
        self.tree.heading('code', text='Code', anchor='center')
        self.tree.heading('name', text='Student Name', anchor='w')
        self.tree.heading('coursework', text='Coursework (60)', anchor='center')
        self.tree.heading('exam', text='Exam (100)', anchor='center')
        self.tree.heading('total', text='Total (160)', anchor='center')
        self.tree.heading('percent', text='Percent (%)', anchor='center')
        self.tree.heading('grade', text='Grade', anchor='center')

        self.tree.column('code', width=80, stretch=tk.NO, anchor='center')
        self.tree.column('name', width=200, anchor='w')
        self.tree.column('coursework', width=120, anchor='center')
        self.tree.column('exam', width=100, anchor='center')
        self.tree.column('total', width=100, anchor='center')
        self.tree.column('percent', width=100, anchor='center')
        self.tree.column('grade', width=80, stretch=tk.NO, anchor='center')
        
        # 4. Add Scrollbar
        vsb = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # 5. Place the Treeview and Scrollbar in the grid
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')

        # 6. Message/Status Text (For single records, errors, and class summary)
        self.status_text = tk.Text(self.content_frame, height=8, wrap='word', bg=COLOR_HEADING_BG, fg=COLOR_TEXT_PRIMARY, font=("Arial", 10))
        self.status_text.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        self.status_text.insert(tk.END, "Summary and individual record details will appear here...")
        self.status_text.config(state=tk.DISABLED) # Make it read-only


    # --- 1. DATA HANDLING FUNCTIONS ---
    
    def _load_data_from_file(self):
        """Reads the student data from the file and puts it in our list."""
        self.student_data_list = [] 
        try:
            with open(FILE_PATH, 'r') as f:
                lines = f.readlines()
                if not lines: return 
                
                for line in lines[1:]: 
                    clean_line = line.strip()
                    if not clean_line: continue
                    
                    parts = clean_line.split(',')
                    if len(parts) == 6:
                        try:
                            student_code = parts[0]
                            name = parts[1]
                            c1 = int(parts[2])
                            c2 = int(parts[3])
                            c3 = int(parts[4])
                            exam = int(parts[5])
                            
                            self.student_data_list.append([student_code, name, c1, c2, c3, exam])
                        except ValueError:
                            messagebox.showwarning("Data Error", f"Skipped bad data line: {clean_line}")
                            
        except FileNotFoundError:
            messagebox.showerror("File Missing", "I can't find the studentMarks.txt file!")

    def _save_data_to_file(self):
        """Writes the current student list back into the file, including the new count."""
        try:
            with open(FILE_PATH, 'w', newline='') as f:
                f.write(str(len(self.student_data_list)) + '\n')
                
                writer = csv.writer(f)
                for student in self.student_data_list:
                    writer.writerow(student) 
            messagebox.showinfo("Success", "All changes have been saved to studentMarks.txt!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file! Error: {e}")

    # --- 2. CALCULATION & FORMATTING FUNCTIONS ---
    
    def _calculate_results(self, student_record):
        """Takes a student's raw data and calculates their score, percent, and grade."""
        # The list is: [Code, Name, C1, C2, C3, Exam]
        coursework_total = student_record[2] + student_record[3] + student_record[4]
        overall_total = coursework_total + student_record[5]
        overall_percent = (overall_total / MAX_TOTAL_MARKS) * 100
        
        grade = 'F'
        if overall_percent >= 70: grade = 'A'
        elif overall_percent >= 60: grade = 'B'
        elif overall_percent >= 50: grade = 'C'
        elif overall_percent >= 40: grade = 'D'
            
        return {
            'code': student_record[0],
            'name': student_record[1],
            'coursework': coursework_total,
            'exam': student_record[5],
            'total': overall_total,
            'percent': overall_percent,
            'grade': grade
        }
        
    def _insert_student_into_tree(self, results):
        """Inserts a single student's calculated data into the Treeview table."""
        self.tree.insert('', tk.END, values=(
            results['code'],
            results['name'],
            f"{results['coursework']}/60",
            f"{results['exam']}/100",
            f"{results['total']}/{MAX_TOTAL_MARKS}",
            f"{results['percent']:.2f}",
            results['grade']
        ))

    def _clear_output(self, title):
        """Clears the Treeview table and the status box, then updates the heading."""
        self.heading_label.config(text=title)
        
        # Clear the Treeview table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Clear the Status Text box
        self.status_text.config(state=tk.NORMAL) # Enable writing
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED) # Disable writing


    # --- 3. MENU FUNCTIONALITY ---
    
    # --- 1. View all student records (ALL RECORDS) ---
    def _view_all_records(self):
        """Shows every student's results in the Treeview and a summary in the status box."""
        self._clear_output("ALL STUDENT RECORDS")
        
        total_percent_sum = 0
        
        if not self.student_data_list:
            self._write_status("The student list is currently empty! Please use 'ADD RECORD' to add students.")
            return

        for student in self.student_data_list:
            results = self._calculate_results(student)
            self._insert_student_into_tree(results)
            total_percent_sum += results['percent']
            
        # Summary!
        num_students = len(self.student_data_list)
        average_percent = total_percent_sum / num_students if num_students > 0 else 0

        summary = (
            f"--- CLASS SUMMARY ---\n"
            f"Total Students in Class: {num_students}\n"
            f"Average Percentage Mark: {average_percent:.2f}%\n"
            f"---------------------"
        )
        self._write_status(summary)
        

    # --- 2. View individual student record (ONE RECORD) ---
    def _view_individual(self):
        """Lets the user search for one student and displays details in the status box."""
        # Modernized prompt title
        search_term = simpledialog.askstring("Search Individual Record (Code or Name)", 
                                             "Enter Student Name OR Student Code to view their results:", 
                                             parent=self.master)
        
        if not search_term: return 

        self._clear_output(f"VIEWING INDIVIDUAL RECORD: '{search_term}'")
        found_student = None

        for student in self.student_data_list:
            if student[0] == search_term or student[1].lower() == search_term.lower():
                found_student = student
                break
        
        if found_student:
            results = self._calculate_results(found_student)
            
            output = (
                f"✅ RECORD FOUND for {results['name']} (Code: {results['code']})\n"
                f"Coursework Total: {results['coursework']}/60 | Exam Mark: {results['exam']}/100\n"
                f"Overall Total: {results['total']}/{MAX_TOTAL_MARKS} | Final Percentage: {results['percent']:.2f}% | Final Grade: {results['grade']}"
            )
            self._write_status(output)
            # For aesthetic purposes, we insert the single record into the table too
            self._insert_student_into_tree(results)
        else:
            self._write_status(f"❌ Error: Couldn't find a student with the name or code '{search_term}'.")


    # --- 3 & 4. Highest/Lowest Score ---
    def _find_extreme_student(self, is_highest):
        """Helper to find the student with the highest or lowest overall score."""
        action_text = "HIGHEST" if is_highest else "LOWEST"
        self._clear_output(f"STUDENT WITH {action_text} OVERALL SCORE")

        if not self.student_data_list:
            self._write_status("The student list is empty!")
            return

        best_student = None
        best_score = -1 if is_highest else MAX_TOTAL_MARKS + 1 

        for student in self.student_data_list:
            results = self._calculate_results(student)
            score = results['total']
            
            if (is_highest and score > best_score) or (not is_highest and score < best_score):
                best_score = score
                best_student = results

        if best_student:
            output = (
                f"🎉 FOUND {action_text} SCORER: {best_student['name']} (Code: {best_student['code']})\n"
                f"Overall Score: {best_student['total']}/{MAX_TOTAL_MARKS} ({best_student['percent']:.2f}%) | Final Grade: {best_student['grade']}\n"
                f"They excelled! "
            )
            self._write_status(output)
            # Display the result in the table too
            self._insert_student_into_tree(best_student)


    def _show_highest(self):
        self._find_extreme_student(is_highest=True)

    def _show_lowest(self):
        self._find_extreme_student(is_highest=False)


    # --- 5. Sort student records (ASCENDING / DESCENDING) ---
    def _sort_records(self, reverse):
        """Sorts the records by percentage and displays them in the Treeview."""
        reverse_sort = reverse 
        
        students_with_percent = []
        for student in self.student_data_list:
            results = self._calculate_results(student)
            students_with_percent.append((results['percent'], results))
            
        students_with_percent.sort(key=lambda x: x[0], reverse=reverse_sort)
        
        self._clear_output(f"RECORDS SORTED BY PERCENTAGE ({'DESCENDING' if reverse_sort else 'ASCENDING'})")
        
        for percent, results in students_with_percent:
            self._insert_student_into_tree(results)
        
        self._write_status(f"Table updated! Showing {len(self.student_data_list)} students sorted by final percentage.")


    # --- 6. Add a student record (ADD RECORD) ---
    def _add_student(self):
        """Opens a modern modal dialog to get new student details."""
        
        # Custom dialog replaces the multiple simpledialog calls
        dialog = AddStudentDialog(self.master, "➕ Add New Student Record")
        
        new_record = dialog.result

        if new_record:
            # Check if student code already exists
            if any(new_record[0] == student[0] for student in self.student_data_list):
                 messagebox.showwarning("Code Exists", f"Student code {new_record[0]} already exists!")
                 return

            self.student_data_list.append(new_record)
            
            self._write_status(f"SUCCESS! Added new student: {new_record[1]}. Remember to click 'SAVE CHANGES'!")
            self._view_all_records() # Refresh the aesthetic table view
        else:
            self._write_status("Adding new record cancelled by user.")


    # --- 7. Delete a student record (DELETE RECORD) ---
    def _delete_student(self):
        """Finds a student and removes them from the list."""
        # Modernized prompt title
        search_term = simpledialog.askstring("Delete Record (Code or Name)", 
                                             "Enter Student Name OR Student Code to DELETE:",
                                             parent=self.master)
        if not search_term: return

        index_to_delete = -1
        deleted_name = ""

        for i, student in enumerate(self.student_data_list):
            if student[0] == search_term or student[1].lower() == search_term.lower():
                index_to_delete = i
                deleted_name = student[1]
                break
        
        if index_to_delete != -1:
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to PERMANENTLY DELETE {deleted_name}'s record?"):
                self.student_data_list.pop(index_to_delete)
                self._write_status(f"BYE BYE! Successfully deleted record for {deleted_name}. Remember to click 'SAVE CHANGES'!")
                self._view_all_records() 
            else:
                self._write_status(f"Phew! Did not delete {deleted_name}.")
        else:
            self._write_status(f"Couldn't find student '{search_term}' to delete. 😥")


    # --- 8. Update a students record (UPDATE RECORD) ---
    def _update_record(self):
        """Lets the user change a student's marks or name."""
        # Modernized prompt title
        search_term = simpledialog.askstring("Find Record to Update (Code or Name)", 
                                             "Enter Student Name OR Student Code to UPDATE:", 
                                             parent=self.master)
        if not search_term: return
        
        target_index = -1
        for i, student in enumerate(self.student_data_list):
            if student[0] == search_term or student[1].lower() == search_term.lower():
                target_index = i
                break
        
        if target_index == -1:
            self._write_status(f"Couldn't find student '{search_term}' to update. 😥")
            return

        student = self.student_data_list[target_index]
        self._write_status(f"Found student: {student[1]} (Code: {student[0]})! Please select what to update.")
        
        choice = simpledialog.askinteger("Update Field Selection", 
                                        "What do you want to change?\n"
                                        "1: Name\n2: Coursework Mark 1\n3: Coursework Mark 2\n"
                                        "4: Coursework Mark 3\n5: Exam Mark",
                                        parent=self.master, minvalue=1, maxvalue=5)

        if choice == 1:
            new_name = simpledialog.askstring("Update Name", f"Enter new name for {student[1]}:", parent=self.master)
            if new_name: student[1] = new_name
            
        elif choice in [2, 3, 4, 5]:
            # Mark index in list is choice + 0 (choice 2 maps to index 2, etc.)
            mark_index = choice + 0 
            max_val = 20 if choice < 5 else 100
            
            def ask_mark(prompt, max_val):
                while True:
                    mark_str = simpledialog.askstring("Input NEW Mark", f"Enter NEW {prompt} (max {max_val}):", parent=self.master)
                    if mark_str is None: return None
                    try:
                        mark = int(mark_str)
                        if 0 <= mark <= max_val: return mark
                        else: messagebox.showwarning("Oops!", f"Mark must be between 0 and {max_val}!")
                    except ValueError: messagebox.showwarning("Oops!", "Please enter a whole number!")

            new_mark = ask_mark(f"Mark for item {choice-1}", max_val)
            if new_mark is not None:
                student[mark_index] = new_mark
        
        else:
            self._write_status("Update cancelled.")
            return

        self._write_status(f"Updated record for {student[1]}! Remember to click 'SAVE CHANGES'!")
        self._view_all_records() # Show the updated table

    # --- Utility to write to the Status Box ---
    def _write_status(self, text):
        """Writes a message to the read-only status text box."""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, text)
        self.status_text.config(state=tk.DISABLED)

# --- Start the whole program! ---
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()