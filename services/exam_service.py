from database.db_manager import DBManager
from models.exam import Exam
from models.semester import Semester
from models.academic_year import AcademicYear

class ExamService:
    """
    Manages business logic related to Exam operations (including CATs).
    Interacts with the DBManager to perform CRUD operations on Exam data.
    """
    def __init__(self):
        """
        Initializes the ExamService with a DBManager instance.
        """
        self.db_manager = DBManager()

    def add_exam(self, name, academic_year_id, semester_id=None, max_marks=100):
        """
        Adds a new exam or CAT to the database.

        Args:
            name (str): The name of the exam (e.g., "Semester 1 Exam", "CAT 1").
            academic_year_id (int): The ID of the academic year this exam belongs to.
            semester_id (int, optional): The ID of the semester this exam belongs to.
                                         Can be None if it's a yearly exam not tied to a specific semester.
            max_marks (int, optional): The maximum marks for this exam. Defaults to 100.

        Returns:
            Exam or None: The created Exam object if successful, None otherwise.
        """
        try:
            exam_data = {
                'name': name,
                'semester_id': semester_id,
                'academic_year_id': academic_year_id,
                'max_marks': max_marks
            }
            new_id = self.db_manager.insert_one('Exams', exam_data)
            if new_id:
                return Exam(id=new_id, **exam_data)
            return None
        except Exception as e:
            print(f"Error adding exam: {e}")
            return None

    def get_exam_by_id(self, exam_id):
        """
        Retrieves an exam by its database ID.

        Args:
            exam_id (int): The database ID of the exam.

        Returns:
            Exam or None: The Exam object if found, None otherwise.
        """
        data = self.db_manager.get_by_id('Exams', exam_id)
        return Exam.from_dict(data) if data else None

    def get_exam_by_name_and_period(self, name, academic_year_id, semester_id=None):
        """
        Retrieves an exam by its name, academic year, and optional semester.

        Args:
            name (str): The name of the exam.
            academic_year_id (int): The ID of the academic year.
            semester_id (int, optional): The ID of the semester.

        Returns:
            Exam or None: The Exam object if found, None otherwise.
        """
        query = "SELECT * FROM Exams WHERE name = ? AND academic_year_id = ?"
        params = [name, academic_year_id]
        if semester_id is not None:
            query += " AND semester_id = ?"
            params.append(semester_id)
        else:
            query += " AND semester_id IS NULL" # For yearly exams not tied to semester

        data = self.db_manager.fetch_one(query, tuple(params))
        return Exam.from_dict(data) if data else None

    def get_exams_by_academic_year(self, academic_year_id):
        """
        Retrieves all exams for a specific academic year.

        Args:
            academic_year_id (int): The ID of the academic year.

        Returns:
            list[dict]: A list of dictionaries, each representing an exam
                        with related semester and academic year names.
        """
        query = """
            SELECT
                e.id,
                e.name,
                e.max_marks,
                e.semester_id,
                s.name AS semester_name,
                e.academic_year_id,
                ay.year_name AS academic_year_name
            FROM Exams e
            JOIN AcademicYears ay ON e.academic_year_id = ay.id
            LEFT JOIN Semesters s ON e.semester_id = s.id
            WHERE e.academic_year_id = ?
            ORDER BY ay.year_name DESC, s.name, e.name
        """
        exams_data = self.db_manager.fetch_all(query, (academic_year_id,))
        return exams_data

    def get_exams_by_semester(self, semester_id, academic_year_id):
        """
        Retrieves all exams for a specific semester within an academic year.

        Args:
            semester_id (int): The ID of the semester.
            academic_year_id (int): The ID of the academic year.

        Returns:
            list[dict]: A list of dictionaries, each representing an exam.
        """
        query = """
            SELECT
                e.id,
                e.name,
                e.max_marks,
                e.semester_id,
                s.name AS semester_name,
                e.academic_year_id,
                ay.year_name AS academic_year_name
            FROM Exams e
            JOIN AcademicYears ay ON e.academic_year_id = ay.id
            JOIN Semesters s ON e.semester_id = s.id
            WHERE e.semester_id = ? AND e.academic_year_id = ?
            ORDER BY e.name
        """
        exams_data = self.db_manager.fetch_all(query, (semester_id, academic_year_id))
        return exams_data


    def get_all_exams(self):
        """
        Retrieves all exams from the database with related semester and academic year names.

        Returns:
            list[dict]: A list of dictionaries, each representing an exam.
        """
        query = """
            SELECT
                e.id,
                e.name,
                e.max_marks,
                e.semester_id,
                s.name AS semester_name,
                e.academic_year_id,
                ay.year_name AS academic_year_name
            FROM Exams e
            JOIN AcademicYears ay ON e.academic_year_id = ay.id
            LEFT JOIN Semesters s ON e.semester_id = s.id
            ORDER BY ay.year_name DESC, s.name, e.name
        """
        exams_data = self.db_manager.fetch_all(query)
        return exams_data

    def update_exam(self, exam_id, name=None, semester_id=None, academic_year_id=None, max_marks=None):
        """
        Updates an existing exam's information.

        Args:
            exam_id (int): The database ID of the exam to update.
            name (str, optional): New name.
            semester_id (int, optional): New semester ID.
            academic_year_id (int, optional): New academic year ID.
            max_marks (int, optional): New maximum marks.

        Returns:
            bool: True if update was successful, False otherwise.
        """
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if semester_id is not None:
            update_data['semester_id'] = semester_id
        if academic_year_id is not None:
            update_data['academic_year_id'] = academic_year_id
        if max_marks is not None:
            update_data['max_marks'] = max_marks

        if not update_data:
            print("No data provided for update.")
            return False

        try:
            rows_affected = self.db_manager.update_one('Exams', exam_id, update_data)
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating exam (ID: {exam_id}): {e}")
            return False

    def delete_exam(self, exam_id):
        """
        Deletes an exam from the database.
        Note: Consider checking for dependent records (e.g., exam results)
              before allowing deletion.

        Args:
            exam_id (int): The database ID of the exam to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            rows_affected = self.db_manager.delete_one('Exams', exam_id)
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting exam (ID: {exam_id}): {e}")
            return False

# Example Usage (for testing purposes)
if __name__ == '__main__':
    exam_service = ExamService()
    db_manager = DBManager() # For fetching IDs for testing

    # Ensure necessary data exists for testing exams
    ay_2023_2024_id = db_manager.get_academic_year_by_name('2023/2024')['id'] if db_manager.get_academic_year_by_name('2023/2024') else db_manager.insert_one('AcademicYears', {'year_name': '2023/2024', 'start_date': '2023-09-01', 'end_date': '2024-07-31'})
    ay_2024_2025_id = db_manager.get_academic_year_by_name('2024/2025')['id'] if db_manager.get_academic_year_by_name('2024/2025') else db_manager.insert_one('AcademicYears', {'year_name': '2024/2025', 'start_date': '2024-09-01', 'end_date': '2025-07-31'})
    sem1_id = db_manager.get_semester_by_name('Semester 1')['id'] if db_manager.get_semester_by_name('Semester 1') else db_manager.insert_one('Semesters', {'name': 'Semester 1', 'start_date': '2023-09-01', 'end_date': '2024-01-31'})
    sem2_id = db_manager.get_semester_by_name('Semester 2')['id'] if db_manager.get_semester_by_name('Semester 2') else db_manager.insert_one('Semesters', {'name': 'Semester 2', 'start_date': '2024-02-01', 'end_date': '2024-07-31'})

    print("\n--- Testing ExamService ---")

    # Add exams
    print("Adding Semester 1 Exam for 2023/2024...")
    exam_s1_23 = exam_service.add_exam("Semester 1 Exam", ay_2023_2024_id, sem1_id, 100)
    if exam_s1_23:
        print(f"Added: {exam_s1_23}")
    else:
        print("Failed to add Semester 1 Exam (might already exist).")

    print("Adding CAT 1 for Semester 1, 2023/2024...")
    cat1_s1_23 = exam_service.add_exam("CAT 1", ay_2023_2024_id, sem1_id, 30)
    if cat1_s1_23:
        print(f"Added: {cat1_s1_23}")
    else:
        print("Failed to add CAT 1 (might already exist).")

    print("Adding Semester 2 Exam for 2023/2024...")
    exam_s2_23 = exam_service.add_exam("Semester 2 Exam", ay_2023_2024_id, sem2_id, 100)
    if exam_s2_23:
        print(f"Added: {exam_s2_23}")
    else:
        print("Failed to add Semester 2 Exam (might already exist).")

    print("Adding Yearly Final Exam for 2023/2024 (no semester)...")
    yearly_exam_23 = exam_service.add_exam("Yearly Final Exam", ay_2023_2024_id, None, 200)
    if yearly_exam_23:
        print(f"Added: {yearly_exam_23}")
    else:
        print("Failed to add Yearly Final Exam (might already exist).")

    # Get all exams
    print("\nAll Exams:")
    all_exams = exam_service.get_all_exams()
    for e in all_exams:
        print(e)

    # Get exams by academic year
    if ay_2023_2024_id:
        print(f"\nExams for Academic Year 2023/2024:")
        exams_ay23 = exam_service.get_exams_by_academic_year(ay_2023_2024_id)
        for e in exams_ay23:
            print(e)

    # Get exams by semester and academic year
    if sem1_id and ay_2023_2024_id:
        print(f"\nExams for Semester 1, 2023/2024:")
        exams_s1_ay23 = exam_service.get_exams_by_semester(sem1_id, ay_2023_2024_id)
        for e in exams_s1_ay23:
            print(e)

    # Update an exam
    if cat1_s1_23:
        print(f"\nUpdating CAT 1 (ID: {cat1_s1_23.id})...")
        updated = exam_service.update_exam(cat1_s1_23.id, max_marks=40)
        if updated:
            updated_cat1 = exam_service.get_exam_by_id(cat1_s1_23.id)
            print(f"Updated: {updated_cat1}")
        else:
            print("Failed to update CAT 1.")

    # Get exam by name and period
    print("\nGetting exam 'Semester 2 Exam' for 2023/2024, Semester 2:")
    found_exam = exam_service.get_exam_by_name_and_period("Semester 2 Exam", ay_2023_2024_id, sem2_id)
    if found_exam:
        print(f"Found: {found_exam}")
    else:
        print("Semester 2 Exam not found.")

    # Delete an exam (use with caution)
    # if yearly_exam_23:
    #     print(f"\nDeleting Yearly Final Exam (ID: {yearly_exam_23.id})...")
    #     deleted = exam_service.delete_exam(yearly_exam_23.id)
    #     if deleted:
    #         print("Yearly Final Exam deleted successfully.")
    #     else:
    #         print("Failed to delete Yearly Final Exam.")

    print("\nAll Exams after operations:")
    all_exams_after = exam_service.get_all_exams()
    for e in all_exams_after:
        print(e)

    db_manager.close_connection() # Close connection after testing
