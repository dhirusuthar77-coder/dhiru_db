"""
sync_to_web_app.py
Pushes MySQL 8.0 data to Google Sheets Web App with the EXACT 8 tabs:
1. achievement_categories
2. students
3. school_records
4. semesters
5. subjects
6. semester_results
7. drop_years
8. achievements
"""

import os
import json
import decimal
import urllib.request
import sqlite3
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Dhiraj@1507")
DB_NAME = os.getenv("DB_NAME", "student_progression")

SQLITE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "student_progression.db")

WEB_APP_URL = os.getenv(
    "GOOGLE_WEB_APP_URL",
    "https://script.google.com/macros/s/AKfycbzmPSEAhyOnK4wwQfA6nsrMl1aNnZp6JGVurP0oiq2nbXC-8EpxfpZ4_bgpDWEQ5Qw/exec"
)

# Exact queries matching user's requested schema and column order
TABLE_QUERIES = {
    "achievement_categories": "SELECT category_id, category_name, category_group, activity_type FROM achievement_categories ORDER BY category_id",
    "students": "SELECT student_id, roll_number, full_name, email, admission_year, current_status, phone, branch FROM students ORDER BY student_id",
    "school_records": "SELECT school_record_id, student_id, qualification_type, board_name, school_name, passing_year, obtained_marks, maximum_marks, percentage FROM school_records ORDER BY student_id, qualification_type",
    "semesters": "SELECT semester_id, student_id, semester_number, academic_year, sgpa, cgpa, result_status, result_date, gap_note FROM semesters ORDER BY student_id, semester_number",
    "subjects": "SELECT subject_id, subject_code, subject_name, credits, semester_number, subject_type FROM subjects ORDER BY semester_number, subject_code",
    "semester_results": "SELECT mark_id AS result_id, student_id, semester_id, subject_id, internal_marks, external_marks, total_marks, grade, result_status FROM semester_results ORDER BY student_id, semester_id, subject_id",
    "drop_years": "SELECT gap_id, student_id, start_year, end_year, reason, description FROM drop_years ORDER BY student_id",
    "achievements": "SELECT entry_id AS achievement_id, student_id, category_id, title, organization, entry_date, description, certificate_url FROM achievements ORDER BY student_id, entry_date DESC"
}

def format_cell(v):
    if v is None:
        return ""
    if isinstance(v, decimal.Decimal):
        return float(v)
    if hasattr(v, "strftime"):
        return v.strftime("%Y-%m-%d %H:%M:%S") if hasattr(v, "hour") else v.strftime("%Y-%m-%d")
    return str(v)

def fetch_payload():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            connection_timeout=1
        )
    except Exception:
        conn = sqlite3.connect(SQLITE_PATH)
    cur = conn.cursor()

    payload_tables = {}
    for tbl, query in TABLE_QUERIES.items():
        cur.execute(query)
        headers = [desc[0] for desc in cur.description]
        raw_rows = cur.fetchall()
        rows = [[format_cell(cell) for cell in row] for row in raw_rows]
        payload_tables[tbl] = {
            "headers": headers,
            "rows": rows
        }

    cur.close()
    conn.close()
    return {"action": "sync_all", "tables": payload_tables}

def sync_mysql_to_web_app(web_app_url=None):
    url = web_app_url or WEB_APP_URL
    print(f"Connecting to MySQL ({DB_NAME}) and extracting exact 8 tables...")
    payload = fetch_payload()

    print(f"Pushing to Google Apps Script Web App:")
    print(f"URL: {url}")
    
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            response_text = res.read().decode("utf-8")
            print("Response Status:", res.status)
            try:
                parsed = json.loads(response_text)
                print("Result:", json.dumps(parsed, indent=2))
                return True, parsed
            except Exception:
                print("Response Body:", response_text[:500])
                return True, response_text
    except Exception as err:
        print(f"Error during synchronization: {err}")
        return False, str(err)

if __name__ == "__main__":
    sync_mysql_to_web_app()
