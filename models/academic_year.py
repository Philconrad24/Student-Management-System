class AcademicYear:
    """
    Represents an academic year (e.g., 2023/2024).
    Corresponds to the 'AcademicYears' table in the database.
    """
    def __init__(self, id=None, year_name=None, start_date=None, end_date=None):
        """
        Initializes an AcademicYear object.

        Args:
            id (int, optional): The unique ID of the academic year.
            year_name (str): The name of the academic year (e.g., "2023/2024").
            start_date (str): The start date of the academic year (YYYY-MM-DD).
            end_date (str): The end date of the academic year (YYYY-MM-DD).
        """
        self.id = id
        self.year_name = year_name
        self.start_date = start_date
        self.end_date = end_date

    def to_dict(self):
        """
        Converts the AcademicYear object to a dictionary, suitable for database operations.
        """
        data = {
            'year_name': self.year_name,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def from_dict(data):
        """
        Creates an AcademicYear object from a dictionary (e.g., from database fetch).
        """
        return AcademicYear(
            id=data.get('id'),
            year_name=data.get('year_name'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date')
        )

    def __repr__(self):
        return (f"AcademicYear(id={self.id}, year_name='{self.year_name}', "
                f"start_date='{self.start_date}', end_date='{self.end_date}')")

    def __str__(self):
        return f"Academic Year: {self.year_name} ({self.start_date} to {self.end_date})"

