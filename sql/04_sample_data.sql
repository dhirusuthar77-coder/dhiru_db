-- ============================================================
-- 04_sample_data.sql
-- Realistic Demo Records for Students, Academics & Portfolio
-- ============================================================

USE student_progression;

-- 1. Portfolio Categories Master Data
INSERT IGNORE INTO portfolio_categories (category_id, category_name, category_group, activity_type) VALUES
(1, 'Internal Seminar', 'Seminar', 'Internal'),
(2, 'External Seminar', 'Seminar', 'External'),
(3, 'Technical Activity', 'Activity', 'Technical'),
(4, 'Co-curricular Activity', 'Activity', 'Co-curricular'),
(5, 'Extra-curricular Activity', 'Activity', 'Extra-curricular'),
(6, 'Technical Certification', 'Certification', 'Technical'),
(7, 'Capstone Project', 'Project', 'Technical'),
(8, 'National Hackathon', 'Hackathon', 'Technical'),
(9, 'Summer Internship', 'Internship', 'Professional'),
(10, 'Workshop Attendance', 'Seminar', 'Technical');

-- 2. Subjects Master Catalog
INSERT IGNORE INTO subjects (subject_id, subject_code, subject_name, credits, semester_number, subject_type) VALUES
(1, 'CS101', 'Engineering Mathematics I', 4, 1, 'Theory'),
(2, 'CS102', 'Programming in C & Data Structures', 4, 1, 'Both'),
(3, 'CS103', 'Basic Electrical & Electronics', 3, 1, 'Both'),
(4, 'CS201', 'Discrete Mathematics', 4, 2, 'Theory'),
(5, 'CS202', 'Object Oriented Programming with Java', 4, 2, 'Both'),
(6, 'CS203', 'Digital Logic Design', 3, 2, 'Both'),
(7, 'CS301', 'Database Management Systems', 4, 3, 'Both'),
(8, 'CS302', 'Operating Systems', 4, 3, 'Both'),
(9, 'CS303', 'Computer Organization & Architecture', 3, 3, 'Theory'),
(10, 'CS401', 'Design & Analysis of Algorithms', 4, 4, 'Both'),
(11, 'CS402', 'Computer Networks', 4, 4, 'Both'),
(12, 'CS403', 'Software Engineering & Agile', 3, 4, 'Theory');

-- 3. Students
INSERT INTO students (student_id, roll_number, enrollment_no, full_name, email, phone, branch, admission_year, current_status) VALUES
(1, '22CS01', 'EN22CS01', 'Aarav Sharma', 'aarav.sharma@example.edu', '9876543210', 'Computer Engineering', 2022, 'Studying'),
(2, '22CS02', 'EN22CS02', 'Priya Patel', 'priya.patel@example.edu', '9876543211', 'Computer Engineering', 2022, 'Studying'),
(3, '22IT01', 'EN22IT01', 'Rohan Verma', 'rohan.verma@example.edu', '9876543212', 'Information Technology', 2022, 'Studying'),
(4, '21ME01', 'EN21ME01', 'Sneha Kulkarni', 'sneha.k@example.edu', '9876543213', 'Mechanical Engineering', 2021, 'On Hold'),
(5, '22EX01', 'EN22EX01', 'Kabir Joshi', 'kabir.j@example.edu', '9876543214', 'Electronics Engineering', 2022, 'Studying')
ON DUPLICATE KEY UPDATE 
    full_name=VALUES(full_name),
    branch=VALUES(branch),
    current_status=VALUES(current_status);

-- 4. School Records (SSC & HSC)
INSERT INTO school_records (school_record_id, student_id, qualification_type, board_name, school_name, passing_year, obtained_marks, maximum_marks, percentage) VALUES
(1, 1, 'SSC', 'CBSE', 'Delhi Public School', 2020, 460.00, 500.00, 92.00),
(2, 1, 'HSC', 'CBSE', 'Delhi Public School', 2022, 445.00, 500.00, 89.00),
(3, 2, 'SSC', 'Maharashtra State Board', 'St. Xavier High School', 2020, 475.00, 500.00, 95.00),
(4, 2, 'HSC', 'Maharashtra State Board', 'Fergusson Junior College', 2022, 460.00, 500.00, 92.00),
(5, 3, 'SSC', 'ICSE', 'Modern Academy', 2020, 430.00, 500.00, 86.00),
(6, 3, 'HSC', 'CBSE', 'Kendriya Vidyalaya', 2022, 410.00, 500.00, 82.00),
(7, 4, 'SSC', 'CBSE', 'National Public School', 2019, 440.00, 500.00, 88.00),
(8, 4, 'HSC', 'CBSE', 'National Public School', 2021, 420.00, 500.00, 84.00)
ON DUPLICATE KEY UPDATE 
    obtained_marks=VALUES(obtained_marks),
    maximum_marks=VALUES(maximum_marks),
    percentage=VALUES(percentage);

-- 5. Semesters
INSERT INTO semesters (semester_id, student_id, semester_number, academic_year, sgpa, cgpa, result_status, result_date, gap_note) VALUES
(1, 1, 1, '2022-23', 8.40, 8.40, 'Completed', '2023-01-15', NULL),
(2, 1, 2, '2022-23', 8.70, 8.55, 'Completed', '2023-06-20', NULL),
(3, 1, 3, '2023-24', 8.90, 8.67, 'Completed', '2024-01-18', NULL),
(4, 1, 4, '2023-24', 9.10, 8.78, 'Completed', '2024-06-25', NULL),
(5, 2, 1, '2022-23', 9.20, 9.20, 'Completed', '2023-01-15', NULL),
(6, 2, 2, '2022-23', 9.40, 9.30, 'Completed', '2023-06-20', NULL),
(7, 2, 3, '2023-24', 9.50, 9.37, 'Completed', '2024-01-18', NULL),
(8, 3, 1, '2022-23', 7.20, 7.20, 'Completed', '2023-01-15', NULL),
(9, 3, 2, '2022-23', 6.80, 7.00, 'Backlog', '2023-06-20', 'Failed in CS201 Discrete Mathematics'),
(10, 3, 3, '2023-24', 7.50, 7.17, 'Completed', '2024-01-18', NULL),
(11, 4, 1, '2021-22', 8.00, 8.00, 'Completed', '2022-01-15', NULL),
(12, 4, 2, '2021-22', 7.80, 7.90, 'Completed', '2022-06-20', NULL),
(13, 4, 3, '2023-24', 0.00, 7.90, 'Gap', '2024-01-18', 'Medical Leave for recovery')
ON DUPLICATE KEY UPDATE 
    sgpa=VALUES(sgpa),
    cgpa=VALUES(cgpa),
    result_status=VALUES(result_status),
    gap_note=VALUES(gap_note);

-- 6. Subject Results & Marks
INSERT INTO semester_subject_marks (mark_id, semester_id, student_id, subject_id, internal_marks, external_marks, total_marks, theory_max_marks, lab_max_marks, grade, result_status) VALUES
(1, 1, 1, 1, 26.00, 68.00, 94.00, 100.00, 30.00, 'O', 'Cleared'),
(2, 1, 1, 2, 28.00, 62.00, 90.00, 100.00, 30.00, 'O', 'Cleared'),
(3, 1, 1, 3, 24.00, 58.00, 82.00, 100.00, 30.00, 'A+', 'Cleared'),
(4, 3, 1, 7, 28.00, 66.00, 94.00, 100.00, 30.00, 'O', 'Cleared'),
(5, 3, 1, 8, 25.00, 60.00, 85.00, 100.00, 30.00, 'A+', 'Cleared'),
(6, 3, 1, 9, 22.00, 55.00, 77.00, 100.00, 30.00, 'A', 'Cleared'),
(7, 8, 3, 1, 20.00, 48.00, 68.00, 100.00, 30.00, 'B+', 'Cleared'),
(8, 9, 3, 4, 12.00, 24.00, 36.00, 100.00, 30.00, 'F', 'Failed')
ON DUPLICATE KEY UPDATE 
    internal_marks=VALUES(internal_marks),
    external_marks=VALUES(external_marks),
    total_marks=VALUES(total_marks),
    grade=VALUES(grade),
    result_status=VALUES(result_status);

-- 7. Attendance Records
INSERT INTO attendance (attendance_id, student_id, subject_id, semester_id, classes_held, classes_attended, attendance_percentage) VALUES
(1, 1, 7, 3, 45, 42, 93.33),
(2, 1, 8, 3, 40, 37, 92.50),
(3, 1, 9, 3, 35, 32, 91.43),
(4, 3, 4, 2, 40, 24, 60.00), -- Warning: Below 75%
(5, 3, 5, 2, 44, 31, 70.45), -- Warning: Below 75%
(6, 2, 7, 3, 45, 44, 97.78),
(7, 5, 1, 1, 40, 36, 90.00)
ON DUPLICATE KEY UPDATE 
    classes_held=VALUES(classes_held),
    classes_attended=VALUES(classes_attended),
    attendance_percentage=VALUES(attendance_percentage);

-- 8. Academic Gaps Tracker
INSERT INTO academic_gaps (gap_id, student_id, start_year, end_year, reason, description) VALUES
(1, 4, 2022, 2023, 'Medical Leave', 'Student was recovering from a severe medical condition during AY 2022-2023. Official clearance submitted.')
ON DUPLICATE KEY UPDATE 
    reason=VALUES(reason),
    description=VALUES(description);

-- 9. Portfolio Entries
INSERT INTO portfolio_entries (entry_id, student_id, category_id, title, organization, entry_date, description, certificate_url) VALUES
(1, 1, 6, 'AWS Certified Cloud Practitioner', 'Amazon Web Services', '2023-08-10', 'Validation of cloud fundamentals and security architectural principles.', 'https://aws.amazon.com/verification/CLD-102938'),
(2, 1, 8, 'Smart India Hackathon Finalist', 'Ministry of Education', '2023-11-20', 'Built an AI-driven smart classroom attendance system using computer vision.', 'https://sih.gov.in/certificate/SIH23-AARAV'),
(3, 1, 7, 'Automated Student Progression Portal', 'College Innovation Cell', '2024-04-12', 'Full-stack DBMS mini-project with interactive Streamlit GUI and MySQL backend.', NULL),
(4, 2, 9, 'Software Engineering Intern', 'Infosys Springboard', '2023-07-30', 'Developed backend microservices with Python and REST APIs.', 'https://infosys.com/springboard/cert/PP-990'),
(5, 2, 6, 'Oracle Certified Associate MySQL 8.0', 'Oracle University', '2024-02-14', 'Demonstrated mastery of SQL indexing, query optimization, and schema design.', 'https://oracle.com/certs/OCA-8821'),
(6, 3, 10, 'Git & GitHub Hands-on Workshop', 'IEEE Student Branch', '2023-03-05', 'Version control fundamentals, branching strategies, and open-source contribution.', NULL)
ON DUPLICATE KEY UPDATE 
    title=VALUES(title),
    organization=VALUES(organization),
    description=VALUES(description);
