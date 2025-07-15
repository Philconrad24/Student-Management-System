# sms_management_system/models/student.py

class Student:
    """
    Represents a student in the Students Management System.
    Corresponds to the 'Students' table in the database.
    """
    def __init__(self, id=None, name=None, student_id=None, contact_info=None, current_grade_id=None):
        """
        Initializes a Student object.

        Args:
            id (int, optional): The unique ID of the student (from the database).
            name (str): The full name of the student.
            student_id (str): The unique student identifier.
            contact_info (str, optional): Contact information for the student.
            current_grade_id (int, optional): Foreign key to the current Grade.
        """
        self.id = id
        self.name = name
        self.student_id = student_id
        self.contact_info = contact_info
        self.current_grade_id = current_grade_id

    def to_dict(self):
        """
        Converts the Student object to a dictionary, suitable for database operations.
        """
        data = {
            'name': self.name,
            'student_id': self.student_id,
            'contact_info': self.contact_info,
            'current_grade_id': self.current_grade_id
        }
        # Remove None values if they are not meant to be inserted/updated
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def from_dict(data):
        """
        Creates a Student object from a dictionary (e.g., from database fetch).
        """
        return Student(
            id=data.get('id'),
            name=data.get('name'),
            student_id=data.get('student_id'),
            contact_info=data.get('contact_info'),
            current_grade_id=data.get('current_grade_id')
        )

    def __repr__(self):
        return (f"Student(id={self.id}, name='{self.name}', "
                f"student_id='{self.student_id}', contact_info='{self.contact_info}', "
                f"current_grade_id={self.current_grade_id})")

    def __str__(self):
        return f"Student ID: {self.student_id}, Name: {self.name}"

