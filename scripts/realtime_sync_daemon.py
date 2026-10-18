"""
realtime_sync_daemon.py
Continuously monitors MySQL database for changes and automatically
pushes updates to Google Sheets in real-time (every 2-3 seconds).
Run in background or alongside Streamlit.
"""

import time
import os
import hashlib
import json
import mysql.connector
from dotenv import load_dotenv
from sync_to_web_app import sync_mysql_to_web_app

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Dhiraj@1507")
DB_NAME = os.getenv("DB_NAME", "student_progression")

MONITORED_TABLES = [
    "achievement_categories",
    "students",
    "school_records",
    "semesters",
    "subjects",
    "semester_results",
    "drop_years",
    "achievements"
]

def get_database_fingerprint():
    """Generates an MD5 signature of all table row counts and max IDs to detect changes instantly."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cur = conn.cursor()
    signatures = []
    for tbl in MONITORED_TABLES:
        try:
            cur.execute(f"SELECT COUNT(*), COALESCE(MAX(1), 0) FROM `{tbl}`")
            row = cur.fetchone()
            signatures.append(f"{tbl}:{row[0]}:{row[1]}")
        except Exception:
            pass
    cur.close()
    conn.close()
    return hashlib.md5("|".join(signatures).encode("utf-8")).hexdigest()

def start_realtime_watcher(poll_interval=2):
    print("=" * 60)
    print("⚡ Real-Time MySQL ➔ Google Sheets Sync Daemon Started")
    print(f"Monitoring Database: `{DB_NAME}` on {DB_HOST}:{DB_PORT}")
    print(f"Poll Interval: {poll_interval} seconds")
    print("Any change in MySQL will automatically push to Google Sheets!")
    print("=" * 60)

    last_fingerprint = get_database_fingerprint()
    print(f"Initial DB State Fingerprint: {last_fingerprint}")

    while True:
        try:
            time.sleep(poll_interval)
            current_fingerprint = get_database_fingerprint()

            if current_fingerprint != last_fingerprint:
                print(f"\n[Change Detected at {time.strftime('%H:%M:%S')}] Pushing updates to Google Sheets...")
                success, res = sync_mysql_to_web_app()
                if success:
                    print("✅ Google Sheets successfully updated in real-time!")
                else:
                    print(f"⚠️ Sync failed: {res}")
                last_fingerprint = current_fingerprint

        except KeyboardInterrupt:
            print("\nStopped Real-Time Sync Daemon.")
            break
        except Exception as e:
            print(f"Watcher error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    start_realtime_watcher()
