class ExamResult:
    """
    Represents an individual student's score for a specific subject in a specific exam.
    Corresponds to the 'ExamResults' table in the database.
    """
    def __init__(self, id=None, student_id=None, exam_id=None, subject_id=None, marks=None):
        """
        Initializes an ExamResult object.

        Args:
            id (int, optional): The unique ID of the exam result.
            student_id (int): Foreign key to the Student.
            exam_id (int): Foreign key to the Exam.
            subject_id (int): Foreign key to the Subject.
            marks (float): The marks obtained by the student in this subject for this exam.
        """
        self.id = id
        self.student_id = student_id
        self.exam_id = exam_id
        self.subject_id = subject_id
        self.marks = marks

    def to_dict(self):
        """
        Converts the ExamResult object to a dictionary, suitable for database operations.
        """
        data = {
            'student_id': self.student_id,
            'exam_id': self.exam_id,
            'subject_id': self.subject_id,
            'marks': self.marks
        }
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def from_dict(data):
        """
        Creates an ExamResult object from a dictionary (e.g., from database fetch).
        """
        return ExamResult(
            id=data.get('id'),
            student_id=data.get('student_id'),
            exam_id=data.get('exam_id'),
            subject_id=data.get('subject_id'),
            marks=data.get('marks')
        )

    def __repr__(self):
        return (f"ExamResult(id={self.id}, student_id={self.student_id}, "
                f"exam_id={self.exam_id}, subject_id={self.subject_id}, marks={self.marks})")

    def __str__(self):
        return (f"Exam Result ID: {self.id}, Student ID: {self.student_id}, "
                f"Exam ID: {self.exam_id}, Subject ID: {self.subject_id}, Marks: {self.marks}")

