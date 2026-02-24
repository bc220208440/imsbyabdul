from django.core.management.base import BaseCommand
from django.db.models import Count
from assets.models import Asset, Category, Location


class Command(BaseCommand):
    """Management command to generate asset by location report"""
    help = 'Generate a report of assets by location'

    def add_arguments(self, parser):
        parser.add_argument(
            '--location',
            type=int,
            help='Location ID to filter by'
        )
        parser.add_argument(
            '--format',
            type=str,
            default='text',
            choices=['text', 'csv'],
            help='Output format (text or csv)'
        )

    def handle(self, *args, **options):
        location_id = options.get('location')
        output_format = options.get('format')

        if location_id:
            try:
                location = Location.objects.get(pk=location_id)
                assets = Asset.objects.filter(location=location).select_related('category')
            except Location.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Location with ID {location_id} not found'))
                return
        else:
            assets = Asset.objects.select_related('category', 'location').all()

        if output_format == 'csv':
            self._output_csv(assets, location_id)
        else:
            self._output_text(assets, location_id)

    def _output_text(self, assets, location_id=None):
        """Output report in text format"""
        if location_id:
            location = Location.objects.get(pk=location_id)
            self.stdout.write(self.style.SUCCESS(f'\n=== Assets at {location.name} ===\n'))
        else:
            self.stdout.write(self.style.SUCCESS('\n=== All Assets by Location ===\n'))

        if location_id:
            self._print_location_assets(assets)
        else:
            # Group by location
            locations = Location.objects.annotate(asset_count=Count('assets'))
            for location in locations:
                self.stdout.write(self.style.SUCCESS(f'\n{location.name} ({location.asset_count} items)\n'))
                location_assets = assets.filter(location=location)
                self._print_location_assets(location_assets)

    def _print_location_assets(self, assets):
        """Print assets in a formatted table"""
        for asset in assets:
            status_map = {
                'AVAILABLE': self.style.SUCCESS('Available'),
                'IN_USE': self.style.WARNING('In Use'),
                'IN_REPAIR': self.style.ERROR('In Repair'),
                'IN_STOCK': self.style.HTTP_INFO('In Stock'),
            }
            status_text = status_map.get(asset.status, asset.status)
            
            self.stdout.write(
                f'  • {asset.name}'
                f'\n    Serial: {asset.serial_number}'
                f'\n    Category: {asset.category.name}'
                f'\n    Status: {status_text}'
                f'\n'
            )

    def _output_csv(self, assets, location_id=None):
        """Output report in CSV format"""
        import csv
        import sys
        
        writer = csv.writer(self.stdout)
        writer.writerow(['Name', 'Serial Number', 'Category', 'Location', 'Status', 'Purchase Date'])
        
        for asset in assets:
            writer.writerow([
                asset.name,
                asset.serial_number,
                asset.category.name,
                asset.location.name if asset.location else 'N/A',
                asset.status,
                asset.purchase_date
            ])
