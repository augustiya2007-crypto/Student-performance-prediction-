import sqlite3


def create_database():

    conn = sqlite3.connect("student.db")
    cur = conn.cursor()

    # Student Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Prediction Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        study_hours REAL,
        attendance REAL,
        internal_marks REAL,
        assignment REAL,
        prediction TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    conn.commit()
    conn.close()
    

    print("✅ Database Created Successfully")


if __name__ == "__main__":
    create_database()