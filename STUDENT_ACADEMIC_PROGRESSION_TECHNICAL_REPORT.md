# STUDENT ACADEMIC PROGRESSION
# USER & TECHNICAL REPORT
### DBMS Mini-Project

**Application:** [http://localhost:8501](http://localhost:8501)  
**GitHub Repository:** [https://github.com/dhirusuthar77-coder/dhiru_db](https://github.com/dhirusuthar77-coder/dhiru_db)  
**Submitted by:** Dhiraj Suthar  
**Roll No:** [Your Roll No - e.g. 44]  
**Class:** T.E. (Computer Engineering / Electronics & Telecommunication)  
**Institute:** VIVA INSTITUTE OF TECHNOLOGY  

---
*Student Academic Progression — User & Technical Report | Page 1*

\pagebreak

---

## Project Details
The following details identify the DBMS mini-project and its deployment.

| Particulars | Details |
| :--- | :--- |
| **Course** | Database Management Systems (DBMS Mini-Project) |
| **Institution** | VIVA Institute of Technology |
| **Live Production Web App** | [http://localhost:8501](http://localhost:8501) |
| **GitHub Repository** | [https://github.com/dhirusuthar77-coder/dhiru_db](https://github.com/dhirusuthar77-coder/dhiru_db) |
| **Primary Database Engine** | SQLite 3 (ACID-compliant, foreign keys enabled, strict 3NF schema) |
| **Cloud Mirror Database** | MySQL 8.0 (InnoDB, remote replication engine) |
| **Live Cloud Synchronization** | Google Apps Script Webhook Pipeline (Bi-directional JSON sync) |

---

## 1. System Architecture & Relational Topology
The project implements a layered three-tier architecture:

| Layer / Component | Responsibilities / Details |
| :--- | :--- |
| **Presentation Layer — Streamlit GUI** | Live web application; interactive navigation panels; Plotly dual-line progression graphs; responsive desktop and mobile layout. |
| **Business & Integration Engine** | Credit-weighted $\text{SGPA} = \frac{\sum (\text{Credits} \times \text{Grade Point})}{\sum \text{Credits}}$; cumulative CGPA across active semesters; drop-year chronology detection and validation alerts; event-driven sync queue and payload snapshot dispatcher. |
| **Local Relational Database — SQLite 3** | Strict 3NF; `PRAGMA foreign_keys = ON;` 8 interconnected relational tables (`students`, `school_records`, `semesters`, `subjects`, `semester_results`, `drop_years`, `achievements`, `achievement_categories`). |
| **Google Sheets Webhook** | Real-time JSON streaming; 8 normalized synchronized sheets matching institutional taxonomy. |
| **Cloud Mirror Database — MySQL 8.0** | Remote persistence and backup; automated triggers; CASCADE/RESTRICT integrity constraints; analytical views. |

---

## 2. Step-by-Step Operational Guide (GUI & Sync Feature)

### Step 1: Accessing the Live System
Open `http://localhost:8501` in a modern web browser such as Chrome, Edge, Safari, or Firefox. The interface provides a responsive layout that automatically adapts to desktop, tablet, and mobile viewport resolutions.

### Step 2: Browsing & Filtering Student Directory
Open **“Dashboard & Analytics”** or **“Student Management”**. The system manages engineering departments including Computer Engineering, Information Technology, Electronics & Telecommunication, AI & Machine Learning, Data Science, and Mechanical Engineering. Search by roll number (examples: `23FC003`, `22CS01`, `21ME01`) or student full name. Key metrics include total enrolled students, active vs. on-hold students, institutional CGPA distribution, and active drop-year warning flags.

---
*Student Academic Progression — User & Technical Report | Page 2*

\pagebreak

---

### Step 3: Academic Progression & SGPA/CGPA
Review the student's 10th SSC and 12th HSC / Diploma schooling history, including board of education, maximum marks, marks obtained, and percentages. The system generates an interactive Plotly dual-line trajectory for Term SGPA and Cumulative CGPA across Semesters 1–8, with credit-attempted vs. credit-earned breakdowns and distinction benchmark thresholds (8.0 CGPA).

### Step 4: Drop-Year Audit Tracking
Open **“Drop Years”**. Academic gap duration is strictly evaluated as $\text{End Year} - \text{Start Year}$, with documented grounds such as Medical Leave, Examination Preparation, or Financial Hardship along with an approving authority. Active warning banners alert faculty on both the student profile dossier and the administrative executive dashboard.

### Step 5: Portfolio & Extracurricular Achievements
Open **“Portfolio & Achievements”**. Categories include Technical Certifications, Capstone Projects, National Hackathons, Internships, Seminars, and Co-curricular Activities. Records store project titles, issuing organizations, verification URLs, scopes (State, National, International), and achievement dates.

### Step 6: Google Sheets Webhook Synchronization
Open **“Google Sheets Sync”**. The synchronization engine connects to the deployed Google Apps Script Webhook endpoint (`https://script.google.com/macros/s/AKfycbzmPSEAhyOnK4wwQfA6nsrMl1aNnZp6JGVurP0oiq2nbXC-8EpxfpZ4_bgpDWEQ5Qw/exec`).

| Sync Action | Description |
| :--- | :--- |
| **Process Pending Queue** | Dispatches uncommitted local INSERT, UPDATE, or DELETE operations to Google Sheets in non-blocking background threads. |
| **Force Full Sync (All 8 Tables)** | Serializes database rows into structured JSON tables and mirrors them across the eight designated sheets. |
| **Live Demo: Add Test Student & Sync** | Creates a new student record in SQLite/MySQL and pushes it to Google Sheets in under 2 seconds. |
| **Verify Spreadsheet** | Verifies tabs in exact sequence: `achievement_categories`, `students`, `school_records`, `semesters`, `subjects`, `semester_results`, `drop_years`, `achievements`. |

---

## 3. Instructions on Modifying & Updating Records in the Database

### Method A: Graphical Forms (Recommended)
1. **Register a Student**: Open **“Student Management”** → **“Add New Student”**; enter roll number, full name, institutional email (`@viva-technology.org`), phone, department, and admission year; select **“Save Student”**. Uniqueness of roll number and email is validated prior to commit.
2. **Update Semester Results**: Open **“Academic Records”** → **“Enter Semester Marks”**; select student, semester, and subject; input internal and external scores; select **“Save Marks”**. System automatically recomputes total marks, letter grades, SGPA, and cumulative CGPA.
3. **Log Academic Gap**: Open **“Drop Years”**; select student and specify start year, end year, reason, and approval note. Validation enforces $\text{End Year} \ge \text{Start Year}$.

---
*Student Academic Progression — User & Technical Report | Page 3*

\pagebreak

---

### Method B: SQL Console
Administrators can execute standard SQL queries directly against the database:

| Purpose | SQL Example |
| :--- | :--- |
| **Update student contact details and status** | `UPDATE students SET phone = '9801437836', current_status = 'Active' WHERE roll_number = '23FC003';` |
| **Correct theory and lab marks** | `UPDATE semester_results SET internal_marks = 26.00, external_marks = 64.00, total_marks = 90.00, grade = 'O', result_status = 'Cleared' WHERE mark_id = 7;` |
| **Recalculate semester SGPA** | `UPDATE semesters SET sgpa = 8.95, cgpa = 8.85 WHERE student_id = 688 AND semester_number = 2;` |
| **Delete an achievement** | `DELETE FROM achievements WHERE entry_id = 3;` |

---

### Method C: Python / CLI Database Administration
For automated or programmatic batch updates, connect via Python using transactions with error handling:

| Step | Example Python Code |
| :--- | :--- |
| **Connect** | `conn = sqlite3.connect('database/student_progression.db')` |
| **Enable foreign keys** | `conn.execute("PRAGMA foreign_keys = ON;")` |
| **Update record** | `cur = conn.cursor(); cur.execute("UPDATE students SET branch = 'Electronics & Telecommunication', email = 'arjun.reddy@viva-technology.org' WHERE roll_number = '23FC003'")` |
| **Successful update** | `conn.commit(); print("Transaction committed successfully.")` |
| **Constraint violation** | `except sqlite3.IntegrityError as err: conn.rollback(); print(f"Integrity violation rolled back: {err}")` |
| **Close connection** | `finally: conn.close()` |

---
*Student Academic Progression — User & Technical Report | Page 4*

\pagebreak

---

## 4. Schema Constraints & Violation Handling
The relational schema enforces strict integrity constraints across all operational tables:

| Constraint Type | Target Entity / Column | Rule Enforced | Violation Handling |
| :--- | :--- | :--- | :--- |
| **PRIMARY KEY** | All 8 tables (`student_id`, `semester_id`, etc.) | Auto-incrementing integer keys guarantee permanent record uniqueness. | `SQLITE_CONSTRAINT_PRIMARYKEY` / MySQL Error 1062; rejected with form notification. |
| **UNIQUE candidate key** | `students(roll_number)` | No duplicate roll numbers across departments. | `SQLITE_CONSTRAINT_UNIQUE`; form halts and reports roll number conflict. |
| **UNIQUE candidate key** | `students(email)` | No duplicate institutional email addresses. | `SQLITE_CONSTRAINT_UNIQUE`; form prevents duplicate email registration. |
| **UNIQUE composite key** | `school_records(student_id, qualification_type)` | At most one SSC (10th) and one HSC (12th) record per student. | `SQLITE_CONSTRAINT_UNIQUE`; existing record is updated in place via `ON DUPLICATE KEY UPDATE`. |
| **UNIQUE composite key** | `semesters(student_id, semester_number)` | Each semester (1–8) logged exactly once per student. | `SQLITE_CONSTRAINT_UNIQUE`; existing semester record is loaded for modification. |
| **CHECK** | `school_records(percentage)` | Percentage must be between 0.00 and 100.00. | `SQLITE_CONSTRAINT_CHECK`; invalid percentages are rejected with alert. |
| **CHECK** | `semesters(sgpa)`, `semesters(cgpa)` | GPA values restricted to the 0.00 to 10.00 scale. | `SQLITE_CONSTRAINT_CHECK`; out-of-range values blocked at engine level. |
| **CHECK** | `drop_years(start_year, end_year)` | `end_year >= start_year`. | `SQLITE_CONSTRAINT_CHECK`; invalid chronology is rejected. |
| **CHECK** | `semester_results(internal_marks, external_marks)` | Non-negative marks within prescribed maximum caps. | `SQLITE_CONSTRAINT_CHECK`; out-of-range examination marks blocked. |
| **FOREIGN KEY — CASCADE** | `students` → `school_records`, `semesters`, `drop_years`, `achievements` | Deleting a student record automatically cleans all dependent child rows. | Automatic transactional cascading delete; guarantees zero orphan records. |
| **FOREIGN KEY — RESTRICT** | `subjects(subject_id)` → `semester_results(subject_id)` | A course cannot be deleted while referenced by active student examination results. | `SQLITE_CONSTRAINT_RESTRICT` / MySQL Error 1451; deletion rejected with explanatory notice. |

---
*Student Academic Progression — User & Technical Report | Page 5*

\pagebreak

---

## 5. Third Normal Form (3NF) Rationale
The schema satisfies Boyce-Codd & Third Normal Form: for every non-trivial functional dependency $X \to Y$, $X$ is a superkey, or $Y \setminus X$ is part of a candidate key.

| Relation | Attributes / Keys | 3NF Rationale |
| :--- | :--- | :--- |
| **`students`** | `student_id` (PK), `roll_number` (UK), `full_name`, `email` (UK), `phone`, `branch`, `admission_year`, `current_status`. | **Functional dependencies:** `student_id` $\to$ all attributes; `roll_number` $\to$ all attributes. All attributes are atomic (1NF); candidate keys are minimal; no non-prime attribute transitively determines another non-prime attribute (3NF). |
| **`semesters`** | `semester_id` (PK), `student_id` (FK), `semester_number`, `academic_year`, `sgpa`, `cgpa`, `result_status`. Candidate key: `(student_id, semester_number)`. | SGPA and CGPA depend strictly on the combination of student and semester number. There is no transitive dependency between academic calendar year and grade point average. |
| **`subjects`** | `subject_id` (PK), `subject_code` (UK), `subject_name`, `credits`, `semester_number`, `subject_type`. | An independent course catalog eliminates insertion, update, and deletion anomalies. Subjects can be scheduled before student enrollment; credit adjustments are updated in one place. |
| **`semester_results`** | `result_id` (PK), `semester_id` (FK), `subject_id` (FK), `internal_marks`, `external_marks`, `total_marks`, `grade`, `result_status`. Candidate key: `(semester_id, subject_id)`. | Result metrics depend uniquely on semester enrollment and subject ID. Theory and practical components are stored in separate atomic columns. |
| **`school_records`** | `school_record_id` (PK), `student_id` (FK), `qualification_type`, `board_name`, `school_name`, `passing_year`, `percentage`. Candidate key: `(student_id, qualification_type)`. | Prior education qualifications are isolated from university progression, eliminating repetitive null fields for students without diplomas. |
| **`drop_years`** | `gap_id` (PK), `student_id` (FK), `start_year`, `end_year`, `reason`, `description`. | Non-academic hiatuses are recorded in a separate entity rather than polluting core semester tables with blank rows. |
| **`achievements`** | `entry_id` (PK), `student_id` (FK), `category_id` (FK), `title`, `organization`, `entry_date`, `certificate_url`. | Many-to-one relationship to students and achievement categories preserves scalability and avoids repetitive strings. |
| **`achievement_categories`** | `category_id` (PK), `category_name` (UK), `category_group`, `activity_type`. | Standardized taxonomy master; prevents category name typos and simplifies analytical grouping. |

---
*Student Academic Progression — User & Technical Report | Page 6*
