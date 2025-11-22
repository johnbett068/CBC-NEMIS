import os
import csv
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from location.models import County, SubCounty, Ward


class Command(BaseCommand):
    help = "Import counties, sub-counties, and wards from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Path to locations.csv file",
            default=os.path.join(settings.BASE_DIR, "locations.csv")
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        if not os.path.exists(file_path):
            raise CommandError(f"CSV file not found at: {file_path}")

        self.stdout.write(self.style.NOTICE(f"Importing locations from {file_path}..."))

        created_count = 0

        with open(file_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                county_name = (row.get("county") or "").strip()
                subcounty_name = (row.get("sub_county") or "").strip()
                ward_name = (row.get("ward") or "").strip()

                if not county_name:
                    continue

                # Create County
                county, _ = County.objects.get_or_create(name=county_name)

                # Create SubCounty
                if subcounty_name:
                    subcounty, _ = SubCounty.objects.get_or_create(
                        name=subcounty_name,
                        county=county
                    )
                else:
                    subcounty = None

                # Create Ward (correct field name: sub_county)
                if subcounty and ward_name:
                    Ward.objects.get_or_create(
                        name=ward_name,
                        sub_county=subcounty
                    )

                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {created_count} location rows")
        )
