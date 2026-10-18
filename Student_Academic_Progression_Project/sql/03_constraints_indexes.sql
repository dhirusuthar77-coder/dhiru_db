-- ============================================================
-- 03_constraints_indexes.sql
-- Check Constraints, Indexes and Referential Safeguards
-- ============================================================

USE student_progression;

-- School Records Constraints
ALTER TABLE school_records
    ADD CONSTRAINT chk_school_obtained CHECK (obtained_marks IS NULL OR obtained_marks >= 0),
    ADD CONSTRAINT chk_school_max CHECK (maximum_marks IS NULL OR maximum_marks > 0),
    ADD CONSTRAINT chk_school_percentage CHECK (percentage IS NULL OR (percentage >= 0 AND percentage <= 100));

-- Semesters Constraints
ALTER TABLE semesters
    ADD CONSTRAINT chk_semester_number CHECK (semester_number BETWEEN 1 AND 12),
    ADD CONSTRAINT chk_sgpa CHECK (sgpa IS NULL OR (sgpa >= 0.0 AND sgpa <= 10.0)),
    ADD CONSTRAINT chk_cgpa CHECK (cgpa IS NULL OR (cgpa >= 0.0 AND cgpa <= 10.0));

-- Subjects Constraints
ALTER TABLE subjects
    ADD CONSTRAINT chk_subject_credits CHECK (credits > 0),
    ADD CONSTRAINT chk_subject_semester CHECK (semester_number BETWEEN 1 AND 12);

-- Subject Marks Constraints
ALTER TABLE semester_subject_marks
    ADD CONSTRAINT chk_internal_marks CHECK (internal_marks IS NULL OR internal_marks >= 0),
    ADD CONSTRAINT chk_external_marks CHECK (external_marks IS NULL OR external_marks >= 0),
    ADD CONSTRAINT chk_total_marks CHECK (total_marks IS NULL OR total_marks >= 0);

-- Attendance Constraints
ALTER TABLE attendance
    ADD CONSTRAINT chk_classes_held CHECK (classes_held >= 0),
    ADD CONSTRAINT chk_classes_attended CHECK (classes_attended >= 0),
    ADD CONSTRAINT chk_attendance_valid CHECK (classes_attended <= classes_held),
    ADD CONSTRAINT chk_attendance_pct CHECK (attendance_percentage IS NULL OR (attendance_percentage >= 0 AND attendance_percentage <= 100));

-- Academic Gaps Constraints
ALTER TABLE academic_gaps
    ADD CONSTRAINT chk_gap_years CHECK (start_year <= end_year);

-- Performance Indexes
CREATE INDEX idx_students_name ON students(full_name);
CREATE INDEX idx_students_branch ON students(branch);
CREATE INDEX idx_students_admission ON students(admission_year);
CREATE INDEX idx_semesters_student_no ON semesters(student_id, semester_number);
CREATE INDEX idx_marks_student ON semester_subject_marks(student_id);
CREATE INDEX idx_marks_status ON semester_subject_marks(result_status);
CREATE INDEX idx_attendance_student_sem ON attendance(student_id, semester_id);
CREATE INDEX idx_portfolio_student ON portfolio_entries(student_id);
CREATE INDEX idx_portfolio_category ON portfolio_entries(category_id);
