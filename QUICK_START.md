# Inventory and Asset Management System - Quick Start Guide

## System Requirements
- Python 3.8+
- MySQL Server 5.7+
- Windows/Mac/Linux OS
- Modern web browser

## Installation Steps

### 1. Verify MySQL is Running
Ensure MySQL server is running on your system. Default configuration:
- Host: localhost
- Port: 3306
- Username: root
- Password: ab2ulr3hman

### 2. Navigate to Project Directory
```bash
cd c:\Users\abdul\inventory_system
```

### 3. Create and Activate Virtual Environment (Optional but Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install django==6.0.2
pip install mysqlclient
```

### 5. Reset Database (If needed)
```python
python -c "import MySQLdb; db = MySQLdb.connect('localhost', 'root', 'ab2ulr3hman'); cursor = db.cursor(); cursor.execute('DROP DATABASE IF EXISTS inventory_db'); cursor.execute('CREATE DATABASE inventory_db'); db.commit(); db.close()"
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Create Demo Data
```bash
python manage.py create_demo_data
```

### 8. Start Development Server
```bash
python manage.py runserver 8000
```

The application will be available at: **http://localhost:8000**

## Login Credentials

After running `create_demo_data`, use these credentials:

### Admin User
- **URL**: http://localhost:8000/login/
- **Username**: admin
- **Password**: password
- **Access**: Full system access

### Manager User
- **Username**: manager
- **Password**: password
- **Access**: View and update asset status/location

### Viewer User
- **Username**: viewer
- **Password**: password
- **Access**: Read-only asset browsing

## Key Features

### Dashboard (All Users)
- View asset statistics
- See low stock alerts
- Quick action buttons
- Recent asset activity

### Asset Management (Admin Only)
- Create new assets
- Full edit capabilities
- Delete assets
- Manage all asset details

### Status Management (Admin & Manager)
- Update asset location
- Change asset status (Available, In Use, In Repair, In Stock)
- Add notes to assets

### Categories (Admin Only)
- Create asset categories
- Set low stock thresholds
- Manage category descriptions
- Delete categories

### Locations (Admin Only)
- Create storage locations
- Define location descriptions
- Track assets per location

### User Management (Admin Only)
- Create new user accounts
- Assign user roles (Admin, Manager, Viewer)
- Activate/deactivate accounts
- Edit user information

### Reports (All Users)
- **Assets by Location**: View all assets at a specific location
- **Low Stock Report**: See categories below inventory threshold
- Printable reports in text format

## Common Tasks

### Adding a New Asset
1. Login as Admin
2. Click "Assets" in sidebar
3. Click "Add New Asset" button
4. Fill in the form:
   - Asset Name: e.g., "Dell Laptop Model XPS 15"
   - Serial Number: unique identifier
   - Category: select from dropdown
   - Location: select optional location
   - Status: initial status
   - Purchase Date: use date picker
   - Price (optional)
   - Notes (optional)
5. Click "Create Asset"

### Updating Asset Status (Manager)
1. Login as Manager
2. Click "Assets"
3. Click on specific asset
4. Click "Edit" button
5. Update Status and Location fields only
6. Click "Update Asset"

### Running a Location Report
1. Click "Reports" → "Assets by Location"
2. Select a location from dropdown
3. Click "Generate Report"
4. View assets at that location
5. Click "Print Report" to print or save as PDF

### Running a Low Stock Report
1. Click "Reports" → "Low Stock"
2. See all categories with low inventory
3. Review deficit amounts
4. Click "Print Report" to export

## Management Commands

### Generate Asset by Location Report
```bash
# View all locations
python manage.py generate_assets_by_location_report

# Specific location (replace 1 with location ID)
python manage.py generate_assets_by_location_report --location 1

# Export as CSV
python manage.py generate_assets_by_location_report --format csv
```

### Generate Low Stock Report
```bash
# Text format
python manage.py generate_low_stock_report

# CSV format
python manage.py generate_low_stock_report --format csv
```

### Create Demo Data
```bash
python manage.py create_demo_data
```

## Troubleshooting

### Issue: "Can't connect to MySQL server"
**Solution**:
1. Ensure MySQL is running
2. Check credentials in `inventory_system/settings.py`
3. Verify database `inventory_db` exists
4. Reset database using the resetcommand above

### Issue: "ModuleNotFoundError: No module named 'MySQLdb'"
**Solution**:
```bash
pip install mysqlclient
```

### Issue: "No such table" error
**Solution**:
```bash
python manage.py migrate
```

### Issue: Pages showing 404 error
**Solution**:
1. Ensure server is running: `python manage.py runserver 8000`
2. Check URL format in address bar
3. Verify login status - some pages require authentication

### Issue: Static files (CSS) not loading
**Solution**:
1. For development, usually not needed
2. For development server, ensure you reload page (Ctrl+F5)

## Admin Panel Access

Access Django Admin at: http://localhost:8000/admin/

**Credentials**: 
- Username: admin
- Password: password

Admin panel features:
- Manage users directly
- Edit all assets
- Manage categories and locations
- View audit logs

## Important Notes

1. **Data Backup**: Always backup your MySQL database before major changes
2. **Secret Key**: The SECRET_KEY in settings.py should be changed in production
3. **Debug Mode**: DEBUG is set to True for development - set to False in production
4. **Static Files**: For production, run `python manage.py collectstatic`
5. **Allowed Hosts**: Update ALLOWED_HOSTS in settings.py for production

## File Structure

```
inventory_system/
├── manage.py                          # Django management script
├── assets/                            # Main application folder
│   ├── models.py                      # Database models
│   ├── views.py                       # View logic
│   ├── forms.py                       # Form definitions
│   ├── admin.py                       # Admin configuration
│   ├── urls.py                        # URL routing
│   ├── management/
│   │   └── commands/
│   │       ├── create_demo_data.py
│   │       ├── generate_assets_by_location_report.py
│   │       └── generate_low_stock_report.py
│   ├── migrations/                    # Database migrations
│   └── templates/
├── inventory_system/
│   ├── settings.py                    # Django configuration
│   ├── urls.py                        # Main URL routing
│   └── wsgi.py
├── templates/                         # HTML templates
│   ├── base.html
│   ├── login.html
│   └── assets/
├── README.md                          # Full documentation
└── API_DOCUMENTATION.md              # API details

```

## Support and Help

For detailed information, see:
- README.md - Full system documentation
- API_DOCUMENTATION.md - API endpoint details

For issues:
1. Check Troubleshooting section above
2. Review Django logs
3. Check browser console for errors (F12)
4. Inspect Django error pages for detailed traceback

## Next Steps

1. **Explore the System**: Login with different roles to understand access levels
2. **Create Sample Data**: Add some test assets through the UI
3. **Generate Reports**: Try location and low stock reports
4. **Manage Users**: Create new users and assign different roles
5. **Customize**: Modify categories and locations to match your organization

---

**Last Updated**: February 24, 2026  
**Version**: 1.0.0
