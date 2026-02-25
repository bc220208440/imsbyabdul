## Simple Inventory and Asset Management System – Compliance Audit

This document audits the current Django project against the provided specification for a **Simple Inventory and Asset Management System with Role-Based Access**. Each requirement is listed with an implementation reference and a compliance verdict.

---

### 1. Overall Goals

- **Requirement**: Web app to track assets (laptops, tools, furniture) for a small organization; core focus on CRUD, secure login, and enforcing business rules; uses a database.
- **Implementation**:
  - Django 6 project (`inventory_system`) using SQLite (`settings.DATABASES`).
  - `assets` app with models: `CustomUser`, `Category`, `Location`, `Asset` (`assets/models.py`).
  - Secure authentication with Django’s auth (`login_view`, `logout_view` in `assets/views.py`, `AUTH_USER_MODEL = 'assets.CustomUser'`).
  - Templates themed via `base.html` with consistent UI.
- **Verdict**: **Compliant**.

---

### 2. Users and Role-Based Authentication

#### 2.1 Roles: Admin, Manager, Viewer

- **Requirement**: Three roles with different capabilities.
- **Implementation**:
  - `CustomUser` model has `role` field with choices `ADMIN`, `MANAGER`, `VIEWER` (`assets/models.py`).
  - Management command `create_demo_data` seeds one user for each role (`admin`, `manager`, `viewer`) with appropriate flags.
- **Verdict**: **Compliant**.

#### 2.2 Admin Capabilities

- **Requirement**: Admin can view, add, edit, delete **all assets** and **user accounts** with no restrictions.
- **Implementation**:
  - Demo `admin` user is created as `is_staff=True`, `is_superuser=True` (`create_demo_data.py`), which grants all perms in Django.
  - Asset CRUD views:
    - `AssetListView`, `AssetDetailView` – `LoginRequiredMixin`, accessible to all authenticated roles for viewing.
    - `AssetCreateView` requires `permission_required = 'assets.add_asset'`.
    - `AssetUpdateView` requires `permission_required = 'assets.change_asset'`.
    - `AssetDeleteView` requires `permission_required = 'assets.delete_asset'`.
  - User management views:
    - `UserListView`, `UserCreateView`, `UserUpdateView`, `UserDeleteView` require `view/add/change/delete_customuser` perms.
  - As superuser, Admin has all these permissions and can fully manage assets and users.
- **Verdict**: **Compliant**.

#### 2.3 Manager Capabilities

- **Requirement**: Manager can view all assets and update **location and status**; cannot add or delete assets.
- **Implementation**:
  - Demo `manager` user:
    - Added to `Manager` group with perms `view_asset`, `change_asset`, `view_category`, `view_location` (`create_demo_data._setup_roles_permissions`).
  - `AssetUpdateView.get_form_class()`:
    - If the user **lacks** `assets.delete_asset` perm (true for Manager), uses `AssetUpdateStatusForm`.
    - `AssetUpdateStatusForm` only includes fields `status`, `location`, `notes` (`assets/forms.py`).
  - `asset_form.html` uses `status_only` context (set in `AssetUpdateView.get_context_data`) to hide all other input fields (name, serial number, category, quantity, purchase date, price) when a Manager edits.
  - No `add_asset` or `delete_asset` permission is assigned to the Manager group, so any attempt to create or delete assets via class-based views is blocked by `PermissionRequiredMixin`.
- **Verdict**: **Compliant**.

#### 2.4 Viewer Capabilities

- **Requirement**: Viewer can access list of assets and details; assets must be read-only.
- **Implementation**:
  - Demo `viewer` user is in `Viewer` group with only `view_asset`, `view_category`, `view_location` permissions.
  - They lack `add/change/delete_asset`, so:
    - `AssetCreateView`, `AssetUpdateView`, `AssetDeleteView` deny access (403) via `PermissionRequiredMixin`.
  - UI:
    - In `asset_list.html`, Edit/Delete buttons are only shown when `user.role == 'ADMIN' or user.role == 'MANAGER'` (Edit) or `user.role == 'ADMIN'` (Delete).
    - In `asset_detail.html`, buttons are controlled by `can_edit`/`can_delete` flags from `AssetDetailView`, which use both the role and Django permissions.
- **Verdict**: **Compliant**.

---

### 3. Asset Management (CRUD)

#### 3.1 Create

- **Requirement**: New assets must be added **by Admins** with: Name, Serial Number, Category, Purchase Date, Initial Location.
- **Implementation**:
  - `Asset` model fields: `name`, `serial_number`, `category` (FK to `Category`), `purchase_date` (DateField), `location` (FK to `Location`) and others (`status`, `quantity`, etc.).
  - `AssetForm` includes these fields.
  - `AssetCreateView` requires `assets.add_asset`; effectively only Admin (superuser) has this permission by default.
  - The form requires category and purchase date; location can be chosen from predefined locations, satisfying initial location assignment.
- **Verdict**: **Compliant**.

#### 3.2 Read

- **Requirement**: List of assets accessible to all users; support search options.
- **Implementation**:
  - `AssetListView` (login required) shows all assets, paginated, for all authenticated roles.
  - `AssetSearchForm` supports:
    - `search` text with `search_type` = all / name / serial.
    - `category` filter (ModelChoice).
    - `location` filter (ModelChoice).
    - `status` filter.
  - `AssetListView.get_queryset()` applies these filters and is rendered in `asset_list.html`.
- **Verdict**: **Compliant**.

#### 3.3 Update

- **Requirement**: Update location and status (e.g., In Use, In Repair, In Stock, Available); only Admins and Managers can change status.
- **Implementation**:
  - `Asset.STATUS_CHOICES` includes `AVAILABLE`, `IN_USE`, `IN_REPAIR`, `IN_STOCK`.
  - `AssetUpdateView` requires `change_asset`; both Admin and Manager have that permission.
  - Managers are restricted to `AssetUpdateStatusForm` (status, location, notes) – enforced server-side by `get_form_class` and template logic.
  - Admins get the full `AssetForm` and can change all details.
- **Verdict**: **Compliant**.

#### 3.4 Delete

- **Requirement**: Only Admin can permanently delete assets.
- **Implementation**:
  - `AssetDeleteView` requires `assets.delete_asset`. Only Admin (superuser) has this permission by default.
  - UI hides Delete buttons for non-admins (`asset_list.html`, `asset_detail.html`).
  - Delete confirmation template `asset_confirm_delete.html` is only reachable when permission checks pass.
- **Verdict**: **Compliant**.

#### 3.5 Predetermined Categories

- **Requirement**: System must use predetermined list of categories (IT Equipment, Office Furniture, Tools, etc.); Admin can control this list.
- **Implementation**:
  - `Category` model with `name`, `description`, `low_stock_threshold`.
  - `create_demo_data` seeds categories: “IT Equipment”, “Office Furniture”, “Tools”, “Miscellaneous”.
  - Category CRUD views:
    - `CategoryListView`, `CategoryCreateView`, `CategoryUpdateView`, `CategoryDeleteView`.
    - All create/update/delete views require corresponding `assets.add_category`, `change_category`, `delete_category` permissions, effectively restricted to Admin.
  - Asset creation uses a foreign key to `Category`, so only predefined categories may be chosen.
- **Verdict**: **Compliant**.

---

### 4. Category Management

- **Requirement**:
  - Use defined list of asset categories.
  - Admins manage this list.
- **Implementation**:
  - See 3.5 above for model and CRUD.
  - `CategoryListView.get_queryset()` annotates `asset_count` and `available_count` for better overview in `category_list.html`.
  - `category_list.html` shows Add/Edit/Delete buttons only when `user.role == 'ADMIN'`.
- **Verdict**: **Compliant**.

---

### 5. Search and Filtering

- **Requirement**: Users can search asset list by Name, Serial Number, or Category; filter by Status and Location.
- **Implementation**:
  - `AssetSearchForm` fields:
    - `search` (text input).
    - `search_type` (`all`, `name`, `serial`).
    - `category` (ModelChoice to `Category`).
    - `location` (ModelChoice to `Location`).
    - `status` (Choice: all + `Asset.STATUS_CHOICES`).
  - `AssetListView.get_queryset()`:
    - If `search_type == 'name'`, filters `name__icontains`.
    - If `search_type == 'serial'`, filters `serial_number__icontains`.
    - Else (all), filters `name`, `serial_number`, or `category__name`.
    - Applies optional `category`, `location`, and `status` filters when provided.
  - `asset_list.html` wires all form fields into a filter bar and provides Reset.
- **Verdict**: **Compliant**.

---

### 6. Location Tracking

- **Requirement**: Assets must be assigned to a predefined list of locations (e.g., Office A, Warehouse 1, Remote Employee). Managers and Admins can update assignment.
- **Implementation**:
  - `Location` model defines locations; `create_demo_data` seeds “Office A”, “Warehouse 1”, “Remote Employee”.
  - `Asset.location` is an FK to `Location`; all location choices come from this table.
  - Location CRUD:
    - `LocationListView`, `LocationCreateView`, `LocationUpdateView`, `LocationDeleteView`.
    - Create/update/delete views require `add/change/delete_location` permissions (Admin effectively).
  - Updates:
    - Admin via full `AssetForm`.
    - Manager via `AssetUpdateStatusForm` (includes `location`).
- **Verdict**: **Compliant**.

---

### 7. Basic Reports

#### 7.1 Assets by Location

- **Requirement**: Printable/exportable report listing all assets for a specific location.
- **Implementation**:
  - `AssetsByLocationReportView`:
    - Uses `Location.objects.annotate(asset_count=Count("assets"))`.
    - When a location is selected, filters `Asset.objects.filter(location=location)` with `select_related`.
    - Renders `report_assets_by_location.html`.
  - Template features:
    - Location selection form.
    - Table listing assets with name, serial, category, status, purchase date.
    - **Print** button (`window.print()`).
    - **Export CSV** link to `ExportAssetsByLocationCSV`.
  - `ExportAssetsByLocationCSV`:
    - Generates CSV with columns: Name, Serial Number, Category, Status, Purchase Date.
- **Verdict**: **Compliant**.

#### 7.2 Low Stock

- **Requirement**: Printable/exportable report of categories where available quantity is **below threshold** (e.g., fewer than 5 available laptops).
- **Implementation**:
  - Each `Category` has `low_stock_threshold` (default 5).
  - `LowStockReportView`:
    - For each `Category`, computes `available_quantity` as the sum of `quantity` for assets with `status="AVAILABLE"`.
    - If `available_quantity < low_stock_threshold`, adds to `low_stock_items` context with `deficit`.
    - Renders `report_low_stock.html`.
  - Template features:
    - Card per low-stock category, showing available, threshold, deficit, and sample assets.
    - **Print** button.
    - **Export CSV** link (`ExportLowStockCSV`).
  - `ExportLowStockCSV`:
    - Iterates categories, computes available quantity, and writes rows only where `available < threshold`.
- **Verdict**: **Compliant**.

---

### 8. Security and Data Integrity Notes

- **Authentication & Sessions**:
  - Uses Django’s built-in authentication middleware; login required for all app features (dashboard, assets, categories, locations, reports, users).
- **Authorization**:
  - Role stored on `CustomUser`, but **critical checks** are done via Django permissions (`PermissionRequiredMixin`, `has_perm`) rather than only checking `role` in templates.
  - Actions like create/update/delete assets, categories, locations, and users are protected at the view level.
- **Database Constraints**:
  - `Asset.serial_number` is unique, enforcing structured inventory.
  - `category` uses `on_delete=PROTECT` to avoid orphaned assets when categories are in use.
  - `location` uses `SET_NULL` so moving/deleting locations doesn’t silently cascade-delete assets.

**Verdict**: The project **fully implements** the required security model and business rules using Django’s auth, role field, and permissions.

---

### 9. Summary Verdict

After auditing models, views, forms, templates, and the demo-data management command, the system:

- Implements all three roles with correct, enforced capabilities.
- Provides complete CRUD for assets, with role-based restrictions exactly as specified.
- Uses predefined, admin-controlled categories and locations.
- Offers robust search/filtering on assets (name, serial, category, status, location).
- Tracks locations and allows Admin/Manager to update asset assignments.
- Delivers both required reports (Assets by Location, Low Stock) with **print and CSV export**.

**Overall conclusion**: The current project **matches the provided specification** for the Simple Inventory and Asset Management System with Role-Based Access. No critical gaps were identified in relation to the stated functional requirements.

