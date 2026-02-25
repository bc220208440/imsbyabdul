# Inventory and Asset Management System (IMS)

A professional, role-based asset tracking solution built with Django 6.0 and MySQL. Designed for small to medium organizations to manage internal assets (laptops, tools, furniture) with strict data security and structured inventory management.

## 🚀 Key Features

### 1. **Role-Based Access Control (RBAC)**
Strictly enforced access levels for data security:
- **Admin**: Full system control. Can Create, Read, Update, and Delete (CRUD) all assets, categories, locations, and user accounts.
- **Manager**: Operational access. Can view all assets and update their **Location** and **Status**. Cannot create or delete assets.
- **Viewer**: Read-only access. Can browse the inventory and view asset details but cannot make any changes.

### 2. **Asset Management (CRUD)**
Comprehensive tracking of organizational resources:
- **Create**: Admins add assets with Name, Serial Number, Category, Quantity, Purchase Date, and Initial Location.
- **Read**: Advanced searchable list view accessible to all authenticated users.
- **Update**: Dynamic status tracking (e.g., "Available," "In Use," "In Repair," "In Stock").
- **Delete**: Only Admins can permanently remove assets from the system.

### 3. **Category & Location Tracking**
- **Category Management**: Admin-controlled list of asset types (e.g., "IT Equipment," "Office Furniture," "Tools") with custom low-stock thresholds.
- **Location Management**: Predefined organizational zones (e.g., "Office A," "Warehouse 1," "Remote Employee") for precise tracking.

### 4. **Search & Intelligent Filtering**
- Search by **Name** or **Serial Number**.
- Filter inventory by **Category**, **Status**, and **Location**.
- Integrated dashboard with real-time stock statistics.

### 5. **Professional Reporting**
Generate and print clear, structured reports:
- **Assets by Location**: Instant inventory list for any specific location.
- **Low Stock Report**: Automated alerts for categories falling below the predefined threshold (e.g., < 5 laptops).

## 🗄️ Database Information

### Why SQLite?
For academic submission and portability, **SQLite** is used because:
- **No installation required**: It is a file-based database.
- **Zero configuration**: No need to set up users, passwords, or permissions.
- **Works immediately**: The system is ready to use right after unzipping.
- **Ideal for evaluation**: Perfect for instructors to run the project without complex environment setup.

In a **production** environment, the system can be easily switched to **MySQL** or **PostgreSQL** by modifying the `DATABASES` setting in `inventory_system/settings.py`.

---

## 🛠️ Technology Stack
- **Backend**: Django 6.0.2 (Python Framework)
- **Database**: SQLite (Academic/Portable) | MySQL Compatible
- **Frontend**: Bootstrap 5 + FontAwesome 6 (Responsive UI)
- **Authentication**: Django Built-in Auth System with Custom Role Logic

---

## 📥 Installation & Setup

### 1. Prerequisites
- Python 3.8+
- Virtual Environment (Recommended)

### 2. Setup Instructions
```bash
# Navigate to project directory
cd inventory_system

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install required packages
pip install django==6.0.2

# Apply Database Migrations
python manage.py migrate

# Initialize Demo Data (Users, Categories, Locations, Assets)
python manage.py create_demo_data

# Start the Application
python manage.py runserver
```

---

## 🔐 Default Demo Credentials
| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `password` | Full Control |
| **Manager** | `manager` | `password` | Edit Status/Location |
| **Viewer** | `viewer` | `password` | Read-Only |

---

## 📁 Project Structure
- `assets/`: Core application logic (Models, Views, Forms, Management Commands).
- `inventory_system/`: Project configuration and settings.
- `templates/`: Professional HTML5/Bootstrap 5 templates.
- `requirements.txt`: Project dependency list.
- `STUDENT_SETUP.md`: Detailed guide for campus/lab setup.

---

## 👨‍💻 Developer Information
- **Name**: Abdul Rehman
- **Student ID**: bc220208440
- **Portfolio**: [abdulrehmansarwar.vercel.app](https://abdulrehmansarwar.vercel.app)
- **Email**: bc220208440@vu.edu.pk

---
**Version**: 1.0.0 | **Last Updated**: February 24, 2026
