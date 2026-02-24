# 🎓 Student Setup & Lab Guide

This guide is designed for students to set up and present the **Inventory and Asset Management System** in a campus lab environment.

## 🛠️ Phase 1: Environment Setup

### 1.1 Prerequisites
- **Python installed**: Verify by running `python --version`.
- **MySQL installed**: Ensure the MySQL service is running.

### 1.2 Installation Steps
1. **Open Terminal**: Navigate to the project root folder.
   ```bash
   cd c:\Users\abdul\inventory_system
   ```
2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   ```
3. **Activate Environment**:
   - **PowerShell**: `.\venv\Scripts\Activate.ps1`
   - **CMD**: `.\venv\Scripts\activate.bat`
4. **Install Dependencies**:
   ```bash
   pip install django==6.0.2 mysqlclient
   ```

---

## 🗄️ Phase 2: Database Configuration

### 2.1 Create Database
Open your MySQL Command Line or Workbench and run:
```sql
CREATE DATABASE inventory_db;
```

### 2.2 Sync Schema & Data
Run the following commands in your project terminal:
```bash
# Apply the database structure
python manage.py migrate

# Load professional demo data (Admins, Managers, Assets)
python manage.py create_demo_data
```

---

## 🖥️ Phase 3: Running & Presenting

### 3.1 Start Server
```bash
python manage.py runserver
```
Go to: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

### 3.2 Presentation Flow (Live Demo)

1.  **Login as Admin** (`admin` / `password`):
    - Demonstrate **User Management**: Create a new user.
    - Demonstrate **Asset CRUD**: Add a new laptop with a serial number.
    - Demonstrate **Category Management**: Edit a category's stock threshold.
2.  **Login as Manager** (`manager` / `password`):
    - Show that the "Add Asset" button is hidden.
    - **Update Status**: Change an asset from "Available" to "In Use".
    - **Change Location**: Move an item to "Warehouse 1".
3.  **Login as Viewer** (`viewer` / `password`):
    - Show that all forms are Read-Only.
    - Demonstrate **Search/Filter**: Search for a specific serial number.
4.  **Reporting**:
    - Go to **Reports** → **Low Stock**.
    - Show the printable view using the "Print Report" button.

---

## 🔍 Phase 4: Verification (Strict Requirements Check)
To ensure the project meets all academic requirements, run:
```bash
python test_requirements.py
```
**Expected Result**: `45/45 Tests Passed`.

---

## ❓ Troubleshooting
- **MySQL Connection Refused**: Check `inventory_system/settings.py` and ensure the `USER` and `PASSWORD` match your local MySQL configuration.
- **Missing Module**: Ensure you are in the `venv` before running `pip install`.
- **404 Page**: Ensure the server is running and you are logged in.

---
**Developer**: Abdul Rehman | **ID**: bc220208440
