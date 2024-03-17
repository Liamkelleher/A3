import psycopg2
from psycopg2 import sql

# Global
global new_student_id

# Connect to the PostgreSQL database
def connect_to_database():
    connection = psycopg2.connect(
        dbname="Assignment3",
        user="postgres",
        password="liam872003",
        host="localhost",
        port="5432"
    )
    return connection

# Populate inital db from specs
def create_initial_database(connection):
    cursor = connection.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS students (
        student_id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        enrollment_date DATE
        )
    """)
    
    # Check if any rows exist in the students table
    cursor.execute("SELECT EXISTS (SELECT 1 FROM students)")
    if cursor.fetchone()[0]:
        print("Students Table already exists")
    else:
        # Insert initial data into the students table
        cursor.execute( """ 
            INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
            ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
            ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
            ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')
        """)
    
    connection.commit()
    cursor.close()

# Get all students from the database
def get_all_students(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()
    cursor.close()
    return students

# Add a new student to the database
def add_student(connection, first_name, last_name, email, enrollment_date):
    cursor = connection.cursor()

    insert_query = sql.SQL("""
        INSERT INTO students (first_name, last_name, email, enrollment_date)
        VALUES (%s, %s, %s, %s)
        RETURNING student_id
    """)

    cursor.execute(insert_query, (first_name, last_name, email, enrollment_date))
    connection.commit()
    new_student_id = cursor.fetchone()[0]
    cursor.close()
    return new_student_id

# Update a student's email
def update_student_email(connection, student_id, new_email):
    cursor = connection.cursor()

    update_query = sql.SQL("""
        UPDATE students
        SET email = %s
        WHERE student_id = %s
    """)

    cursor.execute(update_query, (new_email, student_id))
    connection.commit()
    cursor.close()

# Delete a student from the database
def delete_student(connection, student_id):
    cursor = connection.cursor()

    delete_query = sql.SQL("""
        DELETE FROM students WHERE student_id = %s
    """)

    cursor.execute(delete_query, (student_id,))
    connection.commit()
    cursor.close()

def main():
    connection = connect_to_database()
    if connection is None:
        return

    create_initial_database(connection)

    while True:
        choice = int(input("\n1. Get all Students\n2. Add Student\n3. Update Student Email\n4. Delete Student\n5. Quit\n"))
        match choice:
            case 1:
                print("\nQUESTION ONE DEMO -- Get All Students:")
                students = get_all_students(connection)
                print("All Students:")
                for student in students:
                    print(student)
            case 2:
                print("\nQUESTION TWO DEMO -- Add Student:\n")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                email = input("Enter email: ")
                enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")
                new_student_id = add_student(connection, first_name, last_name, email, enrollment_date)
                print("New Student ID:", new_student_id)
            case 3:
                print("\nQUESTION THREE DEMO -- Update Student Email:\n")
                student_id = input("Enter student ID to update: ")
                new_email = input("Enter new email: ")
                update_student_email(connection, student_id, new_email)
            case 4:
                print("\nQUESTION FOUR DEMO -- Delete Student:\n")
                student_id = input("Enter student ID to delete: ")
                print("Deleting student with ID: " + student_id)
                delete_student(connection, student_id)
                students_after_deletion = get_all_students(connection)
                print("Students after deletion:")
                for student in students_after_deletion:
                    print(student)
            case 5: 
                break
    connection.close()

if __name__ == "__main__":
    main()
