# Student Setup Guide — Inventory & Asset Management System

This guide helps a student run and present the project from scratch on Windows in minutes.

## Prerequisites
- Python 3.8 or newer
- MySQL Server (localhost:3306)
- A terminal (PowerShell or Command Prompt)

## 1) Get the Project
1. Open a terminal.
2. Navigate to the project folder:
   ```bash
   cd c:\Users\abdul\inventory_system
   ```

## 2) Create a Virtual Environment
```bash
python -m venv venv
```

Activate it:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- Mac/Linux (optional info):
  ```bash
  source venv/bin/activate
  ```

## 3) Install Dependencies
```bash
pip install django==6.0.2
pip install mysqlclient
```

## 4) Create the MySQL Database
Ensure MySQL is running. Then create the database:
```bash
mysql -u root -p
```
Inside MySQL:
```sql
CREATE DATABASE inventory_db;
EXIT;
```

If your MySQL username/password differ, update the settings in:
- inventory_system/settings.py → DATABASES section

## 5) Apply Migrations
```bash
python manage.py migrate
```

## 6) Load Demo Data
Creates Admin/Manager/Viewer users and sample data:
```bash
python manage.py create_demo_data
```

## 7) Run the Server
```bash
python manage.py runserver 8000
```
Open http://localhost:8000/ in your browser.

## 8) Login Credentials
| Role    | Username | Password |
|---------|----------|----------|
| Admin   | admin    | password |
| Manager | manager  | password |
| Viewer  | viewer   | password |

## 9) What to Demonstrate
- Assets page: search/filter by name, serial, category, status, location.
- Admin:
  - Create/Edit/Delete assets
  - Manage Categories and Locations
  - Manage Users and assign roles
- Manager:
  - Update asset status and location (no create/delete)
- Viewer:
  - Read-only access to assets and reports
- Reports:
  - Assets by Location
  - Low Stock (based on category thresholds)

## 10) Quick Troubleshooting
- MySQL connection error:
  - Verify MySQL is running and database exists.
  - Check credentials in inventory_system/settings.py (ENGINE/NAME/USER/PASSWORD/HOST/PORT).
- ModuleNotFoundError: MySQLdb
  - Run: `pip install mysqlclient`
- “No such table” error
  - Run: `python manage.py migrate`
- Login issues
  - Re-run: `python manage.py create_demo_data`

## Optional: Verify Requirements
Run the automated checks:
```bash
python test_requirements.py
```
All tests should pass, confirming role-based access, CRUD, search/filtering, and reports.

## Submission Tips
- Show role differences live (Admin vs Manager vs Viewer).
- Keep venv active while presenting.
- If using a different DB user/password, ensure settings match before running.

