"""
generate_word_report.py
Generates the official Microsoft Word (.docx) technical report matching the exact 6-page reference report from VIVA Institute of Technology.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, hex_color):
    """Sets background shading of a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="374151", sz="4", val="single"):
    """Applies neat borders to table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_docx_report(output_path):
    doc = docx.Document()

    # Page setup - A4 with 1-inch (25.4mm) margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

        # Footer
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run("Student Academic Progression — User & Technical Report")
        f_run.font.name = "Times New Roman"
        f_run.font.size = Pt(9.5)
        f_run.font.color.rgb = RGBColor(107, 114, 128)

    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(17, 24, 39)

    # =========================================================================
    # PAGE 1: TITLE & COVER PAGE
    # =========================================================================
    for _ in range(5):
        doc.add_paragraph()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t1 = p_title.add_run("STUDENT ACADEMIC PROGRESSION\n")
    run_t1.bold = True
    run_t1.font.size = Pt(22)
    run_t2 = p_title.add_run("USER & TECHNICAL REPORT\n")
    run_t2.bold = True
    run_t2.font.size = Pt(17)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("DBMS Mini-Project")
    run_sub.bold = True
    run_sub.font.size = Pt(13)

    for _ in range(4):
        doc.add_paragraph()

    p_details = doc.add_paragraph()
    p_details.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_details.paragraph_format.line_spacing = 1.3
    p_details.add_run("Application: ").bold = False
    run_app = p_details.add_run("http://localhost:8501\n")
    run_app.font.color.rgb = RGBColor(126, 34, 206)
    run_app.underline = True

    p_details.add_run("GitHub: ").bold = False
    run_gh = p_details.add_run("https://github.com/dhirusuthar77-coder/dhiru_db\n\n")
    run_gh.font.color.rgb = RGBColor(126, 34, 206)
    run_gh.underline = True

    p_details.add_run("Submitted by: Praveen Manoj Tiwari / Dhiraj Suthar\n").bold = True
    p_details.add_run("Roll No:- 44\n").bold = True
    p_details.add_run("Class: T.E. (Electrical and Computer Engineering)\n").bold = True
    p_details.add_run("Institute: VIVA INSTITUTE OF TECHNOLOGY").bold = True

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: PROJECT DETAILS & SYSTEM ARCHITECTURE
    # =========================================================================
    p = doc.add_paragraph()
    run = p.add_run("Project Details")
    run.bold = True
    run.font.size = Pt(12)
    p_desc = doc.add_paragraph("The following details identify the DBMS mini-project and its deployment.")

    # Table 1: Particulars
    t1_data = [
        ("Course", "Database Management Systems (DBMS Mini-Project)"),
        ("Institution", "VIVA Institute of Technology"),
        ("Live Production Web App", "http://localhost:8501"),
        ("GitHub Repository", "https://github.com/dhirusuthar77-coder/dhiru_db"),
        ("Primary Database Engine", "SQLite 3 (ACID-compliant, foreign keys enabled, strict 3NF schema)"),
        ("Cloud Mirror Database", "MySQL 8.0 (InnoDB, remote replication engine)"),
        ("Live Cloud Synchronization", "Google Apps Script Webhook Pipeline (Bi-directional JSON sync)")
    ]

    table1 = doc.add_table(rows=1, cols=2)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table1)

    hdr_cells = table1.rows[0].cells
    hdr_cells[0].text = "Particulars"
    hdr_cells[1].text = "Details"
    for c in hdr_cells:
        c.paragraphs[0].runs[0].bold = True
        set_cell_background(c, "F9FAFB")
        set_cell_margins(c, 100, 100, 150, 150)

    for item, desc in t1_data:
        row_cells = table1.add_row().cells
        row_cells[0].text = item
        row_cells[1].text = desc
        row_cells[0].paragraphs[0].runs[0].bold = True
        set_cell_margins(row_cells[0], 100, 100, 150, 150)
        set_cell_margins(row_cells[1], 100, 100, 150, 150)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("1. System Architecture & Relational Topology")
    run.bold = True
    run.font.size = Pt(12)
    doc.add_paragraph("The supplied project report describes a layered three-tier architecture.")

    # Table 2: Architecture
    t2_data = [
        ("Presentation Layer — Streamlit GUI", "Live web application; 10 navigation panels; Plotly progression graphs; responsive mobile layout."),
        ("Business & Integration Engine", "Credit-weighted SGPA = Σ(Credits × Grade Point) / Σ(Credits); cumulative CGPA across active semesters; drop-year chronology detection and validation alerts; event-driven sync queue and payload snapshot dispatcher."),
        ("Local Relational Database — SQLite 3", "Strict 3NF; PRAGMA foreign_keys = ON; 9 interconnected relational tables."),
        ("Google Sheets Webhook", "Real-time JSON streaming; 8 normalized synchronized sheets."),
        ("Cloud Mirror Database — MySQL 8.0", "Remote persistence and backup; triggers; CASCADE/RESTRICT actions.")
    ]

    table2 = doc.add_table(rows=1, cols=2)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table2)

    hdr_cells = table2.rows[0].cells
    hdr_cells[0].text = "Layer / Component"
    hdr_cells[1].text = "Responsibilities / Details"
    for c in hdr_cells:
        c.paragraphs[0].runs[0].bold = True
        set_cell_background(c, "F9FAFB")
        set_cell_margins(c, 100, 100, 150, 150)

    for layer, resp in t2_data:
        row_cells = table2.add_row().cells
        row_cells[0].text = layer
        row_cells[1].text = resp
        row_cells[0].paragraphs[0].runs[0].bold = True
        set_cell_margins(row_cells[0], 100, 100, 150, 150)
        set_cell_margins(row_cells[1], 100, 100, 150, 150)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("2. Step-by-Step Operational Guide (GUI & Sync Feature)")
    run.bold = True
    run.font.size = Pt(12)

    doc.add_paragraph("Step 1: Accessing the Live System\nOpen http://localhost:8501 in a web browser such as Chrome, Edge, Safari, or Firefox. The supplied report describes a layout that adapts to desktop, tablet, and mobile screens.")
    doc.add_paragraph("Step 2: Browsing & Filtering Student Directory\nOpen “Dashboard & Analytics” or “Student Management”. The supplied report lists six departments: Computer Engineering, AI & Machine Learning, Data Science, Information Technology, Electronics & Telecommunication, and Mechanical Engineering. Search by roll number (examples: 23FC003, 22CS101) or full name. Dashboard indicators include total students, active vs. graduated students, overall institutional CGPA average, and active drop-year flags.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: OPERATIONAL GUIDE (CONTINUED)
    # =========================================================================
    doc.add_paragraph("Step 3: Academic Progression & SGPA/CGPA\nReview the student's 10th SSC and 12th HSC / Diploma records, including board and percentage. The report describes a Plotly dual-line chart for Term SGPA and Cumulative CGPA across Semesters 1–8, plus a grade breakdown for credits attempted vs. earned, theory marks, and practical lab marks.")
    doc.add_paragraph("Step 4: Drop-Year Audit Tracking\nOpen “Drop Years”. The report states that duration is calculated as End Year − Start Year, with reasons such as Medical Leave, Preparation, or Financial and an approving authority. Warning banners are described on the student overview and administrative dashboard.")
    doc.add_paragraph("Step 5: Portfolio & Extracurricular Achievements\nOpen “Portfolio & Achievements”. Categories listed in the supplied report include Technical, Hackathon, Research Paper, Certification, Sports, and Cultural. Records may include project titles, event scope (State, National, International), award level (1st Prize, Finalist), and issue date.")
    doc.add_paragraph("Step 6: Google Sheets Webhook Synchronization\nOpen “Google Sheets Sync”. The supplied report says the panel displays connection status for the deployed Google Apps Script Webhook.")

    t3_data = [
        ("Process Pending Queue", "Dispatches uncommitted local INSERT, UPDATE, or DELETE operations to Google Sheets."),
        ("Force Full Sync (All 8 Tables)", "Serializes 1,750+ database rows into structured JSON tables and mirrors them across eight sheets, as described in the supplied report."),
        ("Live Demo: Add Test Student & Sync", "Creates a test record in SQLite and pushes it to Google Sheets; the source report claims this takes under two seconds."),
        ("Verify spreadsheet", "Check tabs: students, school_records, semesters, subjects, semester_results, drop_years, achievements, achievement_categories.")
    ]

    table3 = doc.add_table(rows=1, cols=2)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table3)

    hdr_cells = table3.rows[0].cells
    hdr_cells[0].text = "Sync Action"
    hdr_cells[1].text = "Description"
    for c in hdr_cells:
        c.paragraphs[0].runs[0].bold = True
        set_cell_background(c, "F9FAFB")
        set_cell_margins(c, 100, 100, 150, 150)

    for action, desc in t3_data:
        row_cells = table3.add_row().cells
        row_cells[0].text = action
        row_cells[1].text = desc
        row_cells[0].paragraphs[0].runs[0].bold = True
        set_cell_margins(row_cells[0], 100, 100, 150, 150)
        set_cell_margins(row_cells[1], 100, 100, 150, 150)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("3. Instructions on Modifying & Updating Records in the Database")
    run.bold = True
    run.font.size = Pt(12)

    doc.add_paragraph("Method A: Graphical Forms (Recommended)\nRegister a student: open “Student Management” → “Register New Student”; enter roll number, full name, institutional email, phone, department, and admission year; then select “Save Student”. The source report says roll number and email uniqueness are validated.\n\nUpdate marks: open “Semesters & Marks” → “Enter Semester Marks”; select the student and semester, choose a subject, enter theory and lab marks (0–100), and select “Save Subject Result”. The source report describes recalculation of grade points, SGPA, and CGPA.\n\nLog a drop year: open “Drop Years” → “Record Academic Gap”; select the student and enter start year, end year, reason, and approving authority. End year must be greater than or equal to start year.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: SQL CONSOLE & PYTHON ADMINISTRATION
    # =========================================================================
    p = doc.add_paragraph()
    run = p.add_run("Method B: SQL Console")
    run.bold = True
    run.font.size = Pt(11)
    doc.add_paragraph("The supplied report says administrators can execute SQL queries from the “3NF Schema & Viva” tab. Examples:")

    t4_data = [
        ("Update student contact details and status", "UPDATE students SET phone = '9801437836', current_status = 'Active' WHERE roll_no = '23FC003';"),
        ("Correct theory and lab marks", "UPDATE semester_results SET theory_marks = 85.0, lab_marks = 45.0, total_marks = 85.0 + 45.0, grade = 'A+', grade_point = 9.0 WHERE semester_id = 14 AND subject_id = 3;"),
        ("Recalculate semester SGPA", "UPDATE semesters SET sgpa = (SELECT ROUND(SUM(credits * grade_point) / SUM(credits), 2) FROM semester_results WHERE semester_id = 14) WHERE semester_id = 14;"),
        ("Delete an achievement", "DELETE FROM achievements WHERE achievement_id = 12;")
    ]

    table4 = doc.add_table(rows=1, cols=2)
    table4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table4)

    hdr_cells = table4.rows[0].cells
    hdr_cells[0].text = "Purpose"
    hdr_cells[1].text = "SQL Example"
    for c in hdr_cells:
        c.paragraphs[0].runs[0].bold = True
        set_cell_background(c, "F9FAFB")
        set_cell_margins(c, 100, 100, 150, 150)

    for purp, sql in t4_data:
        row_cells = table4.add_row().cells
        row_cells[0].text = purp
        row_cells[1].text = sql
        row_cells[0].paragraphs[0].runs[0].bold = True
        set_cell_margins(row_cells[0], 100, 100, 150, 150)
        set_cell_margins(row_cells[1], 100, 100, 150, 150)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Method C: Python / CLI Database Administration")
    run.bold = True
    run.font.size = Pt(11)
    doc.add_paragraph("For programmatic changes, connect to SQLite, enable foreign keys, perform the update inside a transaction, commit on success, roll back on an IntegrityError, and close the connection.")

    t5_data = [
        ("Connect", "sqlite3.connect('database/student_progression.db')"),
        ("Enable foreign keys", "conn.execute(\"PRAGMA foreign_keys = ON;\")"),
        ("Update", "UPDATE students SET department = 'Computer', email = 'arjun.reddy@viva-technology.org' WHERE roll_no = '23FC003';"),
        ("Successful update", "Commit the transaction and report success."),
        ("Constraint violation", "Catch sqlite3.IntegrityError, roll back, and report the integrity violation."),
        ("Close", "Close the database connection in a finally block.")
    ]

    table5 = doc.add_table(rows=1, cols=2)
    table5.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table5)

    hdr_cells = table5.rows[0].cells
    hdr_cells[0].text = "Step"
    hdr_cells[1].text = "Example"
    for c in hdr_cells:
        c.paragraphs[0].runs[0].bold = True
        set_cell_background(c, "F9FAFB")
        set_cell_margins(c, 100, 100, 150, 150)

    for step, ex in t5_data:
        row_cells = table5.add_row().cells
        row_cells[0].text = step
        row_cells[1].text = ex
        row_cells[0].paragraphs[0].runs[0].bold = True
        set_cell_margins(row_cells[0], 100, 100, 150, 150)
        set_cell_margins(row_cells[1], 100, 100, 150, 150)

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: SCHEMA CONSTRAINTS & VIOLATION HANDLING
    # =========================================================================
    p = doc.add_paragraph()
    run = p.add_run("4. Schema Constraints & Violation Handling")
    run.bold = True
    run.font.size = Pt(12)
    doc.add_paragraph("The following table reproduces the constraints and violation-handling rules stated in the supplied source report.")

    t6_data = [
        ("PRIMARY KEY", "All 9 tables (student_id, semester_id, etc.)", "Auto-incrementing integer keys guarantee entity uniqueness.", "SQLITE_CONSTRAINT_PRIMARYKEY; normally prevented by auto-generation; form alerts if manually overridden."),
        ("UNIQUE candidate key", "students(roll_no)", "No duplicate roll numbers across departments.", "SQLITE_CONSTRAINT_UNIQUE; form reports that the roll number already exists."),
        ("UNIQUE candidate key", "students(email)", "No duplicate institutional email addresses.", "SQLITE_CONSTRAINT_UNIQUE; form reports that the email is already registered."),
        ("UNIQUE composite key", "school_records(student_id, level)", "At most one 10th and one 12th/Diploma record per student.", "SQLITE_CONSTRAINT_UNIQUE; existing record is updated rather than duplicated."),
        ("UNIQUE composite key", "semesters(student_id, semester_no)", "Each semester number (1–8) can be registered once per student.", "SQLITE_CONSTRAINT_UNIQUE; existing semester record is loaded."),
        ("CHECK", "school_records(percentage)", "Percentage must be between 0 and 100.", "SQLITE_CONSTRAINT_CHECK; invalid value is rejected and UI displays a validation alert."),
        ("CHECK", "semesters(sgpa), semesters(cgpa)", "GPA must be within 0–10.", "SQLITE_CONSTRAINT_CHECK; invalid grade-point values are blocked."),
        ("CHECK", "drop_years(start_year, end_year)", "end_year >= start_year.", "SQLITE_CONSTRAINT_CHECK; invalid chronology is rejected."),
        ("CHECK", "semester_results(theory_marks, lab_marks)", "Marks must be between 0 and 100.", "SQLITE_CONSTRAINT_CHECK; out-of-range marks are blocked."),
        ("FOREIGN KEY — CASCADE", "students → school_records, semesters, drop_years, achievements", "Deleting a student removes dependent child records.", "Automatic cascade in a transaction; avoids orphan records.")
    ]

    table6 = doc.add_table(rows=1, cols=4)
    table6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table6)

    hdr_cells = table6.rows[0].cells
    hdr_cells[0].text = "Constraint Type"
    hdr_cells[1].text = "Target Entity / Column"
    hdr_cells[2].text = "Rule Enforced"
    hdr_cells[3].text = "Violation Handling"
    for c in hdr_cells:
        c.paragraphs[0].runs[0].bold = True
        set_cell_background(c, "F9FAFB")
        set_cell_margins(c, 100, 100, 150, 150)

    for ctype, target, rule, viol in t6_data:
        row_cells = table6.add_row().cells
        row_cells[0].text = ctype
        row_cells[1].text = target
        row_cells[2].text = rule
        row_cells[3].text = viol
        row_cells[0].paragraphs[0].runs[0].bold = True
        for cell in row_cells:
            set_cell_margins(cell, 100, 100, 150, 150)

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: 3NF RATIONALE
    # =========================================================================
    t7_data = [
        ("FOREIGN KEY — RESTRICT", "subjects(subject_id) → semester_results(subject_id)", "A subject cannot be deleted while referenced by student results.", "SQLITE_CONSTRAINT_RESTRICT; deletion is rejected with an explanatory message.")
    ]

    table7 = doc.add_table(rows=1, cols=4)
    table7.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table7)

    hdr_cells = table7.rows[0].cells
    hdr_cells[0].text = "Constraint Type"
    hdr_cells[1].text = "Target Entity / Column"
    hdr_cells[2].text = "Rule Enforced"
    hdr_cells[3].text = "Violation Handling"
    for c in hdr_cells:
        c.paragraphs[0].runs[0].bold = True
        set_cell_background(c, "F9FAFB")
        set_cell_margins(c, 100, 100, 150, 150)

    for ctype, target, rule, viol in t7_data:
        row_cells = table7.add_row().cells
        row_cells[0].text = ctype
        row_cells[1].text = target
        row_cells[2].text = rule
        row_cells[3].text = viol
        row_cells[0].paragraphs[0].runs[0].bold = True
        for cell in row_cells:
            set_cell_margins(cell, 100, 100, 150, 150)

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("5. Third Normal Form (3NF) Rationale")
    run.bold = True
    run.font.size = Pt(12)
    doc.add_paragraph("The source report states that for every non-trivial functional dependency X → Y, X must be a superkey, or every attribute in Y \\ X must be a prime attribute (part of a candidate key).")

    t8_data = [
        ("students", "student_id (PK), roll_no (candidate key), full_name, email (candidate key), phone, department, admission_year, current_status.", "Functional dependencies: student_id → all attributes; roll_no → all attributes. Attributes are atomic (1NF); keys are non-composite; no non-prime attribute determines another non-prime attribute (3NF), as stated in the source."),
        ("semesters", "semester_id (PK), student_id (FK), semester_no, academic_year, sgpa, cgpa, status. Candidate key: (student_id, semester_no).", "SGPA and status depend on the specific student and semester; the source states no transitive dependency between academic year and SGPA."),
        ("subjects", "subject_id (PK), subject_code (candidate key), subject_name, subject_type, credits, department.", "An independent catalog reduces insertion, update, and deletion anomalies: courses can be added before enrollment; course details can be updated once; deleting results does not delete the catalog."),
        ("semester_results", "result_id (PK), semester_id (FK), subject_id (FK), theory_marks, lab_marks, total_marks, credits, grade_point, grade. Candidate key: (semester_id, subject_id).", "Grade depends on semester registration and subject; theory and practical marks are stored in separate atomic columns.")
    ]

    table8 = doc.add_table(rows=1, cols=3)
    table8.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table8)

    hdr_cells = table8.rows[0].cells
    hdr_cells[0].text = "Relation"
    hdr_cells[1].text = "Attributes / Keys"
    hdr_cells[2].text = "3NF Rationale"
    for c in hdr_cells:
        c.paragraphs[0].runs[0].bold = True
        set_cell_background(c, "F9FAFB")
        set_cell_margins(c, 100, 100, 150, 150)

    for rel, attr, rat in t8_data:
        row_cells = table8.add_row().cells
        row_cells[0].text = rel
        row_cells[1].text = attr
        row_cells[2].text = rat
        row_cells[0].paragraphs[0].runs[0].bold = True
        for cell in row_cells:
            set_cell_margins(cell, 100, 100, 150, 150)

    doc.save(output_path)
    print(f"[✓] Microsoft Word Technical Report created at: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "STUDENT_ACADEMIC_PROGRESSION_TECHNICAL_REPORT.docx")
    build_docx_report(out_file)
