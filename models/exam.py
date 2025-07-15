class Exam:
    """
    Represents an exam or continuous assessment test (CAT).
    Corresponds to the 'Exams' table in the database.
    """
    def __init__(self, id=None, name=None, semester_id=None, academic_year_id=None, max_marks=None):
        """
        Initializes an Exam object.

        Args:
            id (int, optional): The unique ID of the exam.
            name (str): The name of the exam (e.g., "Semester 1 Exam", "CAT 1").
            semester_id (int, optional): Foreign key to the Semester (can be None for yearly exams).
            academic_year_id (int): Foreign key to the AcademicYear.
            max_marks (int, optional): The maximum marks for this exam.
        """
        self.id = id
        self.name = name
        self.semester_id = semester_id
        self.academic_year_id = academic_year_id
        self.max_marks = max_marks

    def to_dict(self):
        """
        Converts the Exam object to a dictionary, suitable for database operations.
        """
        data = {
            'name': self.name,
            'semester_id': self.semester_id,
            'academic_year_id': self.academic_year_id,
            'max_marks': self.max_marks
        }
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def from_dict(data):
        """
        Creates an Exam object from a dictionary (e.g., from database fetch).
        """
        return Exam(
            id=data.get('id'),
            name=data.get('name'),
            semester_id=data.get('semester_id'),
            academic_year_id=data.get('academic_year_id'),
            max_marks=data.get('max_marks')
        )

    def __repr__(self):
        return (f"Exam(id={self.id}, name='{self.name}', semester_id={self.semester_id}, "
                f"academic_year_id={self.academic_year_id}, max_marks={self.max_marks})")

    def __str__(self):
        return f"Exam: {self.name} (Max Marks: {self.max_marks})"

