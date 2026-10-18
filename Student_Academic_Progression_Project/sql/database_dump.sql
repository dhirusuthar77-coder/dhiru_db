-- ============================================================
-- STUDENT ACADEMIC PROGRESSION & PORTFOLIO MANAGEMENT SYSTEM
-- Complete Relational Database File (MySQL 8.0+)
-- Database: `student_progression`
-- Generated with full 3NF schemas, constraints, indexes & data
-- ============================================================

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `student_progression` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

USE `student_progression`;

--
-- Table structure for table `portfolio_categories`
--

DROP TABLE IF EXISTS `portfolio_categories`;
CREATE TABLE `portfolio_categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category_group` enum('Seminar','Activity','Certification','Project','Hackathon','Internship','Other') COLLATE utf8mb4_unicode_ci NOT NULL,
  `activity_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `portfolio_categories`
--

LOCK TABLES `portfolio_categories` WRITE;
/*!40000 ALTER TABLE `portfolio_categories` DISABLE KEYS */;
INSERT INTO `portfolio_categories` (`category_id`, `category_name`, `category_group`, `activity_type`) VALUES
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
/*!40000 ALTER TABLE `portfolio_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `roll_number` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `enrollment_no` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `branch` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Computer Engineering',
  `admission_year` int NOT NULL DEFAULT '2022',
  `date_of_birth` date DEFAULT NULL,
  `current_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Active',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `roll_number` (`roll_number`),
  UNIQUE KEY `enrollment_no` (`enrollment_no`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_students_name` (`full_name`),
  KEY `idx_students_branch` (`branch`),
  KEY `idx_students_admission` (`admission_year`)
) ENGINE=InnoDB AUTO_INCREMENT=689 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` (`student_id`, `roll_number`, `enrollment_no`, `full_name`, `email`, `phone`, `branch`, `admission_year`, `date_of_birth`, `current_status`, `created_at`) VALUES
  (1, '22CS01', 'EN22CS01', 'Aarav Sharma', 'aarav.sharma@example.edu', '9876543210', 'Computer Engineering', 2022, NULL, 'Studying', '2026-10-18 20:36:16'),
  (2, '22CS02', 'EN22CS02', 'Priya Patel', 'priya.patel@example.edu', '9876543211', 'Computer Engineering', 2022, NULL, 'Studying', '2026-10-18 20:36:16'),
  (3, '22IT01', 'EN22IT01', 'Rohan Verma', 'rohan.verma@example.edu', '9876543212', 'Information Technology', 2022, NULL, 'Studying', '2026-10-18 20:36:16'),
  (4, '21ME01', 'EN21ME01', 'Sneha Kulkarni', 'sneha.k@example.edu', '9876543213', 'Mechanical Engineering', 2021, NULL, 'On Hold', '2026-10-18 20:36:16'),
  (5, '22EX01', 'EN22EX01', 'Kabir Joshi', 'kabir.j@example.edu', '9876543214', 'Electronics Engineering', 2022, NULL, 'Studying', '2026-10-18 20:36:16'),
  (688, '23FC003', 'EN23FC003', 'Arjun Reddy', 'arjun.reddy@viva-technology.org', '9801437836', 'Electronics & Telecommunication Engineering', 2023, NULL, 'Active', '2026-10-18 21:45:02');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_records`
--

DROP TABLE IF EXISTS `school_records`;
CREATE TABLE `school_records` (
  `school_record_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `qualification_type` enum('SSC','HSC') COLLATE utf8mb4_unicode_ci NOT NULL,
  `level` varchar(30) COLLATE utf8mb4_unicode_ci GENERATED ALWAYS AS ((case when (`qualification_type` = _utf8mb4'SSC') then _utf8mb4'Secondary' else _utf8mb4'Higher Secondary' end)) VIRTUAL,
  `board_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `school_name` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `passing_year` year DEFAULT NULL,
  `obtained_marks` decimal(7,2) DEFAULT NULL,
  `maximum_marks` decimal(7,2) DEFAULT NULL,
  `marks_obtained` decimal(7,2) GENERATED ALWAYS AS (`obtained_marks`) VIRTUAL,
  `total_marks` decimal(7,2) GENERATED ALWAYS AS (`maximum_marks`) VIRTUAL,
  `percentage` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`school_record_id`),
  UNIQUE KEY `uq_student_qualification` (`student_id`,`qualification_type`),
  CONSTRAINT `fk_school_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `chk_school_max` CHECK (((`maximum_marks` is null) or (`maximum_marks` > 0))),
  CONSTRAINT `chk_school_obtained` CHECK (((`obtained_marks` is null) or (`obtained_marks` >= 0))),
  CONSTRAINT `chk_school_percentage` CHECK (((`percentage` is null) or ((`percentage` >= 0) and (`percentage` <= 100))))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `school_records`
--

LOCK TABLES `school_records` WRITE;
/*!40000 ALTER TABLE `school_records` DISABLE KEYS */;
INSERT INTO `school_records` (`school_record_id`, `student_id`, `qualification_type`, `board_name`, `school_name`, `passing_year`, `obtained_marks`, `maximum_marks`, `percentage`) VALUES
  (1, 1, 'SSC', 'CBSE', 'Delhi Public School', 2020, 460.00, 500.00, 92.00),
  (2, 1, 'HSC', 'CBSE', 'Delhi Public School', 2022, 445.00, 500.00, 89.00),
  (3, 2, 'SSC', 'Maharashtra State Board', 'St. Xavier High School', 2020, 475.00, 500.00, 95.00),
  (4, 2, 'HSC', 'Maharashtra State Board', 'Fergusson Junior College', 2022, 460.00, 500.00, 92.00),
  (5, 3, 'SSC', 'ICSE', 'Modern Academy', 2020, 430.00, 500.00, 86.00),
  (6, 3, 'HSC', 'CBSE', 'Kendriya Vidyalaya', 2022, 410.00, 500.00, 82.00),
  (7, 4, 'SSC', 'CBSE', 'National Public School', 2019, 440.00, 500.00, 88.00),
  (8, 4, 'HSC', 'CBSE', 'National Public School', 2021, 420.00, 500.00, 84.00),
  (9, 688, 'SSC', 'Maharashtra State Board', 'St. Aloysius High School', 2021, 465.00, 500.00, 93.00),
  (10, 688, 'HSC', 'Maharashtra State Board', 'VIVA College of Arts, Commerce & Science', 2023, 440.00, 500.00, 88.00);
/*!40000 ALTER TABLE `school_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semesters`
--

DROP TABLE IF EXISTS `semesters`;
CREATE TABLE `semesters` (
  `semester_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `semester_number` tinyint NOT NULL,
  `semester_no` tinyint GENERATED ALWAYS AS (`semester_number`) VIRTUAL,
  `academic_year` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sgpa` decimal(4,2) DEFAULT NULL,
  `cgpa` decimal(4,2) DEFAULT NULL,
  `result_status` enum('Completed','Current','Backlog','Gap') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Completed',
  `status` enum('Completed','Current','Backlog','Gap') COLLATE utf8mb4_unicode_ci GENERATED ALWAYS AS (`result_status`) VIRTUAL,
  `result_date` date DEFAULT NULL,
  `gap_note` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`semester_id`),
  UNIQUE KEY `uq_student_semester` (`student_id`,`semester_number`),
  KEY `idx_semesters_student_no` (`student_id`,`semester_number`),
  CONSTRAINT `fk_semester_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `chk_cgpa` CHECK (((`cgpa` is null) or ((`cgpa` >= 0.0) and (`cgpa` <= 10.0)))),
  CONSTRAINT `chk_semester_number` CHECK ((`semester_number` between 1 and 12)),
  CONSTRAINT `chk_sgpa` CHECK (((`sgpa` is null) or ((`sgpa` >= 0.0) and (`sgpa` <= 10.0))))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `semesters`
--

LOCK TABLES `semesters` WRITE;
/*!40000 ALTER TABLE `semesters` DISABLE KEYS */;
INSERT INTO `semesters` (`semester_id`, `student_id`, `semester_number`, `academic_year`, `sgpa`, `cgpa`, `result_status`, `result_date`, `gap_note`) VALUES
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
  (13, 4, 3, '2023-24', 0.00, 7.90, 'Gap', '2024-01-18', 'Medical Leave for recovery'),
  (14, 688, 1, '2023-2024', 8.80, 8.80, 'Completed', NULL, NULL),
  (15, 688, 2, '2023-2024', 9.05, 8.93, 'Completed', NULL, NULL);
/*!40000 ALTER TABLE `semesters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
CREATE TABLE `subjects` (
  `subject_id` int NOT NULL AUTO_INCREMENT,
  `subject_code` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subject_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `credits` int NOT NULL DEFAULT '4',
  `semester_number` tinyint NOT NULL DEFAULT '1',
  `subject_type` enum('Theory','Lab','Both') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Theory',
  PRIMARY KEY (`subject_id`),
  UNIQUE KEY `subject_code` (`subject_code`),
  CONSTRAINT `chk_subject_credits` CHECK ((`credits` > 0)),
  CONSTRAINT `chk_subject_semester` CHECK ((`semester_number` between 1 and 12))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `subjects`
--

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;
INSERT INTO `subjects` (`subject_id`, `subject_code`, `subject_name`, `credits`, `semester_number`, `subject_type`) VALUES
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
/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester_subject_marks`
--

DROP TABLE IF EXISTS `semester_subject_marks`;
CREATE TABLE `semester_subject_marks` (
  `mark_id` int NOT NULL AUTO_INCREMENT,
  `semester_id` int NOT NULL,
  `student_id` int NOT NULL,
  `subject_id` int NOT NULL,
  `internal_marks` decimal(6,2) DEFAULT '0.00',
  `external_marks` decimal(6,2) DEFAULT '0.00',
  `total_marks` decimal(6,2) DEFAULT '0.00',
  `theory_marks` decimal(6,2) GENERATED ALWAYS AS (`external_marks`) VIRTUAL,
  `theory_max_marks` decimal(6,2) DEFAULT '100.00',
  `lab_marks` decimal(6,2) GENERATED ALWAYS AS (`internal_marks`) VIRTUAL,
  `lab_max_marks` decimal(6,2) DEFAULT '50.00',
  `grade` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `result_status` enum('Cleared','Failed','Backlog') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Cleared',
  PRIMARY KEY (`mark_id`),
  UNIQUE KEY `uq_semester_subject` (`semester_id`,`subject_id`),
  KEY `fk_marks_subject` (`subject_id`),
  KEY `idx_marks_student` (`student_id`),
  KEY `idx_marks_status` (`result_status`),
  CONSTRAINT `fk_marks_semester` FOREIGN KEY (`semester_id`) REFERENCES `semesters` (`semester_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_marks_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_marks_subject` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`) ON DELETE RESTRICT,
  CONSTRAINT `chk_external_marks` CHECK (((`external_marks` is null) or (`external_marks` >= 0))),
  CONSTRAINT `chk_internal_marks` CHECK (((`internal_marks` is null) or (`internal_marks` >= 0))),
  CONSTRAINT `chk_total_marks` CHECK (((`total_marks` is null) or (`total_marks` >= 0)))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `semester_subject_marks`
--

LOCK TABLES `semester_subject_marks` WRITE;
/*!40000 ALTER TABLE `semester_subject_marks` DISABLE KEYS */;
INSERT INTO `semester_subject_marks` (`mark_id`, `semester_id`, `student_id`, `subject_id`, `internal_marks`, `external_marks`, `total_marks`, `theory_max_marks`, `lab_max_marks`, `grade`, `result_status`) VALUES
  (1, 1, 1, 1, 26.00, 68.00, 94.00, 100.00, 30.00, 'O', 'Cleared'),
  (2, 1, 1, 2, 28.00, 62.00, 90.00, 100.00, 30.00, 'O', 'Cleared'),
  (3, 1, 1, 3, 24.00, 58.00, 82.00, 100.00, 30.00, 'A+', 'Cleared'),
  (4, 3, 1, 7, 28.00, 66.00, 94.00, 100.00, 30.00, 'O', 'Cleared'),
  (5, 3, 1, 8, 25.00, 60.00, 85.00, 100.00, 30.00, 'A+', 'Cleared'),
  (6, 3, 1, 9, 22.00, 55.00, 77.00, 100.00, 30.00, 'A', 'Cleared'),
  (7, 8, 3, 1, 20.00, 48.00, 68.00, 100.00, 30.00, 'B+', 'Cleared'),
  (8, 9, 3, 4, 12.00, 24.00, 36.00, 100.00, 30.00, 'F', 'Failed');
/*!40000 ALTER TABLE `semester_subject_marks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
CREATE TABLE `attendance` (
  `attendance_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `subject_id` int NOT NULL,
  `semester_id` int NOT NULL,
  `classes_held` int NOT NULL DEFAULT '0',
  `classes_attended` int NOT NULL DEFAULT '0',
  `attendance_percentage` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`attendance_id`),
  UNIQUE KEY `uq_attendance_entry` (`student_id`,`semester_id`,`subject_id`),
  KEY `fk_attendance_subject` (`subject_id`),
  KEY `fk_attendance_semester` (`semester_id`),
  KEY `idx_attendance_student_sem` (`student_id`,`semester_id`),
  CONSTRAINT `fk_attendance_semester` FOREIGN KEY (`semester_id`) REFERENCES `semesters` (`semester_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_attendance_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_attendance_subject` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`) ON DELETE RESTRICT,
  CONSTRAINT `chk_attendance_pct` CHECK (((`attendance_percentage` is null) or ((`attendance_percentage` >= 0) and (`attendance_percentage` <= 100)))),
  CONSTRAINT `chk_attendance_valid` CHECK ((`classes_attended` <= `classes_held`)),
  CONSTRAINT `chk_classes_attended` CHECK ((`classes_attended` >= 0)),
  CONSTRAINT `chk_classes_held` CHECK ((`classes_held` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` (`attendance_id`, `student_id`, `subject_id`, `semester_id`, `classes_held`, `classes_attended`, `attendance_percentage`) VALUES
  (1, 1, 7, 3, 45, 42, 93.33),
  (2, 1, 8, 3, 40, 37, 92.50),
  (3, 1, 9, 3, 35, 32, 91.43),
  (4, 3, 4, 2, 40, 24, 60.00),
  (5, 3, 5, 2, 44, 31, 70.45),
  (6, 2, 7, 3, 45, 44, 97.78),
  (7, 5, 1, 1, 40, 36, 90.00);
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academic_gaps`
--

DROP TABLE IF EXISTS `academic_gaps`;
CREATE TABLE `academic_gaps` (
  `gap_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `start_year` int NOT NULL,
  `end_year` int NOT NULL,
  `reason` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`gap_id`),
  KEY `fk_gap_student` (`student_id`),
  CONSTRAINT `fk_gap_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `chk_gap_years` CHECK ((`start_year` <= `end_year`))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `academic_gaps`
--

LOCK TABLES `academic_gaps` WRITE;
/*!40000 ALTER TABLE `academic_gaps` DISABLE KEYS */;
INSERT INTO `academic_gaps` (`gap_id`, `student_id`, `start_year`, `end_year`, `reason`, `description`) VALUES
  (1, 4, 2022, 2023, 'Medical Leave', 'Student was recovering from a severe medical condition during AY 2022-2023. Official clearance submitted.');
/*!40000 ALTER TABLE `academic_gaps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `portfolio_entries`
--

DROP TABLE IF EXISTS `portfolio_entries`;
CREATE TABLE `portfolio_entries` (
  `entry_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `category_id` int NOT NULL,
  `title` varchar(180) COLLATE utf8mb4_unicode_ci NOT NULL,
  `organization` varchar(180) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `entry_date` date DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `certificate_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`entry_id`),
  KEY `idx_portfolio_student` (`student_id`),
  KEY `idx_portfolio_category` (`category_id`),
  CONSTRAINT `fk_portfolio_category` FOREIGN KEY (`category_id`) REFERENCES `portfolio_categories` (`category_id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_portfolio_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `portfolio_entries`
--

LOCK TABLES `portfolio_entries` WRITE;
/*!40000 ALTER TABLE `portfolio_entries` DISABLE KEYS */;
INSERT INTO `portfolio_entries` (`entry_id`, `student_id`, `category_id`, `title`, `organization`, `entry_date`, `description`, `certificate_url`) VALUES
  (1, 1, 6, 'AWS Certified Cloud Practitioner', 'Amazon Web Services', '2023-08-10', 'Validation of cloud fundamentals and security architectural principles.', 'https://aws.amazon.com/verification/CLD-102938'),
  (2, 1, 8, 'Smart India Hackathon Finalist', 'Ministry of Education', '2023-11-20', 'Built an AI-driven smart classroom attendance system using computer vision.', 'https://sih.gov.in/certificate/SIH23-AARAV'),
  (3, 1, 7, 'Automated Student Progression Portal', 'College Innovation Cell', '2024-04-12', 'Full-stack DBMS mini-project with interactive Streamlit GUI and MySQL backend.', NULL),
  (4, 2, 9, 'Software Engineering Intern', 'Infosys Springboard', '2023-07-30', 'Developed backend microservices with Python and REST APIs.', 'https://infosys.com/springboard/cert/PP-990'),
  (5, 2, 6, 'Oracle Certified Associate MySQL 8.0', 'Oracle University', '2024-02-14', 'Demonstrated mastery of SQL indexing, query optimization, and schema design.', 'https://oracle.com/certs/OCA-8821'),
  (6, 3, 10, 'Git & GitHub Hands-on Workshop', 'IEEE Student Branch', '2023-03-05', 'Version control fundamentals, branching strategies, and open-source contribution.', NULL);
/*!40000 ALTER TABLE `portfolio_entries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- View structure for `achievement_categories`
--

DROP VIEW IF EXISTS `achievement_categories`;
CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `achievement_categories` AS select `portfolio_categories`.`category_id` AS `category_id`,`portfolio_categories`.`category_name` AS `category_name`,`portfolio_categories`.`category_group` AS `category_group`,`portfolio_categories`.`activity_type` AS `activity_type` from `portfolio_categories`;

--
-- View structure for `achievements`
--

DROP VIEW IF EXISTS `achievements`;
CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `achievements` AS select `portfolio_entries`.`entry_id` AS `entry_id`,`portfolio_entries`.`student_id` AS `student_id`,`portfolio_entries`.`category_id` AS `category_id`,`portfolio_entries`.`title` AS `title`,`portfolio_entries`.`organization` AS `organization`,`portfolio_entries`.`entry_date` AS `entry_date`,`portfolio_entries`.`description` AS `description`,`portfolio_entries`.`certificate_url` AS `certificate_url` from `portfolio_entries`;

--
-- View structure for `drop_years`
--

DROP VIEW IF EXISTS `drop_years`;
CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `drop_years` AS select `academic_gaps`.`gap_id` AS `gap_id`,`academic_gaps`.`student_id` AS `student_id`,`academic_gaps`.`start_year` AS `start_year`,`academic_gaps`.`end_year` AS `end_year`,`academic_gaps`.`reason` AS `reason`,`academic_gaps`.`description` AS `description` from `academic_gaps`;

--
-- View structure for `semester_results`
--

DROP VIEW IF EXISTS `semester_results`;
CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `semester_results` AS select `semester_subject_marks`.`mark_id` AS `mark_id`,`semester_subject_marks`.`semester_id` AS `semester_id`,`semester_subject_marks`.`student_id` AS `student_id`,`semester_subject_marks`.`subject_id` AS `subject_id`,`semester_subject_marks`.`internal_marks` AS `internal_marks`,`semester_subject_marks`.`external_marks` AS `external_marks`,`semester_subject_marks`.`total_marks` AS `total_marks`,`semester_subject_marks`.`theory_marks` AS `theory_marks`,`semester_subject_marks`.`theory_max_marks` AS `theory_max_marks`,`semester_subject_marks`.`lab_marks` AS `lab_marks`,`semester_subject_marks`.`lab_max_marks` AS `lab_max_marks`,`semester_subject_marks`.`grade` AS `grade`,`semester_subject_marks`.`result_status` AS `result_status` from `semester_subject_marks`;

--
-- View structure for `subject_results`
--

DROP VIEW IF EXISTS `subject_results`;
CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `subject_results` AS select `semester_subject_marks`.`mark_id` AS `result_id`,`semester_subject_marks`.`student_id` AS `student_id`,`semester_subject_marks`.`semester_id` AS `semester_id`,`semester_subject_marks`.`subject_id` AS `subject_id`,`semester_subject_marks`.`internal_marks` AS `internal_marks`,`semester_subject_marks`.`external_marks` AS `external_marks`,`semester_subject_marks`.`total_marks` AS `total_marks`,`semester_subject_marks`.`grade` AS `grade`,`semester_subject_marks`.`result_status` AS `result_status` from `semester_subject_marks`;

--
-- View structure for `v_attendance_warnings`
--

DROP VIEW IF EXISTS `v_attendance_warnings`;
CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `v_attendance_warnings` AS select `s`.`student_id` AS `student_id`,`s`.`roll_number` AS `roll_number`,`s`.`full_name` AS `full_name`,`s`.`branch` AS `branch`,`sem`.`semester_number` AS `semester_number`,`sub`.`subject_code` AS `subject_code`,`sub`.`subject_name` AS `subject_name`,`att`.`classes_held` AS `classes_held`,`att`.`classes_attended` AS `classes_attended`,`att`.`attendance_percentage` AS `attendance_percentage`,round((75.0 - `att`.`attendance_percentage`),2) AS `shortage_percentage`,ceiling((((0.75 * `att`.`classes_held`) - `att`.`classes_attended`) / 0.25)) AS `classes_needed_for_75` from (((`attendance` `att` join `students` `s` on((`s`.`student_id` = `att`.`student_id`))) join `semesters` `sem` on((`sem`.`semester_id` = `att`.`semester_id`))) join `subjects` `sub` on((`sub`.`subject_id` = `att`.`subject_id`))) where (`att`.`attendance_percentage` < 75.00);

--
-- View structure for `v_backlog_tracker`
--

DROP VIEW IF EXISTS `v_backlog_tracker`;
CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `v_backlog_tracker` AS select `s`.`student_id` AS `student_id`,`s`.`roll_number` AS `roll_number`,`s`.`full_name` AS `full_name`,`s`.`branch` AS `branch`,`sem`.`semester_number` AS `semester_number`,`sub`.`subject_code` AS `subject_code`,`sub`.`subject_name` AS `subject_name`,`sub`.`credits` AS `credits`,`m`.`internal_marks` AS `internal_marks`,`m`.`external_marks` AS `external_marks`,`m`.`total_marks` AS `total_marks`,`m`.`grade` AS `grade`,`m`.`result_status` AS `result_status` from (((`semester_subject_marks` `m` join `students` `s` on((`s`.`student_id` = `m`.`student_id`))) join `semesters` `sem` on((`sem`.`semester_id` = `m`.`semester_id`))) join `subjects` `sub` on((`sub`.`subject_id` = `m`.`subject_id`))) where (`m`.`result_status` in ('Failed','Backlog'));

--
-- View structure for `v_portfolio_summary`
--

DROP VIEW IF EXISTS `v_portfolio_summary`;
CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `v_portfolio_summary` AS select `s`.`student_id` AS `student_id`,`s`.`roll_number` AS `roll_number`,`s`.`full_name` AS `full_name`,`s`.`branch` AS `branch`,count((case when (`c`.`category_group` = 'Certification') then 1 end)) AS `certifications_count`,count((case when (`c`.`category_group` = 'Project') then 1 end)) AS `projects_count`,count((case when (`c`.`category_group` = 'Hackathon') then 1 end)) AS `hackathons_count`,count((case when (`c`.`category_group` = 'Internship') then 1 end)) AS `internships_count`,count((case when (`c`.`category_group` = 'Seminar') then 1 end)) AS `seminars_count`,count((case when (`c`.`category_group` = 'Activity') then 1 end)) AS `activities_count`,count(`p`.`entry_id`) AS `total_entries` from ((`students` `s` left join `portfolio_entries` `p` on((`s`.`student_id` = `p`.`student_id`))) left join `portfolio_categories` `c` on((`c`.`category_id` = `p`.`category_id`))) group by `s`.`student_id`,`s`.`roll_number`,`s`.`full_name`,`s`.`branch`;

--
-- View structure for `v_semester_progression`
--

DROP VIEW IF EXISTS `v_semester_progression`;
CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `v_semester_progression` AS select `s`.`student_id` AS `student_id`,`s`.`roll_number` AS `roll_number`,`s`.`full_name` AS `full_name`,`s`.`branch` AS `branch`,`sem`.`semester_number` AS `semester_number`,`sem`.`academic_year` AS `academic_year`,`sem`.`sgpa` AS `sgpa`,`sem`.`cgpa` AS `cgpa`,`sem`.`result_status` AS `result_status`,`sem`.`gap_note` AS `gap_note` from (`semesters` `sem` join `students` `s` on((`s`.`student_id` = `sem`.`student_id`))) order by `s`.`student_id`,`sem`.`semester_number`;

--
-- View structure for `v_student_academic_summary`
--

DROP VIEW IF EXISTS `v_student_academic_summary`;
CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `v_student_academic_summary` AS select `s`.`student_id` AS `student_id`,`s`.`roll_number` AS `roll_number`,`s`.`enrollment_no` AS `enrollment_no`,`s`.`full_name` AS `full_name`,`s`.`branch` AS `branch`,`s`.`admission_year` AS `admission_year`,`s`.`current_status` AS `current_status`,count(distinct `sem`.`semester_id`) AS `total_semesters_recorded`,max(`sem`.`cgpa`) AS `latest_cgpa`,coalesce(sum((case when (`m`.`result_status` in ('Failed','Backlog')) then 1 else 0 end)),0) AS `total_backlogs_count`,round(avg(`att`.`attendance_percentage`),2) AS `average_attendance_pct`,count(distinct `p`.`entry_id`) AS `total_portfolio_achievements` from ((((`students` `s` left join `semesters` `sem` on((`s`.`student_id` = `sem`.`student_id`))) left join `semester_subject_marks` `m` on((`s`.`student_id` = `m`.`student_id`))) left join `attendance` `att` on((`s`.`student_id` = `att`.`student_id`))) left join `portfolio_entries` `p` on((`s`.`student_id` = `p`.`student_id`))) group by `s`.`student_id`,`s`.`roll_number`,`s`.`enrollment_no`,`s`.`full_name`,`s`.`branch`,`s`.`admission_year`,`s`.`current_status`;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
-- Dump completed successfully.
