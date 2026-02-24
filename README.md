# Inventory and Asset Management System

A comprehensive Django-based web application for managing organizational assets with role-based access control. The system allows tracking of assets (laptops, tools, furniture) across locations with full audit trails.

## Features

### 1. **Role-Based Access Control**
- **Admin**: Full access - create, read, update, delete all assets and manage users
- **Manager**: Can view all assets and update status/location
- **Viewer**: Read-only access to asset lists and details

### 2. **Asset Management (CRUD)**
- **Create**: Admins can add new assets with name, serial number, category, purchase date, and location
- **Read**: All users can view asset list with search and filtering capabilities
- **Update**: Admins and Managers can update asset status and location
- **Delete**: Only Admins can permanently remove assets

### 3. **Category Management**
- Create and manage predefined asset categories (IT Equipment, Office Furniture, Tools, etc.)
- Set low stock thresholds for each category
- Automatic alerts when stock falls below threshold

### 4. **Location Tracking**
- Define predefined storage locations (Office A, Warehouse 1, Remote Employee, etc.)
- Assign assets to locations
- Track asset movements

### 5. **Search and Filtering**
- Search assets by name or serial number
- Filter by category, location, and status
- Advanced query capabilities

### 6. **Reporting**
- **Assets by Location Report**: View all assets at a specific location
- **Low Stock Report**: Identify categories below stock threshold
- Printable/exportable reports in text and CSV formats

### 7. **User Management**
- Create and manage user accounts (Admin only)
- Assign roles to users
- Activate/deactivate accounts

## Technology Stack

- **Backend**: Django 6.0+
- **Database**: MySQL
- **Frontend**: Bootstrap 5
- **Python**: 3.8+

## Installation

### 1. Prerequisites
- Python 3.8 or higher
- MySQL Server running
- pip (Python package installer)

### 2. Setup

```bash
# Clone or navigate to project directory
cd inventory_system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django
pip install mysqlclient

# Create database
mysql -u root -p
CREATE DATABASE inventory_db;
EXIT;

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create demo data
python manage.py create_demo_data

# Start development server
python manage.py runserver
```

## Default Demo Credentials

After running `create_demo_data`, use these credentials to login:

| Role    | Username | Password |
|---------|----------|----------|
| Admin   | admin    | password |
| Manager | manager  | password |
| Viewer  | viewer   | password |

## Project Structure

```
inventory_system/
├── manage.py
├── db.sqlite3
├── templates/
│   ├── base.html                      # Base template with navigation
│   ├── login.html                     # Login page
│   └── assets/
│       ├── dashboard.html             # Dashboard with statistics
│       ├── asset_list.html            # Asset listing with search
│       ├── asset_detail.html          # Asset detail view
│       ├── asset_form.html            # Create/Edit asset form
│       ├── asset_confirm_delete.html  # Delete confirmation
│       ├── category_list.html         # Category listing
│       ├── category_form.html         # Create/Edit category
│       ├── location_list.html         # Location listing
│       ├── location_form.html         # Create/Edit location
│       ├── user_list.html             # User management
│       ├── user_form.html             # Create/Edit user
│       ├── report_assets_by_location.html
│       └── report_low_stock.html
├── inventory_system/
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # URL routing
│   ├── wsgi.py
│   └── asgi.py
└── assets/
    ├── models.py                      # CustomUser, Asset, Category, Location
    ├── views.py                       # All view logic
    ├── forms.py                       # Django forms
    ├── urls.py                        # App URL routing
    ├── admin.py                       # Django admin config
    ├── apps.py
    ├── tests.py
    ├── management/
    │   └── commands/
    │       ├── create_demo_data.py
    │       ├── generate_assets_by_location_report.py
    │       └── generate_low_stock_report.py
    └── migrations/
        └── 0001_initial.py
```

## Database Models

### CustomUser
Extends Django's AbstractUser with role-based access:
- **Fields**: username, email, password, first_name, last_name, role
- **Roles**: ADMIN, MANAGER, VIEWER

### Asset
Tracks organizational assets:
- **Fields**: name, serial_number, category (FK), location (FK), status, purchase_date, purchase_price, assigned_to, notes
- **Status Options**: AVAILABLE, IN_USE, IN_REPAIR, IN_STOCK
- **Audit**: created_by, updated_by, created_at, updated_at

### Category
Asset categories with stock management:
- **Fields**: name, description, low_stock_threshold
- **Relationship**: One-to-Many with Asset

### Location
Storage locations:
- **Fields**: name, description
- **Relationship**: One-to-Many with Asset

## View Access Control

```
View                    Admin   Manager   Viewer
────────────────────────────────────────────────
Dashboard              ✓       ✓         ✓
Asset List             ✓       ✓         ✓
Asset Detail           ✓       ✓         ✓
Create Asset           ✓       ✗         ✗
Update Asset           ✓       ✓(status) ✗
Delete Asset           ✓       ✗         ✗
Categories             ✓       ✓         ✓
Create Category        ✓       ✗         ✗
Locations              ✓       ✓         ✓
Create Location        ✓       ✗         ✗
User Management        ✓       ✗         ✗
Reports                ✓       ✓         ✓
```

## URL Endpoints

### Authentication
- `GET/POST /login/` - User login
- `GET /logout/` - User logout

### Dashboard
- `GET /` - Dashboard with statistics

### Assets
- `GET /assets/` - List all assets
- `GET /assets/<id>/` - Asset detail
- `GET/POST /assets/create/` - Create asset (Admin only)
- `GET/POST /assets/<id>/edit/` - Update asset
- `GET/POST /assets/<id>/delete/` - Delete asset (Admin only)

### Categories
- `GET /categories/` - List categories
- `GET/POST /categories/create/` - Create category (Admin only)
- `GET/POST /categories/<id>/edit/` - Update category (Admin only)
- `GET/POST /categories/<id>/delete/` - Delete category (Admin only)

### Locations
- `GET /locations/` - List locations
- `GET/POST /locations/create/` - Create location (Admin only)
- `GET/POST /locations/<id>/edit/` - Update location (Admin only)
- `GET/POST /locations/<id>/delete/` - Delete location (Admin only)

### Users
- `GET /users/` - List users (Admin only)
- `GET/POST /users/create/` - Create user (Admin only)
- `GET/POST /users/<id>/edit/` - Update user (Admin only)
- `GET/POST /users/<id>/delete/` - Delete user (Admin only)

### Reports
- `GET /reports/assets-by-location/` - Assets by location report
- `GET /reports/low-stock/` - Low stock items report

## Management Commands

### create_demo_data
Creates demo users, categories, and locations for testing.

```bash
python manage.py create_demo_data
```

### generate_assets_by_location_report
Generates asset inventory report by location.

```bash
python manage.py generate_assets_by_location_report --location 1 --format text
python manage.py generate_assets_by_location_report --format csv
```

### generate_low_stock_report
Generates low stock report.

```bash
python manage.py generate_low_stock_report --format text
python manage.py generate_low_stock_report --format csv
```

## Security Features

1. **Role-Based Access Control**: Views check user role before allowing access
2. **CSRF Protection**: All forms include CSRF tokens
3. **Password Hashing**: Passwords are hashed using Django's authentication system
4. **Audit Trail**: Assets track who created and updated them
5. **Session Management**: Django's session framework for secure user sessions

## Usage Examples

### Adding a New Asset
1. Login as Admin
2. Click "Assets" → "Add New Asset"
3. Fill in asset details:
   - Name: "Dell Inspiron Laptop"
   - Serial Number: "DEL-12345"
   - Category: "IT Equipment"
   - Location: "Office A"
   - Status: "Available"
   - Purchase Date: Select date
4. Click "Create Asset"

### Updating Asset Status (Manager)
1. Login as Manager
2. Go to Assets list
3. Click on specific asset
4. Click "Edit" button
5. Update only Status and Location fields
6. Click "Update Asset"

### Viewing Reports
1. Go to Dashboard or Reports menu
2. Select either "Assets by Location" or "Low Stock" report
3. For Assets by Location: Select a location to view all assets there
4. For Low Stock: See all categories below threshold
5. Click "Print Report" to print or export

## Troubleshooting

### Database Connection Error
- Ensure MySQL is running
- Verify credentials in `settings.py` DATABASES section
- Make sure database `inventory_db` exists

### "No module named" error
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`

### Static files not loading
- Run: `python manage.py collectstatic`

## Development

To run tests:
```bash
python manage.py test assets
```

To create a superuser:
```bash
python manage.py createsuperuser
```

To enter Django shell:
```bash
python manage.py shell
```

## Future Enhancements

- Barcode/QR code scanning
- Email notifications for low stock
- Advanced analytics and dashboards
- Asset depreciation tracking
- Maintenance schedules
- Multi-organization support
- API for mobile app
- Bulk import/export functionality

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please contact the administrator.

---

**Version**: 1.0.0  
**Last Updated**: February 24, 2026
