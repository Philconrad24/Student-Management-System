import sqlite3

DATABASE_NAME = 'sms.db'

def create_schema():
    """
    Creates the necessary tables for the Students Management System database.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Table: Grades (e.g., Grade 1, Grade 8)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')

    # Table: Subjects (e.g., Mathematics, Science)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')

    # Table: AcademicYears (e.g., 2023/2024)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AcademicYears (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year_name TEXT NOT NULL UNIQUE,
            start_date TEXT NOT NULL, -- YYYY-MM-DD
            end_date TEXT NOT NULL    -- YYYY-MM-DD
        )
    ''')

    # Table: Semesters (e.g., Semester 1, Semester 2)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Semesters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            start_date TEXT, -- YYYY-MM-DD
            end_date TEXT    -- YYYY-MM-DD
        )
    ''')

    # Table: Students
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT NOT NULL UNIQUE,
            contact_info TEXT,
            current_grade_id INTEGER, -- Current grade the student is in
            FOREIGN KEY (current_grade_id) REFERENCES Grades(id)
        )
    ''')

    # Table: Enrollments (Links students to specific grades in specific academic years)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            academic_year_id INTEGER NOT NULL,
            grade_id INTEGER NOT NULL,
            UNIQUE(student_id, academic_year_id), -- A student can only be enrolled once per academic year
            FOREIGN KEY (student_id) REFERENCES Students(id),
            FOREIGN KEY (academic_year_id) REFERENCES AcademicYears(id),
            FOREIGN KEY (grade_id) REFERENCES Grades(id)
        )
    ''')

    # Table: Exams (e.g., Semester 1 Exam, CAT 1, CAT 2)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            semester_id INTEGER, -- Can be NULL for yearly exams if needed, but for now tied to semester
            academic_year_id INTEGER NOT NULL,
            max_marks INTEGER DEFAULT 100, -- Default max marks for an exam
            UNIQUE(name, semester_id, academic_year_id), -- Ensure unique exam per semester/year
            FOREIGN KEY (semester_id) REFERENCES Semesters(id),
            FOREIGN KEY (academic_year_id) REFERENCES AcademicYears(id)
        )
    ''')

    # Table: ExamResults (Individual student scores for a subject in a specific exam)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ExamResults (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            exam_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            marks REAL NOT NULL, -- Use REAL for decimal marks if needed
            UNIQUE(student_id, exam_id, subject_id), -- A student can only have one result per subject per exam
            FOREIGN KEY (student_id) REFERENCES Students(id),
            FOREIGN KEY (exam_id) REFERENCES Exams(id),
            FOREIGN KEY (subject_id) REFERENCES Subjects(id)
        )
    ''')

    # Table: SemesterResults (Computed results for a student for a specific semester)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SemesterResults (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            semester_id INTEGER NOT NULL,
            academic_year_id INTEGER NOT NULL,
            total_marks REAL,
            average_score REAL,
            grade_rank INTEGER, -- Rank within their grade for that semester
            UNIQUE(student_id, semester_id, academic_year_id),
            FOREIGN KEY (student_id) REFERENCES Students(id),
            FOREIGN KEY (semester_id) REFERENCES Semesters(id),
            FOREIGN KEY (academic_year_id) REFERENCES AcademicYears(id)
        )
    ''')

    # Table: YearlyResults (Computed results for a student for a specific academic year)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS YearlyResults (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            academic_year_id INTEGER NOT NULL,
            total_marks REAL,
            average_score REAL,
            grade_rank INTEGER, -- Rank within their grade for that academic year
            UNIQUE(student_id, academic_year_id),
            FOREIGN KEY (student_id) REFERENCES Students(id),
            FOREIGN KEY (academic_year_id) REFERENCES AcademicYears(id)
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database schema created/verified in {DATABASE_NAME}")

# Call create_schema() when this module is imported or run directly
if __name__ == '__main__':
    create_schema()
