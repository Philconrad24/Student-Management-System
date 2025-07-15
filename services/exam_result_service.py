from database.db_manager import DBManager
from models.exam_result import ExamResult
from models.student import Student
from models.exam import Exam
from models.subject import Subject

class ExamResultService:
    """
    Manages business logic related to individual ExamResult operations.
    Interacts with the DBManager to perform CRUD operations on ExamResult data.
    """
    def __init__(self):
        """
        Initializes the ExamResultService with a DBManager instance.
        """
        self.db_manager = DBManager()

    def add_exam_result(self, student_id, exam_id, subject_id, marks):
        """
        Adds a new exam result for a student in a specific subject and exam.

        Args:
            student_id (int): The ID of the student.
            exam_id (int): The ID of the exam.
            subject_id (int): The ID of the subject.
            marks (float): The marks obtained by the student.

        Returns:
            ExamResult or None: The created ExamResult object if successful, None otherwise.
        """
        try:
            # Check if a result for this student, exam, and subject already exists
            existing_result = self.get_exam_result_by_composite_keys(student_id, exam_id, subject_id)
            if existing_result:
                print(f"Result for student {student_id}, exam {exam_id}, subject {subject_id} already exists. Use update_exam_result instead.")
                return None

            exam_result_data = {
                'student_id': student_id,
                'exam_id': exam_id,
                'subject_id': subject_id,
                'marks': marks
            }
            new_id = self.db_manager.insert_one('ExamResults', exam_result_data)
            if new_id:
                return ExamResult(id=new_id, **exam_result_data)
            return None
        except Exception as e:
            print(f"Error adding exam result: {e}")
            return None

    def get_exam_result_by_id(self, result_id):
        """
        Retrieves an exam result by its database ID.

        Args:
            result_id (int): The database ID of the exam result.

        Returns:
            ExamResult or None: The ExamResult object if found, None otherwise.
        """
        data = self.db_manager.get_by_id('ExamResults', result_id)
        return ExamResult.from_dict(data) if data else None

    def get_exam_result_by_composite_keys(self, student_id, exam_id, subject_id):
        """
        Retrieves an exam result using student, exam, and subject IDs.

        Args:
            student_id (int): The ID of the student.
            exam_id (int): The ID of the exam.
            subject_id (int): The ID of the subject.

        Returns:
            ExamResult or None: The ExamResult object if found, None otherwise.
        """
        query = "SELECT * FROM ExamResults WHERE student_id = ? AND exam_id = ? AND subject_id = ?"
        data = self.db_manager.fetch_one(query, (student_id, exam_id, subject_id))
        return ExamResult.from_dict(data) if data else None

    def get_results_for_student_by_exam(self, student_id, exam_id):
        """
        Retrieves all exam results for a specific student in a given exam.

        Args:
            student_id (int): The ID of the student.
            exam_id (int): The ID of the exam.

        Returns:
            list[dict]: A list of dictionaries, each representing an exam result
                        with subject name included.
        """
        query = """
            SELECT
                er.id,
                er.student_id,
                er.exam_id,
                er.subject_id,
                s.name AS subject_name,
                er.marks
            FROM ExamResults er
            JOIN Subjects s ON er.subject_id = s.id
            WHERE er.student_id = ? AND er.exam_id = ?
            ORDER BY s.name
        """
        results_data = self.db_manager.fetch_all(query, (student_id, exam_id))
        return results_data

    def get_results_for_exam_by_subject(self, exam_id, subject_id):
        """
        Retrieves all exam results for a specific subject in a given exam.

        Args:
            exam_id (int): The ID of the exam.
            subject_id (int): The ID of the subject.

        Returns:
            list[dict]: A list of dictionaries, each representing an exam result
                        with student name included.
        """
        query = """
            SELECT
                er.id,
                er.student_id,
                st.name AS student_name,
                st.student_id AS student_unique_id,
                er.exam_id,
                er.subject_id,
                er.marks
            FROM ExamResults er
            JOIN Students st ON er.student_id = st.id
            WHERE er.exam_id = ? AND er.subject_id = ?
            ORDER BY st.name
        """
        results_data = self.db_manager.fetch_all(query, (exam_id, subject_id))
        return results_data

    def get_all_exam_results(self):
        """
        Retrieves all exam results from the database with related student, exam, and subject names.

        Returns:
            list[dict]: A list of dictionaries, each representing an exam result.
        """
        query = """
            SELECT
                er.id,
                er.student_id,
                st.name AS student_name,
                st.student_id AS student_unique_id,
                er.exam_id,
                e.name AS exam_name,
                e.max_marks AS exam_max_marks,
                er.subject_id,
                sub.name AS subject_name,
                er.marks
            FROM ExamResults er
            JOIN Students st ON er.student_id = st.id
            JOIN Exams e ON er.exam_id = e.id
            JOIN Subjects sub ON er.subject_id = sub.id
            ORDER BY st.name, e.name, sub.name
        """
        results_data = self.db_manager.fetch_all(query)
        return results_data

    def update_exam_result(self, result_id, marks=None):
        """
        Updates an existing exam result's marks.

        Args:
            result_id (int): The database ID of the exam result to update.
            marks (float, optional): New marks.

        Returns:
            bool: True if update was successful, False otherwise.
        """
        update_data = {}
        if marks is not None:
            update_data['marks'] = marks

        if not update_data:
            print("No data provided for update.")
            return False

        try:
            rows_affected = self.db_manager.update_one('ExamResults', result_id, update_data)
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating exam result (ID: {result_id}): {e}")
            return False

    def delete_exam_result(self, result_id):
        """
        Deletes an exam result from the database.

        Args:
            result_id (int): The database ID of the exam result to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            rows_affected = self.db_manager.delete_one('ExamResults', result_id)
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting exam result (ID: {result_id}): {e}")
            return False

# Example Usage (for testing purposes)
if __name__ == '__main__':
    exam_result_service = ExamResultService()
    db_manager = DBManager() # For fetching IDs for testing

    # Ensure necessary data exists for testing exam results
    # Students
    student_john_id = db_manager.get_student_by_unique_id('S001')['id'] if db_manager.get_student_by_unique_id('S001') else db_manager.insert_one('Students', {'name': 'John Doe', 'student_id': 'S001', 'contact_info': 'john@example.com', 'current_grade_id': 1})
    student_jane_id = db_manager.get_student_by_unique_id('S002')['id'] if db_manager.get_student_by_unique_id('S002') else db_manager.insert_one('Students', {'name': 'Jane Smith', 'student_id': 'S002', 'contact_info': 'jane@example.com', 'current_grade_id': 8})

    # Academic Year and Semester
    ay_2023_2024_id = db_manager.get_academic_year_by_name('2023/2024')['id'] if db_manager.get_academic_year_by_name('2023/2024') else db_manager.insert_one('AcademicYears', {'year_name': '2023/2024', 'start_date': '2023-09-01', 'end_date': '2024-07-31'})
    sem1_id = db_manager.get_semester_by_name('Semester 1')['id'] if db_manager.get_semester_by_name('Semester 1') else db_manager.insert_one('Semesters', {'name': 'Semester 1', 'start_date': '2023-09-01', 'end_date': '2024-01-31'})

    # Exams
    exam_s1_23_id = db_manager.get_exam_by_name_and_period("Semester 1 Exam", ay_2023_2024_id, sem1_id)['id'] if db_manager.get_exam_by_name_and_period("Semester 1 Exam", ay_2023_2024_id, sem1_id) else db_manager.insert_one('Exams', {'name': 'Semester 1 Exam', 'academic_year_id': ay_2023_2024_id, 'semester_id': sem1_id, 'max_marks': 100})
    cat1_s1_23_id = db_manager.get_exam_by_name_and_period("CAT 1", ay_2023_2024_id, sem1_id)['id'] if db_manager.get_exam_by_name_and_period("CAT 1", ay_2023_2024_id, sem1_id) else db_manager.insert_one('Exams', {'name': 'CAT 1', 'academic_year_id': ay_2023_2024_id, 'semester_id': sem1_id, 'max_marks': 30})

    # Subjects
    math_id = db_manager.get_subject_by_name('Mathematics')['id'] if db_manager.get_subject_by_name('Mathematics') else db_manager.insert_one('Subjects', {'name': 'Mathematics'})
    science_id = db_manager.get_subject_by_name('Science')['id'] if db_manager.get_subject_by_name('Science') else db_manager.insert_one('Subjects', {'name': 'Science'})

    print("\n--- Testing ExamResultService ---")

    # Add exam results
    print("Adding John Doe's Math result for Semester 1 Exam...")
    john_math_exam_result = exam_result_service.add_exam_result(student_john_id, exam_s1_23_id, math_id, 85.5)
    if john_math_exam_result:
        print(f"Added: {john_math_exam_result}")
    else:
        print("Failed to add John Doe's Math result (might already exist).")

    print("Adding John Doe's Science result for CAT 1...")
    john_science_cat_result = exam_result_service.add_exam_result(student_john_id, cat1_s1_23_id, science_id, 25)
    if john_science_cat_result:
        print(f"Added: {john_science_cat_result}")
    else:
        print("Failed to add John Doe's Science CAT result (might already exist).")

    print("Adding Jane Smith's Math result for Semester 1 Exam...")
    jane_math_exam_result = exam_result_service.add_exam_result(student_jane_id, exam_s1_23_id, math_id, 92)
    if jane_math_exam_result:
        print(f"Added: {jane_math_exam_result}")
    else:
        print("Failed to add Jane Smith's Math result (might already exist).")

    # Get results for a student by exam
    if student_john_id and exam_s1_23_id:
        print(f"\nResults for John Doe in Semester 1 Exam:")
        john_s1_results = exam_result_service.get_results_for_student_by_exam(student_john_id, exam_s1_23_id)
        for r in john_s1_results:
            print(r)

    # Get all exam results
    print("\nAll Exam Results:")
    all_results = exam_result_service.get_all_exam_results()
    for r in all_results:
        print(r)

    # Update an exam result
    if john_math_exam_result:
        print(f"\nUpdating John Doe's Math result (ID: {john_math_exam_result.id})...")
        updated = exam_result_service.update_exam_result(john_math_exam_result.id, marks=88.0)
        if updated:
            updated_john_math = exam_result_service.get_exam_result_by_id(john_math_exam_result.id)
            print(f"Updated: {updated_john_math}")
        else:
            print("Failed to update John Doe's Math result.")

    # Delete an exam result (use with caution)
    # if john_science_cat_result:
    #     print(f"\nDeleting John Doe's Science CAT result (ID: {john_science_cat_result.id})...")
    #     deleted = exam_result_service.delete_exam_result(john_science_cat_result.id)
    #     if deleted:
    #         print("John Doe's Science CAT result deleted successfully.")
    #     else:
    #         print("Failed to delete John Doe's Science CAT result.")

    print("\nAll Exam Results after operations:")
    all_results_after = exam_result_service.get_all_exam_results()
    for r in all_results_after:
        print(r)

    db_manager.close_connection() # Close connection after testing
