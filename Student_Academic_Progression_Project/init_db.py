#!/usr/bin/env python3
"""
init_db.py
Automated Relational Database Initializer for Student Academic Progression System.
Reads and applies modular SQL scripts in strict sequence, verifies schema,
and safely populates seed data with full idempotency.
"""

import os
import sys
import re
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Dhiraj@1507")
DB_NAME = os.getenv("DB_NAME", "student_progression")

SQL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql")

SQL_FILES = [
    "01_create_database.sql",
    "02_create_tables.sql",
    "03_constraints_indexes.sql",
    "04_sample_data.sql",
    "05_views.sql",
]

def get_server_connection():
    """Connects to MySQL server without selecting a database."""
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True
    )

def execute_sql_file(cursor, filepath, target_db=None):
    """Executes multi-statement SQL script with proper delimiter and comment handling."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"SQL file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # If target_db specified, override USE statements and database creation names
    if target_db:
        content = re.sub(r"CREATE DATABASE IF NOT EXISTS \w+", f"CREATE DATABASE IF NOT EXISTS {target_db}", content, flags=re.IGNORECASE)
        content = re.sub(r"USE \w+;", f"USE {target_db};", content, flags=re.IGNORECASE)

    # Split statements by semicolon while ignoring comments
    statements = []
    current = []
    in_block_comment = False

    for line in content.splitlines():
        trimmed = line.strip()
        if not trimmed:
            continue
        if trimmed.startswith("/*") and trimmed.endswith("*/"):
            continue
        if trimmed.startswith("/*"):
            in_block_comment = True
            continue
        if in_block_comment:
            if "*/" in trimmed:
                in_block_comment = False
            continue
        if trimmed.startswith("--") or trimmed.startswith("#"):
            continue

        current.append(line)
        if trimmed.endswith(";"):
            statement = "\n".join(current).rstrip(";").strip()
            if statement:
                statements.append(statement)
            current = []

    for stmt in statements:
        try:
            cursor.execute(stmt)
        except Error as err:
            # Ignore duplicate index or duplicate key warnings gracefully
            if err.errno in (1061, 1060, 1022, 1050):  # Duplicate key/column/table
                continue
            # Also ignore constraint already exists errors (errno 1826 or 3822)
            if "Duplicate constraint name" in str(err) or err.errno in (1826, 3822):
                continue
            raise err

def initialize_database(db_name=None, include_sample_data=True):
    """Initializes the database, runs migrations/schemas, and verifies integrity."""
    target_db = db_name or DB_NAME
    print(f"\n=======================================================")
    print(f"🚀 Initializing Database: '{target_db}' on {DB_HOST}:{DB_PORT}")
    print(f"=======================================================")

    conn = get_server_connection()
    try:
        cur = conn.cursor()

        # Step 1: Ensure database exists
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{target_db}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cur.execute(f"USE `{target_db}`;")

        # Step 2: Run SQL scripts
        for fname in SQL_FILES:
            if not include_sample_data and "04_sample_data" in fname:
                print(f"⏩ Skipping {fname} (sample data disabled)")
                continue

            fpath = os.path.join(SQL_DIR, fname)
            print(f"⚡ Applying {fname}...")
            execute_sql_file(cur, fpath, target_db=target_db)

        # Step 3: Verify created tables
        cur.execute("SHOW TABLES;")
        tables = [row[0] for row in cur.fetchall()]
        print(f"\n✅ Created/Verified {len(tables)} tables and views in '{target_db}':")
        for t in sorted(tables):
            cur.execute(f"SELECT COUNT(*) FROM `{t}`;")
            count = cur.fetchone()[0]
            print(f"   • {t:<28} : {count:>5} records")

        required_tables = [
            "students", "school_records", "semesters", "subjects", 
            "semester_subject_marks", "attendance", "academic_gaps", 
            "portfolio_categories", "portfolio_entries"
        ]
        missing = [rt for rt in required_tables if rt not in tables]
        if missing:
            raise RuntimeError(f"Missing required tables after initialization: {missing}")

        print(f"\n🎉 Database '{target_db}' initialized successfully!")
        return True
    finally:
        conn.close()

if __name__ == "__main__":
    test_mode = "--test" in sys.argv
    db_to_use = "student_progression_test" if test_mode else DB_NAME
    initialize_database(db_name=db_to_use, include_sample_data=True)
