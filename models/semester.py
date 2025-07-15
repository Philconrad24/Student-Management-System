class Semester:
    """
    Represents a semester within an academic year (e.g., Semester 1, Semester 2).
    Corresponds to the 'Semesters' table in the database.
    """
    def __init__(self, id=None, name=None, start_date=None, end_date=None):
        """
        Initializes a Semester object.

        Args:
            id (int, optional): The unique ID of the semester.
            name (str): The name of the semester (e.g., "Semester 1").
            start_date (str, optional): The start date of the semester (YYYY-MM-DD).
            end_date (str, optional): The end date of the semester (YYYY-MM-DD).
        """
        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def to_dict(self):
        """
        Converts the Semester object to a dictionary, suitable for database operations.
        """
        data = {
            'name': self.name,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def from_dict(data):
        """
        Creates a Semester object from a dictionary (e.g., from database fetch).
        """
        return Semester(
            id=data.get('id'),
            name=data.get('name'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date')
        )

    def __repr__(self):
        return (f"Semester(id={self.id}, name='{self.name}', "
                f"start_date='{self.start_date}', end_date='{self.end_date}')")

    def __str__(self):
        return f"Semester: {self.name} ({self.start_date} to {self.end_date})"

