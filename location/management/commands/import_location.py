import os
import csv
from django.core.management.base import BaseCommand, CommandError
from location.models import County, SubCounty, Ward
from django.conf import settings

class Command(BaseCommand):
    help = 'Import counties, sub-counties, and wards from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='The path to the CSV file containing locations',
            default=os.path.join(settings.BASE_DIR, 'locations.csv')
        )

    def handle(self, *args, **options):
        file_path = options['file']

        if not os.path.exists(file_path):
            raise CommandError(f"CSV file not found at {file_path}")

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                county_name = row['county'].strip()
                sub_county_name = row['sub_county'].strip()
                ward_name = row['ward'].strip()

                county, _ = County.objects.get_or_create(name=county_name)
                sub_county, _ = SubCounty.objects.get_or_create(name=sub_county_name, county=county)
                Ward.objects.get_or_create(name=ward_name, sub_county=sub_county)
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} location records'))
