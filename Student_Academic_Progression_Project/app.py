import os
import warnings
from datetime import date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

# Load environment configuration
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="Student Academic Progression System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-cleared {
        background-color: #dcfce7;
        color: #166534;
        padding: 3px 8px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-failed {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 3px 8px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-warning {
        background-color: #fef3c7;
        color: #92400e;
        padding: 3px 8px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Database Connection Helper
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Dhiraj@1507"),
        database=os.getenv("DB_NAME", "student_progression"),
        autocommit=True
    )

def query_df(sql, params=()):
    conn = get_db_connection()
    try:
        return pd.read_sql(sql, conn, params=params)
    finally:
        conn.close()

import threading

def trigger_background_sheet_sync():
    """Silently pushes updated MySQL tables to Google Sheets in a non-blocking background thread."""
    try:
        from scripts.sync_to_web_app import sync_mysql_to_web_app
        sync_mysql_to_web_app()
    except Exception as err:
        print(f"[Auto-Sync Warning] {err}")

def execute(sql, params=(), auto_sync=True):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        last_id = cur.lastrowid
        cur.close()
        
        # Real-time auto sync on any database write (INSERT, UPDATE, DELETE)
        first_word = sql.strip().split()[0].upper()
        if auto_sync and first_word in ("INSERT", "UPDATE", "DELETE", "REPLACE"):
            threading.Thread(target=trigger_background_sheet_sync, daemon=True).start()
            
        return last_id
    finally:
        conn.close()

def check_db_health():
    try:
        conn = get_db_connection()
        conn.close()
        return True, "Connected to MySQL database."
    except Error as e:
        return False, str(e)

# Sidebar Navigation
with st.sidebar:
    st.title("🎓 SAPMS Portal")
    st.caption("Student Academic Progression & Portfolio Management")
    st.divider()
    
    page = st.radio(
        "Navigation Menu",
        ["Dashboard", "Student Management", "Academic Records", "CGPA Target Predictor", "Portfolio & Achievements", "Google Sheets Sync"],
        index=0
    )
    
    st.divider()
    db_ok, db_status = check_db_health()
    if db_ok:
        st.success("🟢 Database Online", icon="✅")
        st.caption("⚡ Real-Time Google Sheet Sync: **Active**")
    else:
        st.error("🔴 Database Offline", icon="⚠️")
        st.caption(db_status)
    
    st.markdown("---")
    st.caption("DBMS Mini-Project • MySQL 8.0 • 3NF Normalized")

if not db_ok:
    st.error("⚠️ MySQL connection failed. Please ensure MySQL Server is running and `.env` credentials are correct.")
    st.info("You can initialize the database schema by running: `python init_db.py` in the terminal.")
    with st.expander("Connection Diagnostic Details"):
        st.code(db_status)
    st.stop()

# ==============================================================================
# 1. DASHBOARD
# ==============================================================================
if page == "Dashboard":
    st.title("📊 Academic Progression Analytics Dashboard")
    st.markdown("Real-time summary of student enrollment, semester performance, attendance warnings, and active backlogs.")

    # KPI Metrics
    try:
        total_students = query_df("SELECT COUNT(*) AS n FROM students").iloc[0]["n"]
        total_semesters = query_df("SELECT COUNT(*) AS n FROM semesters").iloc[0]["n"]
        active_backlogs = query_df("SELECT COUNT(*) AS n FROM semester_subject_marks WHERE result_status IN ('Failed','Backlog')").iloc[0]["n"]
        attendance_alerts = query_df("SELECT COUNT(*) AS n FROM attendance WHERE attendance_percentage < 75.0").iloc[0]["n"]
        total_achievements = query_df("SELECT COUNT(*) AS n FROM portfolio_entries").iloc[0]["n"]
    except Exception as e:
        st.error(f"Error fetching dashboard metrics: {e}")
        st.stop()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Students", int(total_students), "Enrolled")
    c2.metric("Recorded Semesters", int(total_semesters), "Semesters")
    c3.metric("Active Backlogs", int(active_backlogs), "Need Remediation", delta_color="inverse")
    c4.metric("Attendance Alerts", int(attendance_alerts), "< 75% Threshold", delta_color="inverse")
    c5.metric("Achievements", int(total_achievements), "Certificates & Projects")

    st.divider()

    # Visualizations Row
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Students by Engineering Branch")
        branch_df = query_df("SELECT branch, COUNT(*) AS count FROM students GROUP BY branch")
        if not branch_df.empty:
            fig_branch = px.pie(
                branch_df, 
                names="branch", 
                values="count", 
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_branch.update_traces(textposition='inside', textinfo='percent+label')
            fig_branch.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
            st.plotly_chart(fig_branch, use_container_width=True)
        else:
            st.info("No student records found.")

    with col_chart2:
        st.subheader("Academic Status Distribution")
        status_df = query_df("SELECT current_status, COUNT(*) AS count FROM students GROUP BY current_status")
        if not status_df.empty:
            fig_status = px.bar(
                status_df, 
                x="current_status", 
                y="count", 
                color="current_status",
                text="count",
                labels={"current_status": "Status", "count": "Number of Students"},
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_status.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("No student status data available.")

    st.divider()

    # Student Progression Interactive Trend Line
    st.subheader("📈 Student SGPA & CGPA Progression Trend")
    students_list = query_df("SELECT student_id, roll_number, full_name FROM students ORDER BY full_name")
    if not students_list.empty:
        selected_sid = st.selectbox(
            "Select Student to View Progression Trajectory:",
            students_list["student_id"].tolist(),
            format_func=lambda x: f"{students_list.loc[students_list.student_id==x, 'roll_number'].iloc[0]} — {students_list.loc[students_list.student_id==x, 'full_name'].iloc[0]}"
        )
        prog_df = query_df("""
            SELECT semester_number, academic_year, sgpa, cgpa, result_status, gap_note
            FROM semesters WHERE student_id = %s ORDER BY semester_number
        """, (selected_sid,))

        if not prog_df.empty:
            fig_prog = go.Figure()
            fig_prog.add_trace(go.Scatter(
                x=prog_df["semester_number"], y=prog_df["sgpa"],
                mode='lines+markers', name='SGPA',
                line=dict(color='#2563eb', width=3),
                marker=dict(size=8)
            ))
            fig_prog.add_trace(go.Scatter(
                x=prog_df["semester_number"], y=prog_df["cgpa"],
                mode='lines+markers', name='CGPA',
                line=dict(color='#16a34a', width=3, dash='dash'),
                marker=dict(size=8)
            ))
            # Add First Class Distinction line at 8.0
            fig_prog.add_hline(y=8.0, line_dash="dot", line_color="gray", annotation_text="Distinction (8.0)")
            
            fig_prog.update_layout(
                title=f"Progression Trajectory: {students_list.loc[students_list.student_id==selected_sid, 'full_name'].iloc[0]}",
                xaxis_title="Semester Number",
                yaxis_title="Grade Point (0 - 10)",
                yaxis_range=[0, 10.5],
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_prog, use_container_width=True)

            # Display gap indicators if any
            gap_records = prog_df[prog_df["result_status"] == "Gap"]
            if not gap_records.empty:
                for _, r in gap_records.iterrows():
                    st.warning(f"⚠️ **Academic Gap in Semester {int(r['semester_number'])}**: {r['gap_note'] or 'No note provided'}")
        else:
            st.info("No semester records logged for this student yet.")

    st.divider()

    # Alerts & Action Tables Row
    col_alert1, col_alert2 = st.columns(2)

    with col_alert1:
        st.subheader("🚨 Attendance Warnings (< 75%)")
        att_warn_df = query_df("SELECT * FROM v_attendance_warnings")
        if not att_warn_df.empty:
            st.dataframe(
                att_warn_df[["roll_number", "full_name", "subject_code", "attendance_percentage", "shortage_percentage", "classes_needed_for_75"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("🎉 All students currently meet the minimum 75% attendance criteria!")

    with col_alert2:
        st.subheader("📌 Active Backlog Remediation List")
        backlog_df = query_df("SELECT * FROM v_backlog_tracker")
        if not backlog_df.empty:
            st.dataframe(
                backlog_df[["roll_number", "full_name", "semester_number", "subject_code", "total_marks", "grade", "result_status"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("🎉 No active backlogs recorded across all students!")

# ==============================================================================
# 2. STUDENT MANAGEMENT
# ==============================================================================
elif page == "Student Management":
    st.title("👤 Student Profile & Master Management")
    
    tab_list, tab_add, tab_360 = st.tabs(["📋 Student Directory", "➕ Add New Student", "🔍 Comprehensive 360° Profile"])

    # TAB 1: Student Directory & Search/Edit/Delete
    with tab_list:
        st.subheader("Filter & Search Directory")
        c_filter1, c_filter2, c_filter3 = st.columns(3)
        with c_filter1:
            branches = ["All"] + sorted(query_df("SELECT DISTINCT branch FROM students")["branch"].tolist())
            selected_branch = st.selectbox("Filter by Branch", branches)
        with c_filter2:
            years = ["All"] + sorted([str(y) for y in query_df("SELECT DISTINCT admission_year FROM students")["admission_year"].tolist()])
            selected_year = st.selectbox("Filter by Admission Year", years)
        with c_filter3:
            search_query = st.text_input("Search by Name or Roll Number")

        sql_filter = "SELECT student_id, roll_number, enrollment_no, full_name, email, phone, branch, admission_year, current_status FROM students WHERE 1=1"
        params = []
        if selected_branch != "All":
            sql_filter += " AND branch = %s"
            params.append(selected_branch)
        if selected_year != "All":
            sql_filter += " AND admission_year = %s"
            params.append(int(selected_year))
        if search_query.strip():
            sql_filter += " AND (full_name LIKE %s OR roll_number LIKE %s OR enrollment_no LIKE %s)"
            params.extend([f"%{search_query.strip()}%", f"%{search_query.strip()}%", f"%{search_query.strip()}%"])

        sql_filter += " ORDER BY roll_number"
        filtered_df = query_df(sql_filter, tuple(params))
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Edit or Remove Student Record")
        if not filtered_df.empty:
            chosen_student = st.selectbox(
                "Select Student to Modify:",
                filtered_df["student_id"].tolist(),
                format_func=lambda x: f"{filtered_df.loc[filtered_df.student_id==x, 'roll_number'].iloc[0]} — {filtered_df.loc[filtered_df.student_id==x, 'full_name'].iloc[0]}"
            )
            s_row = filtered_df[filtered_df.student_id == chosen_student].iloc[0]

            with st.form("edit_student_form"):
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    e_roll = st.text_input("Roll Number", str(s_row["roll_number"]))
                    e_name = st.text_input("Full Name", str(s_row["full_name"]))
                    e_email = st.text_input("Email", "" if pd.isna(s_row["email"]) else str(s_row["email"]))
                    e_phone = st.text_input("Phone", "" if pd.isna(s_row["phone"]) else str(s_row["phone"]))
                with col_e2:
                    e_branch = st.selectbox(
                        "Branch",
                        ["Computer Engineering", "Information Technology", "Electronics Engineering", "Mechanical Engineering", "Civil Engineering"],
                        index=["Computer Engineering", "Information Technology", "Electronics Engineering", "Mechanical Engineering", "Civil Engineering"].index(s_row["branch"]) if s_row["branch"] in ["Computer Engineering", "Information Technology", "Electronics Engineering", "Mechanical Engineering", "Civil Engineering"] else 0
                    )
                    e_year = st.number_input("Admission Year", min_value=2015, max_value=2030, value=int(s_row["admission_year"]))
                    e_status = st.selectbox(
                        "Status",
                        ["Studying", "Graduated", "Dropped", "On Hold"],
                        index=["Studying", "Graduated", "Dropped", "On Hold"].index(s_row["current_status"])
                    )
                update_btn = st.form_submit_button("💾 Save Profile Updates")

            if update_btn:
                try:
                    execute("""
                        UPDATE students 
                        SET roll_number=%s, full_name=%s, email=%s, phone=%s, branch=%s, admission_year=%s, current_status=%s
                        WHERE student_id=%s
                    """, (e_roll.strip(), e_name.strip(), e_email.strip() or None, e_phone.strip() or None, e_branch, int(e_year), e_status, int(chosen_student)))
                    st.success("Student profile updated successfully!")
                    st.rerun()
                except Error as err:
                    st.error(f"Update failed: {err}")

            # Safe Delete with Confirmation
            st.markdown("#### Danger Zone")
            if st.button("🗑️ Delete This Student", type="secondary"):
                st.session_state["confirm_del_sid"] = int(chosen_student)

            if st.session_state.get("confirm_del_sid") == int(chosen_student):
                st.warning("⚠️ **CAUTION**: Deleting this student will cascade and permanently delete all their school records, semester grades, subject marks, attendance, and portfolio entries.")
                col_d1, col_d2 = st.columns([1, 4])
                with col_d1:
                    if st.button("Yes, Permanently Delete", type="primary"):
                        execute("DELETE FROM students WHERE student_id = %s", (int(chosen_student),))
                        st.session_state.pop("confirm_del_sid", None)
                        st.success("Student record permanently deleted.")
                        st.rerun()
                with col_d2:
                    if st.button("Cancel"):
                        st.session_state.pop("confirm_del_sid", None)
                        st.rerun()

    # TAB 2: Add New Student
    with tab_add:
        st.subheader("Enroll New Student")
        with st.form("add_student_form"):
            c_a1, c_a2 = st.columns(2)
            with c_a1:
                n_roll = st.text_input("Roll Number * (e.g. 23CS01)")
                n_en = st.text_input("Enrollment Number * (e.g. EN23CS01)")
                n_name = st.text_input("Full Name *")
                n_email = st.text_input("Email Address")
            with c_a2:
                n_phone = st.text_input("Phone Number")
                n_branch = st.selectbox(
                    "Branch *",
                    ["Computer Engineering", "Information Technology", "Electronics Engineering", "Mechanical Engineering", "Civil Engineering"]
                )
                n_year = st.number_input("Admission Year *", min_value=2015, max_value=2030, value=2023)
                n_status = st.selectbox("Current Status", ["Studying", "Graduated", "Dropped", "On Hold"])
            submit_student = st.form_submit_button("➕ Create Student Record")

        if submit_student:
            if not n_roll.strip() or not n_en.strip() or not n_name.strip():
                st.error("Roll Number, Enrollment Number, and Full Name are mandatory fields.")
            else:
                try:
                    new_id = execute("""
                        INSERT INTO students (roll_number, enrollment_no, full_name, email, phone, branch, admission_year, current_status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (n_roll.strip(), n_en.strip(), n_name.strip(), n_email.strip() or None, n_phone.strip() or None, n_branch, int(n_year), n_status))
                    st.success(f"Student enrolled successfully with ID: {new_id}")
                    st.rerun()
                except Error as err:
                    st.error(f"Failed to add student: {err}")

    # TAB 3: Comprehensive 360 Profile
    with tab_360:
        st.subheader("Student 360° Consolidated Dossier")
        all_s = query_df("SELECT student_id, roll_number, full_name, branch FROM students ORDER BY full_name")
        if not all_s.empty:
            view_sid = st.selectbox(
                "Select Student Profile to View:",
                all_s["student_id"].tolist(),
                format_func=lambda x: f"{all_s.loc[all_s.student_id==x, 'roll_number'].iloc[0]} — {all_s.loc[all_s.student_id==x, 'full_name'].iloc[0]}"
            )
            s_prof = query_df("SELECT * FROM students WHERE student_id = %s", (view_sid,)).iloc[0]

            # Profile Header Card
            st.markdown(f"""
            ### {s_prof['full_name']}
            **Roll Number:** `{s_prof['roll_number']}` | **Enrollment:** `{s_prof['enrollment_no']}` | **Branch:** `{s_prof['branch']}` | **Year:** `{s_prof['admission_year']}` | **Status:** `{s_prof['current_status']}`
            """)

            # School Records
            st.markdown("#### 🏫 Pre-University Qualifications (SSC & HSC)")
            s_school = query_df("SELECT qualification_type, board_name, school_name, passing_year, obtained_marks, maximum_marks, percentage FROM school_records WHERE student_id = %s", (view_sid,))
            if not s_school.empty:
                st.dataframe(s_school, use_container_width=True, hide_index=True)
            else:
                st.caption("No pre-university school records logged.")

            # Semester Grades
            st.markdown("#### 📚 Semester Academic Performance")
            s_sems = query_df("SELECT semester_number, academic_year, sgpa, cgpa, result_status, result_date, gap_note FROM semesters WHERE student_id = %s ORDER BY semester_number", (view_sid,))
            if not s_sems.empty:
                st.dataframe(s_sems, use_container_width=True, hide_index=True)
            else:
                st.caption("No semester results recorded.")

            # Subject Marks
            st.markdown("#### 📝 Detailed Subject Scores")
            s_marks = query_df("""
                SELECT sem.semester_number, sub.subject_code, sub.subject_name, sub.credits,
                       m.internal_marks, m.external_marks, m.total_marks, m.grade, m.result_status
                FROM semester_subject_marks m
                JOIN semesters sem ON sem.semester_id = m.semester_id
                JOIN subjects sub ON sub.subject_id = m.subject_id
                WHERE m.student_id = %s ORDER BY sem.semester_number, sub.subject_code
            """, (view_sid,))
            if not s_marks.empty:
                st.dataframe(s_marks, use_container_width=True, hide_index=True)
            else:
                st.caption("No individual subject scores recorded.")

            # Attendance Record
            st.markdown("#### 🕒 Attendance Summary")
            s_att = query_df("""
                SELECT sem.semester_number, sub.subject_code, sub.subject_name,
                       att.classes_held, att.classes_attended, att.attendance_percentage
                FROM attendance att
                JOIN semesters sem ON sem.semester_id = att.semester_id
                JOIN subjects sub ON sub.subject_id = att.subject_id
                WHERE att.student_id = %s ORDER BY sem.semester_number
            """, (view_sid,))
            if not s_att.empty:
                st.dataframe(s_att, use_container_width=True, hide_index=True)
            else:
                st.caption("No attendance entries logged.")

            # Achievements
            st.markdown("#### 🏆 Portfolio Achievements & Certifications")
            s_port = query_df("""
                SELECT c.category_group, c.category_name, p.title, p.organization, p.entry_date, p.certificate_url
                FROM portfolio_entries p
                JOIN portfolio_categories c ON c.category_id = p.category_id
                WHERE p.student_id = %s ORDER BY p.entry_date DESC
            """, (view_sid,))
            if not s_port.empty:
                st.dataframe(s_port, use_container_width=True, hide_index=True)
            else:
                st.caption("No portfolio achievements logged.")

# ==============================================================================
# 3. ACADEMIC RECORDS MANAGEMENT
# ==============================================================================
elif page == "Academic Records":
    st.title("📚 Academic Records Management")

    sub_sec = st.selectbox(
        "Choose Academic Record Module:",
        ["School Records (SSC / HSC)", "Semester Summary", "Subject Catalog Master", "Subject Marks & Results", "Attendance Tracker", "Academic Gaps Tracker"]
    )

    students_df = query_df("SELECT student_id, roll_number, full_name FROM students ORDER BY full_name")

    # MODULE 1: School Records
    if sub_sec == "School Records (SSC / HSC)":
        st.subheader("🏫 Pre-University Qualifications (10th SSC & 12th HSC)")
        if students_df.empty:
            st.warning("Please enroll students in Student Management first.")
        else:
            with st.form("school_record_form"):
                col_sc1, col_sc2 = st.columns(2)
                with col_sc1:
                    sc_sid = st.selectbox("Student *", students_df["student_id"].tolist(),
                        format_func=lambda x: f"{students_df.loc[students_df.student_id==x, 'roll_number'].iloc[0]} — {students_df.loc[students_df.student_id==x, 'full_name'].iloc[0]}")
                    sc_type = st.selectbox("Qualification Type *", ["SSC", "HSC"])
                    sc_board = st.text_input("Board Name (e.g. CBSE, State Board, ICSE)")
                    sc_school = st.text_input("School / College Name")
                with col_sc2:
                    sc_year = st.number_input("Passing Year", min_value=2010, max_value=2030, value=2021)
                    sc_obt = st.number_input("Marks Obtained", min_value=0.0, value=450.0, step=1.0)
                    sc_max = st.number_input("Maximum Marks", min_value=1.0, value=500.0, step=1.0)
                    calc_pct = round((sc_obt / sc_max) * 100.0, 2)
                    st.caption(f"Calculated Percentage: **{calc_pct}%**")
                save_sc = st.form_submit_button("💾 Save School Record")

            if save_sc:
                try:
                    pct = round((float(sc_obt) / float(sc_max)) * 100.0, 2)
                    execute("""
                        INSERT INTO school_records (student_id, qualification_type, board_name, school_name, passing_year, obtained_marks, maximum_marks, percentage)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            board_name=VALUES(board_name), school_name=VALUES(school_name), 
                            passing_year=VALUES(passing_year), obtained_marks=VALUES(obtained_marks), 
                            maximum_marks=VALUES(maximum_marks), percentage=VALUES(percentage)
                    """, (int(sc_sid), sc_type, sc_board.strip() or None, sc_school.strip() or None, int(sc_year), float(sc_obt), float(sc_max), pct))
                    st.success(f"{sc_type} record saved successfully!")
                    st.rerun()
                except Error as err:
                    st.error(f"Error saving school record: {err}")

            st.markdown("#### Existing School Records")
            records = query_df("""
                SELECT s.roll_number, s.full_name, sr.qualification_type, sr.board_name, sr.school_name,
                       sr.passing_year, sr.obtained_marks, sr.maximum_marks, sr.percentage
                FROM school_records sr
                JOIN students s ON s.student_id = sr.student_id
                ORDER BY s.roll_number, sr.qualification_type
            """)
            st.dataframe(records, use_container_width=True, hide_index=True)

    # MODULE 2: Semester Summary
    elif sub_sec == "Semester Summary":
        st.subheader("📅 Semester Performance Summary")
        if students_df.empty:
            st.warning("Please enroll students in Student Management first.")
        else:
            with st.form("sem_form"):
                col_sm1, col_sm2 = st.columns(2)
                with col_sm1:
                    sm_sid = st.selectbox("Student *", students_df["student_id"].tolist(),
                        format_func=lambda x: f"{students_df.loc[students_df.student_id==x, 'roll_number'].iloc[0]} — {students_df.loc[students_df.student_id==x, 'full_name'].iloc[0]}")
                    sm_num = st.number_input("Semester Number *", min_value=1, max_value=12, value=1)
                    sm_ay = st.text_input("Academic Year (e.g. 2023-24)", value="2023-24")
                    sm_date = st.date_input("Result Date", value=date.today())
                with col_sm2:
                    sm_sgpa = st.number_input("SGPA (0.0 - 10.0)", min_value=0.0, max_value=10.0, value=8.0, step=0.05)
                    sm_cgpa = st.number_input("CGPA (0.0 - 10.0)", min_value=0.0, max_value=10.0, value=8.0, step=0.05)
                    sm_status = st.selectbox("Result Status", ["Completed", "Current", "Backlog", "Gap"])
                    sm_gap = st.text_input("Gap / Remediation Note (if applicable)")
                save_sem = st.form_submit_button("💾 Save Semester Record")

            if save_sem:
                try:
                    execute("""
                        INSERT INTO semesters (student_id, semester_number, academic_year, sgpa, cgpa, result_status, result_date, gap_note)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            academic_year=VALUES(academic_year), sgpa=VALUES(sgpa), cgpa=VALUES(cgpa),
                            result_status=VALUES(result_status), result_date=VALUES(result_date), gap_note=VALUES(gap_note)
                    """, (int(sm_sid), int(sm_num), sm_ay.strip() or None, float(sm_sgpa), float(sm_cgpa), sm_status, sm_date, sm_gap.strip() or None))
                    st.success("Semester record logged successfully!")
                    st.rerun()
                except Error as err:
                    st.error(f"Error saving semester: {err}")

            st.markdown("#### Master Semester Registry")
            all_sems = query_df("""
                SELECT s.roll_number, s.full_name, sem.semester_number, sem.academic_year,
                       sem.sgpa, sem.cgpa, sem.result_status, sem.result_date, sem.gap_note
                FROM semesters sem
                JOIN students s ON s.student_id = sem.student_id
                ORDER BY s.roll_number, sem.semester_number
            """)
            st.dataframe(all_sems, use_container_width=True, hide_index=True)

    # MODULE 3: Subject Catalog Master
    elif sub_sec == "Subject Catalog Master":
        st.subheader("📖 Course & Subject Catalog")
        with st.form("subject_catalog_form"):
            col_sb1, col_sb2 = st.columns(2)
            with col_sb1:
                sub_code = st.text_input("Subject Code * (e.g. CS501)")
                sub_name = st.text_input("Subject Name * (e.g. Cloud Computing)")
            with col_sb2:
                sub_credits = st.number_input("Credits *", min_value=1, max_value=10, value=4)
                sub_sem = st.number_input("Associated Semester *", min_value=1, max_value=12, value=5)
                sub_type = st.selectbox("Subject Type", ["Theory", "Lab", "Both"])
            add_sub = st.form_submit_button("➕ Add Subject to Catalog")

        if add_sub:
            if not sub_code.strip() or not sub_name.strip():
                st.error("Subject Code and Name are required.")
            else:
                try:
                    execute("""
                        INSERT INTO subjects (subject_code, subject_name, credits, semester_number, subject_type)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (sub_code.strip().upper(), sub_name.strip(), int(sub_credits), int(sub_sem), sub_type))
                    st.success("Subject added to catalog!")
                    st.rerun()
                except Error as err:
                    st.error(f"Failed to add subject: {err}")

        st.markdown("#### Available Subjects")
        subs_df = query_df("SELECT subject_id, subject_code, subject_name, credits, semester_number, subject_type FROM subjects ORDER BY semester_number, subject_code")
        st.dataframe(subs_df, use_container_width=True, hide_index=True)

    # MODULE 4: Subject Marks & Results
    elif sub_sec == "Subject Marks & Results":
        st.subheader("📝 Record Subject-wise Marks & Backlog Outcomes")
        sems_df = query_df("""
            SELECT sem.semester_id, sem.student_id, s.roll_number, s.full_name, sem.semester_number
            FROM semesters sem JOIN students s ON s.student_id = sem.student_id
            ORDER BY s.full_name, sem.semester_number
        """)
        subs_df = query_df("SELECT subject_id, subject_code, subject_name, credits FROM subjects ORDER BY subject_name")

        if sems_df.empty or subs_df.empty:
            st.warning("Please ensure students, semesters, and subjects are configured.")
        else:
            with st.form("marks_entry_form"):
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    chosen_sem = st.selectbox("Select Semester Record *", sems_df["semester_id"].tolist(),
                        format_func=lambda x: f"{sems_df.loc[sems_df.semester_id==x, 'roll_number'].iloc[0]} - {sems_df.loc[sems_df.semester_id==x, 'full_name'].iloc[0]} (Sem {sems_df.loc[sems_df.semester_id==x, 'semester_number'].iloc[0]})")
                    chosen_sub = st.selectbox("Select Subject *", subs_df["subject_id"].tolist(),
                        format_func=lambda x: f"{subs_df.loc[subs_df.subject_id==x, 'subject_code'].iloc[0]} - {subs_df.loc[subs_df.subject_id==x, 'subject_name'].iloc[0]} ({subs_df.loc[subs_df.subject_id==x, 'credits'].iloc[0]} credits)")
                    in_marks = st.number_input("Internal / Lab Marks", min_value=0.0, max_value=50.0, value=25.0, step=0.5)
                with col_m2:
                    ex_marks = st.number_input("External / Theory Marks", min_value=0.0, max_value=100.0, value=65.0, step=0.5)
                    tot_marks = in_marks + ex_marks
                    st.caption(f"Total Marks: **{tot_marks} / 150**")
                    grade_val = st.selectbox("Grade", ["O", "A+", "A", "B+", "B", "C", "P", "F"])
                    res_status = st.selectbox("Result Outcome", ["Cleared", "Failed", "Backlog"])
                save_marks = st.form_submit_button("💾 Save Subject Marks")

            if save_marks:
                try:
                    s_id = int(sems_df.loc[sems_df.semester_id == chosen_sem, 'student_id'].iloc[0])
                    execute("""
                        INSERT INTO semester_subject_marks 
                            (semester_id, student_id, subject_id, internal_marks, external_marks, total_marks, grade, result_status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            internal_marks=VALUES(internal_marks), external_marks=VALUES(external_marks),
                            total_marks=VALUES(total_marks), grade=VALUES(grade), result_status=VALUES(result_status)
                    """, (int(chosen_sem), s_id, int(chosen_sub), float(in_marks), float(ex_marks), float(tot_marks), grade_val, res_status))
                    st.success("Marks recorded successfully!")
                    st.rerun()
                except Error as err:
                    st.error(f"Error logging marks: {err}")

            st.markdown("#### Subject Results Master Log")
            marks_log = query_df("""
                SELECT s.roll_number, s.full_name, sem.semester_number, sub.subject_code, sub.subject_name,
                       m.internal_marks, m.external_marks, m.total_marks, m.grade, m.result_status
                FROM semester_subject_marks m
                JOIN students s ON s.student_id = m.student_id
                JOIN semesters sem ON sem.semester_id = m.semester_id
                JOIN subjects sub ON sub.subject_id = m.subject_id
                ORDER BY s.roll_number, sem.semester_number, sub.subject_code
            """)
            st.dataframe(marks_log, use_container_width=True, hide_index=True)

    # MODULE 5: Attendance Tracker
    elif sub_sec == "Attendance Tracker":
        st.subheader("🕒 Subject Attendance Tracking & Warning Engine")
        sems_df = query_df("""
            SELECT sem.semester_id, sem.student_id, s.roll_number, s.full_name, sem.semester_number
            FROM semesters sem JOIN students s ON s.student_id = sem.student_id
            ORDER BY s.full_name, sem.semester_number
        """)
        subs_df = query_df("SELECT subject_id, subject_code, subject_name FROM subjects ORDER BY subject_name")

        if sems_df.empty or subs_df.empty:
            st.warning("Please configure semesters and subjects first.")
        else:
            with st.form("attendance_form"):
                col_at1, col_at2 = st.columns(2)
                with col_at1:
                    at_sem = st.selectbox("Select Semester Record *", sems_df["semester_id"].tolist(),
                        format_func=lambda x: f"{sems_df.loc[sems_df.semester_id==x, 'roll_number'].iloc[0]} - {sems_df.loc[sems_df.semester_id==x, 'full_name'].iloc[0]} (Sem {sems_df.loc[sems_df.semester_id==x, 'semester_number'].iloc[0]})")
                    at_sub = st.selectbox("Select Subject *", subs_df["subject_id"].tolist(),
                        format_func=lambda x: f"{subs_df.loc[subs_df.subject_id==x, 'subject_code'].iloc[0]} - {subs_df.loc[subs_df.subject_id==x, 'subject_name'].iloc[0]}")
                with col_at2:
                    held = st.number_input("Total Classes Held *", min_value=1, max_value=200, value=40)
                    attended = st.number_input("Classes Attended *", min_value=0, max_value=int(held), value=32)
                    pct_val = round((attended / held) * 100.0, 2)
                    if pct_val < 75.0:
                        st.markdown(f"Attendance: **{pct_val}%** 🔴 *(Below 75% Threshold!)*")
                    else:
                        st.markdown(f"Attendance: **{pct_val}%** 🟢 *(Satisfactory)*")
                save_att = st.form_submit_button("💾 Save Attendance Record")

            if save_att:
                if attended > held:
                    st.error("Classes attended cannot exceed total classes held.")
                else:
                    try:
                        s_id = int(sems_df.loc[sems_df.semester_id == at_sem, 'student_id'].iloc[0])
                        pct = round((float(attended) / float(held)) * 100.0, 2)
                        execute("""
                            INSERT INTO attendance (student_id, subject_id, semester_id, classes_held, classes_attended, attendance_percentage)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                                classes_held=VALUES(classes_held), classes_attended=VALUES(classes_attended),
                                attendance_percentage=VALUES(attendance_percentage)
                        """, (s_id, int(at_sub), int(at_sem), int(held), int(attended), pct))
                        st.success("Attendance updated successfully!")
                        st.rerun()
                    except Error as err:
                        st.error(f"Error saving attendance: {err}")

            st.markdown("#### Attendance Records Master Log")
            att_log = query_df("""
                SELECT s.roll_number, s.full_name, sem.semester_number, sub.subject_code, sub.subject_name,
                       att.classes_held, att.classes_attended, att.attendance_percentage
                FROM attendance att
                JOIN students s ON s.student_id = att.student_id
                JOIN semesters sem ON sem.semester_id = att.semester_id
                JOIN subjects sub ON sub.subject_id = att.subject_id
                ORDER BY s.roll_number, sem.semester_number
            """)
            st.dataframe(att_log, use_container_width=True, hide_index=True)

    # MODULE 6: Academic Gaps Tracker
    elif sub_sec == "Academic Gaps Tracker":
        st.subheader("⏱️ Formal Academic Gap-Year Logging")
        if students_df.empty:
            st.warning("Please enroll students in Student Management first.")
        else:
            with st.form("gap_form"):
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    g_sid = st.selectbox("Student *", students_df["student_id"].tolist(),
                        format_func=lambda x: f"{students_df.loc[students_df.student_id==x, 'roll_number'].iloc[0]} — {students_df.loc[students_df.student_id==x, 'full_name'].iloc[0]}")
                    g_start = st.number_input("Start Year *", min_value=2015, max_value=2030, value=2022)
                    g_end = st.number_input("End Year *", min_value=int(g_start), max_value=2030, value=2023)
                with col_g2:
                    g_reason = st.text_input("Primary Reason * (e.g. Medical, Financial, Competitive Exam)")
                    g_desc = st.text_area("Detailed Explanation & Clearance Details")
                save_gap = st.form_submit_button("💾 Log Academic Gap")

            if save_gap:
                if not g_reason.strip():
                    st.error("Reason is required.")
                elif g_start > g_end:
                    st.error("Start Year must be less than or equal to End Year.")
                else:
                    try:
                        execute("""
                            INSERT INTO academic_gaps (student_id, start_year, end_year, reason, description)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (int(g_sid), int(g_start), int(g_end), g_reason.strip(), g_desc.strip() or None))
                        st.success("Academic gap record logged successfully!")
                        st.rerun()
                    except Error as err:
                        st.error(f"Error logging academic gap: {err}")

            st.markdown("#### Documented Academic Gaps")
            gaps_df = query_df("""
                SELECT s.roll_number, s.full_name, g.start_year, g.end_year, g.reason, g.description
                FROM academic_gaps g
                JOIN students s ON s.student_id = g.student_id
                ORDER BY g.start_year DESC
            """)
            st.dataframe(gaps_df, use_container_width=True, hide_index=True)

# ==============================================================================
# 4. CGPA TARGET PREDICTOR
# ==============================================================================
elif page == "CGPA Target Predictor":
    st.title("🎯 CGPA Target Predictor & Academic Planning Calculator")
    st.markdown("""
    This transparent planning tool projects the **average SGPA required across future semesters** to attain your desired target degree CGPA.
    Calculations use degree credit progression assumptions and clear mathematical constraints.
    """)

    students_list = query_df("SELECT student_id, roll_number, full_name, branch FROM students ORDER BY full_name")
    if students_list.empty:
        st.warning("No student records found.")
    else:
        chosen_sid = st.selectbox(
            "Select Student for Target Planning:",
            students_list["student_id"].tolist(),
            format_func=lambda x: f"{students_list.loc[students_list.student_id==x, 'roll_number'].iloc[0]} — {students_list.loc[students_list.student_id==x, 'full_name'].iloc[0]} ({students_list.loc[students_list.student_id==x, 'branch'].iloc[0]})"
        )

        # Retrieve completed semesters for this student
        sem_records = query_df("""
            SELECT semester_number, academic_year, sgpa, cgpa, result_status
            FROM semesters WHERE student_id = %s AND result_status = 'Completed'
            ORDER BY semester_number
        """, (chosen_sid,))

        completed_sems = len(sem_records)
        latest_cgpa = float(sem_records.iloc[-1]["cgpa"]) if not sem_records.empty else 0.0

        c_p1, c_p2, c_p3 = st.columns(3)
        c_p1.metric("Semesters Completed", f"{completed_sems} / 8 Semesters")
        c_p2.metric("Current Cumulative CGPA", f"{latest_cgpa:.2f}")

        with c_p3:
            target_cgpa = st.number_input("Target Degree CGPA", min_value=0.0, max_value=10.0, value=max(8.5, round(latest_cgpa + 0.5, 2)), step=0.1)

        total_degree_semesters = 8
        remaining_sems = total_degree_semesters - completed_sems

        if remaining_sems <= 0:
            st.info("🎓 All 8 degree semesters are already completed for this student.")
        else:
            # Mathematical formula:
            # Target_CGPA * 8 = (Current_CGPA * completed_sems) + (Required_SGPA * remaining_sems)
            # Required_SGPA = (Target_CGPA * 8 - Current_CGPA * completed_sems) / remaining_sems
            required_sgpa = (target_cgpa * total_degree_semesters - latest_cgpa * completed_sems) / remaining_sems

            st.divider()
            st.subheader("Projection Analysis")

            col_res1, col_res2 = st.columns([1, 2])
            with col_res1:
                st.metric("Required Average SGPA", f"{required_sgpa:.2f}")

            with col_res2:
                if required_sgpa <= 0:
                    st.success("🎉 **Target Already Exceeded**: Your current CGPA already meets or exceeds this target!")
                elif required_sgpa <= 7.5:
                    st.success("🟢 **Comfortably Achievable**: A moderate academic focus will comfortably secure your target CGPA.")
                elif required_sgpa <= 8.5:
                    st.info("🔵 **Realistic with Dedication**: Consistent study and scoring First Class grades will achieve this target.")
                elif required_sgpa <= 9.5:
                    st.warning("🟠 **High Academic Rigor Needed**: Requires distinction scores (9.0+ SGPA) in almost every remaining subject.")
                elif required_sgpa <= 10.0:
                    st.error("🔴 **Extremely Challenging**: Requires near-perfect 10.0 SGPA in every upcoming semester.")
                else:
                    st.error(f"❌ **Mathematically Impossible**: Even scoring a perfect 10.0 SGPA across all remaining {remaining_sems} semesters will reach a maximum CGPA of {((latest_cgpa * completed_sems + 10.0 * remaining_sems) / total_degree_semesters):.2f}.")

            st.markdown(f"""
            > **Calculation Assumptions**:
            > - Standard 4-year undergraduate degree consisting of 8 semesters with equal credit distribution per semester (~20-22 credits/sem).
            > - Current baseline CGPA is **{latest_cgpa:.2f}** over **{completed_sems}** completed semester(s).
            > - Target planning window spans **{remaining_sems}** remaining semester(s).
            > - *Disclaimer: This projection is an academic planning estimate, not a guaranteed outcome.*
            """)

            # Projected trajectory simulation chart
            st.subheader("Projected Semester Trajectory Simulation")
            sim_x = list(range(1, total_degree_semesters + 1))
            sim_y = []
            running_total = 0.0

            for i in range(1, total_degree_semesters + 1):
                if i <= completed_sems:
                    s_val = float(sem_records.loc[sem_records.semester_number == i, 'sgpa'].iloc[0])
                    running_total += s_val
                    sim_y.append(round(running_total / i, 2))
                else:
                    clamped_sgpa = min(10.0, max(0.0, required_sgpa))
                    running_total += clamped_sgpa
                    sim_y.append(round(running_total / i, 2))

            fig_sim = go.Figure()
            fig_sim.add_trace(go.Scatter(
                x=sim_x[:completed_sems], y=sim_y[:completed_sems],
                mode='lines+markers', name='Actual CGPA',
                line=dict(color='#2563eb', width=3), marker=dict(size=8)
            ))
            fig_sim.add_trace(go.Scatter(
                x=sim_x[completed_sems-1:], y=sim_y[completed_sems-1:],
                mode='lines+markers', name='Projected CGPA Pathway',
                line=dict(color='#16a34a', width=3, dash='dot'), marker=dict(size=8)
            ))
            fig_sim.add_hline(y=target_cgpa, line_dash="dash", line_color="#dc2626", annotation_text=f"Target: {target_cgpa}")
            fig_sim.update_layout(
                xaxis_title="Semester",
                yaxis_title="CGPA",
                yaxis_range=[0, 10.5],
                hovermode="x unified"
            )
            st.plotly_chart(fig_sim, use_container_width=True)

# ==============================================================================
# 5. PORTFOLIO & ACHIEVEMENTS
# ==============================================================================
elif page == "Portfolio & Achievements":
    st.title("🏆 Portfolio & Extracurricular Achievements")
    st.markdown("Track technical certifications, capstone projects, hackathons, internships, seminars, and extracurriculars.")

    tab_p_view, tab_p_add = st.tabs(["📂 View Portfolio Entries", "➕ Add Portfolio Record"])

    # TAB 1: View Portfolio
    with tab_p_view:
        category_filter = st.selectbox(
            "Filter by Category Group:",
            ["All Categories", "Certification", "Project", "Hackathon", "Internship", "Seminar", "Activity", "Other"]
        )

        sql_p = """
            SELECT p.entry_id, s.roll_number, s.full_name, c.category_group, c.category_name,
                   p.title, p.organization, p.entry_date, p.description, p.certificate_url
            FROM portfolio_entries p
            JOIN students s ON s.student_id = p.student_id
            JOIN portfolio_categories c ON c.category_id = p.category_id
            WHERE 1=1
        """
        p_params = []
        if category_filter != "All Categories":
            sql_p += " AND c.category_group = %s"
            p_params.append(category_filter)

        sql_p += " ORDER BY p.entry_date DESC"
        entries_df = query_df(sql_p, tuple(p_params))
        st.dataframe(entries_df, use_container_width=True, hide_index=True)

        # Delete Entry Option
        if not entries_df.empty:
            st.divider()
            st.subheader("Manage Existing Entry")
            del_eid = st.selectbox(
                "Select Entry to Delete:",
                entries_df["entry_id"].tolist(),
                format_func=lambda x: f"ID {x} — {entries_df.loc[entries_df.entry_id==x, 'title'].iloc[0]} ({entries_df.loc[entries_df.entry_id==x, 'full_name'].iloc[0]})"
            )
            if st.button("🗑️ Delete Selected Portfolio Record", type="secondary"):
                try:
                    execute("DELETE FROM portfolio_entries WHERE entry_id = %s", (int(del_eid),))
                    st.success("Portfolio entry deleted.")
                    st.rerun()
                except Error as err:
                    st.error(f"Error deleting entry: {err}")

    # TAB 2: Add Entry
    with tab_p_add:
        st.subheader("Log New Achievement")
        students_df = query_df("SELECT student_id, roll_number, full_name FROM students ORDER BY full_name")
        categories_df = query_df("SELECT category_id, category_name, category_group FROM portfolio_categories ORDER BY category_group, category_name")

        if students_df.empty:
            st.warning("Please enroll students first.")
        else:
            with st.form("add_portfolio_form"):
                col_pf1, col_pf2 = st.columns(2)
                with col_pf1:
                    pf_sid = st.selectbox("Student *", students_df["student_id"].tolist(),
                        format_func=lambda x: f"{students_df.loc[students_df.student_id==x, 'roll_number'].iloc[0]} — {students_df.loc[students_df.student_id==x, 'full_name'].iloc[0]}")
                    pf_cat = st.selectbox("Category *", categories_df["category_id"].tolist(),
                        format_func=lambda x: f"[{categories_df.loc[categories_df.category_id==x, 'category_group'].iloc[0]}] {categories_df.loc[categories_df.category_id==x, 'category_name'].iloc[0]}")
                    pf_title = st.text_input("Title / Event Name * (e.g. AWS Certified Solutions Architect)")
                with col_pf2:
                    pf_org = st.text_input("Issuing Organization (e.g. Amazon Web Services, IIT Bombay)")
                    pf_date = st.date_input("Date Issued / Completed", value=date.today())
                    pf_url = st.text_input("Certificate / Repository Verification URL (Optional)")
                pf_desc = st.text_area("Description / Project Overview")
                save_pf = st.form_submit_button("➕ Save Achievement to Portfolio")

            if save_pf:
                if not pf_title.strip():
                    st.error("Title is required.")
                else:
                    try:
                        execute("""
                            INSERT INTO portfolio_entries (student_id, category_id, title, organization, entry_date, description, certificate_url)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (int(pf_sid), int(pf_cat), pf_title.strip(), pf_org.strip() or None, pf_date, pf_desc.strip() or None, pf_url.strip() or None))
                        st.success("Achievement logged successfully!")
                        st.rerun()
                    except Error as err:
                        st.error(f"Error saving entry: {err}")

# ==============================================================================
# 6. GOOGLE SHEETS SYNCHRONIZATION
# ==============================================================================
elif page == "Google Sheets Sync":
    st.title("☁️ Google Sheets Cloud Export & Synchronization")
    st.markdown("""
    Synchronize your local MySQL database tables directly into your designated Google Spreadsheet.
    """)

    web_app_url = os.getenv(
        "GOOGLE_WEB_APP_URL",
        "https://script.google.com/macros/s/AKfycbzeXEiRWIUgBrXagidlUQ7_deJ3bF5aXisBPE-1BOIQ0QXZJYD9x5jM8-XJWfAZSzvy/exec"
    ).strip()

    tab_webapp, tab_gspread, tab_csv = st.tabs(["🚀 Web App Direct Sync (Recommended)", "🔑 Google Cloud Service Account", "📁 Offline CSV Export"])

    with tab_webapp:
        st.subheader("Google Apps Script Web App Integration")
        st.markdown("""
        Pushes all 9 normalized relational tables directly to your Google Sheet without requiring service account JSON keys.
        """)
        
        user_url = st.text_input("Google Apps Script Web App URL:", value=web_app_url)
        
        col_wa1, col_wa2 = st.columns(2)
        with col_wa1:
            if st.button("🔍 Ping Web App Endpoint", type="secondary"):
                import urllib.request
                try:
                    with urllib.request.urlopen(user_url, timeout=10) as response:
                        res_data = response.read().decode("utf-8")
                        st.success("🟢 Web App is ONLINE!")
                        st.json(res_data)
                except Exception as err:
                    st.error(f"Failed to reach Web App: {err}")

        with col_wa2:
            sync_btn = st.button("🚀 Push MySQL Database to Google Sheets", type="primary")

        if sync_btn:
            with st.spinner("Exporting all 9 tables from MySQL to Google Sheets..."):
                try:
                    import decimal
                    import json
                    import urllib.request
                    
                    tables_to_sync = [
                        "students", "school_records", "semesters", "subjects",
                        "semester_subject_marks", "attendance", "academic_gaps",
                        "portfolio_entries", "portfolio_categories"
                    ]

                    def fmt(val):
                        if val is None: return ""
                        if isinstance(val, decimal.Decimal): return float(val)
                        if hasattr(val, "strftime"): return val.strftime("%Y-%m-%d %H:%M:%S") if hasattr(val, "hour") else val.strftime("%Y-%m-%d")
                        return str(val)

                    conn = get_db_connection()
                    cur = conn.cursor()
                    payload_tables = {}
                    for tbl in tables_to_sync:
                        cur.execute(f"SELECT * FROM `{tbl}`")
                        hdrs = [desc[0] for desc in cur.description]
                        raw = cur.fetchall()
                        formatted_rows = [[fmt(c) for c in r] for r in raw]
                        payload_tables[tbl] = {"headers": hdrs, "rows": formatted_rows}
                    cur.close()
                    conn.close()

                    req_data = json.dumps({"action": "sync_all", "tables": payload_tables}).encode("utf-8")
                    post_req = urllib.request.Request(user_url, data=req_data, headers={"Content-Type": "application/json"})

                    with urllib.request.urlopen(post_req, timeout=30) as resp:
                        resp_content = resp.read().decode("utf-8")
                        try:
                            result_json = json.loads(resp_content)
                            if result_json.get("status") == "success":
                                st.success("🎉 Complete database successfully synchronized to your Google Sheet!")
                                st.json(result_json)
                            else:
                                st.warning("Sync responded: " + str(result_json))
                        except Exception:
                            if "doPost" in resp_content:
                                st.error("⚠️ The Google Apps Script needs `doPost(e)` to be deployed. See the instructions below.")
                            else:
                                st.success("🎉 Payload transmitted successfully!")
                except Exception as err:
                    st.error(f"Sync error: {err}")

    with tab_gspread:
        st.subheader("Google Cloud Service Account (gspread)")
        sheet_id = os.getenv("GOOGLE_SHEET_ID", "").strip()
        key_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json").strip()
        st.markdown(f"**Spreadsheet ID:** `{sheet_id or 'Not Configured'}`")
        st.markdown(f"**Service Account File:** `{key_file} ({'Found' if os.path.exists(key_file) else 'Not Found'})`")

    st.divider()
    st.subheader("Offline CSV Export Alternative")
    st.caption("If you do not have Google Cloud service account credentials configured, you can download all tables as local CSV files:")
    csv_tab = st.selectbox("Select Table to Download", ["students", "school_records", "semesters", "subjects", "semester_subject_marks", "attendance", "academic_gaps", "portfolio_entries"])
    table_csv = query_df(f"SELECT * FROM `{csv_tab}`")
    st.download_button(
        label=f"⬇️ Download {csv_tab}.csv",
        data=table_csv.to_csv(index=False).encode('utf-8'),
        file_name=f"{csv_tab}.csv",
        mime='text/csv'
    )
