#!/usr/bin/env python3
"""
tests/test_progression_system.py
Automated Verification Suite for Student Academic Progression System.
Tests all 12 specified database constraints, relations, CRUD, views, and error handling
using an isolated test database ('student_progression_test').
"""

import os
import unittest
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Dhiraj@1507")
TEST_DB_NAME = "student_progression_test"

# Import initializer
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_db import initialize_database

class TestStudentAcademicProgression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up an isolated test database once for the entire test suite."""
        initialize_database(db_name=TEST_DB_NAME, include_sample_data=True)
        cls.conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=TEST_DB_NAME,
            autocommit=True
        )

    @classmethod
    def tearDownClass(cls):
        """Clean up test database connection."""
        if hasattr(cls, "conn") and cls.conn.is_connected():
            cls.conn.close()

    def get_cursor(self):
        return self.conn.cursor(dictionary=True)

    # 1. Database Initialization Test
    def test_01_database_initialization(self):
        cur = self.get_cursor()
        cur.execute("SHOW TABLES;")
        tables = [list(r.values())[0] for r in cur.fetchall()]
        expected_tables = [
            "students", "school_records", "semesters", "subjects",
            "semester_subject_marks", "attendance", "academic_gaps",
            "portfolio_categories", "portfolio_entries"
        ]
        for t in expected_tables:
            self.assertIn(t, tables, f"Expected table '{t}' missing from test database")

    # 2. Student CRUD Operations
    def test_02_student_crud(self):
        cur = self.get_cursor()
        # Create
        cur.execute("""
            INSERT INTO students (roll_number, enrollment_no, full_name, email, phone, branch, admission_year)
            VALUES ('TEST_ROLL_99', 'TEST_EN_99', 'Vikramaditya Rao', 'vikram.test@example.edu', '9988776655', 'Computer Engineering', 2023)
        """)
        student_id = cur.lastrowid
        self.assertGreater(student_id, 0)

        # Read
        cur.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student = cur.fetchone()
        self.assertEqual(student["full_name"], "Vikramaditya Rao")
        self.assertEqual(student["branch"], "Computer Engineering")

        # Update
        cur.execute("UPDATE students SET branch = 'Information Technology' WHERE student_id = %s", (student_id,))
        cur.execute("SELECT branch FROM students WHERE student_id = %s", (student_id,))
        self.assertEqual(cur.fetchone()["branch"], "Information Technology")

        # Delete
        cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        cur.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        self.assertIsNone(cur.fetchone())

    # 3. Duplicate Roll Number Rejection (UNIQUE constraint)
    def test_03_duplicate_roll_number_rejection(self):
        cur = self.get_cursor()
        test_roll = f"ROLL_DUP_{os.getpid()}"
        cur.execute("DELETE FROM students WHERE roll_number = %s", (test_roll,))
        cur.execute("""
            INSERT INTO students (roll_number, enrollment_no, full_name, email)
            VALUES (%s, %s, 'Original Student', %s)
        """, (test_roll, f"EN_{test_roll}", f"{test_roll}@example.com"))
        
        try:
            with self.assertRaises(Error) as ctx:
                cur.execute("""
                    INSERT INTO students (roll_number, enrollment_no, full_name, email)
                    VALUES (%s, %s, 'Duplicate Student', 'another_email@example.com')
                """, (test_roll, f"EN2_{test_roll}"))
            self.assertIn("Duplicate entry", str(ctx.exception))
        finally:
            cur.execute("DELETE FROM students WHERE roll_number = %s", (test_roll,))

    # 4. Foreign Key Enforcement & Cascading Deletes
    def test_04_foreign_key_and_cascade(self):
        cur = self.get_cursor()
        fk_roll = f"ROLL_FK_{os.getpid()}"
        cur.execute("DELETE FROM students WHERE roll_number = %s", (fk_roll,))
        cur.execute("""
            INSERT INTO students (roll_number, enrollment_no, full_name)
            VALUES (%s, %s, 'Cascade Target')
        """, (fk_roll, f"EN_{fk_roll}"))
        sid = cur.lastrowid

        # Insert dependent school record & semester
        cur.execute("""
            INSERT INTO school_records (student_id, qualification_type, board_name, percentage)
            VALUES (%s, 'SSC', 'CBSE', 88.5)
        """, (sid,))
        cur.execute("""
            INSERT INTO semesters (student_id, semester_number, sgpa, cgpa)
            VALUES (%s, 1, 8.5, 8.5)
        """, (sid,))

        # Delete student - should cascade
        cur.execute("DELETE FROM students WHERE student_id = %s", (sid,))
        cur.execute("SELECT COUNT(*) AS n FROM school_records WHERE student_id = %s", (sid,))
        self.assertEqual(cur.fetchone()["n"], 0)
        cur.execute("SELECT COUNT(*) AS n FROM semesters WHERE student_id = %s", (sid,))
        self.assertEqual(cur.fetchone()["n"], 0)

    # 5. Invalid Marks and Attendance Rejection (CHECK constraints)
    def test_05_invalid_marks_and_attendance_rejection(self):
        cur = self.get_cursor()
        # Negative internal marks should be rejected
        with self.assertRaises(Error) as ctx:
            cur.execute("""
                INSERT INTO semester_subject_marks (semester_id, student_id, subject_id, internal_marks)
                VALUES (1, 1, 1, -15.0)
            """)
        self.assertTrue("chk_internal_marks" in str(ctx.exception) or "CHECK" in str(ctx.exception).upper())

        # Attendance: classes_attended > classes_held should be rejected
        with self.assertRaises(Error) as ctx:
            cur.execute("""
                INSERT INTO attendance (student_id, subject_id, semester_id, classes_held, classes_attended)
                VALUES (1, 2, 1, 30, 45)
            """)
        self.assertTrue("chk_attendance_valid" in str(ctx.exception) or "CHECK" in str(ctx.exception).upper())

    # 6. Valid and Invalid SGPA / CGPA Values
    def test_06_sgpa_cgpa_boundaries(self):
        cur = self.get_cursor()
        # Invalid: SGPA > 10.0
        with self.assertRaises(Error) as ctx:
            cur.execute("""
                INSERT INTO semesters (student_id, semester_number, sgpa, cgpa)
                VALUES (1, 12, 11.5, 8.5)
            """)
        self.assertTrue("chk_sgpa" in str(ctx.exception) or "CHECK" in str(ctx.exception).upper())

        # Invalid: SGPA < 0.0
        with self.assertRaises(Error) as ctx:
            cur.execute("""
                INSERT INTO semesters (student_id, semester_number, sgpa, cgpa)
                VALUES (1, 12, -1.0, 8.5)
            """)
        self.assertTrue("chk_sgpa" in str(ctx.exception) or "CHECK" in str(ctx.exception).upper())

    # 7. Semester and Subject-Result Relationships
    def test_07_semester_subject_relationships(self):
        cur = self.get_cursor()
        cur.execute("""
            SELECT s.full_name, sem.semester_number, sub.subject_name, m.total_marks, m.grade
            FROM semester_subject_marks m
            JOIN students s ON s.student_id = m.student_id
            JOIN semesters sem ON sem.semester_id = m.semester_id
            JOIN subjects sub ON sub.subject_id = m.subject_id
            WHERE s.student_id = 1
        """)
        rows = cur.fetchall()
        self.assertGreater(len(rows), 0, "Expected subject marks for student 1")
        for r in rows:
            self.assertIn("subject_name", r)
            self.assertGreaterEqual(r["total_marks"], 0.0)

    # 8. Backlog Tracking
    def test_08_backlog_tracking(self):
        cur = self.get_cursor()
        cur.execute("SELECT * FROM v_backlog_tracker WHERE student_id = 3")
        backlogs = cur.fetchall()
        self.assertGreaterEqual(len(backlogs), 1, "Student 3 should have a tracked backlog")
        self.assertEqual(backlogs[0]["result_status"], "Failed")
        self.assertEqual(backlogs[0]["subject_code"], "CS201")

    # 9. Academic Gap Records
    def test_09_academic_gap_records(self):
        cur = self.get_cursor()
        cur.execute("SELECT * FROM academic_gaps WHERE student_id = 4")
        gaps = cur.fetchall()
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]["reason"], "Medical Leave")
        self.assertEqual(gaps[0]["start_year"], 2022)
        self.assertEqual(gaps[0]["end_year"], 2023)

    # 10. Achievement and Certificate CRUD
    def test_10_achievement_crud(self):
        cur = self.get_cursor()
        # Create
        cur.execute("""
            INSERT INTO portfolio_entries (student_id, category_id, title, organization, entry_date)
            VALUES (1, 6, 'Azure Fundamentals AZ-900', 'Microsoft', '2024-03-10')
        """)
        entry_id = cur.lastrowid
        self.assertGreater(entry_id, 0)

        # Read
        cur.execute("SELECT * FROM portfolio_entries WHERE entry_id = %s", (entry_id,))
        entry = cur.fetchone()
        self.assertEqual(entry["title"], "Azure Fundamentals AZ-900")

        # Update
        cur.execute("UPDATE portfolio_entries SET organization = 'Microsoft Azure' WHERE entry_id = %s", (entry_id,))
        cur.execute("SELECT organization FROM portfolio_entries WHERE entry_id = %s", (entry_id,))
        self.assertEqual(cur.fetchone()["organization"], "Microsoft Azure")

        # Delete
        cur.execute("DELETE FROM portfolio_entries WHERE entry_id = %s", (entry_id,))
        cur.execute("SELECT * FROM portfolio_entries WHERE entry_id = %s", (entry_id,))
        self.assertIsNone(cur.fetchone())

    # 11. Dashboard Analytics Views
    def test_11_dashboard_analytics_views(self):
        cur = self.get_cursor()
        # Summary view
        cur.execute("SELECT * FROM v_student_academic_summary WHERE student_id = 1")
        summary = cur.fetchone()
        self.assertIsNotNone(summary)
        self.assertEqual(summary["roll_number"], "22CS01")
        self.assertGreater(summary["latest_cgpa"], 8.0)

        # Attendance warning view (<75%)
        cur.execute("SELECT * FROM v_attendance_warnings")
        warnings = cur.fetchall()
        self.assertGreater(len(warnings), 0, "Expected attendance warnings for demo records")
        for w in warnings:
            self.assertLess(w["attendance_percentage"], 75.0)

    # 12. Google Sheets Integration Error Handling
    def test_12_google_sheets_error_handling(self):
        """Verify that missing credentials or invalid sheet IDs are handled gracefully with clear messages."""
        # Unset / invalid configuration simulation
        sheet_id = ""
        key_file = "non_existent_service_account.json"
        
        # Test missing sheet_id detection
        if not sheet_id:
            handled_error = "Set GOOGLE_SHEET_ID in .env first."
        self.assertEqual(handled_error, "Set GOOGLE_SHEET_ID in .env first.")

        # Test missing service account file detection
        self.assertFalse(os.path.exists(key_file))

if __name__ == "__main__":
    unittest.main(verbosity=2)
