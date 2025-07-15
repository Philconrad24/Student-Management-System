from database.db_manager import DBManager
from models.grade import Grade

class GradeService:
    """
    Manages business logic related to Grade operations.
    Interacts with the DBManager to perform CRUD operations on Grade data.
    """
    def __init__(self):
        """
        Initializes the GradeService with a DBManager instance.
        """
        self.db_manager = DBManager()

    def add_grade(self, name, description=None):
        """
        Adds a new grade to the database.

        Args:
            name (str): The name of the grade (e.g., "Grade 1").
            description (str, optional): A brief description of the grade.

        Returns:
            Grade or None: The created Grade object if successful, None otherwise.
        """
        try:
            grade_data = {'name': name, 'description': description}
            new_id = self.db_manager.insert_one('Grades', grade_data)
            if new_id:
                return Grade(id=new_id, **grade_data)
            return None
        except Exception as e:
            print(f"Error adding grade: {e}")
            return None

    def get_grade_by_id(self, grade_id):
        """
        Retrieves a grade by its database ID.

        Args:
            grade_id (int): The database ID of the grade.

        Returns:
            Grade or None: The Grade object if found, None otherwise.
        """
        data = self.db_manager.get_by_id('Grades', grade_id)
        return Grade.from_dict(data) if data else None

    def get_grade_by_name(self, name):
        """
        Retrieves a grade by its name.

        Args:
            name (str): The name of the grade (e.g., "Grade 1").

        Returns:
            Grade or None: The Grade object if found, None otherwise.
        """
        query = "SELECT * FROM Grades WHERE name = ?"
        data = self.db_manager.fetch_one(query, (name,))
        return Grade.from_dict(data) if data else None

    def get_all_grades(self):
        """
        Retrieves all grades from the database.

        Returns:
            list[Grade]: A list of Grade objects.
        """
        grades_data = self.db_manager.get_all('Grades', order_by='name')
        return [Grade.from_dict(data) for data in grades_data]

    def update_grade(self, grade_id, name=None, description=None):
        """
        Updates an existing grade's information.

        Args:
            grade_id (int): The database ID of the grade to update.
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
            rows_affected = self.db_manager.update_one('Grades', grade_id, update_data)
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating grade (ID: {grade_id}): {e}")
            return False

    def delete_grade(self, grade_id):
        """
        Deletes a grade from the database.
        Note: Consider checking for dependent records (e.g., students assigned to this grade)
              before allowing deletion in a production system.

        Args:
            grade_id (int): The database ID of the grade to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            rows_affected = self.db_manager.delete_one('Grades', grade_id)
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting grade (ID: {grade_id}): {e}")
            return False

# Example Usage (for testing purposes)
if __name__ == '__main__':
    grade_service = GradeService()

    print("\n--- Testing GradeService ---")

    # Add grades
    print("Adding Grade 1...")
    grade1 = grade_service.add_grade("Grade 1", "First year of primary school")
    if grade1:
        print(f"Added: {grade1}")
    else:
        print("Failed to add Grade 1 (might already exist).")

    print("Adding Grade 8...")
    grade8 = grade_service.add_grade("Grade 8", "Final year of primary school")
    if grade8:
        print(f"Added: {grade8}")
    else:
        print("Failed to add Grade 8 (might already exist).")

    # Get all grades
    print("\nAll Grades:")
    all_grades = grade_service.get_all_grades()
    for g in all_grades:
        print(g)

    # Update a grade
    if grade1:
        print(f"\nUpdating Grade 1 (ID: {grade1.id})...")
        updated = grade_service.update_grade(grade1.id, description="Updated description for Grade 1")
        if updated:
            updated_grade1 = grade_service.get_grade_by_id(grade1.id)
            print(f"Updated: {updated_grade1}")
        else:
            print("Failed to update Grade 1.")

    # Get grade by name
    print("\nGetting grade by name 'Grade 8':")
    found_grade8 = grade_service.get_grade_by_name("Grade 8")
    if found_grade8:
        print(f"Found: {found_grade8}")
    else:
        print("Grade 8 not found.")

    # Delete a grade (use with caution during testing if students are linked)
    # if grade1:
    #     print(f"\nDeleting Grade 1 (ID: {grade1.id})...")
    #     deleted = grade_service.delete_grade(grade1.id)
    #     if deleted:
    #         print("Grade 1 deleted successfully.")
    #     else:
    #         print("Failed to delete Grade 1.")

    print("\nAll Grades after operations:")
    all_grades_after = grade_service.get_all_grades()
    for g in all_grades_after:
        print(g)

    # Note: DBManager connection is managed internally by each service instance.
    # For a full application, you might manage a single connection more centrally
    # or ensure all services close their connections properly.
