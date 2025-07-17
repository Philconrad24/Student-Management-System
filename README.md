# Student Management System Summary
A desktop application built with Python and CustomTkinter for managing student information, grades, subjects, academic years, semesters, exams, and results. This system offers a user-friendly interface that enables schools or educational institutions to monitor their students' academic progress.

Features
Student Management: Add, update, delete, and view student records, including their name, student ID, contact information, and current grade.

Grade Management: Define and manage different academic grades (e.g., Grade 1, Grade 8).

Subject Management: Add, modify, and remove subjects offered at the institution.

Academic Year Management: Organize academic periods with defined start and end dates.

Semester Management: Manage semesters within academic years, also with start and end dates.

Exam/CAT Management: Create and manage various exams or Continuous Assessment Tests (CATs) for different academic years and semesters.

Exam Result Entry: Record and update individual student marks for specific exams and subjects.

Semester Result Computation: Automatically calculate and store total marks, average scores, and ranks for students based on their exam results within a specific semester.

Yearly Result Computation: Automatically calculate and store total marks, average scores, and ranks for students based on their exam results across an entire academic year.

User-Friendly Interface: A modern and responsive GUI built with customtkinter.

SQLite Database: Uses a local SQLite database for data persistence.

Prerequisites
Before running this application, ensure you have the following installed:

Python 3.x

pip (Python package installer)

Installation
Clone the repository (if applicable) or download the project files.

# If using git
git clone <repository_url>
cd sms_management_system

Install the required Python packages.

pip install customtkinter

(Note: sqlite3 is typically included with Python, so no separate installation is needed for the database.)

Project Structure
The project is organized into the following directories and files:

sms_management_system/
├── main.py                     # Main entry point of the application
├── database/
│   └── db_manager.py           # Handles database connection and operations
│   └── __init__.py             # Makes 'database' a Python package
├── models/
│   └── student.py              # Defines the Student data model
│   └── grade.py                # Defines the Grade data model
│   └── subject.py              # Defines the Subject data model
│   └── academic_year.py        # Defines the AcademicYear data model
│   └── semester.py             # Defines the Semester data model
│   └── exam.py                 # Defines the Exam data model
│   └── exam_result.py          # Defines the ExamResult data model
│   └── semester_result.py      # Defines the SemesterResult data model
│   └── yearly_result.py        # Defines the YearlyResult data model
│   └── __init__.py             # Makes 'models' a Python package
├── services/
│   └── student_service.py      # Business logic for Student operations
│   └── grade_service.py        # Business logic for Grade operations
│   └── subject_service.py      # Business logic for Subject operations
│   └── academic_year_service.py# Business logic for AcademicYear operations
│   └── semester_service.py     # Business logic for Semester operations
│   └── exam_service.py         # Business logic for Exam operations
│   └── exam_result_service.py  # Business logic for ExamResult operations
│   └── semester_result_service.py # Business logic for SemesterResult operations
│   └── yearly_result_service.py# Business logic for YearlyResult operations
│   └── __init__.py             # Makes 'services' a Python package
├── gui/
│   └── main_window.py          # Main GUI window setup with CustomTkinter
│   └── __init__.py             # Makes 'gui' a Python package
├── utils/
│   └── helpers.py              # Utility functions (e.g., date validation, message boxes)
│   └── __init__.py             # Makes 'utils' a Python package
└── README.md                   # This file

Usage
Run the application.

Navigate to the sms_management_system directory in your terminal and run:

python main.py

Initial Setup (if database is empty)
Upon the first run, the application will automatically populate the database with some default grades, subjects, academic years, and semesters if no existing data is found. You will see a confirmation message for this.

Navigate Through Tabs
The application features a tabbed interface. Click on the tabs at the top (Students, Grades, Subjects, etc.) to switch between different management modules.

Add/Update/Delete Records

Input Fields: Use the input fields at the top of each tab to enter details for new records or modify existing ones.

Buttons: Click "Add", "Update", or "Delete" buttons to perform the respective actions.

Treeview: Select a row in the table (Treeview) to load its data into the input fields for updating or deleting.

Clear Fields: Use the "Clear Fields" button to reset the input forms.

Compute Results

In the "Semester Results" and "Yearly Results" tabs, select the relevant Academic Year and/or Semester using the dropdowns.

Click the "Compute Results" button to calculate and store the aggregate results for students. These results will then appear in the table below.
