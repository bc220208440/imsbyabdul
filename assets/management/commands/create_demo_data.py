from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from assets.models import Category, Location

User = get_user_model()


class Command(BaseCommand):
    """Management command to create demo data"""
    help = 'Create demo users, categories, and locations for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating demo data...\n'))

        # Create demo users
        self._create_demo_users()

        # Create demo categories
        self._create_demo_categories()

        # Create demo locations
        self._create_demo_locations()

        self.stdout.write(self.style.SUCCESS('\nDemo data created successfully!'))

    def _create_demo_users(self):
        """Create demo users with different roles"""
        users_data = [
            {
                'username': 'admin',
                'password': 'password',
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'ADMIN',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'manager',
                'password': 'password',
                'email': 'manager@example.com',
                'first_name': 'Manager',
                'last_name': 'User',
                'role': 'MANAGER',
                'is_staff': False,
            },
            {
                'username': 'viewer',
                'password': 'password',
                'email': 'viewer@example.com',
                'first_name': 'Viewer',
                'last_name': 'User',
                'role': 'VIEWER',
                'is_staff': False,
            },
        ]

        for user_data in users_data:
            username = user_data.pop('username')
            password = user_data.pop('password')
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    **user_data
                )
                self.stdout.write(f'  ✓ Created {user.role} user: {username}')
            else:
                self.stdout.write(f'  → User {username} already exists')

    def _create_demo_categories(self):
        """Create demo asset categories"""
        categories_data = [
            {
                'name': 'IT Equipment',
                'description': 'Computers, laptops, servers, and networking equipment',
                'low_stock_threshold': 5,
            },
            {
                'name': 'Office Furniture',
                'description': 'Desks, chairs, cabinets, and office fixtures',
                'low_stock_threshold': 3,
            },
            {
                'name': 'Tools',
                'description': 'Hand tools, power tools, and equipment',
                'low_stock_threshold': 5,
            },
            {
                'name': 'Miscellaneous',
                'description': 'Other items and equipment',
                'low_stock_threshold': 2,
            },
        ]

        for cat_data in categories_data:
            name = cat_data['name']
            if not Category.objects.filter(name=name).exists():
                Category.objects.create(**cat_data)
                self.stdout.write(f'  ✓ Created category: {name}')
            else:
                self.stdout.write(f'  → Category {name} already exists')

    def _create_demo_locations(self):
        """Create demo storage locations"""
        locations_data = [
            {
                'name': 'Office A',
                'description': 'Main office building',
            },
            {
                'name': 'Warehouse 1',
                'description': 'Primary storage warehouse',
            },
            {
                'name': 'Remote Employee',
                'description': 'Assets for remote workers',
            },
        ]

        for loc_data in locations_data:
            name = loc_data['name']
            if not Location.objects.filter(name=name).exists():
                Location.objects.create(**loc_data)
                self.stdout.write(f'  ✓ Created location: {name}')
            else:
                self.stdout.write(f'  → Location {name} already exists')
