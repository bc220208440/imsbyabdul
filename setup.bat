@echo off
echo === Simple Inventory and Asset Management System – Setup ===

REM Create virtual environment if it does not exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists. Skipping creation.
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing Python dependencies from requirements.txt...
pip install -r requirements.txt

REM Apply database migrations
echo Applying database migrations...
python manage.py migrate

REM Create demo data (users, categories, locations)
echo Creating demo data (users, categories, locations)...
python manage.py create_demo_data

REM Start the development server
echo Starting Django development server at http://127.0.0.1:8000/ ...
python manage.py runserver

pause

