class Enrollment:
    """
    Represents a student's enrollment in a specific grade for an academic year.
    Corresponds to the 'Enrollments' table in the database.
    """
    def __init__(self, id=None, student_id=None, academic_year_id=None, grade_id=None):
        """
        Initializes an Enrollment object.

        Args:
            id (int, optional): The unique ID of the enrollment.
            student_id (int): Foreign key to the Student.
            academic_year_id (int): Foreign key to the AcademicYear.
            grade_id (int): Foreign key to the Grade the student is enrolled in for that year.
        """
        self.id = id
        self.student_id = student_id
        self.academic_year_id = academic_year_id
        self.grade_id = grade_id

    def to_dict(self):
        """
        Converts the Enrollment object to a dictionary, suitable for database operations.
        """
        data = {
            'student_id': self.student_id,
            'academic_year_id': self.academic_year_id,
            'grade_id': self.grade_id
        }
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def from_dict(data):
        """
        Creates an Enrollment object from a dictionary (e.g., from database fetch).
        """
        return Enrollment(
            id=data.get('id'),
            student_id=data.get('student_id'),
            academic_year_id=data.get('academic_year_id'),
            grade_id=data.get('grade_id')
        )

    def __repr__(self):
        return (f"Enrollment(id={self.id}, student_id={self.student_id}, "
                f"academic_year_id={self.academic_year_id}, grade_id={self.grade_id})")

    def __str__(self):
        return (f"Enrollment ID: {self.id}, Student ID: {self.student_id}, "
                f"Academic Year ID: {self.academic_year_id}, Grade ID: {self.grade_id}")

