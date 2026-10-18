import sqlite3
import pandas as pd

conn = sqlite3.connect('database/student_progression.db')

queries = [
    ("Dashboard total students", "SELECT COUNT(*) AS n FROM students"),
    ("Dashboard total semesters", "SELECT COUNT(*) AS n FROM semesters"),
    ("Dashboard active backlogs", "SELECT COUNT(*) AS n FROM semester_subject_marks WHERE result_status IN ('Failed','Backlog')"),
    ("Dashboard attendance alerts", "SELECT COUNT(*) AS n FROM attendance WHERE attendance_percentage < 75.0"),
    ("Dashboard total achievements", "SELECT COUNT(*) AS n FROM portfolio_entries"),
    ("Branch pie chart", "SELECT branch, COUNT(*) AS count FROM students GROUP BY branch"),
    ("Status bar chart", "SELECT current_status, COUNT(*) AS count FROM students GROUP BY current_status"),
    ("Progression trajectory", "SELECT semester_number, academic_year, sgpa, cgpa, result_status, gap_note FROM semesters WHERE student_id = ? ORDER BY semester_number", (1,)),
    ("Attendance warnings view", "SELECT * FROM v_attendance_warnings"),
    ("Backlog tracker view", "SELECT * FROM v_backlog_tracker"),
    ("Student directory", "SELECT student_id, roll_number, enrollment_no, full_name, email, phone, branch, admission_year, current_status FROM students WHERE 1=1 ORDER BY roll_number"),
    ("Student 360 profile", "SELECT * FROM students WHERE student_id = ?", (688,)),
    ("Student school records", "SELECT qualification_type, board_name, passing_year, percentage FROM school_records WHERE student_id = ?", (688,)),
    ("Student semesters", "SELECT semester_number, academic_year, sgpa, cgpa, result_status FROM semesters WHERE student_id = ?", (688,)),
    ("Student attendance", "SELECT s.subject_code, a.classes_held, a.classes_attended, a.attendance_percentage, a.status FROM attendance a JOIN subjects s ON s.subject_id=a.subject_id WHERE a.student_id = ?", (1,)),
    ("Portfolio entries", "SELECT c.category_name, p.title, p.organization, p.entry_date FROM portfolio_entries p JOIN portfolio_categories c ON c.category_id=p.category_id WHERE p.student_id = ?", (1,)),
    ("Semester summary view", "SELECT sem.semester_id, s.roll_number, s.full_name, sem.semester_number, sem.academic_year, sem.sgpa, sem.cgpa, sem.result_status, sem.gap_note FROM semesters sem JOIN students s ON s.student_id = sem.student_id ORDER BY s.roll_number, sem.semester_number")
]

for item in queries:
    name = item[0]
    q = item[1]
    params = item[2] if len(item) > 2 else ()
    df = pd.read_sql(q, conn, params=params)
    print(f"[✓] {name}: {len(df)} rows returned")

conn.close()
print("\nAll queries tested and verified on SQLite!")
