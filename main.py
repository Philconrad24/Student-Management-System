from gui.main_window import StudentManagementApp
from database.schema import create_schema  # To ensure database is set up on app start


def main():
    """
    Main function to initialize the database and run the GUI application.
    """
    # Ensure the database schema is created/updated
    create_schema()

    # Run the GUI application
    app = StudentManagementApp()
    app.mainloop()


if __name__ == "__main__":
    main()