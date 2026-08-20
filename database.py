import sqlite3

DB_NAME = "students.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            python_marks INTEGER,
            sql_marks INTEGER,
            aptitude_marks INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            marks INTEGER NOT NULL CHECK(marks >= 0 AND marks <= 100),
            UNIQUE(student_id, subject_id),
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE
        )
    """)

    # Preserve the original three subjects/data when upgrading an existing database.
    cursor.execute("SELECT COUNT(*) FROM subjects")
    subject_count = cursor.fetchone()[0]

    if subject_count == 0:
        cursor.executemany(
            "INSERT OR IGNORE INTO subjects (name) VALUES (?)",
            [("Python",), ("SQL",), ("Aptitude",)]
        )

    connection.commit()

    # Migrate existing Python/SQL/Aptitude marks into the new dynamic tables.
    cursor.execute("""
        SELECT id, python_marks, sql_marks, aptitude_marks
        FROM students
    """)
    old_students = cursor.fetchall()

    subject_ids = {}
    for subject_name in ("Python", "SQL", "Aptitude"):
        cursor.execute(
            "SELECT id FROM subjects WHERE name = ?",
            (subject_name,)
        )
        row = cursor.fetchone()
        if row:
            subject_ids[subject_name] = row[0]

    for student_id, python, sql, aptitude in old_students:
        values = {
            "Python": python,
            "SQL": sql,
            "Aptitude": aptitude,
        }

        for subject_name, marks in values.items():
            if marks is None or subject_name not in subject_ids:
                continue

            cursor.execute("""
                INSERT OR IGNORE INTO student_marks
                (student_id, subject_id, marks)
                VALUES (?, ?, ?)
            """, (student_id, subject_ids[subject_name], int(marks)))

    connection.commit()
    connection.close()


def get_subjects():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name FROM subjects ORDER BY name")
    subjects = cursor.fetchall()

    connection.close()
    return subjects


def add_subject(name):
    name = name.strip()
    if not name:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO subjects (name) VALUES (?)",
            (name,)
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def delete_subject(subject_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM student_marks WHERE subject_id = ?",
        (subject_id,)
    )
    cursor.execute(
        "DELETE FROM subjects WHERE id = ?",
        (subject_id,)
    )

    connection.commit()
    connection.close()


def add_student(name, marks):
    connection = get_connection()
    cursor = connection.cursor()

    # The original database schema contains legacy NOT NULL columns
    # for Python, SQL, and Aptitude. Keep them at 0 for compatibility;
    # actual marks are stored dynamically in student_marks.
    cursor.execute("""
        INSERT INTO students
        (name, python_marks, sql_marks, aptitude_marks)
        VALUES (?, 0, 0, 0)
    """, (name,))
    student_id = cursor.lastrowid

    for subject_id, score in marks.items():
        cursor.execute("""
            INSERT INTO student_marks
            (student_id, subject_id, marks)
            VALUES (?, ?, ?)
        """, (int(student_id), int(subject_id), int(score)))

    connection.commit()
    connection.close()


def get_students():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.id,
            s.name,
            sub.id,
            sub.name,
            sm.marks
        FROM students s
        LEFT JOIN student_marks sm
            ON s.id = sm.student_id
        LEFT JOIN subjects sub
            ON sub.id = sm.subject_id
        ORDER BY s.id, sub.name
    """)

    rows = cursor.fetchall()
    connection.close()

    students = {}

    for student_id, name, subject_id, subject_name, marks in rows:
        if student_id not in students:
            students[student_id] = {
                "id": student_id,
                "name": name,
                "marks": {}
            }

        if subject_id is not None and subject_name is not None and marks is not None:
            students[student_id]["marks"][subject_name] = marks

    return list(students.values())


def update_student(student_id, name, marks):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE students SET name = ? WHERE id = ?",
        (name, student_id)
    )

    cursor.execute(
        "DELETE FROM student_marks WHERE student_id = ?",
        (student_id,)
    )

    for subject_id, score in marks.items():
        cursor.execute("""
            INSERT INTO student_marks
            (student_id, subject_id, marks)
            VALUES (?, ?, ?)
        """, (int(student_id), int(subject_id), int(score)))

    connection.commit()
    connection.close()


def delete_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM student_marks WHERE student_id = ?",
        (student_id,)
    )
    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()