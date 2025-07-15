# sms_management_system/gui/main_window.py

import customtkinter as ctk
from tkinter import ttk # Still need ttk for Treeview
from tkinter import messagebox # Using messagebox directly for now
from utils.helpers import show_info_message, show_error_message, show_warning_message, ask_confirmation

# Import services
from services.student_service import StudentService
from services.grade_service import GradeService
from services.subject_service import SubjectService
from services.academic_year_service import AcademicYearService
from services.semester_service import SemesterService
from services.exam_service import ExamService
from services.exam_result_service import ExamResultService
from services.semester_result_service import SemesterResultService
from services.yearly_result_service import YearlyResultService

# Import validation helpers
from utils.helpers import is_valid_date, is_valid_email, is_valid_student_id, is_valid_marks

class StudentManagementApp(ctk.CTk):
    """
    The main application window for the Students Management System,
    using CustomTkinter for a modern GUI.
    """
    def __init__(self):
        super().__init__()
        self.title("Students Management System")
        self.geometry("1400x800") # Increased size for better layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Set CustomTkinter appearance and theme
        ctk.set_appearance_mode("System") # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue") # Themes: "blue" (default), "green", "dark-blue"

        # Initialize services
        self.student_service = StudentService()
        self.grade_service = GradeService()
        self.subject_service = SubjectService()
        self.academic_year_service = AcademicYearService()
        self.semester_service = SemesterService()
        self.exam_service = ExamService()
        self.exam_result_service = ExamResultService()
        self.semester_result_service = SemesterResultService()
        self.yearly_result_service = YearlyResultService()

        self._create_widgets()
        self._load_initial_data() # Load some initial data for dropdowns etc.

    def _create_widgets(self):
        """
        Creates and arranges the main GUI widgets.
        Uses a CTkTabview (tabbed interface) for different modules.
        """
        self.tab_view = ctk.CTkTabview(self, width=1380, height=780)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create tabs
        self.student_tab = self.tab_view.add("Students")
        self.grade_tab = self.tab_view.add("Grades")
        self.subject_tab = self.tab_view.add("Subjects")
        self.academic_year_tab = self.tab_view.add("Academic Years")
        self.semester_tab = self.tab_view.add("Semesters")
        self.exam_tab = self.tab_view.add("Exams/CATs")
        self.exam_result_tab = self.tab_view.add("Exam Results")
        self.semester_result_tab = self.tab_view.add("Semester Results")
        self.yearly_result_tab = self.tab_view.add("Yearly Results")

        # Configure tab grids to expand content
        self.student_tab.grid_columnconfigure(0, weight=1)
        self.student_tab.grid_rowconfigure(2, weight=1) # Treeview row
        self.grade_tab.grid_columnconfigure(0, weight=1)
        self.grade_tab.grid_rowconfigure(2, weight=1)
        self.subject_tab.grid_columnconfigure(0, weight=1)
        self.subject_tab.grid_rowconfigure(2, weight=1)
        self.academic_year_tab.grid_columnconfigure(0, weight=1)
        self.academic_year_tab.grid_rowconfigure(2, weight=1)
        self.semester_tab.grid_columnconfigure(0, weight=1)
        self.semester_tab.grid_rowconfigure(2, weight=1)
        self.exam_tab.grid_columnconfigure(0, weight=1)
        self.exam_tab.grid_rowconfigure(2, weight=1)
        self.exam_result_tab.grid_columnconfigure(0, weight=1)
        self.exam_result_tab.grid_rowconfigure(2, weight=1)
        self.semester_result_tab.grid_columnconfigure(0, weight=1)
        self.semester_result_tab.grid_rowconfigure(1, weight=1) # Treeview row
        self.yearly_result_tab.grid_columnconfigure(0, weight=1)
        self.yearly_result_tab.grid_rowconfigure(1, weight=1) # Treeview row


        # Populate each tab
        self._setup_student_tab()
        self._setup_grade_tab()
        self._setup_subject_tab()
        self._setup_academic_year_tab()
        self._setup_semester_tab()
        self._setup_exam_tab()
        self._setup_exam_result_tab()
        self._setup_semester_result_tab()
        self._setup_yearly_result_tab()

    def _load_initial_data(self):
        """
        Loads initial data into the database if it's empty.
        This ensures we have some default grades, subjects, etc.
        """
        # Load grades
        if not self.grade_service.get_all_grades():
            print("No grades found, populating default grades...")
            for i in range(1, 9):
                self.grade_service.add_grade(f"Grade {i}", f"Grade {i} level")
            show_info_message("Setup Complete", "Default grades (1-8) have been added.")

        # Load subjects
        if not self.subject_service.get_all_subjects():
            print("No subjects found, populating default subjects...")
            predefined_subjects = [
                {'name': 'Mathematics', 'description': 'Study of numbers and shapes'},
                {'name': 'Science', 'description': 'Study of the natural world'},
                {'name': 'English', 'description': 'Language arts'},
                {'name': 'Kiswahili', 'description': 'National language'},
                {'name': 'Social Studies', 'description': 'History and Geography'},
                {'name': 'Religious Education', 'description': 'Study of religion'},
                {'name': 'Art and Craft', 'description': 'Creative expression'},
                {'name': 'Physical Education', 'description': 'Sports and fitness'}
            ]
            for subject_data in predefined_subjects:
                self.subject_service.add_subject(subject_data['name'], subject_data['description'])
            show_info_message("Setup Complete", "Default subjects have been added.")

        # Load academic years
        if not self.academic_year_service.get_all_academic_years():
            print("No academic years found, populating default academic years...")
            self.academic_year_service.add_academic_year("2023/2024", "2023-09-01", "2024-07-31")
            self.academic_year_service.add_academic_year("2024/2025", "2024-09-01", "2025-07-31")
            show_info_message("Setup Complete", "Default academic years have been added.")

        # Load semesters
        if not self.semester_service.get_all_semesters():
            print("No semesters found, populating default semesters...")
            self.semester_service.add_semester("Semester 1", "2023-09-01", "2024-01-31")
            self.semester_service.add_semester("Semester 2", "2024-02-01", "2024-07-31")
            show_info_message("Setup Complete", "Default semesters have been added.")

        # Refresh data in all tabs after initial load
        self.refresh_all_tabs()

    def refresh_all_tabs(self):
        """Refreshes data displayed in all tabs."""
        self._load_students_to_treeview()
        self._load_grades_to_treeview()
        self._load_subjects_to_treeview()
        self._load_academic_years_to_treeview()
        self._load_semesters_to_treeview()
        self._load_exams_to_treeview()
        self._load_exam_results_to_treeview()
        self._load_semester_results_to_treeview()
        self._load_yearly_results_to_treeview()

        # Update dropdowns in Student tab if needed
        self._populate_grade_dropdown()
        self._populate_exam_dropdowns() # For exam results tab
        self._populate_student_dropdowns() # For exam results tab
        self._populate_subject_dropdowns() # For exam results tab
        self._populate_academic_year_dropdowns() # For exam results, semester results, yearly results
        self._populate_semester_dropdowns() # For exam results, semester results

    def _setup_student_tab(self):
        """Sets up the Students tab GUI."""
        # Frame for input fields
        input_frame = ctk.CTkFrame(self.student_tab, corner_radius=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1) # Allow entry field to expand

        ctk.CTkLabel(input_frame, text="Student Details", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(input_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.student_name_entry = ctk.CTkEntry(input_frame, width=300)
        self.student_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Student ID:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.student_id_entry = ctk.CTkEntry(input_frame, width=300)
        self.student_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Contact Info:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.student_contact_entry = ctk.CTkEntry(input_frame, width=300)
        self.student_contact_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Current Grade:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.grade_options = []
        self.grade_id_map = {} # Map grade name to ID
        self.student_grade_combobox = ctk.CTkComboBox(input_frame, state="readonly", width=300, values=self.grade_options)
        self.student_grade_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.student_grade_combobox.bind("<<ComboboxSelected>>", self._on_grade_selected) # Bind event

        # Buttons
        button_frame = ctk.CTkFrame(self.student_tab, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure((0,1,2,3), weight=1) # Distribute buttons evenly

        ctk.CTkButton(button_frame, text="Add Student", command=self._add_student).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Update Student", command=self._update_student).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Delete Student", command=self._delete_student).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Clear Fields", command=self._clear_student_fields).grid(row=0, column=3, padx=5, pady=5, sticky="ew")


        # Treeview for displaying students
        self.student_tree = ttk.Treeview(self.student_tab, columns=("ID", "Name", "Student ID", "Contact Info", "Grade"), show="headings")
        self.student_tree.heading("ID", text="ID")
        self.student_tree.heading("Name", text="Name")
        self.student_tree.heading("Student ID", text="Student ID")
        self.student_tree.heading("Contact Info", text="Contact Info")
        self.student_tree.heading("Grade", text="Grade")

        self.student_tree.column("ID", width=50, stretch=ctk.NO)
        self.student_tree.column("Name", width=150)
        self.student_tree.column("Student ID", width=100)
        self.student_tree.column("Contact Info", width=200)
        self.student_tree.column("Grade", width=100)

        self.student_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.student_tree.bind("<<TreeviewSelect>>", self._on_student_select)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.student_tab, orient="vertical", command=self.student_tree.yview)
        scrollbar.grid(row=2, column=1, sticky="ns", pady=10)
        self.student_tree.configure(yscrollcommand=scrollbar.set)


        self._load_students_to_treeview()
        self._populate_grade_dropdown()

    def _populate_grade_dropdown(self):
        """Populates the grade combobox with available grades."""
        grades = self.grade_service.get_all_grades()
        self.grade_options = [grade.name for grade in grades]
        self.grade_id_map = {grade.name: grade.id for grade in grades}
        self.student_grade_combobox.configure(values=self.grade_options)
        if self.grade_options:
            self.student_grade_combobox.set(self.grade_options[0]) # Set default
        else:
            self.student_grade_combobox.set("")

    def _on_grade_selected(self, event):
        """Handles selection in the grade combobox."""
        selected_grade_name = self.student_grade_combobox.get()
        # You can use self.grade_id_map[selected_grade_name] to get the ID

    def _load_students_to_treeview(self):
        """Loads student data into the Treeview."""
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        students = self.student_service.get_all_students()
        for student in students:
            self.student_tree.insert("", "end", values=(
                student['id'],
                student['name'],
                student['student_id'],
                student['contact_info'],
                student['grade_name'] # Use grade_name from the joined query
            ), iid=student['id']) # Use student ID as iid for easy lookup

    def _on_student_select(self, event):
        """Populates entry fields when a student is selected in the Treeview."""
        selected_item = self.student_tree.focus()
        if selected_item:
            values = self.student_tree.item(selected_item, 'values')
            self.student_name_entry.delete(0, ctk.END)
            self.student_name_entry.insert(0, values[1])
            self.student_id_entry.delete(0, ctk.END)
            self.student_id_entry.insert(0, values[2])
            self.student_contact_entry.delete(0, ctk.END)
            self.student_contact_entry.insert(0, values[3])
            # Set combobox value
            grade_name = values[4]
            if grade_name in self.grade_options:
                self.student_grade_combobox.set(grade_name)
            else:
                self.student_grade_combobox.set("") # Clear if grade name not found

    def _add_student(self):
        """Adds a new student to the database."""
        name = self.student_name_entry.get().strip()
        student_id = self.student_id_entry.get().strip()
        contact_info = self.student_contact_entry.get().strip()
        selected_grade_name = self.student_grade_combobox.get()
        current_grade_id = self.grade_id_map.get(selected_grade_name)

        if not name or not student_id or not current_grade_id:
            show_error_message("Input Error", "Name, Student ID, and Current Grade are required.")
            return
        if not is_valid_student_id(student_id):
            show_error_message("Input Error", "Invalid Student ID format.")
            return
        if contact_info and not is_valid_email(contact_info):
            show_error_message("Input Error", "Invalid Contact Info (email format expected).")
            return

        if self.student_service.get_student_by_unique_id(student_id):
            show_error_message("Input Error", "Student with this ID already exists.")
            return

        new_student = self.student_service.add_student(name, student_id, contact_info, current_grade_id)
        if new_student:
            show_info_message("Success", f"Student '{name}' added successfully.")
            self._clear_student_fields()
            self._load_students_to_treeview()
        else:
            show_error_message("Error", "Failed to add student. Check logs.")

    def _update_student(self):
        """Updates an existing student's information."""
        selected_item = self.student_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select a student to update.")
            return

        student_db_id = self.student_tree.item(selected_item, 'iid')
        name = self.student_name_entry.get().strip()
        student_id_text = self.student_id_entry.get().strip() # This is the new unique ID
        contact_info = self.student_contact_entry.get().strip()
        selected_grade_name = self.student_grade_combobox.get()
        current_grade_id = self.grade_id_map.get(selected_grade_name)

        if not name or not student_id_text or not current_grade_id:
            show_error_message("Input Error", "Name, Student ID, and Current Grade are required.")
            return
        if not is_valid_student_id(student_id_text):
            show_error_message("Input Error", "Invalid Student ID format.")
            return
        if contact_info and not is_valid_email(contact_info):
            show_error_message("Input Error", "Invalid Contact Info (email format expected).")
            return

        # Check if the new student_id_text is already taken by another student
        existing_student = self.student_service.get_student_by_unique_id(student_id_text)
        if existing_student and existing_student.id != student_db_id:
            show_error_message("Input Error", "Another student with this ID already exists.")
            return

        updated = self.student_service.update_student(
            student_db_id,
            name=name,
            student_unique_id=student_id_text, # Pass the new unique ID
            contact_info=contact_info,
            current_grade_id=current_grade_id
        )
        if updated:
            show_info_message("Success", f"Student '{name}' updated successfully.")
            self._clear_student_fields()
            self._load_students_to_treeview()
        else:
            show_error_message("Error", "Failed to update student. Check logs.")

    def _delete_student(self):
        """Deletes a selected student from the database."""
        selected_item = self.student_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select a student to delete.")
            return

        student_db_id = self.student_tree.item(selected_item, 'iid')
        student_name = self.student_tree.item(selected_item, 'values')[1] # Get name for confirmation

        if ask_confirmation("Confirm Deletion", f"Are you sure you want to delete student '{student_name}'? This action cannot be undone."):
            deleted = self.student_service.delete_student(student_db_id)
            if deleted:
                show_info_message("Success", f"Student '{student_name}' deleted successfully.")
                self._clear_student_fields()
                self._load_students_to_treeview()
            else:
                show_error_message("Error", "Failed to delete student. Check logs.")

    def _clear_student_fields(self):
        """Clears the student input fields."""
        self.student_name_entry.delete(0, ctk.END)
        self.student_id_entry.delete(0, ctk.END)
        self.student_contact_entry.delete(0, ctk.END)
        if self.grade_options:
            self.student_grade_combobox.set(self.grade_options[0]) # Reset to first option
        else:
            self.student_grade_combobox.set("") # Clear if no options


    # --- Grade Tab Setup ---
    def _setup_grade_tab(self):
        """Sets up the Grades tab GUI."""
        input_frame = ctk.CTkFrame(self.grade_tab, corner_radius=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Grade Details", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(input_frame, text="Grade Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.grade_name_entry = ctk.CTkEntry(input_frame, width=300)
        self.grade_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.grade_description_entry = ctk.CTkEntry(input_frame, width=300)
        self.grade_description_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        button_frame = ctk.CTkFrame(self.grade_tab, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure((0,1,2,3), weight=1)

        ctk.CTkButton(button_frame, text="Add Grade", command=self._add_grade).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Update Grade", command=self._update_grade).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Delete Grade", command=self._delete_grade).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Clear Fields", command=self._clear_grade_fields).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.grade_tree = ttk.Treeview(self.grade_tab, columns=("ID", "Name", "Description"), show="headings")
        self.grade_tree.heading("ID", text="ID")
        self.grade_tree.heading("Name", text="Name")
        self.grade_tree.heading("Description", text="Description")

        self.grade_tree.column("ID", width=50, stretch=ctk.NO)
        self.grade_tree.column("Name", width=150)
        self.grade_tree.column("Description", width=300)

        self.grade_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.grade_tab, orient="vertical", command=self.grade_tree.yview)
        scrollbar.grid(row=2, column=1, sticky="ns", pady=10)
        self.grade_tree.configure(yscrollcommand=scrollbar.set)

        self.grade_tree.bind("<<TreeviewSelect>>", self._on_grade_select)

        self._load_grades_to_treeview()

    def _load_grades_to_treeview(self):
        """Loads grade data into the Treeview."""
        for item in self.grade_tree.get_children():
            self.grade_tree.delete(item)
        grades = self.grade_service.get_all_grades()
        for grade in grades:
            self.grade_tree.insert("", "end", values=(grade.id, grade.name, grade.description), iid=grade.id)

    def _on_grade_select(self, event):
        """Populates entry fields when a grade is selected in the Treeview."""
        selected_item = self.grade_tree.focus()
        if selected_item:
            values = self.grade_tree.item(selected_item, 'values')
            self.grade_name_entry.delete(0, ctk.END)
            self.grade_name_entry.insert(0, values[1])
            self.grade_description_entry.delete(0, ctk.END)
            self.grade_description_entry.insert(0, values[2])

    def _add_grade(self):
        """Adds a new grade to the database."""
        name = self.grade_name_entry.get().strip()
        description = self.grade_description_entry.get().strip()

        if not name:
            show_error_message("Input Error", "Grade Name is required.")
            return

        if self.grade_service.get_grade_by_name(name):
            show_error_message("Input Error", "Grade with this name already exists.")
            return

        new_grade = self.grade_service.add_grade(name, description if description else None)
        if new_grade:
            show_info_message("Success", f"Grade '{name}' added successfully.")
            self._clear_grade_fields()
            self._load_grades_to_treeview()
            self._populate_grade_dropdown() # Refresh student dropdown
        else:
            show_error_message("Error", "Failed to add grade. Check logs.")

    def _update_grade(self):
        """Updates an existing grade's information."""
        selected_item = self.grade_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select a grade to update.")
            return

        grade_db_id = self.grade_tree.item(selected_item, 'iid')
        name = self.grade_name_entry.get().strip()
        description = self.grade_description_entry.get().strip()

        if not name:
            show_error_message("Input Error", "Grade Name is required.")
            return

        # Check if the new name is already taken by another grade
        existing_grade = self.grade_service.get_grade_by_name(name)
        if existing_grade and existing_grade.id != grade_db_id:
            show_error_message("Input Error", "Another grade with this name already exists.")
            return

        updated = self.grade_service.update_grade(
            grade_db_id,
            name=name,
            description=description if description else None
        )
        if updated:
            show_info_message("Success", f"Grade '{name}' updated successfully.")
            self._clear_grade_fields()
            self._load_grades_to_treeview()
            self._populate_grade_dropdown() # Refresh student dropdown
        else:
            show_error_message("Error", "Failed to update grade. Check logs.")

    def _delete_grade(self):
        """Deletes a selected grade from the database."""
        selected_item = self.grade_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select a grade to delete.")
            return

        grade_db_id = self.grade_tree.item(selected_item, 'iid')
        grade_name = self.grade_tree.item(selected_item, 'values')[1]

        # Check for dependencies (e.g., students assigned to this grade)
        # This is a simple check; a more robust system would query the Students table.
        students_in_grade_query = "SELECT COUNT(*) FROM Students WHERE current_grade_id = ?"
        count_students = self.student_service.db_manager.fetch_one(students_in_grade_query, (grade_db_id,))['COUNT(*)']
        if count_students > 0:
            show_error_message("Deletion Error", f"Cannot delete grade '{grade_name}'. {count_students} students are currently assigned to this grade.")
            return

        if ask_confirmation("Confirm Deletion", f"Are you sure you want to delete grade '{grade_name}'? This action cannot be undone."):
            deleted = self.grade_service.delete_grade(grade_db_id)
            if deleted:
                show_info_message("Success", f"Grade '{grade_name}' deleted successfully.")
                self._clear_grade_fields()
                self._load_grades_to_treeview()
                self._populate_grade_dropdown() # Refresh student dropdown
            else:
                show_error_message("Error", "Failed to delete grade. Check logs.")

    def _clear_grade_fields(self):
        """Clears the grade input fields."""
        self.grade_name_entry.delete(0, ctk.END)
        self.grade_description_entry.delete(0, ctk.END)


    # --- Subject Tab Setup ---
    def _setup_subject_tab(self):
        """Sets up the Subjects tab GUI."""
        input_frame = ctk.CTkFrame(self.subject_tab, corner_radius=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Subject Details", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(input_frame, text="Subject Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.subject_name_entry = ctk.CTkEntry(input_frame, width=300)
        self.subject_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.subject_description_entry = ctk.CTkEntry(input_frame, width=300)
        self.subject_description_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        button_frame = ctk.CTkFrame(self.subject_tab, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure((0,1,2,3), weight=1)

        ctk.CTkButton(button_frame, text="Add Subject", command=self._add_subject).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Update Subject", command=self._update_subject).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Delete Subject", command=self._delete_subject).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Clear Fields", command=self._clear_subject_fields).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.subject_tree = ttk.Treeview(self.subject_tab, columns=("ID", "Name", "Description"), show="headings")
        self.subject_tree.heading("ID", text="ID")
        self.subject_tree.heading("Name", text="Name")
        self.subject_tree.heading("Description", text="Description")

        self.subject_tree.column("ID", width=50, stretch=ctk.NO)
        self.subject_tree.column("Name", width=150)
        self.subject_tree.column("Description", width=300)

        self.subject_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.subject_tab, orient="vertical", command=self.subject_tree.yview)
        scrollbar.grid(row=2, column=1, sticky="ns", pady=10)
        self.subject_tree.configure(yscrollcommand=scrollbar.set)

        self.subject_tree.bind("<<TreeviewSelect>>", self._on_subject_select)

        self._load_subjects_to_treeview()

    def _load_subjects_to_treeview(self):
        """Loads subject data into the Treeview."""
        for item in self.subject_tree.get_children():
            self.subject_tree.delete(item)
        subjects = self.subject_service.get_all_subjects()
        for subject in subjects:
            self.subject_tree.insert("", "end", values=(subject.id, subject.name, subject.description), iid=subject.id)

    def _on_subject_select(self, event):
        """Populates entry fields when a subject is selected in the Treeview."""
        selected_item = self.subject_tree.focus()
        if selected_item:
            values = self.subject_tree.item(selected_item, 'values')
            self.subject_name_entry.delete(0, ctk.END)
            self.subject_name_entry.insert(0, values[1])
            self.subject_description_entry.delete(0, ctk.END)
            self.subject_description_entry.insert(0, values[2])

    def _add_subject(self):
        """Adds a new subject to the database."""
        name = self.subject_name_entry.get().strip()
        description = self.subject_description_entry.get().strip()

        if not name:
            show_error_message("Input Error", "Subject Name is required.")
            return

        if self.subject_service.get_subject_by_name(name):
            show_error_message("Input Error", "Subject with this name already exists.")
            return

        new_subject = self.subject_service.add_subject(name, description if description else None)
        if new_subject:
            show_info_message("Success", f"Subject '{name}' added successfully.")
            self._clear_subject_fields()
            self._load_subjects_to_treeview()
            self._populate_subject_dropdowns() # Refresh dropdowns that use subjects
        else:
            show_error_message("Error", "Failed to add subject. Check logs.")

    def _update_subject(self):
        """Updates an existing subject's information."""
        selected_item = self.subject_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select a subject to update.")
            return

        subject_db_id = self.subject_tree.item(selected_item, 'iid')
        name = self.subject_name_entry.get().strip()
        description = self.subject_description_entry.get().strip()

        if not name:
            show_error_message("Input Error", "Subject Name is required.")
            return

        existing_subject = self.subject_service.get_subject_by_name(name)
        if existing_subject and existing_subject.id != subject_db_id:
            show_error_message("Input Error", "Another subject with this name already exists.")
            return

        updated = self.subject_service.update_subject(
            subject_db_id,
            name=name,
            description=description if description else None
        )
        if updated:
            show_info_message("Success", f"Subject '{name}' updated successfully.")
            self._clear_subject_fields()
            self._load_subjects_to_treeview()
            self._populate_subject_dropdowns() # Refresh dropdowns that use subjects
        else:
            show_error_message("Error", "Failed to update subject. Check logs.")

    def _delete_subject(self):
        """Deletes a selected subject from the database."""
        selected_item = self.subject_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select a subject to delete.")
            return

        subject_db_id = self.subject_tree.item(selected_item, 'iid')
        subject_name = self.subject_tree.item(selected_item, 'values')[1]

        # Check for dependencies (e.g., exam results linked to this subject)
        exam_results_for_subject_query = "SELECT COUNT(*) FROM ExamResults WHERE subject_id = ?"
        count_results = self.subject_service.db_manager.fetch_one(exam_results_for_subject_query, (subject_db_id,))['COUNT(*)']
        if count_results > 0:
            show_error_message("Deletion Error", f"Cannot delete subject '{subject_name}'. {count_results} exam results are linked to this subject.")
            return

        if ask_confirmation("Confirm Deletion", f"Are you sure you want to delete subject '{subject_name}'? This action cannot be undone."):
            deleted = self.subject_service.delete_subject(subject_db_id)
            if deleted:
                show_info_message("Success", f"Subject '{subject_name}' deleted successfully.")
                self._clear_subject_fields()
                self._load_subjects_to_treeview()
                self._populate_subject_dropdowns() # Refresh dropdowns that use subjects
            else:
                show_error_message("Error", "Failed to delete subject. Check logs.")

    def _clear_subject_fields(self):
        """Clears the subject input fields."""
        self.subject_name_entry.delete(0, ctk.END)
        self.subject_description_entry.delete(0, ctk.END)


    # --- Academic Year Tab Setup ---
    def _setup_academic_year_tab(self):
        """Sets up the Academic Years tab GUI."""
        input_frame = ctk.CTkFrame(self.academic_year_tab, corner_radius=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Academic Year Details", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(input_frame, text="Year Name (e.g., 2023/2024):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ay_name_entry = ctk.CTkEntry(input_frame, width=300)
        self.ay_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ay_start_date_entry = ctk.CTkEntry(input_frame, width=300)
        self.ay_start_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="End Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.ay_end_date_entry = ctk.CTkEntry(input_frame, width=300)
        self.ay_end_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        button_frame = ctk.CTkFrame(self.academic_year_tab, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure((0,1,2,3), weight=1)

        ctk.CTkButton(button_frame, text="Add Academic Year", command=self._add_academic_year).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Update Academic Year", command=self._update_academic_year).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Delete Academic Year", command=self._delete_academic_year).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Clear Fields", command=self._clear_academic_year_fields).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.academic_year_tree = ttk.Treeview(self.academic_year_tab, columns=("ID", "Year Name", "Start Date", "End Date"), show="headings")
        self.academic_year_tree.heading("ID", text="ID")
        self.academic_year_tree.heading("Year Name", text="Year Name")
        self.academic_year_tree.heading("Start Date", text="Start Date")
        self.academic_year_tree.heading("End Date", text="End Date")

        self.academic_year_tree.column("ID", width=50, stretch=ctk.NO)
        self.academic_year_tree.column("Year Name", width=150)
        self.academic_year_tree.column("Start Date", width=100)
        self.academic_year_tree.column("End Date", width=100)

        self.academic_year_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.academic_year_tab, orient="vertical", command=self.academic_year_tree.yview)
        scrollbar.grid(row=2, column=1, sticky="ns", pady=10)
        self.academic_year_tree.configure(yscrollcommand=scrollbar.set)

        self.academic_year_tree.bind("<<TreeviewSelect>>", self._on_academic_year_select)

        self._load_academic_years_to_treeview()

    def _load_academic_years_to_treeview(self):
        """Loads academic year data into the Treeview."""
        for item in self.academic_year_tree.get_children():
            self.academic_year_tree.delete(item)
        academic_years = self.academic_year_service.get_all_academic_years()
        for ay in academic_years:
            self.academic_year_tree.insert("", "end", values=(ay.id, ay.year_name, ay.start_date, ay.end_date), iid=ay.id)

    def _on_academic_year_select(self, event):
        """Populates entry fields when an academic year is selected in the Treeview."""
        selected_item = self.academic_year_tree.focus()
        if selected_item:
            values = self.academic_year_tree.item(selected_item, 'values')
            self.ay_name_entry.delete(0, ctk.END)
            self.ay_name_entry.insert(0, values[1])
            self.ay_start_date_entry.delete(0, ctk.END)
            self.ay_start_date_entry.insert(0, values[2])
            self.ay_end_date_entry.delete(0, ctk.END)
            self.ay_end_date_entry.insert(0, values[3])

    def _add_academic_year(self):
        """Adds a new academic year to the database."""
        year_name = self.ay_name_entry.get().strip()
        start_date = self.ay_start_date_entry.get().strip()
        end_date = self.ay_end_date_entry.get().strip()

        if not year_name or not start_date or not end_date:
            show_error_message("Input Error", "All fields are required.")
            return
        if not is_valid_date(start_date) or not is_valid_date(end_date):
            show_error_message("Input Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        if self.academic_year_service.get_academic_year_by_name(year_name):
            show_error_message("Input Error", "Academic Year with this name already exists.")
            return

        new_ay = self.academic_year_service.add_academic_year(year_name, start_date, end_date)
        if new_ay:
            show_info_message("Success", f"Academic Year '{year_name}' added successfully.")
            self._clear_academic_year_fields()
            self._load_academic_years_to_treeview()
            self._populate_academic_year_dropdowns() # Refresh dropdowns
        else:
            show_error_message("Error", "Failed to add academic year. Check logs.")

    def _update_academic_year(self):
        """Updates an existing academic year's information."""
        selected_item = self.academic_year_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select an academic year to update.")
            return

        ay_db_id = self.academic_year_tree.item(selected_item, 'iid')
        year_name = self.ay_name_entry.get().strip()
        start_date = self.ay_start_date_entry.get().strip()
        end_date = self.ay_end_date_entry.get().strip()

        if not year_name or not start_date or not end_date:
            show_error_message("Input Error", "All fields are required.")
            return
        if not is_valid_date(start_date) or not is_valid_date(end_date):
            show_error_message("Input Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        existing_ay = self.academic_year_service.get_academic_year_by_name(year_name)
        if existing_ay and existing_ay.id != ay_db_id:
            show_error_message("Input Error", "Another academic year with this name already exists.")
            return

        updated = self.academic_year_service.update_academic_year(
            ay_db_id,
            year_name=year_name,
            start_date=start_date,
            end_date=end_date
        )
        if updated:
            show_info_message("Success", f"Academic Year '{year_name}' updated successfully.")
            self._clear_academic_year_fields()
            self._load_academic_years_to_treeview()
            self._populate_academic_year_dropdowns() # Refresh dropdowns
        else:
            show_error_message("Error", "Failed to update academic year. Check logs.")

    def _delete_academic_year(self):
        """Deletes a selected academic year from the database."""
        selected_item = self.academic_year_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select an academic year to delete.")
            return

        ay_db_id = self.academic_year_tree.item(selected_item, 'iid')
        ay_name = self.academic_year_tree.item(selected_item, 'values')[1]

        # Check for dependencies (enrollments, exams, results)
        enrollments_query = "SELECT COUNT(*) FROM Enrollments WHERE academic_year_id = ?"
        exams_query = "SELECT COUNT(*) FROM Exams WHERE academic_year_id = ?"
        sem_results_query = "SELECT COUNT(*) FROM SemesterResults WHERE academic_year_id = ?"
        yearly_results_query = "SELECT COUNT(*) FROM YearlyResults WHERE academic_year_id = ?"

        count_enrollments = self.academic_year_service.db_manager.fetch_one(enrollments_query, (ay_db_id,))['COUNT(*)']
        count_exams = self.academic_year_service.db_manager.fetch_one(exams_query, (ay_db_id,))['COUNT(*)']
        count_sem_results = self.academic_year_service.db_manager.fetch_one(sem_results_query, (ay_db_id,))['COUNT(*)']
        count_yearly_results = self.academic_year_service.db_manager.fetch_one(yearly_results_query, (ay_db_id,))['COUNT(*)']

        if any([count_enrollments, count_exams, count_sem_results, count_yearly_results]):
            error_msg = f"Cannot delete Academic Year '{ay_name}'. It has existing dependencies:\n"
            if count_enrollments: error_msg += f"- {count_enrollments} enrollments\n"
            if count_exams: error_msg += f"- {count_exams} exams\n"
            if count_sem_results: error_msg += f"- {count_sem_results} semester results\n"
            if count_yearly_results: error_msg += f"- {count_yearly_results} yearly results\n"
            show_error_message("Deletion Error", error_msg)
            return

        if ask_confirmation("Confirm Deletion", f"Are you sure you want to delete Academic Year '{ay_name}'? This action cannot be undone."):
            deleted = self.academic_year_service.delete_academic_year(ay_db_id)
            if deleted:
                show_info_message("Success", f"Academic Year '{ay_name}' deleted successfully.")
                self._clear_academic_year_fields()
                self._load_academic_years_to_treeview()
                self._populate_academic_year_dropdowns() # Refresh dropdowns
            else:
                show_error_message("Error", "Failed to delete academic year. Check logs.")

    def _clear_academic_year_fields(self):
        """Clears the academic year input fields."""
        self.ay_name_entry.delete(0, ctk.END)
        self.ay_start_date_entry.delete(0, ctk.END)
        self.ay_end_date_entry.delete(0, ctk.END)


    # --- Semester Tab Setup ---
    def _setup_semester_tab(self):
        """Sets up the Semesters tab GUI."""
        input_frame = ctk.CTkFrame(self.semester_tab, corner_radius=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Semester Details", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(input_frame, text="Semester Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.semester_name_entry = ctk.CTkEntry(input_frame, width=300)
        self.semester_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.semester_start_date_entry = ctk.CTkEntry(input_frame, width=300)
        self.semester_start_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="End Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.semester_end_date_entry = ctk.CTkEntry(input_frame, width=300)
        self.semester_end_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        button_frame = ctk.CTkFrame(self.semester_tab, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure((0,1,2,3), weight=1)

        ctk.CTkButton(button_frame, text="Add Semester", command=self._add_semester).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Update Semester", command=self._update_semester).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Delete Semester", command=self._delete_semester).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Clear Fields", command=self._clear_semester_fields).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.semester_tree = ttk.Treeview(self.semester_tab, columns=("ID", "Name", "Start Date", "End Date"), show="headings")
        self.semester_tree.heading("ID", text="ID")
        self.semester_tree.heading("Name", text="Name")
        self.semester_tree.heading("Start Date", text="Start Date")
        self.semester_tree.heading("End Date", text="End Date")

        self.semester_tree.column("ID", width=50, stretch=ctk.NO)
        self.semester_tree.column("Name", width=150)
        self.semester_tree.column("Start Date", width=100)
        self.semester_tree.column("End Date", width=100)

        self.semester_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.semester_tab, orient="vertical", command=self.semester_tree.yview)
        scrollbar.grid(row=2, column=1, sticky="ns", pady=10)
        self.semester_tree.configure(yscrollcommand=scrollbar.set)

        self.semester_tree.bind("<<TreeviewSelect>>", self._on_semester_select)

        self._load_semesters_to_treeview()

    def _load_semesters_to_treeview(self):
        """Loads semester data into the Treeview."""
        for item in self.semester_tree.get_children():
            self.semester_tree.delete(item)
        semesters = self.semester_service.get_all_semesters()
        for sem in semesters:
            self.semester_tree.insert("", "end", values=(sem.id, sem.name, sem.start_date, sem.end_date), iid=sem.id)

    def _on_semester_select(self, event):
        """Populates entry fields when a semester is selected in the Treeview."""
        selected_item = self.semester_tree.focus()
        if selected_item:
            values = self.semester_tree.item(selected_item, 'values')
            self.semester_name_entry.delete(0, ctk.END)
            self.semester_name_entry.insert(0, values[1])
            self.semester_start_date_entry.delete(0, ctk.END)
            self.semester_start_date_entry.insert(0, values[2])
            self.semester_end_date_entry.delete(0, ctk.END)
            self.semester_end_date_entry.insert(0, values[3])

    def _add_semester(self):
        """Adds a new semester to the database."""
        name = self.semester_name_entry.get().strip()
        start_date = self.semester_start_date_entry.get().strip()
        end_date = self.semester_end_date_entry.get().strip()

        if not name:
            show_error_message("Input Error", "Semester Name is required.")
            return
        if start_date and not is_valid_date(start_date):
            show_error_message("Input Error", "Invalid Start Date format. Use YYYY-MM-DD.")
            return
        if end_date and not is_valid_date(end_date):
            show_error_message("Input Error", "Invalid End Date format. Use YYYY-MM-DD.")
            return

        if self.semester_service.get_semester_by_name(name):
            show_error_message("Input Error", "Semester with this name already exists.")
            return

        new_sem = self.semester_service.add_semester(name, start_date if start_date else None, end_date if end_date else None)
        if new_sem:
            show_info_message("Success", f"Semester '{name}' added successfully.")
            self._clear_semester_fields()
            self._load_semesters_to_treeview()
            self._populate_semester_dropdowns() # Refresh dropdowns
        else:
            show_error_message("Error", "Failed to add semester. Check logs.")

    def _update_semester(self):
        """Updates an existing semester's information."""
        selected_item = self.semester_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select a semester to update.")
            return

        semester_db_id = self.semester_tree.item(selected_item, 'iid')
        name = self.semester_name_entry.get().strip()
        start_date = self.semester_start_date_entry.get().strip()
        end_date = self.semester_end_date_entry.get().strip()

        if not name:
            show_error_message("Input Error", "Semester Name is required.")
            return
        if start_date and not is_valid_date(start_date):
            show_error_message("Input Error", "Invalid Start Date format. Use YYYY-MM-DD.")
            return
        if end_date and not is_valid_date(end_date):
            show_error_message("Input Error", "Invalid End Date format. Use YYYY-MM-DD.")
            return

        existing_sem = self.semester_service.get_semester_by_name(name)
        if existing_sem and existing_sem.id != semester_db_id:
            show_error_message("Input Error", "Another semester with this name already exists.")
            return

        updated = self.semester_service.update_semester(
            semester_db_id,
            name=name,
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None
        )
        if updated:
            show_info_message("Success", f"Semester '{name}' updated successfully.")
            self._clear_semester_fields()
            self._load_semesters_to_treeview()
            self._populate_semester_dropdowns() # Refresh dropdowns
        else:
            show_error_message("Error", "Failed to update semester. Check logs.")

    def _delete_semester(self):
        """Deletes a selected semester from the database."""
        selected_item = self.semester_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select a semester to delete.")
            return

        semester_db_id = self.semester_tree.item(selected_item, 'iid')
        semester_name = self.semester_tree.item(selected_item, 'values')[1]

        # Check for dependencies (exams, semester results)
        exams_query = "SELECT COUNT(*) FROM Exams WHERE semester_id = ?"
        sem_results_query = "SELECT COUNT(*) FROM SemesterResults WHERE semester_id = ?"

        count_exams = self.semester_service.db_manager.fetch_one(exams_query, (semester_db_id,))['COUNT(*)']
        count_sem_results = self.semester_service.db_manager.fetch_one(sem_results_query, (semester_db_id,))['COUNT(*)']

        if any([count_exams, count_sem_results]):
            error_msg = f"Cannot delete Semester '{semester_name}'. It has existing dependencies:\n"
            if count_exams: error_msg += f"- {count_exams} exams\n"
            if count_sem_results: error_msg += f"- {count_sem_results} semester results\n"
            show_error_message("Deletion Error", error_msg)
            return

        if ask_confirmation("Confirm Deletion", f"Are you sure you want to delete Semester '{semester_name}'? This action cannot be undone."):
            deleted = self.semester_service.delete_semester(semester_db_id)
            if deleted:
                show_info_message("Success", f"Semester '{semester_name}' deleted successfully.")
                self._clear_semester_fields()
                self._load_semesters_to_treeview()
                self._populate_semester_dropdowns() # Refresh dropdowns
            else:
                show_error_message("Error", "Failed to delete semester. Check logs.")

    def _clear_semester_fields(self):
        """Clears the semester input fields."""
        self.semester_name_entry.delete(0, ctk.END)
        self.semester_start_date_entry.delete(0, ctk.END)
        self.semester_end_date_entry.delete(0, ctk.END)


    # --- Exam/CAT Tab Setup ---
    def _setup_exam_tab(self):
        """Sets up the Exams/CATs tab GUI."""
        input_frame = ctk.CTkFrame(self.exam_tab, corner_radius=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Exam/CAT Details", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(input_frame, text="Exam Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.exam_name_entry = ctk.CTkEntry(input_frame, width=300)
        self.exam_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Academic Year:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.exam_ay_options = []
        self.exam_ay_id_map = {}
        self.exam_ay_combobox = ctk.CTkComboBox(input_frame, state="readonly", width=300, values=self.exam_ay_options)
        self.exam_ay_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Semester (Optional):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.exam_semester_options = ["None"] # Option for yearly exams
        self.exam_semester_id_map = {"None": None}
        self.exam_semester_combobox = ctk.CTkComboBox(input_frame, state="readonly", width=300, values=self.exam_semester_options)
        self.exam_semester_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Max Marks:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.exam_max_marks_entry = ctk.CTkEntry(input_frame, width=300)
        self.exam_max_marks_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.exam_max_marks_entry.insert(0, "100") # Default value

        button_frame = ctk.CTkFrame(self.exam_tab, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure((0,1,2,3), weight=1)

        ctk.CTkButton(button_frame, text="Add Exam/CAT", command=self._add_exam).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Update Exam/CAT", command=self._update_exam).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Delete Exam/CAT", command=self._delete_exam).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Clear Fields", command=self._clear_exam_fields).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.exam_tree = ttk.Treeview(self.exam_tab, columns=("ID", "Name", "Academic Year", "Semester", "Max Marks"), show="headings")
        self.exam_tree.heading("ID", text="ID")
        self.exam_tree.heading("Name", text="Name")
        self.exam_tree.heading("Academic Year", text="Academic Year")
        self.exam_tree.heading("Semester", text="Semester")
        self.exam_tree.heading("Max Marks", text="Max Marks")

        self.exam_tree.column("ID", width=50, stretch=ctk.NO)
        self.exam_tree.column("Name", width=150)
        self.exam_tree.column("Academic Year", width=100)
        self.exam_tree.column("Semester", width=100)
        self.exam_tree.column("Max Marks", width=80)

        self.exam_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.exam_tab, orient="vertical", command=self.exam_tree.yview)
        scrollbar.grid(row=2, column=1, sticky="ns", pady=10)
        self.exam_tree.configure(yscrollcommand=scrollbar.set)

        self.exam_tree.bind("<<TreeviewSelect>>", self._on_exam_select)

        self._populate_academic_year_dropdowns()
        self._populate_semester_dropdowns()
        self._load_exams_to_treeview()

    def _populate_academic_year_dropdowns(self):
        """Populates academic year comboboxes."""
        academic_years = self.academic_year_service.get_all_academic_years()
        self.exam_ay_options = [ay.year_name for ay in academic_years]
        self.exam_ay_id_map = {ay.year_name: ay.id for ay in academic_years}
        self.exam_ay_combobox.configure(values=self.exam_ay_options)
        if self.exam_ay_options:
            self.exam_ay_combobox.set(self.exam_ay_options[0])
        else:
            self.exam_ay_combobox.set("")

        # Also update the academic year dropdowns in other tabs if they exist
        if hasattr(self, 'exam_result_ay_combobox'):
            self.exam_result_ay_combobox.configure(values=self.exam_ay_options)
            if self.exam_ay_options: self.exam_result_ay_combobox.set(self.exam_ay_options[0])
            else: self.exam_result_ay_combobox.set("")
        if hasattr(self, 'semester_result_ay_combobox'):
            self.semester_result_ay_combobox.configure(values=self.exam_ay_options)
            if self.exam_ay_options: self.semester_result_ay_combobox.set(self.exam_ay_options[0])
            else: self.semester_result_ay_combobox.set("")
        if hasattr(self, 'yearly_result_ay_combobox'):
            self.yearly_result_ay_combobox.configure(values=self.exam_ay_options)
            if self.exam_ay_options: self.yearly_result_ay_combobox.set(self.exam_ay_options[0])
            else: self.yearly_result_ay_combobox.set("")


    def _populate_semester_dropdowns(self):
        """Populates semester comboboxes."""
        semesters = self.semester_service.get_all_semesters()
        self.exam_semester_options = ["None"] + [sem.name for sem in semesters]
        self.exam_semester_id_map = {"None": None}
        self.exam_semester_id_map.update({sem.name: sem.id for sem in semesters})
        self.exam_semester_combobox.configure(values=self.exam_semester_options)
        self.exam_semester_combobox.set("None") # Default to None

        # Also update the semester dropdowns in other tabs if they exist
        if hasattr(self, 'exam_result_semester_combobox'):
            self.exam_result_semester_combobox.configure(values=self.exam_semester_options)
            self.exam_result_semester_combobox.set("None")
        if hasattr(self, 'semester_result_semester_combobox'):
            self.semester_result_semester_combobox.configure(values=self.exam_semester_options)
            self.semester_result_semester_combobox.set("None")


    def _load_exams_to_treeview(self):
        """Loads exam data into the Treeview."""
        for item in self.exam_tree.get_children():
            self.exam_tree.delete(item)
        exams = self.exam_service.get_all_exams()
        for exam in exams:
            self.exam_tree.insert("", "end", values=(
                exam['id'],
                exam['name'],
                exam['academic_year_name'],
                exam['semester_name'] if exam['semester_name'] else "N/A",
                exam['max_marks']
            ), iid=exam['id'])

    def _on_exam_select(self, event):
        """Populates entry fields when an exam is selected in the Treeview."""
        selected_item = self.exam_tree.focus()
        if selected_item:
            values = self.exam_tree.item(selected_item, 'values')
            self.exam_name_entry.delete(0, ctk.END)
            self.exam_name_entry.insert(0, values[1])
            self.exam_max_marks_entry.delete(0, ctk.END)
            self.exam_max_marks_entry.insert(0, values[4])

            ay_name = values[2]
            if ay_name in self.exam_ay_options:
                self.exam_ay_combobox.set(ay_name)
            else:
                self.exam_ay_combobox.set("")

            semester_name = values[3]
            if semester_name in self.exam_semester_options:
                self.exam_semester_combobox.set(semester_name)
            else:
                self.exam_semester_combobox.set("None")

    def _add_exam(self):
        """Adds a new exam/CAT to the database."""
        name = self.exam_name_entry.get().strip()
        selected_ay_name = self.exam_ay_combobox.get()
        academic_year_id = self.exam_ay_id_map.get(selected_ay_name)
        selected_semester_name = self.exam_semester_combobox.get()
        semester_id = self.exam_semester_id_map.get(selected_semester_name)
        max_marks_str = self.exam_max_marks_entry.get().strip()

        if not name or not academic_year_id:
            show_error_message("Input Error", "Exam Name and Academic Year are required.")
            return
        if not max_marks_str or not is_valid_marks(max_marks_str):
            show_error_message("Input Error", "Max Marks must be a non-negative number.")
            return
        max_marks = float(max_marks_str)

        if self.exam_service.get_exam_by_name_and_period(name, academic_year_id, semester_id):
            show_error_message("Input Error", "An exam/CAT with this name already exists for this academic year and semester.")
            return

        new_exam = self.exam_service.add_exam(name, academic_year_id, semester_id, max_marks)
        if new_exam:
            show_info_message("Success", f"Exam/CAT '{name}' added successfully.")
            self._clear_exam_fields()
            self._load_exams_to_treeview()
            self._populate_exam_dropdowns() # Refresh dropdowns that use exams
        else:
            show_error_message("Error", "Failed to add exam/CAT. Check logs.")

    def _update_exam(self):
        """Updates an existing exam/CAT's information."""
        selected_item = self.exam_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select an exam/CAT to update.")
            return

        exam_db_id = self.exam_tree.item(selected_item, 'iid')
        name = self.exam_name_entry.get().strip()
        selected_ay_name = self.exam_ay_combobox.get()
        academic_year_id = self.exam_ay_id_map.get(selected_ay_name)
        selected_semester_name = self.exam_semester_combobox.get()
        semester_id = self.exam_semester_id_map.get(selected_semester_name)
        max_marks_str = self.exam_max_marks_entry.get().strip()

        if not name or not academic_year_id:
            show_error_message("Input Error", "Exam Name and Academic Year are required.")
            return
        if not max_marks_str or not is_valid_marks(max_marks_str):
            show_error_message("Input Error", "Max Marks must be a non-negative number.")
            return
        max_marks = float(max_marks_str)

        existing_exam = self.exam_service.get_exam_by_name_and_period(name, academic_year_id, semester_id)
        if existing_exam and existing_exam.id != exam_db_id:
            show_error_message("Input Error", "Another exam/CAT with this name already exists for this academic year and semester.")
            return

        updated = self.exam_service.update_exam(
            exam_db_id,
            name=name,
            academic_year_id=academic_year_id,
            semester_id=semester_id,
            max_marks=max_marks
        )
        if updated:
            show_info_message("Success", f"Exam/CAT '{name}' updated successfully.")
            self._clear_exam_fields()
            self._load_exams_to_treeview()
            self._populate_exam_dropdowns() # Refresh dropdowns
        else:
            show_error_message("Error", "Failed to update exam/CAT. Check logs.")

    def _delete_exam(self):
        """Deletes a selected exam/CAT from the database."""
        selected_item = self.exam_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select an exam/CAT to delete.")
            return

        exam_db_id = self.exam_tree.item(selected_item, 'iid')
        exam_name = self.exam_tree.item(selected_item, 'values')[1]

        # Check for dependencies (exam results)
        exam_results_query = "SELECT COUNT(*) FROM ExamResults WHERE exam_id = ?"
        count_results = self.exam_service.db_manager.fetch_one(exam_results_query, (exam_db_id,))['COUNT(*)']
        if count_results > 0:
            show_error_message("Deletion Error", f"Cannot delete Exam/CAT '{exam_name}'. {count_results} exam results are linked to this exam.")
            return

        if ask_confirmation("Confirm Deletion", f"Are you sure you want to delete Exam/CAT '{exam_name}'? This action cannot be undone."):
            deleted = self.exam_service.delete_exam(exam_db_id)
            if deleted:
                show_info_message("Success", f"Exam/CAT '{exam_name}' deleted successfully.")
                self._clear_exam_fields()
                self._load_exams_to_treeview()
                self._populate_exam_dropdowns() # Refresh dropdowns
            else:
                show_error_message("Error", "Failed to delete exam/CAT. Check logs.")

    def _clear_exam_fields(self):
        """Clears the exam/CAT input fields."""
        self.exam_name_entry.delete(0, ctk.END)
        self.exam_max_marks_entry.delete(0, ctk.END)
        self.exam_max_marks_entry.insert(0, "100")
        if self.exam_ay_options:
            self.exam_ay_combobox.set(self.exam_ay_options[0])
        else:
            self.exam_ay_combobox.set("")
        self.exam_semester_combobox.set("None")

    def _populate_exam_dropdowns(self):
        """Populates the exam comboboxes for Exam Results tab."""
        exams = self.exam_service.get_all_exams()
        self.exam_result_exam_options = [f"{e['name']} ({e['academic_year_name']} - {e['semester_name'] if e['semester_name'] else 'Yearly'})" for e in exams]
        self.exam_result_exam_id_map = {f"{e['name']} ({e['academic_year_name']} - {e['semester_name'] if e['semester_name'] else 'Yearly'})": e['id'] for e in exams}
        if hasattr(self, 'exam_result_exam_combobox'):
            self.exam_result_exam_combobox.configure(values=self.exam_result_exam_options)
            if self.exam_result_exam_options:
                self.exam_result_exam_combobox.set(self.exam_result_exam_options[0])
            else:
                self.exam_result_exam_combobox.set("")

    def _populate_student_dropdowns(self):
        """Populates student comboboxes for Exam Results tab."""
        students = self.student_service.get_all_students()
        self.exam_result_student_options = [f"{s['name']} ({s['student_id']})" for s in students]
        self.exam_result_student_id_map = {f"{s['name']} ({s['student_id']})": s['id'] for s in students}
        if hasattr(self, 'exam_result_student_combobox'):
            self.exam_result_student_combobox.configure(values=self.exam_result_student_options)
            if self.exam_result_student_options:
                self.exam_result_student_combobox.set(self.exam_result_student_options[0])
            else:
                self.exam_result_student_combobox.set("")

    def _populate_subject_dropdowns(self):
        """Populates subject comboboxes for Exam Results tab."""
        subjects = self.subject_service.get_all_subjects()
        self.exam_result_subject_options = [s.name for s in subjects]
        self.exam_result_subject_id_map = {s.name: s.id for s in subjects}
        if hasattr(self, 'exam_result_subject_combobox'):
            self.exam_result_subject_combobox.configure(values=self.exam_result_subject_options)
            if self.exam_result_subject_options:
                self.exam_result_subject_combobox.set(self.exam_result_subject_options[0])
            else:
                self.exam_result_subject_combobox.set("")

    # --- Exam Result Tab Setup ---
    def _setup_exam_result_tab(self):
        """Sets up the Exam Results tab GUI."""
        input_frame = ctk.CTkFrame(self.exam_result_tab, corner_radius=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Exam Result Details", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(input_frame, text="Student:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.exam_result_student_combobox = ctk.CTkComboBox(input_frame, state="readonly", width=300)
        self.exam_result_student_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Exam/CAT:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.exam_result_exam_combobox = ctk.CTkComboBox(input_frame, state="readonly", width=300)
        self.exam_result_exam_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Subject:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.exam_result_subject_combobox = ctk.CTkComboBox(input_frame, state="readonly", width=300)
        self.exam_result_subject_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Marks:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.exam_result_marks_entry = ctk.CTkEntry(input_frame, width=300)
        self.exam_result_marks_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        button_frame = ctk.CTkFrame(self.exam_result_tab, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        button_frame.grid_columnconfigure((0,1,2,3), weight=1)

        ctk.CTkButton(button_frame, text="Add Result", command=self._add_exam_result).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Update Result", command=self._update_exam_result).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Delete Result", command=self._delete_exam_result).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(button_frame, text="Clear Fields", command=self._clear_exam_result_fields).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.exam_result_tree = ttk.Treeview(self.exam_result_tab, columns=("ID", "Student", "Exam", "Subject", "Marks"), show="headings")
        self.exam_result_tree.heading("ID", text="ID")
        self.exam_result_tree.heading("Student", text="Student")
        self.exam_result_tree.heading("Exam", text="Exam")
        self.exam_result_tree.heading("Subject", text="Subject")
        self.exam_result_tree.heading("Marks", text="Marks")

        self.exam_result_tree.column("ID", width=50, stretch=ctk.NO)
        self.exam_result_tree.column("Student", width=150)
        self.exam_result_tree.column("Exam", width=150)
        self.exam_result_tree.column("Subject", width=100)
        self.exam_result_tree.column("Marks", width=80)

        self.exam_result_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.exam_result_tab, orient="vertical", command=self.exam_result_tree.yview)
        scrollbar.grid(row=2, column=1, sticky="ns", pady=10)
        self.exam_result_tree.configure(yscrollcommand=scrollbar.set)

        self.exam_result_tree.bind("<<TreeviewSelect>>", self._on_exam_result_select)

        self._populate_student_dropdowns()
        self._populate_exam_dropdowns()
        self._populate_subject_dropdowns()
        self._load_exam_results_to_treeview()

    def _load_exam_results_to_treeview(self):
        """Loads exam result data into the Treeview."""
        for item in self.exam_result_tree.get_children():
            self.exam_result_tree.delete(item)
        results = self.exam_result_service.get_all_exam_results()
        for res in results:
            self.exam_result_tree.insert("", "end", values=(
                res['id'],
                f"{res['student_name']} ({res['student_unique_id']})",
                f"{res['exam_name']} ({res['academic_year_name']} - {res['semester_name'] if res['semester_name'] else 'Yearly'})",
                res['subject_name'],
                res['marks']
            ), iid=res['id'])

    def _on_exam_result_select(self, event):
        """Populates entry fields when an exam result is selected in the Treeview."""
        selected_item = self.exam_result_tree.focus()
        if selected_item:
            values = self.exam_result_tree.item(selected_item, 'values')
            self.exam_result_student_combobox.set(values[1])
            self.exam_result_exam_combobox.set(values[2])
            self.exam_result_subject_combobox.set(values[3])
            self.exam_result_marks_entry.delete(0, ctk.END)
            self.exam_result_marks_entry.insert(0, values[4])

    def _add_exam_result(self):
        """Adds a new exam result."""
        selected_student_text = self.exam_result_student_combobox.get()
        student_id = self.exam_result_student_id_map.get(selected_student_text)
        selected_exam_text = self.exam_result_exam_combobox.get()
        exam_id = self.exam_result_exam_id_map.get(selected_exam_text)
        selected_subject_text = self.exam_result_subject_combobox.get()
        subject_id = self.exam_result_subject_id_map.get(selected_subject_text)
        marks_str = self.exam_result_marks_entry.get().strip()

        if not student_id or not exam_id or not subject_id or not marks_str:
            show_error_message("Input Error", "All fields are required.")
            return
        if not is_valid_marks(marks_str):
            show_error_message("Input Error", "Marks must be a non-negative number.")
            return
        marks = float(marks_str)

        new_result = self.exam_result_service.add_exam_result(student_id, exam_id, subject_id, marks)
        if new_result:
            show_info_message("Success", "Exam result added successfully.")
            self._clear_exam_result_fields()
            self._load_exam_results_to_treeview()
        else:
            show_error_message("Error", "Failed to add exam result. It might already exist or there was a database error.")

    def _update_exam_result(self):
        """Updates an existing exam result."""
        selected_item = self.exam_result_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select an exam result to update.")
            return

        result_db_id = self.exam_result_tree.item(selected_item, 'iid')
        marks_str = self.exam_result_marks_entry.get().strip()

        if not marks_str or not is_valid_marks(marks_str):
            show_error_message("Input Error", "Marks must be a non-negative number.")
            return
        marks = float(marks_str)

        updated = self.exam_result_service.update_exam_result(result_db_id, marks=marks)
        if updated:
            show_info_message("Success", "Exam result updated successfully.")
            self._clear_exam_result_fields()
            self._load_exam_results_to_treeview()
        else:
            show_error_message("Error", "Failed to update exam result. Check logs.")

    def _delete_exam_result(self):
        """Deletes a selected exam result."""
        selected_item = self.exam_result_tree.focus()
        if not selected_item:
            show_warning_message("Selection Error", "Please select an exam result to delete.")
            return

        result_db_id = self.exam_result_tree.item(selected_item, 'iid')
        result_info = self.exam_result_tree.item(selected_item, 'values')

        if ask_confirmation("Confirm Deletion", f"Are you sure you want to delete the result for '{result_info[1]}' in '{result_info[3]}' ({result_info[2]})? This action cannot be undone."):
            deleted = self.exam_result_service.delete_exam_result(result_db_id)
            if deleted:
                show_info_message("Success", "Exam result deleted successfully.")
                self._clear_exam_result_fields()
                self._load_exam_results_to_treeview()
            else:
                show_error_message("Error", "Failed to delete exam result. Check logs.")

    def _clear_exam_result_fields(self):
        """Clears the exam result input fields."""
        if self.exam_result_student_options:
            self.exam_result_student_combobox.set(self.exam_result_student_options[0])
        else:
            self.exam_result_student_combobox.set("")
        if self.exam_result_exam_options:
            self.exam_result_exam_combobox.set(self.exam_result_exam_options[0])
        else:
            self.exam_result_exam_combobox.set("")
        if self.exam_result_subject_options:
            self.exam_result_subject_combobox.set(self.exam_result_subject_options[0])
        else:
            self.exam_result_subject_combobox.set("")
        self.exam_result_marks_entry.delete(0, ctk.END)


    # --- Semester Result Tab Setup ---
    def _setup_semester_result_tab(self):
        """Sets up the Semester Results tab GUI."""
        control_frame = ctk.CTkFrame(self.semester_result_tab, corner_radius=10)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        control_frame.grid_columnconfigure((1,3), weight=1) # Allow comboboxes to expand

        ctk.CTkLabel(control_frame, text="Compute Semester Results", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(control_frame, text="Academic Year:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.semester_result_ay_combobox = ctk.CTkComboBox(control_frame, state="readonly", width=200)
        self.semester_result_ay_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.semester_result_ay_combobox.bind("<<ComboboxSelected>>", self._on_semester_result_ay_select)

        ctk.CTkLabel(control_frame, text="Semester:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.semester_result_semester_combobox = ctk.CTkComboBox(control_frame, state="readonly", width=200)
        self.semester_result_semester_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkButton(control_frame, text="Compute Results", command=self._compute_semester_results).grid(row=1, column=4, padx=10, pady=5, sticky="ew")

        self.semester_result_tree = ttk.Treeview(self.semester_result_tab, columns=(
            "ID", "Student", "Academic Year", "Semester", "Total Marks", "Average Score", "Rank"
        ), show="headings")
        self.semester_result_tree.heading("ID", text="ID")
        self.semester_result_tree.heading("Student", text="Student")
        self.semester_result_tree.heading("Academic Year", text="Academic Year") # Corrected line
        self.semester_result_tree.heading("Semester", text="Semester")
        self.semester_result_tree.heading("Total Marks", text="Total Marks")
        self.semester_result_tree.heading("Average Score", text="Average Score")
        self.semester_result_tree.heading("Rank", text="Rank")

        self.semester_result_tree.column("ID", width=50, stretch=ctk.NO)
        self.semester_result_tree.column("Student", width=150)
        self.semester_result_tree.column("Academic Year", width=100)
        self.semester_result_tree.column("Semester", width=100)
        self.semester_result_tree.column("Total Marks", width=100)
        self.semester_result_tree.column("Average Score", width=100)
        self.semester_result_tree.column("Rank", width=80)

        self.semester_result_tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.semester_result_tab, orient="vertical", command=self.semester_result_tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns", pady=10)
        self.semester_result_tree.configure(yscrollcommand=scrollbar.set)

        self._populate_academic_year_dropdowns() # Re-use from exam tab
        self._populate_semester_dropdowns()     # Re-use from exam tab
        self._load_semester_results_to_treeview()

    def _on_semester_result_ay_select(self, event):
        """Handles academic year selection in semester result tab."""
        # This can be used to filter semesters if needed, but for now
        # semesters are global.

    def _load_semester_results_to_treeview(self):
        """Loads semester result data into the Treeview."""
        for item in self.semester_result_tree.get_children():
            self.semester_result_tree.delete(item)
        results = self.semester_result_service.get_all_semester_results()
        for res in results:
            self.semester_result_tree.insert("", "end", values=(
                res['id'],
                f"{res['student_name']} ({res['student_unique_id']})",
                res['academic_year_name'],
                res['semester_name'],
                f"{res['total_marks']:.2f}",
                f"{res['average_score']:.2f}%",
                res['grade_rank']
            ), iid=res['id'])

    def _compute_semester_results(self):
        """Triggers computation and storage of semester results."""
        selected_ay_name = self.semester_result_ay_combobox.get()
        academic_year_id = self.exam_ay_id_map.get(selected_ay_name) # Re-use map
        selected_semester_name = self.semester_result_semester_combobox.get()
        semester_id = self.exam_semester_id_map.get(selected_semester_name) # Re-use map

        if not academic_year_id or not semester_id:
            show_error_message("Selection Error", "Please select an Academic Year and Semester.")
            return

        if ask_confirmation("Confirm Computation", f"This will compute/recompute semester results for all students in {selected_ay_name}, {selected_semester_name}. Continue?"):
            try:
                self.semester_result_service.compute_and_store_semester_results(academic_year_id, semester_id)
                show_info_message("Success", "Semester results computed and stored successfully.")
                self._load_semester_results_to_treeview()
            except Exception as e:
                show_error_message("Computation Error", f"An error occurred during semester result computation: {e}")


    # --- Yearly Result Tab Setup ---
    def _setup_yearly_result_tab(self):
        """Sets up the Yearly Results tab GUI."""
        control_frame = ctk.CTkFrame(self.yearly_result_tab, corner_radius=10)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        control_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(control_frame, text="Compute Yearly Results", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(control_frame, text="Academic Year:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.yearly_result_ay_combobox = ctk.CTkComboBox(control_frame, state="readonly", width=200)
        self.yearly_result_ay_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkButton(control_frame, text="Compute Results", command=self._compute_yearly_results).grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        self.yearly_result_tree = ttk.Treeview(self.yearly_result_tab, columns=(
            "ID", "Student", "Academic Year", "Total Marks", "Average Score", "Rank"
        ), show="headings")
        self.yearly_result_tree.heading("ID", text="ID")
        self.yearly_result_tree.heading("Student", text="Student")
        self.yearly_result_tree.heading("Academic Year", text="Academic Year")
        self.yearly_result_tree.heading("Total Marks", text="Total Marks")
        self.yearly_result_tree.heading("Average Score", text="Average Score")
        self.yearly_result_tree.heading("Rank", text="Rank")

        self.yearly_result_tree.column("ID", width=50, stretch=ctk.NO)
        self.yearly_result_tree.column("Student", width=150)
        self.yearly_result_tree.column("Academic Year", width=100)
        self.yearly_result_tree.column("Total Marks", width=100)
        self.yearly_result_tree.column("Average Score", width=100)
        self.yearly_result_tree.column("Rank", width=80)

        self.yearly_result_tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.yearly_result_tab, orient="vertical", command=self.yearly_result_tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns", pady=10)
        self.yearly_result_tree.configure(yscrollcommand=scrollbar.set)

        self._populate_academic_year_dropdowns() # Re-use from exam tab
        self._load_yearly_results_to_treeview()

    def _load_yearly_results_to_treeview(self):
        """Loads yearly result data into the Treeview."""
        for item in self.yearly_result_tree.get_children():
            self.yearly_result_tree.delete(item)
        results = self.yearly_result_service.get_all_yearly_results()
        for res in results:
            self.yearly_result_tree.insert("", "end", values=(
                res['id'],
                f"{res['student_name']} ({res['student_unique_id']})",
                res['academic_year_name'],
                f"{res['total_marks']:.2f}",
                f"{res['average_score']:.2f}%",
                res['grade_rank']
            ), iid=res['id'])

    def _compute_yearly_results(self):
        """Triggers computation and storage of yearly results."""
        selected_ay_name = self.yearly_result_ay_combobox.get()
        academic_year_id = self.exam_ay_id_map.get(selected_ay_name)

        if not academic_year_id:
            show_error_message("Selection Error", "Please select an Academic Year.")
            return

        if ask_confirmation("Confirm Computation", f"This will compute/recompute yearly results for all students in {selected_ay_name}. Continue?"):
            try:
                self.yearly_result_service.compute_and_store_yearly_results(academic_year_id)
                show_info_message("Success", "Yearly results computed and stored successfully.")
                self._load_yearly_results_to_treeview()
            except Exception as e:
                show_error_message("Computation Error", f"An error occurred during yearly result computation: {e}")


# Main application entry point
if __name__ == "__main__":
    app = StudentManagementApp()
    app.mainloop()
