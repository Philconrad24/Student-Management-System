from database.db_manager import DBManager
from models.academic_year import AcademicYear

class AcademicYearService:
    """
    Manages business logic related to AcademicYear operations.
    Interacts with the DBManager to perform CRUD operations on AcademicYear data.
    """
    def __init__(self):
        """
        Initializes the AcademicYearService with a DBManager instance.
        """
        self.db_manager = DBManager()

    def add_academic_year(self, year_name, start_date, end_date):
        """
        Adds a new academic year to the database.

        Args:
            year_name (str): The name of the academic year (e.g., "2023/2024").
            start_date (str): The start date (YYYY-MM-DD).
            end_date (str): The end date (YYYY-MM-DD).

        Returns:
            AcademicYear or None: The created AcademicYear object if successful, None otherwise.
        """
        try:
            ay_data = {'year_name': year_name, 'start_date': start_date, 'end_date': end_date}
            new_id = self.db_manager.insert_one('AcademicYears', ay_data)
            if new_id:
                return AcademicYear(id=new_id, **ay_data)
            return None
        except Exception as e:
            print(f"Error adding academic year: {e}")
            return None

    def get_academic_year_by_id(self, ay_id):
        """
        Retrieves an academic year by its database ID.

        Args:
            ay_id (int): The database ID of the academic year.

        Returns:
            AcademicYear or None: The AcademicYear object if found, None otherwise.
        """
        data = self.db_manager.get_by_id('AcademicYears', ay_id)
        return AcademicYear.from_dict(data) if data else None

    def get_academic_year_by_name(self, year_name):
        """
        Retrieves an academic year by its name.

        Args:
            year_name (str): The name of the academic year (e.g., "2023/2024").

        Returns:
            AcademicYear or None: The AcademicYear object if found, None otherwise.
        """
        query = "SELECT * FROM AcademicYears WHERE year_name = ?"
        data = self.db_manager.fetch_one(query, (year_name,))
        return AcademicYear.from_dict(data) if data else None

    def get_all_academic_years(self):
        """
        Retrieves all academic years from the database.

        Returns:
            list[AcademicYear]: A list of AcademicYear objects.
        """
        ays_data = self.db_manager.get_all('AcademicYears', order_by='year_name DESC')
        return [AcademicYear.from_dict(data) for data in ays_data]

    def update_academic_year(self, ay_id, year_name=None, start_date=None, end_date=None):
        """
        Updates an existing academic year's information.

        Args:
            ay_id (int): The database ID of the academic year to update.
            year_name (str, optional): New name.
            start_date (str, optional): New start date (YYYY-MM-DD).
            end_date (str, optional): New end date (YYYY-MM-DD).

        Returns:
            bool: True if update was successful, False otherwise.
        """
        update_data = {}
        if year_name is not None:
            update_data['year_name'] = year_name
        if start_date is not None:
            update_data['start_date'] = start_date
        if end_date is not None:
            update_data['end_date'] = end_date

        if not update_data:
            print("No data provided for update.")
            return False

        try:
            rows_affected = self.db_manager.update_one('AcademicYears', ay_id, update_data)
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating academic year (ID: {ay_id}): {e}")
            return False

    def delete_academic_year(self, ay_id):
        """
        Deletes an academic year from the database.
        Note: Consider checking for dependent records (e.g., enrollments, exams)
              before allowing deletion.

        Args:
            ay_id (int): The database ID of the academic year to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            rows_affected = self.db_manager.delete_one('AcademicYears', ay_id)
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting academic year (ID: {ay_id}): {e}")
            return False

# Example Usage (for testing purposes)
if __name__ == '__main__':
    ay_service = AcademicYearService()

    print("\n--- Testing AcademicYearService ---")

    # Add academic years (2023/2024 should be in schema.py initial setup)
    print("Adding Academic Year 2024/2025...")
    ay_2024_2025 = ay_service.add_academic_year("2024/2025", "2024-09-01", "2025-07-31")
    if ay_2024_2025:
        print(f"Added: {ay_2024_2025}")
    else:
        print("Failed to add 2024/2025 (might already exist).")

    # Get all academic years
    print("\nAll Academic Years:")
    all_ays = ay_service.get_all_academic_years()
    for ay in all_ays:
        print(ay)

    # Update an academic year
    if ay_2024_2025:
        print(f"\nUpdating 2024/2025 (ID: {ay_2024_2025.id})...")
        updated = ay_service.update_academic_year(ay_2024_2025.id, end_date="2025-08-15")
        if updated:
            updated_ay = ay_service.get_academic_year_by_id(ay_2024_2025.id)
            print(f"Updated: {updated_ay}")
        else:
            print("Failed to update 2024/2025.")

    # Get academic year by name
    print("\nGetting academic year by name '2023/2024':")
    found_ay = ay_service.get_academic_year_by_name("2023/2024")
    if found_ay:
        print(f"Found: {found_ay}")
    else:
        print("2023/2024 not found.")

    # Delete an academic year (use with caution)
    # if ay_2024_2025:
    #     print(f"\nDeleting 2024/2025 (ID: {ay_2024_2025.id})...")
    #     deleted = ay_service.delete_academic_year(ay_2024_2025.id)
    #     if deleted:
    #         print("2024/2025 deleted successfully.")
    #     else:
    #         print("Failed to delete 2024/2025.")

    print("\nAll Academic Years after operations:")
    all_ays_after = ay_service.get_all_academic_years()
    for ay in all_ays_after:
        print(ay)
