from database.db_manager import DBManager
from models.semester_result import SemesterResult
from models.student import Student
from models.semester import Semester
from models.academic_year import AcademicYear
from models.exam import Exam
from models.exam_result import ExamResult


class SemesterResultService:
    """
    Manages business logic related to SemesterResult operations,
    including computation of semester results and ranking.
    """

    def __init__(self):
        """
        Initializes the SemesterResultService with a DBManager instance.
        """
        self.db_manager = DBManager()

    def add_semester_result(self, student_id, semester_id, academic_year_id,
                            total_marks=None, average_score=None, grade_rank=None):
        """
        Adds a new semester result or updates an existing one.
        This method is primarily called internally after computation.

        Args:
            student_id (int): The ID of the student.
            semester_id (int): The ID of the semester.
            academic_year_id (int): The ID of the academic year.
            total_marks (float, optional): The total marks for the semester.
            average_score (float, optional): The average score for the semester.
            grade_rank (int, optional): The student's rank within their grade for this semester.

        Returns:
            SemesterResult or None: The created/updated SemesterResult object if successful, None otherwise.
        """
        try:
            existing_result = self.get_semester_result_by_composite_keys(
                student_id, semester_id, academic_year_id)

            semester_result_data = {
                'student_id': student_id,
                'semester_id': semester_id,
                'academic_year_id': academic_year_id,
                'total_marks': total_marks,
                'average_score': average_score,
                'grade_rank': grade_rank
            }

            if existing_result:
                # Update existing result
                self.db_manager.update_one('SemesterResults', existing_result.id, semester_result_data)
                return SemesterResult(id=existing_result.id, **semester_result_data)
            else:
                # Insert new result
                new_id = self.db_manager.insert_one('SemesterResults', semester_result_data)
                if new_id:
                    return SemesterResult(id=new_id, **semester_result_data)
            return None
        except Exception as e:
            print(f"Error adding/updating semester result: {e}")
            return None

    def get_semester_result_by_id(self, result_id):
        """
        Retrieves a semester result by its database ID.

        Args:
            result_id (int): The database ID of the semester result.

        Returns:
            SemesterResult or None: The SemesterResult object if found, None otherwise.
        """
        data = self.db_manager.get_by_id('SemesterResults', result_id)
        return SemesterResult.from_dict(data) if data else None

    def get_semester_result_by_composite_keys(self, student_id, semester_id, academic_year_id):
        """
        Retrieves a semester result using student, semester, and academic year IDs.

        Args:
            student_id (int): The ID of the student.
            semester_id (int): The ID of the semester.
            academic_year_id (int): The ID of the academic year.

        Returns:
            SemesterResult or None: The SemesterResult object if found, None otherwise.
        """
        query = "SELECT * FROM SemesterResults WHERE student_id = ? AND semester_id = ? AND academic_year_id = ?"
        data = self.db_manager.fetch_one(query, (student_id, semester_id, academic_year_id))
        return SemesterResult.from_dict(data) if data else None

    def get_semester_results_for_student(self, student_id):
        """
        Retrieves all semester results for a specific student.

        Args:
            student_id (int): The ID of the student.

        Returns:
            list[dict]: A list of dictionaries, each representing a semester result
                        with semester and academic year names.
        """
        query = """
            SELECT
                sr.id,
                sr.student_id,
                st.name AS student_name,
                sr.semester_id,
                sem.name AS semester_name,
                sr.academic_year_id,
                ay.year_name AS academic_year_name,
                sr.total_marks,
                sr.average_score,
                sr.grade_rank
            FROM SemesterResults sr
            JOIN Students st ON sr.student_id = st.id
            JOIN Semesters sem ON sr.semester_id = sem.id
            JOIN AcademicYears ay ON sr.academic_year_id = ay.id
            WHERE sr.student_id = ?
            ORDER BY ay.year_name DESC, sem.name
        """
        results_data = self.db_manager.fetch_all(query, (student_id,))
        return results_data

    def get_semester_results_by_academic_year_and_grade(self, academic_year_id, grade_id):
        """
        Retrieves all semester results for students in a specific grade
        within a given academic year.

        Args:
            academic_year_id (int): The ID of the academic year.
            grade_id (int): The ID of the grade.

        Returns:
            list[dict]: A list of dictionaries, each representing a semester result
                        with student, semester, academic year, and grade names.
        """
        query = """
            SELECT
                sr.id,
                sr.student_id,
                s.name AS student_name,
                s.student_id AS student_unique_id,
                sr.semester_id,
                sem.name AS semester_name,
                sr.academic_year_id,
                ay.year_name AS academic_year_name,
                sr.total_marks,
                sr.average_score,
                sr.grade_rank
            FROM SemesterResults sr
            JOIN Students s ON sr.student_id = s.id
            JOIN Semesters sem ON sr.semester_id = sem.id
            JOIN AcademicYears ay ON sr.academic_year_id = ay.id
            WHERE sr.academic_year_id = ?
            AND s.current_grade_id = ? -- Assuming current_grade_id reflects their grade for the year
            ORDER BY sr.average_score DESC, s.name
        """
        results_data = self.db_manager.fetch_all(query, (academic_year_id, grade_id))
        return results_data

    def get_all_semester_results(self):
        """
        Retrieves all semester results from the database with related details.

        Returns:
            list[dict]: A list of dictionaries, each representing a semester result.
        """
        query = """
            SELECT
                sr.id,
                sr.student_id,
                st.name AS student_name,
                st.student_id AS student_unique_id,
                sr.semester_id,
                sem.name AS semester_name,
                sr.academic_year_id,
                ay.year_name AS academic_year_name,
                sr.total_marks,
                sr.average_score,
                sr.grade_rank
            FROM SemesterResults sr
            JOIN Students st ON sr.student_id = st.id
            JOIN Semesters sem ON sr.semester_id = sem.id
            JOIN AcademicYears ay ON sr.academic_year_id = ay.id
            ORDER BY ay.year_name DESC, sem.name, st.name
        """
        results_data = self.db_manager.fetch_all(query)
        return results_data

    def update_semester_result(self, result_id, total_marks=None, average_score=None, grade_rank=None):
        """
        Updates an existing semester result's computed values.

        Args:
            result_id (int): The database ID of the semester result to update.
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
            rows_affected = self.db_manager.update_one('SemesterResults', result_id, update_data)
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating semester result (ID: {result_id}): {e}")
            return False

    def delete_semester_result(self, result_id):
        """
        Deletes a semester result from the database.

        Args:
            result_id (int): The database ID of the semester result to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            rows_affected = self.db_manager.delete_one('SemesterResults', result_id)
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting semester result (ID: {result_id}): {e}")
            return False

    def compute_and_store_semester_results(self, academic_year_id, semester_id):
        """
        Computes the final results for all students for a given semester
        and stores them in the SemesterResults table.
        Also computes and assigns ranks per grade.

        Args:
            academic_year_id (int): The ID of the academic year.
            semester_id (int): The ID of the semester.
        """
        print(f"\n--- Computing Semester Results for AY {academic_year_id}, Semester {semester_id} ---")

        # 1. Get all students enrolled in this academic year
        # We need their current_grade_id to group them for ranking
        query_students = """
            SELECT
                s.id AS student_id,
                s.current_grade_id AS grade_id
            FROM Students s
            JOIN Enrollments e ON s.id = e.student_id
            WHERE e.academic_year_id = ?
        """
        students_in_year = self.db_manager.fetch_all(query_students, (academic_year_id,))

        if not students_in_year:
            print("No students found enrolled in this academic year. No semester results to compute.")
            return

        # Get all exams (Semester Exam, CAT1, CAT2) for this semester and academic year
        query_exams = """
            SELECT id, name, max_marks
            FROM Exams
            WHERE academic_year_id = ? AND semester_id = ?
            AND (name LIKE '%Semester%' OR name LIKE '%CAT%')
        """
        semester_exams = self.db_manager.fetch_all(query_exams, (academic_year_id, semester_id))

        if not semester_exams:
            print(
                f"No relevant exams (Semester Exam, CAT1, CAT2) found for Semester {semester_id}, AY {academic_year_id}. Cannot compute semester results.")
            return

        semester_exam_ids = [e['id'] for e in semester_exams if 'Semester' in e['name']]
        cat_exam_ids = [e['id'] for e in semester_exams if 'CAT' in e['name']]

        # Dictionary to hold results per student and their grade for ranking
        student_semester_data = {}  # {student_id: {'total_marks': X, 'num_subjects': Y, 'grade_id': Z}}

        for student_info in students_in_year:
            student_id = student_info['student_id']
            grade_id = student_info['grade_id']

            total_semester_exam_marks = 0
            total_cat_marks = 0
            num_subjects_with_exam_results = 0

            # Fetch all exam results for this student in this semester's exams
            query_student_results = """
                SELECT er.marks, e.name AS exam_name, e.max_marks AS exam_max_marks
                FROM ExamResults er
                JOIN Exams e ON er.exam_id = e.id
                WHERE er.student_id = ? AND e.academic_year_id = ? AND e.semester_id = ?
            """
            student_exam_results = self.db_manager.fetch_all(query_student_results,
                                                             (student_id, academic_year_id, semester_id))

            if not student_exam_results:
                # print(f"No exam results found for student {student_id} in Semester {semester_id}. Skipping.")
                continue  # Skip students with no results for this semester

            # Group results by subject to ensure we count each subject once for average
            subject_marks = {}  # {subject_id: {'exam_marks': [], 'cat_marks': []}}

            # Aggregate marks per subject from all relevant exams
            for res in student_exam_results:
                exam_name = res['exam_name']
                marks = res['marks']
                exam_max_marks = res['exam_max_marks']

                # Determine if it's a semester exam or a CAT
                if 'Semester' in exam_name:
                    total_semester_exam_marks += marks
                elif 'CAT' in exam_name:
                    total_cat_marks += marks

            # For simplicity, let's assume total_marks is sum of all relevant exam marks
            # And average_score is total_marks / (number of subjects * number of main exams/CATs)
            # A more robust system would calculate average per subject, then sum averages.

            # Simplified calculation based on total marks from all relevant exams
            # This needs to be refined based on how 'average scores' are truly calculated.
            # Let's assume for now: (Sum of Semester Exam Scores) + (Average of CAT 1 & CAT 2)
            # This requires knowing how many subjects the student took and how many main exams/CATs there are.

            # Revised Calculation Logic:
            # Sum of Semester Exam scores + Sum of CAT scores (assuming CATs are weighted equally)
            # Total possible marks for the semester for a student will depend on the number of subjects
            # and the max marks for each exam type (Semester Exam, CAT1, CAT2)
            # This is complex without knowing the number of subjects per student.

            # Let's simplify: Sum of all recorded marks for main exams and CATs for this semester
            # Average will be total marks / count of *valid* marks entries.
            # This assumes all subjects have results for all relevant exams.

            # Let's get actual subjects for the student for this academic year and grade
            query_student_subjects = """
                SELECT DISTINCT s.id AS subject_id
                FROM Subjects s
                JOIN ExamResults er ON s.id = er.subject_id
                JOIN Exams e ON er.exam_id = e.id
                WHERE er.student_id = ?
                AND e.academic_year_id = ?
                AND e.semester_id = ?
            """
            student_subjects_in_semester = self.db_manager.fetch_all(query_student_subjects,
                                                                     (student_id, academic_year_id, semester_id))
            num_subjects_with_results = len(student_subjects_in_semester)

            if num_subjects_with_results == 0:
                print(f"Student {student_id} has no subjects with results in Semester {semester_id}. Skipping.")
                continue

            # Calculate total marks and average score for the semester
            # Based on the functional requirement:
            # "final result for each semester based on the sum of semester exam scores
            # and the average scores for CAT 1 and CAT 2."
            # This implies a per-subject calculation then aggregation.

            # Let's refine:
            # For each subject, get Semester Exam score and average CAT scores.
            # Sum these per-subject totals for the overall semester total.
            # Average is overall semester total / (number of subjects * (1 main exam + 1 average CAT score))
            # This is still tricky without knowing which CATs apply to which subjects.

            # Simpler interpretation:
            # Total marks = sum of all marks from "Semester X Exam" + sum of marks from "CAT 1" + sum of marks from "CAT 2"
            # Average score = Total marks / (Number of subjects * (Max marks of Semester Exam + Avg Max Marks of CATs))
            # This needs a more direct way to get all subjects a student is taking.

            # Let's assume, for now, that "sum of semester exam scores" means the sum of scores
            # from the 'Semester X Exam' for all subjects.
            # And "average scores for CAT 1 and CAT 2" means (CAT1_score + CAT2_score) / 2 for each subject,
            # and then summing these averages across subjects.

            total_semester_score = 0.0
            total_possible_semester_score = 0.0
            num_subjects_counted = 0

            # Get all subjects a student has results for in this semester
            query_subjects_with_results = """
                SELECT DISTINCT er.subject_id, s.name AS subject_name
                FROM ExamResults er
                JOIN Subjects s ON er.subject_id = s.id
                JOIN Exams e ON er.exam_id = e.id
                WHERE er.student_id = ? AND e.academic_year_id = ? AND e.semester_id = ?
            """
            subjects_with_results = self.db_manager.fetch_all(query_subjects_with_results,
                                                              (student_id, academic_year_id, semester_id))

            for subject_entry in subjects_with_results:
                subject_id = subject_entry['subject_id']

                # Get Semester Exam score for this subject
                sem_exam_query = """
                    SELECT er.marks, e.max_marks
                    FROM ExamResults er
                    JOIN Exams e ON er.exam_id = e.id
                    WHERE er.student_id = ? AND er.subject_id = ? AND e.academic_year_id = ? AND e.semester_id = ? AND e.name LIKE '%Semester%Exam%'
                """
                sem_exam_result = self.db_manager.fetch_one(sem_exam_query,
                                                            (student_id, subject_id, academic_year_id, semester_id))

                subject_semester_exam_score = sem_exam_result['marks'] if sem_exam_result else 0.0
                subject_semester_exam_max_marks = sem_exam_result['max_marks'] if sem_exam_result else 0.0

                # Get CAT scores for this subject
                cat_scores = []
                cat_max_marks = []
                cat_query = """
                    SELECT er.marks, e.max_marks
                    FROM ExamResults er
                    JOIN Exams e ON er.exam_id = e.id
                    WHERE er.student_id = ? AND er.subject_id = ? AND e.academic_year_id = ? AND e.semester_id = ? AND e.name LIKE '%CAT%'
                """
                cat_results = self.db_manager.fetch_all(cat_query,
                                                        (student_id, subject_id, academic_year_id, semester_id))

                for cat_res in cat_results:
                    cat_scores.append(cat_res['marks'])
                    cat_max_marks.append(cat_res['max_marks'])

                avg_cat_score = sum(cat_scores) / len(cat_scores) if cat_scores else 0.0
                avg_cat_max_marks = sum(cat_max_marks) / len(cat_max_marks) if cat_max_marks else 0.0

                # Compute per-subject total for the semester
                # "sum of semester exam scores and the average scores for CAT 1 and CAT 2."
                # This implies: (Semester Exam Score) + (Average of CAT scores)
                subject_total_for_semester = subject_semester_exam_score + avg_cat_score
                subject_possible_total_for_semester = subject_semester_exam_max_marks + avg_cat_max_marks

                if subject_possible_total_for_semester > 0:  # Only count subjects where there were actual exams
                    total_semester_score += subject_total_for_semester
                    total_possible_semester_score += subject_possible_total_for_semester
                    num_subjects_counted += 1

            if num_subjects_counted == 0:
                print(f"Student {student_id} has no valid subject results for semester calculation. Skipping.")
                continue

            average_score = (
                                        total_semester_score / total_possible_semester_score) * 100 if total_possible_semester_score > 0 else 0.0

            student_semester_data[student_id] = {
                'total_marks': total_semester_score,
                'average_score': average_score,
                'grade_id': grade_id  # For ranking
            }

        # 2. Compute ranks per grade
        grades_in_year = sorted(
            list(set([s['grade_id'] for s in students_in_year if s['student_id'] in student_semester_data])))

        for grade_id in grades_in_year:
            # Filter students belonging to this grade and who have computed results
            students_in_grade = [
                (s_id, data['average_score'])
                for s_id, data in student_semester_data.items()
                if data['grade_id'] == grade_id
            ]
            # Sort by average score in descending order
            students_in_grade.sort(key=lambda x: x[1], reverse=True)

            current_rank = 1
            prev_score = -1  # Sentinel value
            for i, (s_id, avg_score) in enumerate(students_in_grade):
                if avg_score != prev_score:
                    current_rank = i + 1
                student_semester_data[s_id]['grade_rank'] = current_rank
                prev_score = avg_score

        # 3. Store/Update results in SemesterResults table
        for student_id, data in student_semester_data.items():
            self.add_semester_result(
                student_id=student_id,
                semester_id=semester_id,
                academic_year_id=academic_year_id,
                total_marks=data['total_marks'],
                average_score=data['average_score'],
                grade_rank=data['grade_rank']
            )
            print(
                f"Computed/Stored Semester Result for Student {student_id}: Total={data['total_marks']:.2f}, Avg={data['average_score']:.2f}%, Rank={data['grade_rank']}")

        print("Semester result computation complete.")


# Example Usage (for testing purposes)
if __name__ == '__main__':
    semester_result_service = SemesterResultService()
    db_manager = DBManager()  # For fetching IDs for testing

    # --- Setup Test Data (ensure these exist from previous tests or insert them) ---
    # Grades
    grade1_id = db_manager.get_grade_by_name('Grade 1')['id'] if db_manager.get_grade_by_name(
        'Grade 1') else db_manager.insert_one('Grades', {'name': 'Grade 1'})
    grade2_id = db_manager.get_grade_by_name('Grade 2')['id'] if db_manager.get_grade_by_name(
        'Grade 2') else db_manager.insert_one('Grades', {'name': 'Grade 2'})
    grade8_id = db_manager.get_grade_by_name('Grade 8')['id'] if db_manager.get_grade_by_name(
        'Grade 8') else db_manager.insert_one('Grades', {'name': 'Grade 8'})

    # Academic Year and Semesters
    ay_2023_2024_id = db_manager.get_academic_year_by_name('2023/2024')['id'] if db_manager.get_academic_year_by_name(
        '2023/2024') else db_manager.insert_one('AcademicYears', {'year_name': '2023/2024', 'start_date': '2023-09-01',
                                                                  'end_date': '2024-07-31'})
    sem1_id = db_manager.get_semester_by_name('Semester 1')['id'] if db_manager.get_semester_by_name(
        'Semester 1') else db_manager.insert_one('Semesters', {'name': 'Semester 1', 'start_date': '2023-09-01',
                                                               'end_date': '2024-01-31'})
    sem2_id = db_manager.get_semester_by_name('Semester 2')['id'] if db_manager.get_semester_by_name(
        'Semester 2') else db_manager.insert_one('Semesters', {'name': 'Semester 2', 'start_date': '2024-02-01',
                                                               'end_date': '2024-07-31'})

    # Students (ensure their current_grade_id is set correctly for ranking)
    student_john_id = db_manager.get_student_by_unique_id('S001')['id'] if db_manager.get_student_by_unique_id(
        'S001') else db_manager.insert_one('Students', {'name': 'John Doe', 'student_id': 'S001',
                                                        'contact_info': 'john@example.com',
                                                        'current_grade_id': grade1_id})
    student_jane_id = db_manager.get_student_by_unique_id('S002')['id'] if db_manager.get_student_by_unique_id(
        'S002') else db_manager.insert_one('Students', {'name': 'Jane Smith', 'student_id': 'S002',
                                                        'contact_info': 'jane@example.com',
                                                        'current_grade_id': grade1_id})  # Jane also in Grade 1 for ranking test
    student_mike_id = db_manager.get_student_by_unique_id('S003')['id'] if db_manager.get_student_by_unique_id(
        'S003') else db_manager.insert_one('Students', {'name': 'Mike Brown', 'student_id': 'S003',
                                                        'contact_info': 'mike@example.com',
                                                        'current_grade_id': grade2_id})

    # Subjects
    math_id = db_manager.get_subject_by_name('Mathematics')['id'] if db_manager.get_subject_by_name(
        'Mathematics') else db_manager.insert_one('Subjects', {'name': 'Mathematics'})
    science_id = db_manager.get_subject_by_name('Science')['id'] if db_manager.get_subject_by_name(
        'Science') else db_manager.insert_one('Subjects', {'name': 'Science'})
    english_id = db_manager.get_subject_by_name('English')['id'] if db_manager.get_subject_by_name(
        'English') else db_manager.insert_one('Subjects', {'name': 'English'})

    # Enrollments (important for `compute_and_store_semester_results` to find students)
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

    # Exam Results (ensure these are added before computing semester results)
    # John Doe (Grade 1)
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

    # Jane Smith (Grade 1)
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

    # Mike Brown (Grade 2)
    db_manager.insert_one('ExamResults',
                          {'student_id': student_mike_id, 'exam_id': exam_s1_23_id, 'subject_id': math_id, 'marks': 90})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_mike_id, 'exam_id': cat1_s1_23_id, 'subject_id': math_id, 'marks': 29})
    db_manager.insert_one('ExamResults',
                          {'student_id': student_mike_id, 'exam_id': cat2_s1_23_id, 'subject_id': math_id, 'marks': 30})

    print("\n--- Testing SemesterResultService ---")

    # Compute and store semester results
    semester_result_service.compute_and_store_semester_results(ay_2023_2024_id, sem1_id)

    # Get all semester results
    print("\nAll Semester Results:")
    all_semester_results = semester_result_service.get_all_semester_results()
    for r in all_semester_results:
        print(r)

    # Get semester results for a specific student
    if student_john_id:
        print(f"\nSemester Results for John Doe (ID: {student_john_id}):")
        john_semester_results = semester_result_service.get_semester_results_for_student(student_john_id)
        for r in john_semester_results:
            print(r)

    # Get semester results by academic year and grade
    if ay_2023_2024_id and grade1_id:
        print(f"\nSemester Results for 2023/2024, Grade 1:")
        grade1_semester_results = semester_result_service.get_semester_results_by_academic_year_and_grade(
            ay_2023_2024_id, grade1_id)
        for r in grade1_semester_results:
            print(r)

    # Update a semester result (e.g., if re-computation changes rank or scores)
    # This is typically handled by `compute_and_store_semester_results` itself
    # but provided for direct update capability if needed.
    # if all_semester_results:
    #     first_result_id = all_semester_results[0]['id']
    #     print(f"\nUpdating first semester result (ID: {first_result_id})...")
    #     updated = semester_result_service.update_semester_result(first_result_id, total_marks=150.0, average_score=75.0, grade_rank=99)
    #     if updated:
    #         updated_result = semester_result_service.get_semester_result_by_id(first_result_id)
    #         print(f"Updated: {updated_result}")
    #     else:
    #         print("Failed to update semester result.")

    # Delete a semester result (use with caution)
    # if all_semester_results:
    #     last_result_id = all_semester_results[-1]['id']
    #     print(f"\nDeleting last semester result (ID: {last_result_id})...")
    #     deleted = semester_result_service.delete_semester_result(last_result_id)
    #     if deleted:
    #         print("Semester result deleted successfully.")
    #     else:
    #         print("Failed to delete semester result.")

    print("\nAll Semester Results after operations:")
    all_semester_results_after = semester_result_service.get_all_semester_results()
    for r in all_semester_results_after:
        print(r)

    db_manager.close_connection()  # Close connection after testing
