# sms_management_system/database/db_manager.py

import sqlite3
from database.schema import DATABASE_NAME, create_schema

class DBManager:
    """
    Manages database connections and provides generic CRUD operations.
    """
    def __init__(self):
        """
        Initializes the DBManager, ensuring the database schema exists.
        """
        create_schema() # Ensure schema is created when DBManager is instantiated
        self.conn = None

    def get_connection(self):
        """
        Establishes and returns a database connection.
        """
        if self.conn is None:
            self.conn = sqlite3.connect(DATABASE_NAME)
            self.conn.row_factory = sqlite3.Row # Allows accessing columns by name
        return self.conn

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, query, params=()):
        """
        Executes a SQL query with optional parameters.
        Commits changes for INSERT, UPDATE, DELETE statements.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback() # Rollback changes in case of error
            raise # Re-raise the exception to be handled by the caller

    def fetch_all(self, query, params=()):
        """
        Fetches all rows from a SELECT query.
        Returns a list of dictionaries (or Row objects).
        """
        cursor = self.execute_query(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def fetch_one(self, query, params=()):
        """
        Fetches a single row from a SELECT query.
        Returns a dictionary (or Row object) or None if no row is found.
        """
        cursor = self.execute_query(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def insert_one(self, table_name, data):
        """
        Inserts a single record into the specified table.
        Args:
            table_name (str): The name of the table.
            data (dict): A dictionary where keys are column names and values are data.
        Returns:
            int: The ID of the newly inserted row.
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor = self.execute_query(query, tuple(data.values()))
        return cursor.lastrowid

    def update_one(self, table_name, record_id, data):
        """
        Updates a single record in the specified table by its ID.
        Args:
            table_name (str): The name of the table.
            record_id (int): The ID of the record to update.
            data (dict): A dictionary where keys are column names and values are new data.
        Returns:
            int: Number of rows updated (0 or 1).
        """
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
        params = tuple(data.values()) + (record_id,)
        cursor = self.execute_query(query, params)
        return cursor.rowcount

    def delete_one(self, table_name, record_id):
        """
        Deletes a single record from the specified table by its ID.
        Args:
            table_name (str): The name of the table.
            record_id (int): The ID of the record to delete.
        Returns:
            int: Number of rows deleted (0 or 1).
        """
        query = f"DELETE FROM {table_name} WHERE id = ?"
        cursor = self.execute_query(query, (record_id,))
        return cursor.rowcount

    def get_all(self, table_name, order_by=None):
        """
        Retrieves all records from a table.
        Args:
            table_name (str): The name of the table.
            order_by (str, optional): Column to order results by. Defaults to None.
        Returns:
            list: A list of dictionaries representing the records.
        """
        query = f"SELECT * FROM {table_name}"
        if order_by:
            query += f" ORDER BY {order_by}"
        return self.fetch_all(query)

    def get_by_id(self, table_name, record_id):
        """
        Retrieves a single record by its ID.
        Args:
            table_name (str): The name of the table.
            record_id (int): The ID of the record.
        Returns:
            dict: The record as a dictionary, or None if not found.
        """
        query = f"SELECT * FROM {table_name} WHERE id = ?"
        return self.fetch_one(query, (record_id,))

# Example Usage (for testing purposes)
if __name__ == '__main__':
    db_manager = DBManager()

    # Test Grades
    print("\n--- Testing Grades ---")
    try:
        grade_id_1 = db_manager.insert_one('Grades', {'name': 'Grade 1', 'description': 'First year of primary school'})
        grade_id_8 = db_manager.insert_one('Grades', {'name': 'Grade 8', 'description': 'Final year of primary school'})
        print(f"Inserted Grade 1 (ID: {grade_id_1}) and Grade 8 (ID: {grade_id_8})")
    except sqlite3.IntegrityError as e:
        print(f"Grades already exist or unique constraint violated: {e}")

    grades = db_manager.get_all('Grades')
    print("All Grades:", grades)

    # Test Subjects
    print("\n--- Testing Subjects ---")
    predefined_subjects = [
        {'name': 'Mathematics', 'description': 'Study of numbers and shapes'},
        {'name': 'Science', 'description': 'Study of the natural world'},
        {'name': 'English', 'description': 'Language arts'},
        {'name': 'Kiswahili', 'description': 'National language'},
        {'name': 'Social Studies', 'description': 'History and Geography'},
        {'name': 'Religious Education', 'description': 'Study of religion'},
        {'name': 'Art and Craft', 'description': 'Creative expression'},
        {'name': 'Physical Education', 'description': 'Sports and fitness'}
    ]
    for subject_data in predefined_subjects:
        try:
            subject_id = db_manager.insert_one('Subjects', subject_data)
            print(f"Inserted subject {subject_data['name']} (ID: {subject_id})")
        except sqlite3.IntegrityError as e:
            print(f"Subject '{subject_data['name']}' already exists or unique constraint violated: {e}")

    subjects = db_manager.get_all('Subjects')
    print("All Subjects:", subjects)

    # Test Academic Years
    print("\n--- Testing Academic Years ---")
    try:
        ay_id = db_manager.insert_one('AcademicYears', {'year_name': '2023/2024', 'start_date': '2023-09-01', 'end_date': '2024-07-31'})
        print(f"Inserted Academic Year 2023/2024 (ID: {ay_id})")
    except sqlite3.IntegrityError as e:
        print(f"Academic Year already exists or unique constraint violated: {e}")
    academic_years = db_manager.get_all('AcademicYears')
    print("All Academic Years:", academic_years)


    # Test Semesters
    print("\n--- Testing Semesters ---")
    try:
        sem1_id = db_manager.insert_one('Semesters', {'name': 'Semester 1', 'start_date': '2023-09-01', 'end_date': '2024-01-31'})
        sem2_id = db_manager.insert_one('Semesters', {'name': 'Semester 2', 'start_date': '2024-02-01', 'end_date': '2024-07-31'})
        print(f"Inserted Semester 1 (ID: {sem1_id}) and Semester 2 (ID: {sem2_id})")
    except sqlite3.IntegrityError as e:
        print(f"Semesters already exist or unique constraint violated: {e}")
    semesters = db_manager.get_all('Semesters')
    print("All Semesters:", semesters)


    # Test Students
    print("\n--- Testing Students ---")
    try:
        student_id_john = db_manager.insert_one('Students', {'name': 'John Doe', 'student_id': 'S001', 'contact_info': 'john.doe@example.com', 'current_grade_id': grade_id_1})
        student_id_jane = db_manager.insert_one('Students', {'name': 'Jane Smith', 'student_id': 'S002', 'contact_info': 'jane.smith@example.com', 'current_grade_id': grade_id_8})
        print(f"Inserted John Doe (ID: {student_id_john}) and Jane Smith (ID: {student_id_jane})")
    except sqlite3.IntegrityError as e:
        print(f"Students already exist or unique constraint violated: {e}")
    students = db_manager.get_all('Students')
    print("All Students:", students)

    # Test update
    print("\n--- Testing Update ---")
    db_manager.update_one('Students', student_id_john, {'contact_info': 'john.d@newemail.com'})
    updated_john = db_manager.get_by_id('Students', student_id_john)
    print("Updated John Doe:", updated_john)

    # Test delete
    # print("\n--- Testing Delete ---")
    # db_manager.delete_one('Students', student_id_jane)
    # students_after_delete = db_manager.get_all('Students')
    # print("Students after deleting Jane:", students_after_delete)

    db_manager.close_connection()
