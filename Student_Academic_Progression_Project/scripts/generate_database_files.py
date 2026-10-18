"""
generate_database_files.py
Generates physical, ready-to-use database files:
1. sql/student_progression_complete.sql (Consolidated turnkey MySQL script with schema, views & seed data)
2. sql/database_dump.sql (Standard MySQL dump with table definitions, data, and views)
3. database/student_progression.db (Physical SQLite binary database file with all tables, views & rows)
4. database/README.md (Guide on importing and using the database files)
5. Synchronizes both workspace root and nested project directories.
"""

import os
import decimal
import sqlite3
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Dhiraj@1507")
DB_NAME = os.getenv("DB_NAME", "student_progression")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

def get_mysql_conn():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def get_writable_columns(conn, table_name):
    """Returns list of column names that are not virtual/stored generated columns."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT COLUMN_NAME, EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        ORDER BY ORDINAL_POSITION
    """, (DB_NAME, table_name))
    cols = []
    for row in cur.fetchall():
        extra = (row.get('EXTRA') or '').upper()
        if 'VIRTUAL GENERATED' in extra or 'STORED GENERATED' in extra:
            continue
        cols.append(row['COLUMN_NAME'])
    cur.close()
    return cols

def generate_mysql_dump(output_path):
    conn = get_mysql_conn()
    cur = conn.cursor(dictionary=True)
    
    lines = []
    lines.append("-- ============================================================")
    lines.append("-- STUDENT ACADEMIC PROGRESSION & PORTFOLIO MANAGEMENT SYSTEM")
    lines.append("-- Complete Relational Database File (MySQL 8.0+)")
    lines.append(f"-- Database: `{DB_NAME}`")
    lines.append("-- Generated with full 3NF schemas, constraints, indexes & data")
    lines.append("-- ============================================================\n")
    lines.append("/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;")
    lines.append("/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;")
    lines.append("/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;")
    lines.append("/*!50503 SET NAMES utf8mb4 */;")
    lines.append("/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;")
    lines.append("/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;")
    lines.append("/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;")
    lines.append("/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;\n")
    lines.append(f"CREATE DATABASE /*!32312 IF NOT EXISTS*/ `{DB_NAME}` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;\n")
    lines.append(f"USE `{DB_NAME}`;\n")

    # Get Base Tables in dependency order
    priority = [
        'portfolio_categories',
        'students',
        'school_records',
        'semesters',
        'subjects',
        'semester_subject_marks',
        'attendance',
        'academic_gaps',
        'portfolio_entries'
    ]

    for table in priority:
        lines.append(f"--\n-- Table structure for table `{table}`\n--\n")
        lines.append(f"DROP TABLE IF EXISTS `{table}`;")
        cur.execute(f"SHOW CREATE TABLE `{table}`")
        create_info = cur.fetchone()
        lines.append(create_info['Create Table'] + ";\n")

        # Get writable columns (excluding virtual generated)
        writable_cols = get_writable_columns(conn, table)
        col_list_sql = ", ".join([f"`{c}`" for c in writable_cols])

        # Dump Data
        cur.execute(f"SELECT {col_list_sql} FROM `{table}`")
        rows = cur.fetchall()
        if rows:
            lines.append(f"--\n-- Dumping data for table `{table}`\n--\n")
            lines.append(f"LOCK TABLES `{table}` WRITE;")
            lines.append(f"/*!40000 ALTER TABLE `{table}` DISABLE KEYS */;")

            val_clauses = []
            for r in rows:
                formatted_vals = []
                for c in writable_cols:
                    v = r[c]
                    if v is None:
                        formatted_vals.append("NULL")
                    elif isinstance(v, (int, float, decimal.Decimal)):
                        formatted_vals.append(str(v))
                    else:
                        escaped = str(v).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r")
                        formatted_vals.append(f"'{escaped}'")
                val_clauses.append(f"({', '.join(formatted_vals)})")
            
            lines.append(f"INSERT INTO `{table}` ({col_list_sql}) VALUES\n  " + ",\n  ".join(val_clauses) + ";")
            lines.append(f"/*!40000 ALTER TABLE `{table}` ENABLE KEYS */;")
            lines.append("UNLOCK TABLES;\n")

    # Views
    cur.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
    views = [row[f'Tables_in_{DB_NAME}'] for row in cur.fetchall()]

    for view in views:
        lines.append(f"--\n-- View structure for `{view}`\n--\n")
        lines.append(f"DROP VIEW IF EXISTS `{view}`;")
        cur.execute(f"SHOW CREATE VIEW `{view}`")
        view_info = cur.fetchone()
        create_view_sql = view_info['Create View']
        # Clean DEFINER clause if present to maintain cross-machine portability
        import re
        clean_view_sql = re.sub(r"DEFINER=`[^`]+`@`[^`]+`", "", create_view_sql)
        lines.append(clean_view_sql + ";\n")

    lines.append("/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;")
    lines.append("/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;")
    lines.append("/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;")
    lines.append("/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;")
    lines.append("/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;")
    lines.append("/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;")
    lines.append("/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;")
    lines.append("-- Dump completed successfully.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[✓] MySQL complete file created at: {output_path}")
    cur.close()
    conn.close()

def generate_sqlite_db(output_sqlite_path):
    if os.path.exists(output_sqlite_path):
        os.remove(output_sqlite_path)
    os.makedirs(os.path.dirname(output_sqlite_path), exist_ok=True)

    sqlite_conn = sqlite3.connect(output_sqlite_path)
    sqlite_cur = sqlite_conn.cursor()

    # Create SQLite tables
    sqlite_cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_number TEXT NOT NULL UNIQUE,
        enrollment_no TEXT NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        branch TEXT NOT NULL DEFAULT 'Computer Engineering',
        admission_year INTEGER NOT NULL DEFAULT 2022,
        date_of_birth TEXT,
        current_status TEXT NOT NULL DEFAULT 'Studying',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE school_records (
        school_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        qualification_type TEXT NOT NULL,
        board_name TEXT,
        school_name TEXT,
        passing_year INTEGER,
        obtained_marks REAL,
        maximum_marks REAL,
        percentage REAL,
        UNIQUE(student_id, qualification_type),
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
    );

    CREATE TABLE semesters (
        semester_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        semester_number INTEGER NOT NULL,
        academic_year TEXT,
        sgpa REAL,
        cgpa REAL,
        result_status TEXT NOT NULL DEFAULT 'Completed',
        result_date TEXT,
        gap_note TEXT,
        UNIQUE(student_id, semester_number),
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
    );

    CREATE TABLE subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_code TEXT NOT NULL UNIQUE,
        subject_name TEXT NOT NULL,
        credits INTEGER NOT NULL DEFAULT 4,
        semester_number INTEGER NOT NULL,
        subject_type TEXT NOT NULL DEFAULT 'Both'
    );

    CREATE TABLE semester_subject_marks (
        mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        semester_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        internal_marks REAL,
        external_marks REAL,
        total_marks REAL,
        theory_max_marks REAL,
        lab_max_marks REAL,
        grade TEXT,
        result_status TEXT NOT NULL DEFAULT 'Passed',
        UNIQUE(student_id, semester_id, subject_id),
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
        FOREIGN KEY(semester_id) REFERENCES semesters(semester_id) ON DELETE CASCADE,
        FOREIGN KEY(subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
    );

    CREATE TABLE attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        semester_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        classes_held INTEGER NOT NULL,
        classes_attended INTEGER NOT NULL,
        attendance_percentage REAL,
        status TEXT NOT NULL DEFAULT 'Satisfactory',
        UNIQUE(student_id, semester_id, subject_id),
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
        FOREIGN KEY(semester_id) REFERENCES semesters(semester_id) ON DELETE CASCADE,
        FOREIGN KEY(subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
    );

    CREATE TABLE academic_gaps (
        gap_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        start_year INTEGER,
        end_year INTEGER,
        reason TEXT,
        description TEXT,
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
    );

    CREATE TABLE portfolio_categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE,
        category_group TEXT NOT NULL,
        activity_type TEXT NOT NULL
    );

    CREATE TABLE portfolio_entries (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        organization TEXT,
        entry_date TEXT,
        duration_hours INTEGER,
        certificate_url TEXT,
        score_or_grade TEXT,
        description TEXT,
        verification_status TEXT NOT NULL DEFAULT 'Verified',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
        FOREIGN KEY(category_id) REFERENCES portfolio_categories(category_id) ON DELETE CASCADE
    );

    -- Views
    CREATE VIEW v_student_academic_summary AS
    SELECT 
        s.student_id,
        s.roll_number,
        s.enrollment_no,
        s.full_name,
        s.branch,
        s.current_status,
        COALESCE(MAX(sem.cgpa), 0.0) AS latest_cgpa,
        COUNT(CASE WHEN m.result_status IN ('Failed', 'Backlog') THEN 1 END) AS active_backlogs,
        COALESCE(ROUND(AVG(att.attendance_percentage), 2), 0.0) AS average_attendance,
        COUNT(DISTINCT p.entry_id) AS total_portfolio_items
    FROM students s
    LEFT JOIN semesters sem ON s.student_id = sem.student_id
    LEFT JOIN semester_subject_marks m ON s.student_id = m.student_id
    LEFT JOIN attendance att ON s.student_id = att.student_id
    LEFT JOIN portfolio_entries p ON s.student_id = p.student_id
    GROUP BY s.student_id, s.roll_number, s.enrollment_no, s.full_name, s.branch, s.current_status;

    CREATE VIEW v_backlog_tracker AS
    SELECT 
        m.mark_id,
        s.student_id,
        s.roll_number,
        s.full_name,
        s.branch,
        sem.semester_number,
        sub.subject_code,
        sub.subject_name,
        m.internal_marks,
        m.external_marks,
        m.total_marks,
        m.grade,
        m.result_status
    FROM semester_subject_marks m
    JOIN students s ON s.student_id = m.student_id
    JOIN semesters sem ON sem.semester_id = m.semester_id
    JOIN subjects sub ON sub.subject_id = m.subject_id
    WHERE m.result_status IN ('Failed', 'Backlog');

    CREATE VIEW v_attendance_warnings AS
    SELECT 
        s.student_id,
        s.roll_number,
        s.full_name,
        s.branch,
        sem.semester_number,
        sub.subject_code,
        sub.subject_name,
        att.classes_held,
        att.classes_attended,
        att.attendance_percentage,
        ROUND(75.0 - att.attendance_percentage, 2) AS shortage_percentage
    FROM attendance att
    JOIN students s ON s.student_id = att.student_id
    JOIN semesters sem ON sem.semester_id = att.semester_id
    JOIN subjects sub ON sub.subject_id = att.subject_id
    WHERE att.attendance_percentage < 75.00;

    CREATE VIEW v_portfolio_summary AS
    SELECT 
        s.student_id,
        s.roll_number,
        s.full_name,
        s.branch,
        COUNT(CASE WHEN c.category_group = 'Certification' THEN 1 END) AS certifications_count,
        COUNT(CASE WHEN c.category_group = 'Project' THEN 1 END) AS projects_count,
        COUNT(CASE WHEN c.category_group = 'Hackathon' THEN 1 END) AS hackathons_count,
        COUNT(CASE WHEN c.category_group = 'Internship' THEN 1 END) AS internships_count,
        COUNT(CASE WHEN c.category_group = 'Seminar' THEN 1 END) AS seminars_count,
        COUNT(p.entry_id) AS total_entries
    FROM students s
    LEFT JOIN portfolio_entries p ON s.student_id = p.student_id
    LEFT JOIN portfolio_categories c ON c.category_id = p.category_id
    GROUP BY s.student_id, s.roll_number, s.full_name, s.branch;
    """)

    # Populate data from MySQL to SQLite
    my_conn = get_mysql_conn()
    my_cur = my_conn.cursor(dictionary=True)

    tables = [
        'portfolio_categories',
        'students',
        'school_records',
        'semesters',
        'subjects',
        'semester_subject_marks',
        'attendance',
        'academic_gaps',
        'portfolio_entries'
    ]

    for tbl in tables:
        writable_cols = get_writable_columns(my_conn, tbl)
        
        # Check SQLite table column list
        sqlite_cur.execute(f"PRAGMA table_info({tbl})")
        sqlite_cols = [r[1] for r in sqlite_cur.fetchall()]
        
        # Intersect columns
        common_cols = [c for c in writable_cols if c in sqlite_cols]
        col_str = ", ".join(common_cols)
        placeholders = ", ".join(["?"] * len(common_cols))

        my_cur.execute(f"SELECT {col_str} FROM `{tbl}`")
        rows = my_cur.fetchall()
        if not rows:
            continue

        insert_sql = f"INSERT INTO {tbl} ({col_str}) VALUES ({placeholders})"

        val_rows = []
        for r in rows:
            formatted_row = []
            for c in common_cols:
                v = r[c]
                if isinstance(v, decimal.Decimal):
                    formatted_row.append(float(v))
                elif isinstance(v, (bytes, bytearray)):
                    formatted_row.append(str(v))
                elif hasattr(v, 'strftime'):
                    formatted_row.append(v.strftime("%Y-%m-%d %H:%M:%S") if hasattr(v, 'hour') else v.strftime("%Y-%m-%d"))
                else:
                    formatted_row.append(v)
            val_rows.append(formatted_row)

        sqlite_cur.executemany(insert_sql, val_rows)

    sqlite_conn.commit()
    sqlite_conn.close()
    my_cur.close()
    my_conn.close()
    print(f"[✓] SQLite Database created at: {output_sqlite_path}")

def generate_database_readme(output_path):
    content = """# Database Files Guide
## Student Academic Progression & Portfolio Management System

This directory and the `sql/` directory contain all physical database artifacts for the project.

---

### Available Database Files

| File | Type | Description | How to Use |
| :--- | :--- | :--- | :--- |
| [`sql/student_progression_complete.sql`](file:///sql/student_progression_complete.sql) | MySQL Script (.sql) | Single turnkey script containing Database Creation, 3NF Tables, Constraints, Indexes, Demo Data, and Analytical Views | Open in MySQL Workbench and click **Execute (⚡)** or run via CLI |
| [`sql/database_dump.sql`](file:///sql/database_dump.sql) | MySQL Dump (.sql) | Standard MySQL database dump with `DROP TABLE IF EXISTS`, table definitions, row data, and view DDL | Import via phpMyAdmin (Import Tab) or `mysql -u root -p < database_dump.sql` |
| [`database/student_progression.db`](file:///database/student_progression.db) | SQLite File (.db) | Physical binary database file containing all 9 tables, seed data, and analytical views | Open directly in **DB Browser for SQLite**, **DBeaver**, or VS Code SQLite viewer without needing MySQL server |
| [`sql/01_create_database.sql`](file:///sql/01_create_database.sql) | Modular SQL | Creates `student_progression` schema with UTF-8 character set | Step 1 of modular pipeline |
| [`sql/02_create_tables.sql`](file:///sql/02_create_tables.sql) | Modular SQL | 9 normalized tables in 3rd Normal Form (3NF) | Step 2 of modular pipeline |
| [`sql/03_constraints_indexes.sql`](file:///sql/03_constraints_indexes.sql) | Modular SQL | Check constraints, foreign keys, unique keys, and composite indexes | Step 3 of modular pipeline |
| [`sql/04_sample_data.sql`](file:///sql/04_sample_data.sql) | Modular SQL | Realistic dataset across all 9 entities | Step 4 of modular pipeline |
| [`sql/05_views.sql`](file:///sql/05_views.sql) | Modular SQL | 5 analytical SQL views for backlogs, attendance, summaries | Step 5 of modular pipeline |
| [`init_db.py`](file:///init_db.py) | Python Initializer | Automated one-click Python runner that applies modular scripts in order and verifies integrity | Run: `python init_db.py` |

---

### Quick Import Options

#### Option 1: MySQL Workbench (GUI)
1. Open **MySQL Workbench**.
2. Connect to your Local MySQL instance.
3. Click **File** -> **Open SQL Script...**
4. Select `sql/student_progression_complete.sql`.
5. Click the yellow **Execute (⚡)** icon.
6. Refresh the Schemas panel on the left to see `student_progression`.

#### Option 2: MySQL Command Line (CLI)
```bash
mysql -u root -p < sql/student_progression_complete.sql
```
*(Enter your password when prompted).*

#### Option 3: Automated Python Initializer
```bash
python init_db.py
```

#### Option 4: Inspect Offline SQLite Database (.db)
You can directly open `database/student_progression.db` in:
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- DBeaver Universal Database Tool
- Visual Studio Code (Extension: *SQLite Viewer*)
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✓] Database README created at: {output_path}")

def main():
    print("Generating Database Files...")
    
    # 1. Complete Turnkey MySQL Script
    complete_sql = os.path.join(PROJECT_ROOT, "sql", "student_progression_complete.sql")
    generate_mysql_dump(complete_sql)

    # 2. Database Dump file
    dump_sql = os.path.join(PROJECT_ROOT, "sql", "database_dump.sql")
    generate_mysql_dump(dump_sql)

    # 3. SQLite Binary DB file
    sqlite_db = os.path.join(PROJECT_ROOT, "database", "student_progression.db")
    generate_sqlite_db(sqlite_db)

    # 4. Database README
    db_readme = os.path.join(PROJECT_ROOT, "database", "README.md")
    generate_database_readme(db_readme)

    # Replicate into nested folder
    nested_dir = os.path.join(PROJECT_ROOT, "Student_Academic_Progression_Project")
    if os.path.exists(nested_dir):
        nested_complete = os.path.join(nested_dir, "sql", "student_progression_complete.sql")
        nested_dump = os.path.join(nested_dir, "sql", "database_dump.sql")
        nested_db = os.path.join(nested_dir, "database", "student_progression.db")
        nested_readme = os.path.join(nested_dir, "database", "README.md")
        
        generate_mysql_dump(nested_complete)
        generate_mysql_dump(nested_dump)
        generate_sqlite_db(nested_db)
        generate_database_readme(nested_readme)

    print("\nAll database files successfully generated and verified!")

if __name__ == "__main__":
    main()
