# Simple Inventory and Asset Management System (IMS)

A role-based asset tracking web application built with Django 6.0 and SQLite.  
It is designed for **small organizations** to manage internal assets (laptops, tools, furniture), track where they are located, and strictly control who can view or modify data according to their **user role**.

This project focuses on:
- **Data security** via authentication and role-based permissions.
- **Structured CRUD operations** on assets, categories, locations, and users.
- **Enforced business rules** that match the given academic specification.

The detailed compliance audit is documented in `final.md`.

---

## 🚀 Functional Overview

### 1. Users & Role-Based Authentication

The system defines three explicit roles using the `CustomUser` model:

- **Admin**
  - Can view, add, edit, and delete **all assets**.
  - Can manage **user accounts**, **categories**, and **locations**.
  - Has unrestricted access (implemented as a Django superuser with full permissions).

- **Manager**
  - Can view **all assets**.
  - Can update **Location** and **Status** (and notes) of any asset.
  - **Cannot** create new assets or delete existing ones (no `add_asset` / `delete_asset` permissions).

- **Viewer**
  - Can access the **asset list** and **asset details**.
  - Assets are strictly **read-only** for this role (no CRUD permissions).

Authentication is handled by Django’s built-in auth system (`login_view`, `logout_view`), and authorization is enforced using Django permissions plus a `role` field on the custom user.

---

### 2. Asset Management (CRUD)

The core of the system is heavy CRUD on the `Asset` model:

- **Create (Admin only)**  
  Admins add new assets with:
  - **Name**
  - **Serial Number** (unique)
  - **Category** (from predefined list)
  - **Purchase Date**
  - **Initial Location** (from predefined list)
  - Quantity, status, optional price and notes

- **Read (All roles)**  
  - `AssetListView` shows a searchable and filterable table of all assets.
  - `AssetDetailView` shows a detail page styled to match the main UI theme.

- **Update (Admin + Manager)**  
  - Admins can update **all fields** of an asset.
  - Managers can only update **Status**, **Location**, and **Notes**, using a restricted form.
  - Supported statuses: **Available**, **In Use**, **In Repair**, **In Stock**.

- **Delete (Admin only)**  
  - Only users with `assets.delete_asset` (Admins) can permanently remove assets.
  - Delete actions are hidden from non-admin roles in the UI and protected at the view level.

---

### 3. Category & Location Management

#### Category Management

- The system uses a **defined list of categories**, such as:
  - "IT Equipment"
  - "Office Furniture"
  - "Tools"
  - "Miscellaneous"
- Categories are stored in the `Category` model and seeded by the `create_demo_data` command.
- Only Admins can:
  - Add new categories.
  - Edit existing ones.
  - Delete categories.
- Each category also has a **low-stock threshold** used by the Low Stock report.

#### Location Tracking

- The `Location` model represents a **predefined list of locations**, seeded as:
  - "Office A"
  - "Warehouse 1"
  - "Remote Employee"
- Every asset must be assigned to one of these locations.
- Admins and Managers can update an asset’s location through the update views.

---

### 4. Search & Filtering

The asset list supports robust search and filtering for all authenticated users:

- Search by:
  - **Name**
  - **Serial Number**
  - Combined search that also matches **Category** name.
- Filter by:
  - **Category**
  - **Status**
  - **Location**

These filters are implemented via `AssetSearchForm` and applied in `AssetListView.get_queryset`.

---

### 5. Basic Reports

The system provides two simple, printable/exportable reports as required:

- **Assets by Location**
  - Lets the user select a location and view all assets currently assigned there.
  - Supports:
    - On-screen table view.
    - **Print** (browser `window.print`).
    - **CSV export** via a dedicated view.

- **Low Stock**
  - For each category, sums the quantity of assets with status **Available**.
  - Lists categories where the available quantity is **below the category’s threshold** (e.g., fewer than 5 laptops).
  - Supports on-screen viewing, printing, and CSV export.

These reports demonstrate structured data access and simple analytics on top of the inventory data.

---

## 🗄️ Database Information

### Why SQLite?

For academic submission and ease of evaluation, the default database is **SQLite**:

- **File-based** – no server installation required.
- **Zero configuration** – works immediately after cloning/unzipping.
- **Portable** – the same `db.sqlite3` can be shipped with the project if needed.

The Django ORM is used everywhere, so switching to **MySQL** or **PostgreSQL** only requires editing the `DATABASES` setting in `inventory_system/settings.py`.

---

## 🛠️ Technology Stack

- **Backend**: Django 6.0.2 (Python)
- **Database**: SQLite (default, production-ready with MySQL/PostgreSQL)
- **Frontend**: Bootstrap 5, FontAwesome 6, custom CSS in `base.html`
- **Authentication/Authorization**: Django Auth with `CustomUser`, groups, and permissions

---

## 📥 Installation & Setup

### 1. Quick Start – Zero Config (Windows)

This is the **easiest** way for a new user to run the project locally.

1. Open **PowerShell** or **Command Prompt** and run:

   ```bash
   git clone https://github.com/<your-username>/imsbyabdul.git
   cd imsbyabdul
   .\setup.bat
   ```

2. Wait until the script finishes. It will automatically:
   - Create a virtual environment (`venv`).
   - Install all dependencies from `requirements.txt`.
   - Run database migrations.
   - Create demo users, categories, and locations.
   - Start the Django development server on `http://127.0.0.1:8000/`.

3. Open your browser and log in using the demo credentials below.

> If you don’t have `git`, you can also download the ZIP from GitHub, extract it, open a terminal in the extracted folder, and run `setup.bat`.

---

### 2. Standard Setup (All Platforms)

#### Prerequisites

- Python 3.8+
- Virtual environment tool (`venv` is built into Python)

#### Manual steps

```bash
# 1) Navigate to project root
cd imsbyabdul

# 2) Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS / Linux
source venv/bin/activate

# 3) Install required packages
pip install -r requirements.txt

# 4) Apply database migrations
python manage.py migrate

# 5) Initialize demo data (users, categories, locations)
python manage.py create_demo_data

# 6) Start the development server
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser.

---

## 🔐 Default Demo Credentials

| Role      | Username | Password  | Access Level                  |
| :-------- | :------- | :-------- | :---------------------------- |
| **Admin** | `admin`  | `password`| Full control (all CRUD + users) |
| **Manager** | `manager` | `password` | View all; edit status/location only |
| **Viewer** | `viewer` | `password` | Read-only access to assets     |

---

## 📁 Project Structure

- `assets/` – models, views, forms, management commands, URLs.
- `inventory_system/` – Django project configuration and settings.
- `templates/` – Bootstrap-based templates (`assets/` pages + `base.html`).
- `final.md` – detailed compliance audit against the academic specification.
- `requirements.txt` – Python dependency list.
- `STUDENT_SETUP.md` – optional, extended setup notes for lab/campus machines.

---

## 👨‍💻 Developer Information

- **Name**: Abdul Rehman  
- **Student ID**: bc220208440  
- **Portfolio**: [abdulrehmansarwar.vercel.app](https://abdulrehmansarwar.vercel.app)  
- **Email**: bc220208440@vu.edu.pk  

---

**Version**: 1.0.1 | **Last Updated**: February 25, 2026
