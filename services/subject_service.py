from database.db_manager import DBManager
from models.subject import Subject

class SubjectService:
    """
    Manages business logic related to Subject operations.
    Interacts with the DBManager to perform CRUD operations on Subject data.
    """
    def __init__(self):
        """
        Initializes the SubjectService with a DBManager instance.
        """
        self.db_manager = DBManager()

    def add_subject(self, name, description=None):
        """
        Adds a new subject to the database.

        Args:
            name (str): The name of the subject.
            description (str, optional): A brief description of the subject.

        Returns:
            Subject or None: The created Subject object if successful, None otherwise.
        """
        try:
            subject_data = {'name': name, 'description': description}
            new_id = self.db_manager.insert_one('Subjects', subject_data)
            if new_id:
                return Subject(id=new_id, **subject_data)
            return None
        except Exception as e:
            print(f"Error adding subject: {e}")
            return None

    def get_subject_by_id(self, subject_id):
        """
        Retrieves a subject by its database ID.

        Args:
            subject_id (int): The database ID of the subject.

        Returns:
            Subject or None: The Subject object if found, None otherwise.
        """
        data = self.db_manager.get_by_id('Subjects', subject_id)
        return Subject.from_dict(data) if data else None

    def get_subject_by_name(self, name):
        """
        Retrieves a subject by its name.

        Args:
            name (str): The name of the subject.

        Returns:
            Subject or None: The Subject object if found, None otherwise.
        """
        query = "SELECT * FROM Subjects WHERE name = ?"
        data = self.db_manager.fetch_one(query, (name,))
        return Subject.from_dict(data) if data else None

    def get_all_subjects(self):
        """
        Retrieves all subjects from the database.

        Returns:
            list[Subject]: A list of Subject objects.
        """
        subjects_data = self.db_manager.get_all('Subjects', order_by='name')
        return [Subject.from_dict(data) for data in subjects_data]

    def update_subject(self, subject_id, name=None, description=None):
        """
        Updates an existing subject's information.

        Args:
            subject_id (int): The database ID of the subject to update.
            name (str, optional): New name.
            description (str, optional): New description.

        Returns:
            bool: True if update was successful, False otherwise.
        """
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if description is not None:
            update_data['description'] = description

        if not update_data:
            print("No data provided for update.")
            return False

        try:
            rows_affected = self.db_manager.update_one('Subjects', subject_id, update_data)
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating subject (ID: {subject_id}): {e}")
            return False

    def delete_subject(self, subject_id):
        """
        Deletes a subject from the database.
        Note: Consider checking for dependent records (e.g., exam results for this subject)
              before allowing deletion in a production system.

        Args:
            subject_id (int): The database ID of the subject to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            rows_affected = self.db_manager.delete_one('Subjects', subject_id)
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting subject (ID: {subject_id}): {e}")
            return False

# Example Usage (for testing purposes)
if __name__ == '__main__':
    subject_service = SubjectService()

    print("\n--- Testing SubjectService ---")

    # Add subjects (these should already be in schema.py initial setup)
    print("Adding extra subject 'Computer Science'...")
    cs_subject = subject_service.add_subject("Computer Science", "Study of computation and algorithms")
    if cs_subject:
        print(f"Added: {cs_subject}")
    else:
        print("Failed to add Computer Science (might already exist).")

    # Get all subjects
    print("\nAll Subjects:")
    all_subjects = subject_service.get_all_subjects()
    for s in all_subjects:
        print(s)

    # Update a subject
    if cs_subject:
        print(f"\nUpdating Computer Science (ID: {cs_subject.id})...")
        updated = subject_service.update_subject(cs_subject.id, description="Updated description for CS")
        if updated:
            updated_cs = subject_service.get_subject_by_id(cs_subject.id)
            print(f"Updated: {updated_cs}")
        else:
            print("Failed to update Computer Science.")

    # Get subject by name
    print("\nGetting subject by name 'Mathematics':")
    found_math = subject_service.get_subject_by_name("Mathematics")
    if found_math:
        print(f"Found: {found_math}")
    else:
        print("Mathematics not found.")

    # Delete a subject (use with caution during testing if results are linked)
    # if cs_subject:
    #     print(f"\nDeleting Computer Science (ID: {cs_subject.id})...")
    #     deleted = subject_service.delete_subject(cs_subject.id)
    #     if deleted:
    #         print("Computer Science deleted successfully.")
    #     else:
    #         print("Failed to delete Computer Science.")

    print("\nAll Subjects after operations:")
    all_subjects_after = subject_service.get_all_subjects()
    for s in all_subjects_after:
        print(s)
