class Grade:
    """
    Represents a grade level (e.g., Grade 1, Grade 8).
    Corresponds to the 'Grades' table in the database.
    """
    def __init__(self, id=None, name=None, description=None):
        """
        Initializes a Grade object.

        Args:
            id (int, optional): The unique ID of the grade.
            name (str): The name of the grade (e.g., "Grade 1").
            description (str, optional): A brief description of the grade.
        """
        self.id = id
        self.name = name
        self.description = description

    def to_dict(self):
        """
        Converts the Grade object to a dictionary, suitable for database operations.
        """
        data = {
            'name': self.name,
            'description': self.description
        }
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def from_dict(data):
        """
        Creates a Grade object from a dictionary (e.g., from database fetch).
        """
        return Grade(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description')
        )

    def __repr__(self):
        return f"Grade(id={self.id}, name='{self.name}', description='{self.description}')"

    def __str__(self):
        return f"Grade: {self.name}"

