import sqlite3

DB_NAME = "database/studentos.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            deadline TEXT,
            category TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            exam_date TEXT,
            study_hours INTEGER,
            difficulty TEXT,
            plan TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT,
            subject TEXT NOT NULL,
            topics TEXT,
            confidence INTEGER,
            revision_suggestion TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_gaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_role TEXT NOT NULL,
            current_skills TEXT,
            missing_skills TEXT,
            strong_skills TEXT,
            suggestions TEXT
        )
    """)

    conn.commit()
    conn.close()