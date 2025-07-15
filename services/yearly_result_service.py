from database.db_manager import DBManager
from models.yearly_result import YearlyResult
from models.student import Student
from models.academic_year import AcademicYear
from services.semester_result_service import SemesterResultService  # To get semester results


class YearlyResultService:
    """
    Manages business logic related to YearlyResult operations,
    including computation of yearly results and ranking.
    """

    def __init__(self):
        """
        Initializes the YearlyResultService with a DBManager instance.
        """
        self.db_manager = DBManager()
        self.semester_result_service = SemesterResultService()  # Dependency

    def add_yearly_result(self, student_id, academic_year_id,
                          total_marks=None, average_score=None, grade_rank=None):
        """
        Adds a new yearly result or updates an existing one.
        This method is primarily called internally after computation.

        Args:
            student_id (int): The ID of the student.
            academic_year_id (int): The ID of the academic year.
            total_marks (float, optional): The total marks for the academic year.
            average_score (float, optional): The average score for the academic year.
            grade_rank (int, optional): The student's rank within their grade for this academic year.

        Returns:
            YearlyResult or None: The created/updated YearlyResult object if successful, None otherwise.
        """
        try:
            existing_result = self.get_yearly_result_by_composite_keys(
                student_id, academic_year_id)

            yearly_result_data = {
                'student_id': student_id,
                'academic_year_id': academic_year_id,
                'total_marks': total_marks,
                'average_score': average_score,
                'grade_rank': grade_rank
            }

            if existing_result:
                # Update existing result
                self.db_manager.update_one('YearlyResults', existing_result.id, yearly_result_data)
                return YearlyResult(id=existing_result.id, **yearly_result_data)
            else:
                # Insert new result
                new_id = self.db_manager.insert_one('YearlyResults', yearly_result_data)
                if new_id:
                    return YearlyResult(id=new_id, **yearly_result_data)
            return None
        except Exception as e:
            print(f"Error adding/updating yearly result: {e}")
            return None

    def get_yearly_result_by_id(self, result_id):
        """
        Retrieves a yearly result by its database ID.

        Args:
            result_id (int): The database ID of the yearly result.

        Returns:
            YearlyResult or None: The YearlyResult object if found, None otherwise.
        """
        data = self.db_manager.get_by_id('YearlyResults', result_id)
        return YearlyResult.from_dict(data) if data else None

    def get_yearly_result_by_composite_keys(self, student_id, academic_year_id):
        """
        Retrieves a yearly result using student and academic year IDs.

        Args:
            student_id (int): The ID of the student.
            academic_year_id (int): The ID of the academic year.

        Returns:
            YearlyResult or None: The YearlyResult object if found, None otherwise.
        """
        query = "SELECT * FROM YearlyResults WHERE student_id = ? AND academic_year_id = ?"
        data = self.db_manager.fetch_one(query, (student_id, academic_year_id))
        return YearlyResult.from_dict(data) if data else None

    def get_yearly_results_for_student(self, student_id):
        """
        Retrieves all yearly results for a specific student.

        Args:
            student_id (int): The ID of the student.

        Returns:
            list[dict]: A list of dictionaries, each representing a yearly result
                        with academic year name.
        """
        query = """
            SELECT
                yr.id,
                yr.student_id,
                st.name AS student_name,
                yr.academic_year_id,
                ay.year_name AS academic_year_name,
                yr.total_marks,
                yr.average_score,
                yr.grade_rank
            FROM YearlyResults yr
            JOIN Students st ON yr.student_id = st.id
            JOIN AcademicYears ay ON yr.academic_year_id = ay.id
            WHERE yr.student_id = ?
            ORDER BY ay.year_name DESC
        """
        results_data = self.db_manager.fetch_all(query, (student_id,))
        return results_data

    def get_yearly_results_by_academic_year_and_grade(self, academic_year_id, grade_id):
        """
        Retrieves all yearly results for students in a specific grade
        within a given academic year.

        Args:
            academic_year_id (int): The ID of the academic year.
            grade_id (int): The ID of the grade.

        Returns:
            list[dict]: A list of dictionaries, each representing a yearly result
                        with student, academic year, and grade names.
        """
        query = """
            SELECT
                yr.id,
                yr.student_id,
                s.name AS student_name,
                s.student_id AS student_unique_id,
                yr.academic_year_id,
                ay.year_name AS academic_year_name,
                yr.total_marks,
                yr.average_score,
                yr.grade_rank
            FROM YearlyResults yr
            JOIN Students s ON yr.student_id = s.id
            JOIN AcademicYears ay ON yr.academic_year_id = ay.id
            WHERE yr.academic_year_id = ?
            AND s.current_grade_id = ? -- Assuming current_grade_id reflects their grade for the year
            ORDER BY yr.average_score DESC, s.name
        """
        results_data = self.db_manager.fetch_all(query, (academic_year_id, grade_id))
        return results_data

    def get_all_yearly_results(self):
        """
        Retrieves all yearly results from the database with related details.

        Returns:
            list[dict]: A list of dictionaries, each representing a yearly result.
        """
        query = """
            SELECT
                yr.id,
                yr.student_id,
                st.name AS student_name,
                st.student_id AS student_unique_id,
                yr.academic_year_id,
                ay.year_name AS academic_year_name,
                yr.total_marks,
                yr.average_score,
                yr.grade_rank
            FROM YearlyResults yr
            JOIN Students st ON yr.student_id = st.id
            JOIN AcademicYears ay ON yr.academic_year_id = ay.id
            ORDER BY ay.year_name DESC, st.name
        """
        results_data = self.db_manager.fetch_all(query)
        return results_data

    def update_yearly_result(self, result_id, total_marks=None, average_score=None, grade_rank=None):
        """
        Updates an existing yearly result's computed values.

        Args:
            result_id (int): The database ID of the yearly result to update.
            total_marks (float, optional): New total marks.
            average_score (float, optional): New average score.
            grade_rank (int, optional): New rank.

        Returns:
            bool: True if update was successful, False otherwise.
        """
        update_data = {}
        if total_marks is not None:
            update_data['total_marks'] = total_marks
        if average_score is not None:
            update_data['average_score'] = average_score
        if grade_rank is not None:
            update_data['grade_rank'] = grade_rank

        if not update_data:
            print("No data provided for update.")
            return False

        try:
            rows_affected = self.db_manager.update_one('YearlyResults', result_id, update_data)
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating yearly result (ID: {result_id}): {e}")
            return False

    def delete_yearly_result(self, result_id):
        """
        Deletes a yearly result from the database.

        Args:
            result_id (int): The database ID of the yearly result to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            rows_affected = self.db_manager.delete_one('YearlyResults', result_id)
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting yearly result (ID: {result_id}): {e}")
            return False

    def compute_and_store_yearly_results(self, academic_year_id):
        """
        Computes the final yearly results for all students for a given academic year
        by summing up their semester results and then ranking them.

        Args:
            academic_year_id (int): The ID of the academic year.
        """
        print(f"\n--- Computing Yearly Results for AY {academic_year_id} ---")

        # 1. Get all semester results for this academic year
        query_semester_results = """
            SELECT
                sr.student_id,
                sr.total_marks,
                sr.average_score,
                s.current_grade_id AS grade_id -- Need student's grade for yearly ranking
            FROM SemesterResults sr
            JOIN Students s ON sr.student_id = s.id
            WHERE sr.academic_year_id = ?
        """
        semester_results_data = self.db_manager.fetch_all(query_semester_results, (academic_year_id,))

        if not semester_results_data:
            print("No semester results found for this academic year. Cannot compute yearly results.")
            return

        # Aggregate semester results per student
        student_yearly_data = {}  # {student_id: {'total_marks': X, 'count_semesters': Y, 'grade_id': Z}}

        for res in semester_results_data:
            student_id = res['student_id']
            total_marks = res['total_marks']
            average_score = res['average_score']  # This is semester average, not yearly avg

            if student_id not in student_yearly_data:
                student_yearly_data[student_id] = {
                    'total_marks_sum': 0.0,
                    'average_score_sum': 0.0,  # Sum of semester averages
                    'num_semesters': 0,
                    'grade_id': res['grade_id']
                }
            student_yearly_data[student_id]['total_marks_sum'] += total_marks
            student_yearly_data[student_id]['average_score_sum'] += average_score
            student_yearly_data[student_id]['num_semesters'] += 1

        # Calculate final yearly total and average for each student
        for student_id, data in student_yearly_data.items():
            final_total_marks = data['total_marks_sum']
            final_average_score = data['average_score_sum'] / data['num_semesters'] if data[
                                                                                           'num_semesters'] > 0 else 0.0

            student_yearly_data[student_id]['total_marks'] = final_total_marks
            student_yearly_data[student_id]['average_score'] = final_average_score

        # 2. Compute ranks per grade for the academic year
        # Get all unique grades involved in this academic year's results
        grades_in_year = sorted(list(set([s['grade_id'] for s in student_yearly_data.values()])))

        for grade_id in grades_in_year:
            # Filter students belonging to this grade and who have computed yearly results
            students_in_grade = [
                (s_id, data['average_score'])
                for s_id, data in student_yearly_data.items()
                if data['grade_id'] == grade_id
            ]
            # Sort by average score in descending order
            students_in_grade.sort(key=lambda x: x[1], reverse=True)

            current_rank = 1
            prev_score = -1  # Sentinel value
            for i, (s_id, avg_score) in enumerate(students_in_grade):
                if avg_score != prev_score:
                    current_rank = i + 1
                student_yearly_data[s_id]['grade_rank'] = current_rank
                prev_score = avg_score

        # 3. Store/Update results in YearlyResults table
        for student_id, data in student_yearly_data.items():
            self.add_yearly_result(
                student_id=student_id,
                academic_year_id=academic_year_id,
                total_marks=data['total_marks'],
                average_score=data['average_score'],
                grade_rank=data['grade_rank']
            )
            print(
                f"Computed/Stored Yearly Result for Student {student_id}: Total={data['total_marks']:.2f}, Avg={data['average_score']:.2f}%, Rank={data['grade_rank']}")

        print("Yearly result computation complete.")


# Example Usage (for testing purposes)
if __name__ == '__main__':
    yearly_result_service = YearlyResultService()
    db_manager = DBManager()  # For fetching IDs for testing

    # --- Ensure Semester Results exist for computation ---
    # Run the SemesterResultService test block or ensure data is present
    from services.semester_result_service import SemesterResultService

    sem_res_service = SemesterResultService()

    # Setup necessary data (copy-pasted from semester_result_service test for completeness)
    grade1_id = db_manager.get_grade_by_name('Grade 1')['id'] if db_manager.get_grade_by_name(
        'Grade 1') else db_manager.insert_one('Grades', {'name': 'Grade 1'})
    grade2_id = db_manager.get_grade_by_name('Grade 2')['id'] if db_manager.get_grade_by_name(
        'Grade 2') else db_manager.insert_one('Grades', {'name': 'Grade 2'})
    ay_2023_2024_id = db_manager.get_academic_year_by_name('2023/2024')['id'] if db_manager.get_academic_year_by_name(
        '2023/2024') else db_manager.insert_one('AcademicYears', {'year_name': '2023/2024', 'start_date': '2023-09-01',
                                                                  'end_date': '2024-07-31'})
    sem1_id = db_manager.get_semester_by_name('Semester 1')['id'] if db_manager.get_semester_by_name(
        'Semester 1') else db_manager.insert_one('Semesters', {'name': 'Semester 1', 'start_date': '2023-09-01',
                                                               'end_date': '2024-01-31'})
    sem2_id = db_manager.get_semester_by_name('Semester 2')['id'] if db_manager.get_semester_by_name(
        'Semester 2') else db_manager.insert_one('Semesters', {'name': 'Semester 2', 'start_date': '2024-02-01',
                                                               'end_date': '2024-07-31'})
    student_john_id = db_manager.get_student_by_unique_id('S001')['id'] if db_manager.get_student_by_unique_id(
        'S001') else db_manager.insert_one('Students', {'name': 'John Doe', 'student_id': 'S001',
                                                        'contact_info': 'john@example.com',
                                                        'current_grade_id': grade1_id})
    student_jane_id = db_manager.get_student_by_unique_id('S002')['id'] if db_manager.get_student_by_unique_id(
        'S002') else db_manager.insert_one('Students', {'name': 'Jane Smith', 'student_id': 'S002',
                                                        'contact_info': 'jane@example.com',
                                                        'current_grade_id': grade1_id})
    student_mike_id = db_manager.get_student_by_unique_id('S003')['id'] if db_manager.get_student_by_unique_id(
        'S003') else db_manager.insert_one('Students', {'name': 'Mike Brown', 'student_id': 'S003',
                                                        'contact_info': 'mike@example.com',
                                                        'current_grade_id': grade2_id})
    math_id = db_manager.get_subject_by_name('Mathematics')['id'] if db_manager.get_subject_by_name(
        'Mathematics') else db_manager.insert_one('Subjects', {'name': 'Mathematics'})
    science_id = db_manager.get_subject_by_name('Science')['id'] if db_manager.get_subject_by_name(
        'Science') else db_manager.insert_one('Subjects', {'name': 'Science'})
    english_id = db_manager.get_subject_by_name('English')['id'] if db_manager.get_subject_by_name(
        'English') else db_manager.insert_one('Subjects', {'name': 'English'})

    # Enrollments
    db_manager.insert_one('Enrollments',
                          {'student_id': student_john_id, 'academic_year_id': ay_2023_2024_id, 'grade_id': grade1_id})
    db_manager.insert_one('Enrollments',
                          {'student_id': student_jane_id, 'academic_year_id': ay_2023_2024_id, 'grade_id': grade1_id})
    db_manager.insert_one('Enrollments',
                          {'student_id': student_mike_id, 'academic_year_id': ay_2023_2024_id, 'grade_id': grade2_id})

    # Exams
    exam_s1_23_id = db_manager.get_exam_by_name_and_period("Semester 1 Exam", ay_2023_2024_id, sem1_id)[
        'id'] if db_manager.get_exam_by_name_and_period("Semester 1 Exam", ay_2023_2024_id,
                                                        sem1_id) else db_manager.insert_one('Exams',
                                                                                            {'name': 'Semester 1 Exam',
                                                                                             'academic_year_id': ay_2023_2024_id,
                                                                                             'semester_id': sem1_id,
                                                                                             'max_marks': 100})
    cat1_s1_23_id = db_manager.get_exam_by_name_and_period("CAT 1", ay_2023_2024_id, sem1_id)[
        'id'] if db_manager.get_exam_by_name_and_period("CAT 1", ay_2023_2024_id, sem1_id) else db_manager.insert_one(
        'Exams', {'name': 'CAT 1', 'academic_year_id': ay_2023_2024_id, 'semester_id': sem1_id, 'max_marks': 30})
    cat2_s1_23_id = db_manager.get_exam_by_name_and_period("CAT 2", ay_2023_2024_id, sem1_id)[
        'id'] if db_manager.get_exam_by_name_and_period("CAT 2", ay_2023_2024_id, sem1_id) else db_manager.insert_one(
        'Exams', {'name': 'CAT 2', 'academic_year_id': ay_2023_2024_id, 'semester_id': sem1_id, 'max_marks': 30})
    exam_s2_23_id = db_manager.get_exam_by_name_and_period("Semester 2 Exam", ay_2023_2024_id, sem2_id)[
        'id'] if db_manager.get_exam_by_name_and_period("Semester 2 Exam", ay_2023_2024_id,
                                                        sem2_id) else db_manager.insert_one('Exams',
                                                                                            {'name': 'Semester 2 Exam',
                                                                                             'academic_year_id': ay_2023_2024_id,
                                                                                             'semester_id': sem2_id,
                                                                                             'max_marks': 100})
    cat1_s2_23_id = db_manager.get_exam_by_name_and_period("CAT 1", ay_2023_2024_id, sem2_id)[
        'id'] if db_manager.get_exam_by_name_and_period("CAT 1", ay_2023_2024_id, sem2_id) else db_manager.insert_one(
        'Exams', {'name': 'CAT 1', 'academic_year_id': ay_2023_2024_id, 'semester_id': sem2_id, 'max_marks': 30})
    cat2_s2_23_id = db_manager.get_exam_by_name_and_period("CAT 2", ay_2023_2024_id, sem2_id)[
        'id'] if db_manager.get_exam_by_name_and_period("CAT 2", ay_2023_2024_id, sem2_id) else db_manager.insert_one(
        'Exams', {'name': 'CAT 2', 'academic_year_id': ay_2023_2024_id, 'semester_id': sem2_id, 'max_marks': 30})

    # Exam Results (ensure these are added for both semesters)
    # John Doe S1
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': exam_s1_23_id, 'subject_id': math_id, 'marks': 70})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': cat1_s1_23_id, 'subject_id': math_id, 'marks': 25})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': cat2_s1_23_id, 'subject_id': math_id, 'marks': 28})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': exam_s1_23_id, 'subject_id': science_id,
                           'marks': 65})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': cat1_s1_23_id, 'subject_id': science_id,
                           'marks': 20})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': cat2_s1_23_id, 'subject_id': science_id,
                           'marks': 22})
    # John Doe S2
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': exam_s2_23_id, 'subject_id': math_id, 'marks': 75})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': cat1_s2_23_id, 'subject_id': math_id, 'marks': 26})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': cat2_s2_23_id, 'subject_id': math_id, 'marks': 29})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': exam_s2_23_id, 'subject_id': science_id,
                           'marks': 70})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': cat1_s2_23_id, 'subject_id': science_id,
                           'marks': 23})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_john_id, 'exam_id': cat2_s2_23_id, 'subject_id': science_id,
                           'marks': 25})

    # Jane Smith S1
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': exam_s1_23_id, 'subject_id': math_id, 'marks': 80})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': cat1_s1_23_id, 'subject_id': math_id, 'marks': 28})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': cat2_s1_23_id, 'subject_id': math_id, 'marks': 29})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': exam_s1_23_id, 'subject_id': english_id,
                           'marks': 75})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': cat1_s1_23_id, 'subject_id': english_id,
                           'marks': 26})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': cat2_s1_23_id, 'subject_id': english_id,
                           'marks': 27})
    # Jane Smith S2
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': exam_s2_23_id, 'subject_id': math_id, 'marks': 85})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': cat1_s2_23_id, 'subject_id': math_id, 'marks': 29})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': cat2_s2_23_id, 'subject_id': math_id, 'marks': 30})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': exam_s2_23_id, 'subject_id': english_id,
                           'marks': 80})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': cat1_s2_23_id, 'subject_id': english_id,
                           'marks': 28})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_jane_id, 'exam_id': cat2_s2_23_id, 'subject_id': english_id,
                           'marks': 29})

    # Mike Brown S1
    db_manager.insert_one('ExamResults',
                          {'student_id': student_mike_id, 'exam_id': exam_s1_23_id, 'subject_id': math_id, 'marks': 90})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_mike_id, 'exam_id': cat1_s1_23_id, 'subject_id': math_id, 'marks': 29})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_mike_id, 'exam_id': cat2_s1_23_id, 'subject_id': math_id, 'marks': 30})
    # Mike Brown S2
    db_manager.insert_one('ExamResults',
                          {'student_id': student_mike_id, 'exam_id': exam_s2_23_id, 'subject_id': math_id, 'marks': 95})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_mike_id, 'exam_id': cat1_s2_23_id, 'subject_id': math_id, 'marks': 30})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_mike_id, 'exam_id': cat2_s2_23_id, 'subject_id': math_id, 'marks': 30})

    # First, compute Semester 1 results
    sem_res_service.compute_and_store_semester_results(ay_2023_2024_id, sem1_id)
    # Then, compute Semester 2 results
    sem_res_service.compute_and_store_semester_results(ay_2023_2024_id, sem2_id)

    print("\n--- Testing YearlyResultService ---")

    # Compute and store yearly results
    yearly_result_service.compute_and_store_yearly_results(ay_2023_2024_id)

    # Get all yearly results
    print("\nAll Yearly Results:")
    all_yearly_results = yearly_result_service.get_all_yearly_results()
    for r in all_yearly_results:
        print(r)

    # Get yearly results for a specific student
    if student_john_id:
        print(f"\nYearly Results for John Doe (ID: {student_john_id}):")
        john_yearly_results = yearly_result_service.get_yearly_results_for_student(student_john_id)
        for r in john_yearly_results:
            print(r)

    # Get yearly results by academic year and grade
    if ay_2023_2024_id and grade1_id:
        print(f"\nYearly Results for 2023/2024, Grade 1:")
        grade1_yearly_results = yearly_result_service.get_yearly_results_by_academic_year_and_grade(ay_2023_2024_id,
                                                                                                    grade1_id)
        for r in grade1_yearly_results:
            print(r)

    # Update a yearly result (typically handled by `compute_and_store_yearly_results` itself)
    # if all_yearly_results:
    #     first_yr_id = all_yearly_results[0]['id']
    #     print(f"\nUpdating first yearly result (ID: {first_yr_id})...")
    #     updated = yearly_result_service.update_yearly_result(first_yr_id, total_marks=300.0, average_score=75.0, grade_rank=99)
    #     if updated:
    #         updated_yr = yearly_result_service.get_yearly_result_by_id(first_yr_id)
    #         print(f"Updated: {updated_yr}")
    #     else:
    #         print("Failed to update yearly result.")

    # Delete a yearly result (use with caution)
    # if all_yearly_results:
    #     last_yr_id = all_yearly_results[-1]['id']
    #     print(f"\nDeleting last yearly result (ID: {last_yr_id})...")
    #     deleted = yearly_result_service.delete_yearly_result(last_yr_id)
    #     if deleted:
    #         print("Yearly result deleted successfully.")
    #     else:
    #         print("Failed to delete yearly result.")

    print("\nAll Yearly Results after operations:")
    all_yearly_results_after = yearly_result_service.get_all_yearly_results()
    for r in all_yearly_results_after:
        print(r)

    db_manager.close_connection()  # Close connection after testing
