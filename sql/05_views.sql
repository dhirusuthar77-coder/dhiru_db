-- ============================================================
-- 05_views.sql
-- Analytical Database Views for Academic Progression & Reporting
-- ============================================================

USE student_progression;

-- 1. Student Academic Summary View
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

-- 2. Backlog Tracking View
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

-- 3. Attendance Warnings View (<75% Threshold)
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

-- 4. Semester Progression View
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

-- 5. Portfolio Summary View
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

-- 6. Alias Views for Legacy & Dual Name Compatibility
CREATE OR REPLACE VIEW subject_results AS
SELECT 
    mark_id AS result_id,
    student_id,
    semester_id,
    subject_id,
    internal_marks,
    external_marks,
    total_marks,
    grade,
    result_status
FROM semester_subject_marks;

CREATE OR REPLACE VIEW achievements AS
SELECT 
    entry_id AS achievement_id,
    student_id,
    category_id,
    title,
    organization AS issuing_organization,
    entry_date AS issue_date,
    certificate_url,
    description
FROM portfolio_entries;
