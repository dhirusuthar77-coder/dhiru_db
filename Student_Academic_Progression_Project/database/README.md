# Database Files Guide
## Student Academic Progression & Portfolio Management System

This directory and the `sql/` directory contain all physical database artifacts for the project.

---

### Available Database Files

| File | Type | Description | How to Use |
| :--- | :--- | :--- | :--- |
| [`sql/student_progression_complete.sql`](file:///sql/student_progression_complete.sql) | MySQL Script (.sql) | Single turnkey script containing Database Creation, 3NF Tables, Constraints, Indexes, Demo Data, and Analytical Views | Open in MySQL Workbench and click **Execute (⚡)** or run via CLI |
| [`sql/database_dump.sql`](file:///sql/database_dump.sql) | MySQL Dump (.sql) | Standard MySQL database dump with `DROP TABLE IF EXISTS`, table definitions, row data, and view DDL | Import via phpMyAdmin (Import Tab) or `mysql -u root -p < database_dump.sql` |
| [`database/student_progression.db`](file:///database/student_progression.db) | SQLite File (.db) | Physical binary database file containing all 9 tables, seed data, and analytical views | Open directly in **DB Browser for SQLite**, **DBeaver**, or VS Code SQLite viewer without needing MySQL server |
| [`sql/01_create_database.sql`](file:///sql/01_create_database.sql) | Modular SQL | Creates `student_progression` schema with UTF-8 character set | Step 1 of modular pipeline |
| [`sql/02_create_tables.sql`](file:///sql/02_create_tables.sql) | Modular SQL | 9 normalized tables in 3rd Normal Form (3NF) | Step 2 of modular pipeline |
| [`sql/03_constraints_indexes.sql`](file:///sql/03_constraints_indexes.sql) | Modular SQL | Check constraints, foreign keys, unique keys, and composite indexes | Step 3 of modular pipeline |
| [`sql/04_sample_data.sql`](file:///sql/04_sample_data.sql) | Modular SQL | Realistic dataset across all 9 entities | Step 4 of modular pipeline |
| [`sql/05_views.sql`](file:///sql/05_views.sql) | Modular SQL | 5 analytical SQL views for backlogs, attendance, summaries | Step 5 of modular pipeline |
| [`init_db.py`](file:///init_db.py) | Python Initializer | Automated one-click Python runner that applies modular scripts in order and verifies integrity | Run: `python init_db.py` |

---

### Quick Import Options

#### Option 1: MySQL Workbench (GUI)
1. Open **MySQL Workbench**.
2. Connect to your Local MySQL instance.
3. Click **File** -> **Open SQL Script...**
4. Select `sql/student_progression_complete.sql`.
5. Click the yellow **Execute (⚡)** icon.
6. Refresh the Schemas panel on the left to see `student_progression`.

#### Option 2: MySQL Command Line (CLI)
```bash
mysql -u root -p < sql/student_progression_complete.sql
```
*(Enter your password when prompted).*

#### Option 3: Automated Python Initializer
```bash
python init_db.py
```

#### Option 4: Inspect Offline SQLite Database (.db)
You can directly open `database/student_progression.db` in:
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- DBeaver Universal Database Tool
- Visual Studio Code (Extension: *SQLite Viewer*)
