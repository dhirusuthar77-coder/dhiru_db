-- ============================================================
-- Student Academic Progression & Portfolio Management System
-- Consolidated Complete Schema (MySQL 8.0+)
-- Third Normal Form (3NF) with Constraints, Indexes, Views & Demo Data
-- ============================================================

CREATE DATABASE IF NOT EXISTS student_progression
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE student_progression;

-- 1. Students Master Table
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    roll_number VARCHAR(30) NOT NULL UNIQUE,
    enrollment_no VARCHAR(30) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NULL UNIQUE,
    phone VARCHAR(30) NULL,
    branch VARCHAR(60) NOT NULL DEFAULT 'Computer Engineering',
    admission_year INT NOT NULL DEFAULT 2022,
    date_of_birth DATE NULL,
    current_status ENUM('Studying','Graduated','Dropped','On Hold') NOT NULL DEFAULT 'Studying',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. School Records (SSC & HSC)
CREATE TABLE IF NOT EXISTS school_records (
    school_record_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    qualification_type ENUM('SSC','HSC') NOT NULL,
    level VARCHAR(30) GENERATED ALWAYS AS (CASE WHEN qualification_type='SSC' THEN 'Secondary' ELSE 'Higher Secondary' END) VIRTUAL,
    board_name VARCHAR(100) NULL,
    school_name VARCHAR(150) NULL,
    passing_year YEAR NULL,
    obtained_marks DECIMAL(7,2) NULL,
    maximum_marks DECIMAL(7,2) NULL,
    marks_obtained DECIMAL(7,2) GENERATED ALWAYS AS (obtained_marks) VIRTUAL,
    total_marks DECIMAL(7,2) GENERATED ALWAYS AS (maximum_marks) VIRTUAL,
    percentage DECIMAL(5,2) NULL,
    CONSTRAINT uq_student_qualification UNIQUE(student_id, qualification_type),
    CONSTRAINT fk_school_student FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT chk_school_obtained CHECK (obtained_marks IS NULL OR obtained_marks >= 0),
    CONSTRAINT chk_school_max CHECK (maximum_marks IS NULL OR maximum_marks > 0),
    CONSTRAINT chk_school_percentage CHECK (percentage IS NULL OR (percentage >= 0 AND percentage <= 100))
);

-- 3. Semesters Summary
CREATE TABLE IF NOT EXISTS semesters (
    semester_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    semester_number TINYINT NOT NULL,
    semester_no TINYINT GENERATED ALWAYS AS (semester_number) VIRTUAL,
    academic_year VARCHAR(20) NULL,
    sgpa DECIMAL(4,2) NULL,
    cgpa DECIMAL(4,2) NULL,
    result_status ENUM('Completed','Current','Backlog','Gap') NOT NULL DEFAULT 'Completed',
    status ENUM('Completed','Current','Backlog','Gap') GENERATED ALWAYS AS (result_status) VIRTUAL,
    result_date DATE NULL,
    gap_note VARCHAR(255) NULL,
    CONSTRAINT uq_student_semester UNIQUE(student_id, semester_number),
    CONSTRAINT fk_semester_student FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT chk_semester_number CHECK (semester_number BETWEEN 1 AND 12),
    CONSTRAINT chk_sgpa CHECK (sgpa IS NULL OR (sgpa >= 0.0 AND sgpa <= 10.0)),
    CONSTRAINT chk_cgpa CHECK (cgpa IS NULL OR (cgpa >= 0.0 AND cgpa <= 10.0))
);

-- 4. Subjects Master Catalog
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(30) NOT NULL UNIQUE,
    subject_name VARCHAR(150) NOT NULL,
    credits INT NOT NULL DEFAULT 4,
    semester_number TINYINT NOT NULL DEFAULT 1,
    subject_type ENUM('Theory','Lab','Both') NOT NULL DEFAULT 'Theory',
    CONSTRAINT chk_subject_credits CHECK (credits > 0),
    CONSTRAINT chk_subject_semester CHECK (semester_number BETWEEN 1 AND 12)
);

-- 5. Subject Results & Marks
CREATE TABLE IF NOT EXISTS semester_subject_marks (
    mark_id INT AUTO_INCREMENT PRIMARY KEY,
    semester_id INT NOT NULL,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    internal_marks DECIMAL(6,2) NULL DEFAULT 0.0,
    external_marks DECIMAL(6,2) NULL DEFAULT 0.0,
    total_marks DECIMAL(6,2) NULL DEFAULT 0.0,
    theory_marks DECIMAL(6,2) GENERATED ALWAYS AS (external_marks) VIRTUAL,
    theory_max_marks DECIMAL(6,2) NULL DEFAULT 100.0,
    lab_marks DECIMAL(6,2) GENERATED ALWAYS AS (internal_marks) VIRTUAL,
    lab_max_marks DECIMAL(6,2) NULL DEFAULT 50.0,
    grade VARCHAR(5) NULL,
    result_status ENUM('Cleared','Failed','Backlog') NOT NULL DEFAULT 'Cleared',
    CONSTRAINT uq_semester_subject UNIQUE(semester_id, subject_id),
    CONSTRAINT fk_marks_semester FOREIGN KEY(semester_id) REFERENCES semesters(semester_id) ON DELETE CASCADE,
    CONSTRAINT fk_marks_student FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_marks_subject FOREIGN KEY(subject_id) REFERENCES subjects(subject_id) ON DELETE RESTRICT,
    CONSTRAINT chk_internal_marks CHECK (internal_marks IS NULL OR internal_marks >= 0),
    CONSTRAINT chk_external_marks CHECK (external_marks IS NULL OR external_marks >= 0),
    CONSTRAINT chk_total_marks CHECK (total_marks IS NULL OR total_marks >= 0)
);

-- 6. Subject Attendance
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    semester_id INT NOT NULL,
    classes_held INT NOT NULL DEFAULT 0,
    classes_attended INT NOT NULL DEFAULT 0,
    attendance_percentage DECIMAL(5,2) NULL,
    CONSTRAINT uq_attendance_entry UNIQUE(student_id, semester_id, subject_id),
    CONSTRAINT fk_attendance_student FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_attendance_subject FOREIGN KEY(subject_id) REFERENCES subjects(subject_id) ON DELETE RESTRICT,
    CONSTRAINT fk_attendance_semester FOREIGN KEY(semester_id) REFERENCES semesters(semester_id) ON DELETE CASCADE,
    CONSTRAINT chk_classes_held CHECK (classes_held >= 0),
    CONSTRAINT chk_classes_attended CHECK (classes_attended >= 0),
    CONSTRAINT chk_attendance_valid CHECK (classes_attended <= classes_held),
    CONSTRAINT chk_attendance_pct CHECK (attendance_percentage IS NULL OR (attendance_percentage >= 0 AND attendance_percentage <= 100))
);

-- 7. Academic Gaps Tracker
CREATE TABLE IF NOT EXISTS academic_gaps (
    gap_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    start_year INT NOT NULL,
    end_year INT NOT NULL,
    reason VARCHAR(200) NOT NULL,
    description TEXT NULL,
    CONSTRAINT fk_gap_student FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT chk_gap_years CHECK (start_year <= end_year)
);

-- 8. Portfolio Categories Master
CREATE TABLE IF NOT EXISTS portfolio_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(60) NOT NULL UNIQUE,
    category_group ENUM('Seminar','Activity','Certification','Project','Hackathon','Internship','Other') NOT NULL,
    activity_type VARCHAR(50) NULL
);

-- 9. Portfolio Entries & Student Achievements
CREATE TABLE IF NOT EXISTS portfolio_entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    category_id INT NOT NULL,
    title VARCHAR(180) NOT NULL,
    organization VARCHAR(180) NULL,
    entry_date DATE NULL,
    description TEXT NULL,
    certificate_url VARCHAR(500) NULL,
    CONSTRAINT fk_portfolio_student FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_portfolio_category FOREIGN KEY(category_id) REFERENCES portfolio_categories(category_id) ON DELETE RESTRICT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_students_name ON students(full_name);
CREATE INDEX IF NOT EXISTS idx_students_branch ON students(branch);
CREATE INDEX IF NOT EXISTS idx_students_admission ON students(admission_year);
CREATE INDEX IF NOT EXISTS idx_semesters_student_no ON semesters(student_id, semester_number);
CREATE INDEX IF NOT EXISTS idx_marks_student ON semester_subject_marks(student_id);
CREATE INDEX IF NOT EXISTS idx_marks_status ON semester_subject_marks(result_status);
CREATE INDEX IF NOT EXISTS idx_attendance_student_sem ON attendance(student_id, semester_id);
CREATE INDEX IF NOT EXISTS idx_portfolio_student ON portfolio_entries(student_id);
CREATE INDEX IF NOT EXISTS idx_portfolio_category ON portfolio_entries(category_id);

-- Views
CREATE OR REPLACE VIEW v_student_academic_summary AS
SELECT 
    s.student_id,
    s.roll_number,
    s.enrollment_no,
    s.full_name,
    s.branch,
    s.admission_year,
    s.current_status,
    COUNT(DISTINCT sem.semester_id) AS total_semesters_recorded,
    MAX(sem.cgpa) AS latest_cgpa,
    COALESCE(SUM(CASE WHEN m.result_status IN ('Failed','Backlog') THEN 1 ELSE 0 END), 0) AS total_backlogs_count,
    ROUND(AVG(att.attendance_percentage), 2) AS average_attendance_pct,
    COUNT(DISTINCT p.entry_id) AS total_portfolio_achievements
FROM students s
LEFT JOIN semesters sem ON s.student_id = sem.student_id
LEFT JOIN semester_subject_marks m ON s.student_id = m.student_id
LEFT JOIN attendance att ON s.student_id = att.student_id
LEFT JOIN portfolio_entries p ON s.student_id = p.student_id
GROUP BY s.student_id, s.roll_number, s.enrollment_no, s.full_name, s.branch, s.admission_year, s.current_status;

CREATE OR REPLACE VIEW v_backlog_tracker AS
SELECT 
    s.student_id,
    s.roll_number,
    s.full_name,
    s.branch,
    sem.semester_number,
    sub.subject_code,
    sub.subject_name,
    sub.credits,
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

CREATE OR REPLACE VIEW v_attendance_warnings AS
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
    ROUND(75.0 - att.attendance_percentage, 2) AS shortage_percentage,
    CEIL((0.75 * att.classes_held - att.classes_attended) / 0.25) AS classes_needed_for_75
FROM attendance att
JOIN students s ON s.student_id = att.student_id
JOIN semesters sem ON sem.semester_id = att.semester_id
JOIN subjects sub ON sub.subject_id = att.subject_id
WHERE att.attendance_percentage < 75.00;

CREATE OR REPLACE VIEW v_semester_progression AS
SELECT 
    s.student_id,
    s.roll_number,
    s.full_name,
    s.branch,
    sem.semester_number,
    sem.academic_year,
    sem.sgpa,
    sem.cgpa,
    sem.result_status,
    sem.gap_note
FROM semesters sem
JOIN students s ON s.student_id = sem.student_id
ORDER BY s.student_id, sem.semester_number;

CREATE OR REPLACE VIEW v_portfolio_summary AS
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
    COUNT(CASE WHEN c.category_group = 'Activity' THEN 1 END) AS activities_count,
    COUNT(p.entry_id) AS total_entries
FROM students s
LEFT JOIN portfolio_entries p ON s.student_id = p.student_id
LEFT JOIN portfolio_categories c ON c.category_id = p.category_id
GROUP BY s.student_id, s.roll_number, s.full_name, s.branch;

CREATE OR REPLACE VIEW subject_results AS
SELECT mark_id AS result_id, student_id, semester_id, subject_id, internal_marks, external_marks, total_marks, grade, result_status
FROM semester_subject_marks;

CREATE OR REPLACE VIEW achievements AS
SELECT entry_id AS achievement_id, student_id, category_id, title, organization AS issuing_organization, entry_date AS issue_date, certificate_url, description
FROM portfolio_entries;
