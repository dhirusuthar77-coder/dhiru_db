-- ============================================================
-- 02_create_tables.sql
-- Table Definitions in Third Normal Form (3NF)
-- ============================================================

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
    CONSTRAINT fk_school_student FOREIGN KEY(student_id) REFERENCES students(student_id)
      ON DELETE CASCADE
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
    CONSTRAINT fk_semester_student FOREIGN KEY(student_id) REFERENCES students(student_id)
      ON DELETE CASCADE
);

-- 4. Subjects Master Catalog
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(30) NOT NULL UNIQUE,
    subject_name VARCHAR(150) NOT NULL,
    credits INT NOT NULL DEFAULT 4,
    semester_number TINYINT NOT NULL DEFAULT 1,
    subject_type ENUM('Theory','Lab','Both') NOT NULL DEFAULT 'Theory'
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
    CONSTRAINT fk_marks_semester FOREIGN KEY(semester_id) REFERENCES semesters(semester_id)
      ON DELETE CASCADE,
    CONSTRAINT fk_marks_student FOREIGN KEY(student_id) REFERENCES students(student_id)
      ON DELETE CASCADE,
    CONSTRAINT fk_marks_subject FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
      ON DELETE RESTRICT
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
    CONSTRAINT fk_attendance_student FOREIGN KEY(student_id) REFERENCES students(student_id)
      ON DELETE CASCADE,
    CONSTRAINT fk_attendance_subject FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
      ON DELETE RESTRICT,
    CONSTRAINT fk_attendance_semester FOREIGN KEY(semester_id) REFERENCES semesters(semester_id)
      ON DELETE CASCADE
);

-- 7. Academic Gaps Tracker
CREATE TABLE IF NOT EXISTS academic_gaps (
    gap_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    start_year INT NOT NULL,
    end_year INT NOT NULL,
    reason VARCHAR(200) NOT NULL,
    description TEXT NULL,
    CONSTRAINT fk_gap_student FOREIGN KEY(student_id) REFERENCES students(student_id)
      ON DELETE CASCADE
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
    CONSTRAINT fk_portfolio_student FOREIGN KEY(student_id) REFERENCES students(student_id)
      ON DELETE CASCADE,
    CONSTRAINT fk_portfolio_category FOREIGN KEY(category_id) REFERENCES portfolio_categories(category_id)
      ON DELETE RESTRICT
);
