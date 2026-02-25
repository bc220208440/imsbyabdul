# Quick Start Guide ⚡

Follow these steps to get the **Inventory and Asset Management System** running in less than 5 minutes.

## 1. System Requirements
- **Python**: 3.8 or higher
- **Browser**: Chrome, Edge, or Firefox

## 2. Fast Setup (Windows)

```powershell
# 1. Create Environment
python -m venv venv
.\venv\Scripts\activate

# 2. Install Packages
pip install django==6.0.2

# 3. Database Note
# SQLite is used by default. No separate database installation required.

# 4. Migrate & Initialize
python manage.py migrate
python manage.py create_demo_data

# 5. Launch
python manage.py runserver
```

## 3. Database Information
### Why SQLite?
For academic submission and portability, **SQLite** is used because:
- **No installation required**
- **Zero configuration**
- **Works immediately after unzip**
- **Ideal for evaluation environments**

In production, the system can easily be switched to **MySQL** or **PostgreSQL** by modifying the `DATABASES` setting in `settings.py`.

## 3. Access the System
- **URL**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Default Credentials**:

| User | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `admin` | `password` |
| **Manager** | `manager` | `password` |
| **Viewer** | `viewer` | `password` |

## 4. Key Functional Areas to Test
1. **Admin Power**: Go to "Assets" → "Add New Asset". Manage Categories & Users.
2. **Manager Role**: Login as manager. Update an asset's location or status (no delete/create).
3. **Search**: Use the search bar on the Assets page to find items by Serial Number.
4. **Reports**: Go to "Reports" → "Low Stock" to see categories needing restock.

---
For detailed lab environment instructions, see [STUDENT_SETUP.md](./STUDENT_SETUP.md).
