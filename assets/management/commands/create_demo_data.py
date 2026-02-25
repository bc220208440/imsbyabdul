from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from assets.models import Category, Location

User = get_user_model()


class Command(BaseCommand):
    """Management command to create demo data"""
    help = 'Create demo users, categories, and locations for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating demo data...\n'))

        self._create_demo_users()

        self._create_demo_categories()

        self._create_demo_locations()

        self._setup_roles_permissions()

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

    def _setup_roles_permissions(self):
        perms_map = {
            'Viewer': [
                'view_asset',
                'view_category',
                'view_location',
            ],
            'Manager': [
                'view_asset',
                'change_asset',
                'view_category',
                'view_location',
            ],
        }

        def get_perms(codenames):
            return list(
                Permission.objects.filter(
                    codename__in=codenames,
                    content_type__app_label='assets',
                )
            )

        viewer_group, _ = Group.objects.get_or_create(name='Viewer')
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        viewer_group.permissions.set(get_perms(perms_map['Viewer']))
        manager_group.permissions.set(get_perms(perms_map['Manager']))

        try:
            admin_user = User.objects.get(username='admin')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
        except User.DoesNotExist:
            pass

        try:
            manager_user = User.objects.get(username='manager')
            manager_user.groups.clear()
            manager_user.groups.add(manager_group)
            manager_user.save()
            self.stdout.write('  ✓ Ensured permissions for user: manager (Manager group)')
        except User.DoesNotExist:
            pass

        try:
            viewer_user = User.objects.get(username='viewer')
            viewer_user.groups.clear()
            viewer_user.groups.add(viewer_group)
            viewer_user.save()
            self.stdout.write('  ✓ Ensured permissions for user: viewer (Viewer group)')
        except User.DoesNotExist:
            pass
