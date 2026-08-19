import sqlite3

DB_NAME = "students.db"


def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            python_marks INTEGER NOT NULL,
            sql_marks INTEGER NOT NULL,
            aptitude_marks INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_student(name, python_marks, sql_marks, aptitude_marks):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, python_marks, sql_marks, aptitude_marks)
        VALUES (?, ?, ?, ?)
    """, (name, python_marks, sql_marks, aptitude_marks))

    connection.commit()
    connection.close()


def get_students():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    connection.close()

    return students


def update_student(
    student_id,
    name,
    python_marks,
    sql_marks,
    aptitude_marks
):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?,
            python_marks = ?,
            sql_marks = ?,
            aptitude_marks = ?
        WHERE id = ?
    """, (
        name,
        python_marks,
        sql_marks,
        aptitude_marks,
        student_id
    ))

    connection.commit()
    connection.close()


def delete_student(student_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()