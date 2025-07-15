class SemesterResult:
    """
    Represents the computed final result for a student for a specific semester.
    Corresponds to the 'SemesterResults' table in the database.
    """
    def __init__(self, id=None, student_id=None, semester_id=None, academic_year_id=None,
                 total_marks=None, average_score=None, grade_rank=None):
        """
        Initializes a SemesterResult object.

        Args:
            id (int, optional): The unique ID of the semester result.
            student_id (int): Foreign key to the Student.
            semester_id (int): Foreign key to the Semester.
            academic_year_id (int): Foreign key to the AcademicYear.
            total_marks (float, optional): The sum of all marks for the semester.
            average_score (float, optional): The average score for the semester.
            grade_rank (int, optional): The student's rank within their grade for this semester.
        """
        self.id = id
        self.student_id = student_id
        self.semester_id = semester_id
        self.academic_year_id = academic_year_id
        self.total_marks = total_marks
        self.average_score = average_score
        self.grade_rank = grade_rank

    def to_dict(self):
        """
        Converts the SemesterResult object to a dictionary, suitable for database operations.
        """
        data = {
            'student_id': self.student_id,
            'semester_id': self.semester_id,
            'academic_year_id': self.academic_year_id,
            'total_marks': self.total_marks,
            'average_score': self.average_score,
            'grade_rank': self.grade_rank
        }
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def from_dict(data):
        """
        Creates a SemesterResult object from a dictionary (e.g., from database fetch).
        """
        return SemesterResult(
            id=data.get('id'),
            student_id=data.get('student_id'),
            semester_id=data.get('semester_id'),
            academic_year_id=data.get('academic_year_id'),
            total_marks=data.get('total_marks'),
            average_score=data.get('average_score'),
            grade_rank=data.get('grade_rank')
        )

    def __repr__(self):
        return (f"SemesterResult(id={self.id}, student_id={self.student_id}, "
                f"semester_id={self.semester_id}, academic_year_id={self.academic_year_id}, "
                f"total_marks={self.total_marks}, average_score={self.average_score}, "
                f"grade_rank={self.grade_rank})")

    def __str__(self):
        return (f"Semester Result for Student ID: {self.student_id}, Semester ID: {self.semester_id}, "
                f"Total Marks: {self.total_marks}, Average: {self.average_score}, Rank: {self.grade_rank}")

