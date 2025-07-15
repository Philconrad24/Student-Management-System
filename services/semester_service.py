from database.db_manager import DBManager
from models.semester import Semester

class SemesterService:
    """
    Manages business logic related to Semester operations.
    Interacts with the DBManager to perform CRUD operations on Semester data.
    """
    def __init__(self):
        """
        Initializes the SemesterService with a DBManager instance.
        """
        self.db_manager = DBManager()

    def add_semester(self, name, start_date=None, end_date=None):
        """
        Adds a new semester to the database.

        Args:
            name (str): The name of the semester (e.g., "Semester 1").
            start_date (str, optional): The start date (YYYY-MM-DD).
            end_date (str, optional): The end date (YYYY-MM-DD).

        Returns:
            Semester or None: The created Semester object if successful, None otherwise.
        """
        try:
            semester_data = {'name': name, 'start_date': start_date, 'end_date': end_date}
            new_id = self.db_manager.insert_one('Semesters', semester_data)
            if new_id:
                return Semester(id=new_id, **semester_data)
            return None
        except Exception as e:
            print(f"Error adding semester: {e}")
            return None

    def get_semester_by_id(self, semester_id):
        """
        Retrieves a semester by its database ID.

        Args:
            semester_id (int): The database ID of the semester.

        Returns:
            Semester or None: The Semester object if found, None otherwise.
        """
        data = self.db_manager.get_by_id('Semesters', semester_id)
        return Semester.from_dict(data) if data else None

    def get_semester_by_name(self, name):
        """
        Retrieves a semester by its name.

        Args:
            name (str): The name of the semester (e.g., "Semester 1").

        Returns:
            Semester or None: The Semester object if found, None otherwise.
        """
        query = "SELECT * FROM Semesters WHERE name = ?"
        data = self.db_manager.fetch_one(query, (name,))
        return Semester.from_dict(data) if data else None

    def get_all_semesters(self):
        """
        Retrieves all semesters from the database.

        Returns:
            list[Semester]: A list of Semester objects.
        """
        semesters_data = self.db_manager.get_all('Semesters', order_by='name')
        return [Semester.from_dict(data) for data in semesters_data]

    def update_semester(self, semester_id, name=None, start_date=None, end_date=None):
        """
        Updates an existing semester's information.

        Args:
            semester_id (int): The database ID of the semester to update.
            name (str, optional): New name.
            start_date (str, optional): New start date (YYYY-MM-DD).
            end_date (str, optional): New end date (YYYY-MM-DD).

        Returns:
            bool: True if update was successful, False otherwise.
        """
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if start_date is not None:
            update_data['start_date'] = start_date
        if end_date is not None:
            update_data['end_date'] = end_date

        if not update_data:
            print("No data provided for update.")
            return False

        try:
            rows_affected = self.db_manager.update_one('Semesters', semester_id, update_data)
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating semester (ID: {semester_id}): {e}")
            return False

    def delete_semester(self, semester_id):
        """
        Deletes a semester from the database.
        Note: Consider checking for dependent records (e.g., exams, semester results)
              before allowing deletion.

        Args:
            semester_id (int): The database ID of the semester to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            rows_affected = self.db_manager.delete_one('Semesters', semester_id)
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting semester (ID: {semester_id}): {e}")
            return False

# Example Usage (for testing purposes)
if __name__ == '__main__':
    semester_service = SemesterService()

    print("\n--- Testing SemesterService ---")

    # Add semesters (Semester 1 and Semester 2 should be in schema.py initial setup)
    print("Adding extra semester 'Summer Term'...")
    summer_term = semester_service.add_semester("Summer Term", "2024-07-01", "2024-08-31")
    if summer_term:
        print(f"Added: {summer_term}")
    else:
        print("Failed to add Summer Term (might already exist).")

    # Get all semesters
    print("\nAll Semesters:")
    all_semesters = semester_service.get_all_semesters()
    for s in all_semesters:
        print(s)

    # Update a semester
    if summer_term:
        print(f"\nUpdating Summer Term (ID: {summer_term.id})...")
        updated = semester_service.update_semester(summer_term.id, end_date="2024-09-15")
        if updated:
            updated_sem = semester_service.get_semester_by_id(summer_term.id)
            print(f"Updated: {updated_sem}")
        else:
            print("Failed to update Summer Term.")

    # Get semester by name
    print("\nGetting semester by name 'Semester 1':")
    found_sem1 = semester_service.get_semester_by_name("Semester 1")
    if found_sem1:
        print(f"Found: {found_sem1}")
    else:
        print("Semester 1 not found.")

    # Delete a semester (use with caution)
    # if summer_term:
    #     print(f"\nDeleting Summer Term (ID: {summer_term.id})...")
    #     deleted = semester_service.delete_semester(summer_term.id)
    #     if deleted:
    #         print("Summer Term deleted successfully.")
    #     else:
    #         print("Failed to delete Summer Term.")

    print("\nAll Semesters after operations:")
    all_semesters_after = semester_service.get_all_semesters()
    for s in all_semesters_after:
        print(s)
