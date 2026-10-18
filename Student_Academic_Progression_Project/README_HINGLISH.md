# 🎓 Student Academic Progression & Portfolio Management System (SAPMS)
## Complete DBMS Mini-Project (Windows + MySQL 8.0 + Python + Streamlit)

Yeh ek complete, industry-standard **DBMS Mini-Project** hai jo engineering students ke pure academic career, semester progression, backlogs, attendance alerts, portfolio achievements aur target CGPA prediction ko ek relational MySQL database me manage karta hai.

---

## 🌟 1. Key Features
- **Student 360° Management**: Full CRUD (Add, Edit, View, Delete with cascade protection), branch filtering aur roll-number search.
- **Pre-University Records**: SSC (10th) aur HSC (12th) ke boards, marks aur percentage tracking.
- **Semester Progression**: SGPA aur CGPA graph with Distinction (8.0) line.
- **Subject-Wise Results & Backlogs**: Internal (lab), external (theory) marks aur active backlog tracking table.
- **Attendance Warning Engine**: 75% se kam attendance wale students ke liye dynamic alerts aur required classes ka calculation.
- **Academic Gap Tracking**: Medical/financial gap years ka formal documentation.
- **CGPA Target Predictor**: Transparent calculator jo future semesters me required SGPA calculate karta hai.
- **Portfolio & Achievements**: Technical certifications (AWS, Oracle), hackathons (SIH), capstone projects aur internships tracking.
- **Google Sheets Cloud Sync**: Official Google Sheets API se one-way live export aur offline CSV download.

---

## 💻 2. System Requirements
1. **Operating System**: Windows 10 ya 11
2. **Python**: Python 3.10+ (tested on Python 3.15)
3. **Database**: MySQL Server 8.0+ (running on port 3306)

---

## 🚀 3. Quick Start Guide (Windows PowerShell Commands)

Apne terminal (PowerShell ya CMD) me project folder ke andar jaakar niche diye gaye commands step-by-step run karo:

### Step 1: Project Folder me Navigate karo
```powershell
cd c:\Users\Dheeru\Downloads\Student_Academic_Progression_Project\Student_Academic_Progression_Project
```

### Step 2: Dependencies Install karo
```powershell
pip install -r requirements.txt
```

### Step 3: Database Initialize karo (Automatic Setup)
Yeh command automatically MySQL me `student_progression` database banayegi, sare 3NF tables banayegi, check constraints aur indexes lagayegi, analytical views set karegi aur sample records daal degi:
```powershell
python init_db.py
```

### Step 4: Automated Tests Run karo
Verify karo ki sare 12 database constraints, foreign keys, aur features correctly pass ho rahe hain:
```powershell
python -m unittest tests/test_progression_system.py -v
```

### Step 5: Streamlit Web Application Start karo
```powershell
streamlit run app.py
```
App browser me open ho jayegi (`http://localhost:8501`).

---

## 🗄️ 4. Database Schema Structure (3NF Normalized)

Database ka naam: `student_progression`

| Table Name | Description | Key Columns |
|---|---|---|
| `students` | Master student profiles | `student_id` (PK), `roll_number` (UK), `full_name`, `branch`, `admission_year` |
| `school_records` | SSC & HSC pre-university records | `school_record_id` (PK), `student_id` (FK), `qualification_type`, `percentage` |
| `semesters` | Semester SGPA & CGPA progression | `semester_id` (PK), `student_id` (FK), `semester_number`, `sgpa`, `cgpa` |
| `subjects` | Master subject catalog | `subject_id` (PK), `subject_code` (UK), `credits`, `semester_number` |
| `semester_subject_marks` | Subject scores & backlogs | `mark_id` (PK), `semester_id` (FK), `subject_id` (FK), `total_marks`, `result_status` |
| `attendance` | Attendance tracking | `attendance_id` (PK), `student_id` (FK), `subject_id` (FK), `classes_held`, `attended` |
| `academic_gaps` | Formal gap years tracking | `gap_id` (PK), `student_id` (FK), `start_year`, `end_year`, `reason` |
| `portfolio_categories` | Categories master | `category_id` (PK), `category_name` (UK), `category_group` |
| `portfolio_entries` | Certifications, hackathons, projects | `entry_id` (PK), `student_id` (FK), `category_id` (FK), `title`, `organization` |

### Analytical Views:
- `v_student_academic_summary`: Student performance overview.
- `v_backlog_tracker`: Active failed/backlog subjects.
- `v_attendance_warnings`: Students with attendance < 75%.
- `v_semester_progression`: Trendline data for SGPA and CGPA.
- `v_portfolio_summary`: Count of certifications, hackathons, projects per student.

---

## 🔒 5. Configuration & Environment (.env)

`.env` file me MySQL credentials configured hain:
```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=Dhiraj@1507
DB_NAME=student_progression

# Optional Google Sheets Sync
GOOGLE_SHEETS_SYNC=0
GOOGLE_SHEET_ID=
GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
```

---

## ☁️ 6. Google Sheets API Sync Setup (Optional)
1. Google Cloud Console me jaakar naya project banao aur **Google Sheets API** enable karo.
2. Service Account create karke JSON key download karo aur uska naam `service_account.json` rakhkar project root me paste karo.
3. Ek Google Sheet banao aur Service Account ke email address ko **Editor** access share karo.
4. Sheet ka ID copy karke `.env` me `GOOGLE_SHEET_ID` me daalo.
5. App ke "Google Sheets Sync" page par jaakar "Synchronize MySQL Data to Google Sheets Now" button dabao.
*(Note: Agar credentials nahi hain, toh bhi aap har table ko ek click me offline CSV download kar sakte ho!)*

---

## 🎤 7. DBMS Mini-Project Viva Voce Questions & Answers

**Q1: Is project me 3NF normalization kaise achieve ki gayi hai?**
> **Ans**: Har table me atomic values hain (1NF). Kisi bhi table me partial key dependency nahi hai (2NF). Aur subject details (`subjects`), category details (`portfolio_categories`) alag master tables me hain, jisse transitive dependency eliminate ho jati hai (3NF).

**Q2: Attendance warning engine kaise calculate karta hai?**
> **Ans**: Jab `attendance_percentage < 75.0%` hota hai, system view `v_attendance_warnings` trigger hota hai. Shortage recovery formula `CEIL((0.75 * held - attended) / 0.25)` se bata deta hai ki student ko 75% tak pahunchne ke liye agle kitne continuous classes attend karne padenge.

**Q3: Referential Integrity kaise maintain hoti hai?**
> **Ans**: Foreign keys me `ON DELETE CASCADE` rule use kiya gaya hai. Agar koi student delete hota hai, toh uske dependent school records, semester marks, aur attendance automatically safely delete ho jate hain taaki database me koi orphan data na bache.
