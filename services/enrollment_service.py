from database.db_manager import DBManager
from models.enrollment import Enrollment
from models.student import Student
from models.academic_year import AcademicYear
from models.grade import Grade

class EnrollmentService:
    """
    Manages business logic related to Student Enrollment operations.
    Interacts with the DBManager to perform CRUD operations on Enrollment data.
    """
    def __init__(self):
        """
        Initializes the EnrollmentService with a DBManager instance.
        """
        self.db_manager = DBManager()

    def add_enrollment(self, student_id, academic_year_id, grade_id):
        """
        Enrolls a student in a specific grade for an academic year.

        Args:
            student_id (int): The ID of the student.
            academic_year_id (int): The ID of the academic year.
            grade_id (int): The ID of the grade.

        Returns:
            Enrollment or None: The created Enrollment object if successful, None otherwise.
        """
        try:
            enrollment_data = {
                'student_id': student_id,
                'academic_year_id': academic_year_id,
                'grade_id': grade_id
            }
            new_id = self.db_manager.insert_one('Enrollments', enrollment_data)
            if new_id:
                return Enrollment(id=new_id, **enrollment_data)
            return None
        except Exception as e:
            print(f"Error adding enrollment: {e}")
            return None

    def get_enrollment_by_id(self, enrollment_id):
        """
        Retrieves an enrollment by its database ID.

        Args:
            enrollment_id (int): The database ID of the enrollment.

        Returns:
            Enrollment or None: The Enrollment object if found, None otherwise.
        """
        data = self.db_manager.get_by_id('Enrollments', enrollment_id)
        return Enrollment.from_dict(data) if data else None

    def get_enrollments_for_student(self, student_id):
        """
        Retrieves all enrollments for a specific student.

        Args:
            student_id (int): The ID of the student.

        Returns:
            list[dict]: A list of dictionaries, each representing an enrollment
                        with student, academic year, and grade names included.
        """
        query = """
            SELECT
                e.id,
                e.student_id,
                s.name AS student_name,
                s.student_id AS student_unique_id,
                e.academic_year_id,
                ay.year_name AS academic_year_name,
                e.grade_id,
                g.name AS grade_name
            FROM Enrollments e
            JOIN Students s ON e.student_id = s.id
            JOIN AcademicYears ay ON e.academic_year_id = ay.id
            JOIN Grades g ON e.grade_id = g.id
            WHERE e.student_id = ?
            ORDER BY ay.year_name DESC
        """
        enrollments_data = self.db_manager.fetch_all(query, (student_id,))
        return enrollments_data

    def get_enrollments_by_academic_year_and_grade(self, academic_year_id, grade_id):
        """
        Retrieves all enrollments for a specific academic year and grade.

        Args:
            academic_year_id (int): The ID of the academic year.
            grade_id (int): The ID of the grade.

        Returns:
            list[dict]: A list of dictionaries, each representing an enrollment
                        with student details.
        """
        query = """
            SELECT
                e.id,
                e.student_id,
                s.name AS student_name,
                s.student_id AS student_unique_id,
                e.academic_year_id,
                ay.year_name AS academic_year_name,
                e.grade_id,
                g.name AS grade_name
            FROM Enrollments e
            JOIN Students s ON e.student_id = s.id
            JOIN AcademicYears ay ON e.academic_year_id = ay.id
            JOIN Grades g ON e.grade_id = g.id
            WHERE e.academic_year_id = ? AND e.grade_id = ?
            ORDER BY s.name
        """
        enrollments_data = self.db_manager.fetch_all(query, (academic_year_id, grade_id))
        return enrollments_data

    def get_all_enrollments(self):
        """
        Retrieves all enrollments from the database with related details.

        Returns:
            list[dict]: A list of dictionaries, each representing an enrollment
                        with student, academic year, and grade names included.
        """
        query = """
            SELECT
                e.id,
                e.student_id,
                s.name AS student_name,
                s.student_id AS student_unique_id,
                e.academic_year_id,
                ay.year_name AS academic_year_name,
                e.grade_id,
                g.name AS grade_name
            FROM Enrollments e
            JOIN Students s ON e.student_id = s.id
            JOIN AcademicYears ay ON e.academic_year_id = ay.id
            JOIN Grades g ON e.grade_id = g.id
            ORDER BY ay.year_name DESC, g.name, s.name
        """
        enrollments_data = self.db_manager.fetch_all(query)
        return enrollments_data

    def update_enrollment(self, enrollment_id, student_id=None, academic_year_id=None, grade_id=None):
        """
        Updates an existing enrollment's information.

        Args:
            enrollment_id (int): The database ID of the enrollment to update.
            student_id (int, optional): New student ID.
            academic_year_id (int, optional): New academic year ID.
            grade_id (int, optional): New grade ID.

        Returns:
            bool: True if update was successful, False otherwise.
        """
        update_data = {}
        if student_id is not None:
            update_data['student_id'] = student_id
        if academic_year_id is not None:
            update_data['academic_year_id'] = academic_year_id
        if grade_id is not None:
            update_data['grade_id'] = grade_id

        if not update_data:
            print("No data provided for update.")
            return False

        try:
            rows_affected = self.db_manager.update_one('Enrollments', enrollment_id, update_data)
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating enrollment (ID: {enrollment_id}): {e}")
            return False

    def delete_enrollment(self, enrollment_id):
        """
        Deletes an enrollment from the database.

        Args:
            enrollment_id (int): The database ID of the enrollment to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            rows_affected = self.db_manager.delete_one('Enrollments', enrollment_id)
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting enrollment (ID: {enrollment_id}): {e}")
            return False

# Example Usage (for testing purposes)
if __name__ == '__main__':
    enrollment_service = EnrollmentService()
    db_manager = DBManager() # For fetching IDs for testing

    # Ensure necessary data exists for testing enrollments
    grade1_id = db_manager.get_grade_by_name('Grade 1')['id'] if db_manager.get_grade_by_name('Grade 1') else db_manager.insert_one('Grades', {'name': 'Grade 1'})
    grade8_id = db_manager.get_grade_by_name('Grade 8')['id'] if db_manager.get_grade_by_name('Grade 8') else db_manager.insert_one('Grades', {'name': 'Grade 8'})
    ay_2023_2024_id = db_manager.get_academic_year_by_name('2023/2024')['id'] if db_manager.get_academic_year_by_name('2023/2024') else db_manager.insert_one('AcademicYears', {'year_name': '2023/2024', 'start_date': '2023-09-01', 'end_date': '2024-07-31'})
    ay_2024_2025_id = db_manager.get_academic_year_by_name('2024/2025')['id'] if db_manager.get_academic_year_by_name('2024/2025') else db_manager.insert_one('AcademicYears', {'year_name': '2024/2025', 'start_date': '2024-09-01', 'end_date': '2025-07-31'})

    student_john_id = db_manager.get_student_by_unique_id('S001')['id'] if db_manager.get_student_by_unique_id('S001') else db_manager.insert_one('Students', {'name': 'John Doe', 'student_id': 'S001', 'contact_info': 'john@example.com', 'current_grade_id': grade1_id})
    student_jane_id = db_manager.get_student_by_unique_id('S002')['id'] if db_manager.get_student_by_unique_id('S002') else db_manager.insert_one('Students', {'name': 'Jane Smith', 'student_id': 'S002', 'contact_info': 'jane@example.com', 'current_grade_id': grade8_id})


    print("\n--- Testing EnrollmentService ---")

    # Add enrollments
    print("Enrolling John Doe in Grade 1 for 2023/2024...")
    enroll_john_g1_ay23 = enrollment_service.add_enrollment(student_john_id, ay_2023_2024_id, grade1_id)
    if enroll_john_g1_ay23:
        print(f"Added: {enroll_john_g1_ay23}")
    else:
        print("Failed to enroll John Doe (might already exist).")

    print("Enrolling Jane Smith in Grade 8 for 2023/2024...")
    enroll_jane_g8_ay23 = enrollment_service.add_enrollment(student_jane_id, ay_2023_2024_id, grade8_id)
    if enroll_jane_g8_ay23:
        print(f"Added: {enroll_jane_g8_ay23}")
    else:
        print("Failed to enroll Jane Smith (might already exist).")

    print("Enrolling John Doe in Grade 2 for 2024/2025 (promotion)...")
    # Assuming Grade 2 exists or creating it for testing
    grade2_id = db_manager.get_grade_by_name('Grade 2')['id'] if db_manager.get_grade_by_name('Grade 2') else db_manager.insert_one('Grades', {'name': 'Grade 2'})
    enroll_john_g2_ay24 = enrollment_service.add_enrollment(student_john_id, ay_2024_2025_id, grade2_id)
    if enroll_john_g2_ay24:
        print(f"Added: {enroll_john_g2_ay24}")
    else:
        print("Failed to enroll John Doe in Grade 2 for 2024/2025 (might already exist).")


    # Get all enrollments
    print("\nAll Enrollments:")
    all_enrollments = enrollment_service.get_all_enrollments()
    for e in all_enrollments:
        print(e)

    # Get enrollments for a specific student
    if student_john_id:
        print(f"\nEnrollments for John Doe (ID: {student_john_id}):")
        john_enrollments = enrollment_service.get_enrollments_for_student(student_john_id)
        for e in john_enrollments:
            print(e)

    # Get enrollments by academic year and grade
    if ay_2023_2024_id and grade1_id:
        print(f"\nEnrollments for 2023/2024, Grade 1:")
        enrollments_g1_ay23 = enrollment_service.get_enrollments_by_academic_year_and_grade(ay_2023_2024_id, grade1_id)
        for e in enrollments_g1_ay23:
            print(e)

    # Update an enrollment (e.g., correct grade)
    if enroll_john_g1_ay23:
        print(f"\nUpdating John Doe's 2023/2024 enrollment (ID: {enroll_john_g1_ay23.id})...")
        # Let's say John was actually in Grade 1.5 (hypothetically, if we had such a grade)
        # For now, let's just re-confirm his grade.
        updated = enrollment_service.update_enrollment(enroll_john_g1_ay23.id, grade_id=grade1_id)
        if updated:
            updated_enrollment = enrollment_service.get_enrollment_by_id(enroll_john_g1_ay23.id)
            print(f"Updated: {updated_enrollment}")
        else:
            print("Failed to update John Doe's enrollment.")

    # Delete an enrollment (use with caution)
    # if enroll_john_g1_ay23:
    #     print(f"\nDeleting John Doe's 2023/2024 enrollment (ID: {enroll_john_g1_ay23.id})...")
    #     deleted = enrollment_service.delete_enrollment(enroll_john_g1_ay23.id)
    #     if deleted:
    #         print("John Doe's 2023/2024 enrollment deleted successfully.")
    #     else:
    #         print("Failed to delete John Doe's 2023/2024 enrollment.")

    print("\nAll Enrollments after operations:")
    all_enrollments_after = enrollment_service.get_all_enrollments()
    for e in all_enrollments_after:
        print(e)

    db_manager.close_connection() # Close connection after testing
