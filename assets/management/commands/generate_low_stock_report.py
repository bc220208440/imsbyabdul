from django.core.management.base import BaseCommand
from assets.models import Asset, Category


class Command(BaseCommand):
    """Management command to generate low stock report"""
    help = 'Generate a report of items with low stock levels'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            type=str,
            default='text',
            choices=['text', 'csv'],
            help='Output format (text or csv)'
        )

    def handle(self, *args, **options):
        output_format = options.get('format')
        low_stock_items = []

        # Find categories with low stock
        for category in Category.objects.all():
            available_count = category.assets.filter(status='AVAILABLE').count()
            if available_count < category.low_stock_threshold:
                low_stock_items.append({
                    'category': category,
                    'available': available_count,
                    'threshold': category.low_stock_threshold,
                    'deficit': category.low_stock_threshold - available_count,
                    'assets': category.assets.filter(status='AVAILABLE')
                })

        if output_format == 'csv':
            self._output_csv(low_stock_items)
        else:
            self._output_text(low_stock_items)

    def _output_text(self, low_stock_items):
        """Output report in text format"""
        if not low_stock_items:
            self.stdout.write(self.style.SUCCESS('\n=== Low Stock Report ===\n'))
            self.stdout.write(self.style.SUCCESS('All categories are stocked!'))
            return

        self.stdout.write(self.style.SUCCESS('\n=== Low Stock Report ===\n'))
        self.stdout.write(self.style.WARNING(f'Found {len(low_stock_items)} categories with low stock\n'))

        for item in low_stock_items:
            self.stdout.write(self.style.ERROR(f'\n{item["category"].name}'))
            self.stdout.write(
                f'  Available: {item["available"]} / Threshold: {item["threshold"]}\n'
                f'  Deficit: {item["deficit"]} unit(s)\n'
            )
            
            self.stdout.write('  Available Assets:')
            for asset in item['assets']:
                self.stdout.write(f'    • {asset.name} ({asset.serial_number})')

    def _output_csv(self, low_stock_items):
        """Output report in CSV format"""
        import csv
        
        writer = csv.writer(self.stdout)
        writer.writerow(['Category', 'Available', 'Threshold', 'Deficit', 'Asset Name', 'Serial Number'])
        
        for item in low_stock_items:
            category_name = item['category'].name
            available = item['available']
            threshold = item['threshold']
            deficit = item['deficit']
            
            if item['assets']:
                for asset in item['assets']:
                    writer.writerow([
                        category_name,
                        available,
                        threshold,
                        deficit,
                        asset.name,
                        asset.serial_number
                    ])
            else:
                writer.writerow([
                    category_name,
                    available,
                    threshold,
                    deficit,
                    'N/A',
                    'N/A'
                ])
