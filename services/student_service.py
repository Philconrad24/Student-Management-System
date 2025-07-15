from database.db_manager import DBManager
from models.student import Student
from models.grade import Grade # Import Grade model to fetch grade names

class StudentService:
    """
    Manages business logic related to Student operations.
    Interacts with the DBManager to perform CRUD operations on Student data.
    """
    def __init__(self):
        """
        Initializes the StudentService with a DBManager instance.
        """
        self.db_manager = DBManager()

    def add_student(self, name, student_id, contact_info, current_grade_id):
        """
        Adds a new student to the database.

        Args:
            name (str): The full name of the student.
            student_id (str): The unique student identifier.
            contact_info (str): Contact information for the student.
            current_grade_id (int): The ID of the current grade the student is in.

        Returns:
            Student or None: The created Student object if successful, None otherwise.
        """
        try:
            student_data = {
                'name': name,
                'student_id': student_id,
                'contact_info': contact_info,
                'current_grade_id': current_grade_id
            }
            new_id = self.db_manager.insert_one('Students', student_data)
            if new_id:
                # Return the newly created student object with its ID
                return Student(id=new_id, **student_data)
            return None
        except Exception as e:
            print(f"Error adding student: {e}")
            return None

    def get_student_by_id(self, student_id):
        """
        Retrieves a student by their database ID.

        Args:
            student_id (int): The database ID of the student.

        Returns:
            Student or None: The Student object if found, None otherwise.
        """
        data = self.db_manager.get_by_id('Students', student_id)
        return Student.from_dict(data) if data else None

    def get_student_by_unique_id(self, unique_student_id):
        """
        Retrieves a student by their unique student_id (e.g., 'S001').

        Args:
            unique_student_id (str): The unique student ID string.

        Returns:
            Student or None: The Student object if found, None otherwise.
        """
        query = "SELECT * FROM Students WHERE student_id = ?"
        data = self.db_manager.fetch_one(query, (unique_student_id,))
        return Student.from_dict(data) if data else None

    def get_all_students(self):
        """
        Retrieves all students from the database, including their grade names.

        Returns:
            list[dict]: A list of dictionaries, each representing a student
                        with their grade name included.
        """
        query = """
            SELECT
                s.id,
                s.name,
                s.student_id,
                s.contact_info,
                s.current_grade_id,
                g.name AS grade_name
            FROM Students s
            LEFT JOIN Grades g ON s.current_grade_id = g.id
            ORDER BY s.name
        """
        students_data = self.db_manager.fetch_all(query)
        # Convert to list of dictionaries for easier consumption by GUI
        return students_data

    def update_student(self, student_id, name=None, student_unique_id=None, contact_info=None, current_grade_id=None):
        """
        Updates an existing student's information.

        Args:
            student_id (int): The database ID of the student to update.
            name (str, optional): New name.
            student_unique_id (str, optional): New unique student ID.
            contact_info (str, optional): New contact information.
            current_grade_id (int, optional): New current grade ID.

        Returns:
            bool: True if update was successful, False otherwise.
        """
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if student_unique_id is not None:
            update_data['student_id'] = student_unique_id
        if contact_info is not None:
            update_data['contact_info'] = contact_info
        if current_grade_id is not None:
            update_data['current_grade_id'] = current_grade_id

        if not update_data:
            print("No data provided for update.")
            return False

        try:
            rows_affected = self.db_manager.update_one('Students', student_id, update_data)
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating student (ID: {student_id}): {e}")
            return False

    def delete_student(self, student_id):
        """
        Deletes a student from the database.
        Note: This should ideally also handle cascading deletes or prevent deletion
              if related records (e.g., exam results) exist. For simplicity,
              we'll just delete the student record for now.

        Args:
            student_id (int): The database ID of the student to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            rows_affected = self.db_manager.delete_one('Students', student_id)
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting student (ID: {student_id}): {e}")
            return False

# Example Usage (for testing purposes)
if __name__ == '__main__':
    student_service = StudentService()

    # Ensure some grades exist for testing
    from database.db_manager import DBManager
    db_manager = DBManager()
    grade1_id = db_manager.insert_one('Grades', {'name': 'Grade 1', 'description': 'First year'})
    grade8_id = db_manager.insert_one('Grades', {'name': 'Grade 8', 'description': 'Final year'})

    print("\n--- Testing StudentService ---")

    # Add students
    print("Adding John Doe...")
    john = student_service.add_student("John Doe", "S001", "john@example.com", grade1_id)
    if john:
        print(f"Added: {john}")
    else:
        print("Failed to add John Doe.")

    print("Adding Jane Smith...")
    jane = student_service.add_student("Jane Smith", "S002", "jane@example.com", grade8_id)
    if jane:
        print(f"Added: {jane}")
    else:
        print("Failed to add Jane Smith.")

    # Get all students
    print("\nAll Students:")
    all_students = student_service.get_all_students()
    for s in all_students:
        print(s)

    # Update a student
    if john:
        print(f"\nUpdating John Doe (ID: {john.id})...")
        updated = student_service.update_student(john.id, contact_info="john.new@example.com", current_grade_id=grade8_id)
        if updated:
            updated_john = student_service.get_student_by_id(john.id)
            print(f"Updated: {updated_john}")
        else:
            print("Failed to update John Doe.")

    # Get student by unique ID
    print("\nGetting student by unique ID 'S002':")
    found_jane = student_service.get_student_by_unique_id("S002")
    if found_jane:
        print(f"Found: {found_jane}")
    else:
        print("Student S002 not found.")

    # Delete a student
    if john:
        print(f"\nDeleting John Doe (ID: {john.id})...")
        deleted = student_service.delete_student(john.id)
        if deleted:
            print("John Doe deleted successfully.")
        else:
            print("Failed to delete John Doe.")

    print("\nAll Students after deletion:")
    all_students_after_delete = student_service.get_all_students()
    for s in all_students_after_delete:
        print(s)

    db_manager.close_connection() # Close connection after testing
