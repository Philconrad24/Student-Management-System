class Subject:
    """
    Represents an academic subject (e.g., Mathematics, Science).
    Corresponds to the 'Subjects' table in the database.
    """
    def __init__(self, id=None, name=None, description=None):
        """
        Initializes a Subject object.

        Args:
            id (int, optional): The unique ID of the subject.
            name (str): The name of the subject.
            description (str, optional): A brief description of the subject.
        """
        self.id = id
        self.name = name
        self.description = description

    def to_dict(self):
        """
        Converts the Subject object to a dictionary, suitable for database operations.
        """
        data = {
            'name': self.name,
            'description': self.description
        }
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def from_dict(data):
        """
        Creates a Subject object from a dictionary (e.g., from database fetch).
        """
        return Subject(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description')
        )

    def __repr__(self):
        return f"Subject(id={self.id}, name='{self.name}', description='{self.description}')"

    def __str__(self):
        return f"Subject: {self.name}"

