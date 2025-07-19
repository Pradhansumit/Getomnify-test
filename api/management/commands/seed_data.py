from datetime import datetime, timedelta

import pytz
from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import FitnessClass


class Command(BaseCommand):
    help = "Seed the database with sample fitness classes"

    def handle(self, *args, **options):
        # Clear existing data
        FitnessClass.objects.all().delete()
        self.stdout.write("Cleared existing fitness classes...")

        # Get IST timezone
        ist = pytz.timezone("Asia/Kolkata")

        # Start from tomorrow
        tomorrow = timezone.now().date() + timedelta(days=1)

        # Sample classes data
        classes_data = [
            {
                "name": "Yoga",
                "instructor": "Sarah Johnson",
                "total_slots": 20,
                "available_slots": 20,
                "time": "09:00",
            },
            {
                "name": "Zumba",
                "instructor": "Maria Rodriguez",
                "total_slots": 25,
                "available_slots": 25,
                "time": "10:30",
            },
            {
                "name": "HIIT",
                "instructor": "Mike Chen",
                "total_slots": 15,
                "available_slots": 15,
                "time": "14:00",
            },
            {
                "name": "Yoga",
                "instructor": "Priya Sharma",
                "total_slots": 18,
                "available_slots": 18,
                "time": "16:00",
            },
            {
                "name": "Zumba",
                "instructor": "Carlos Mendez",
                "total_slots": 22,
                "available_slots": 22,
                "time": "18:30",
            },
        ]

        # Create classes for the next 7 days
        created_count = 0
        for day_offset in range(7):
            current_date = tomorrow + timedelta(days=day_offset)

            for class_data in classes_data:
                # Parse time and create datetime
                time_parts = class_data["time"].split(":")
                hour, minute = int(time_parts[0]), int(time_parts[1])

                # Create naive datetime and localize to IST
                naive_datetime = datetime.combine(
                    current_date, datetime.min.time().replace(hour=hour, minute=minute)
                )
                ist_datetime = ist.localize(naive_datetime)

                # Create the fitness class
                fitness_class = FitnessClass.objects.create(
                    name=class_data["name"],
                    datetime_ist=ist_datetime,
                    instructor=class_data["instructor"],
                    total_slots=class_data["total_slots"],
                    available_slots=class_data["available_slots"],
                )
                created_count += 1

                self.stdout.write(
                    f"Created: {fitness_class.name} with {fitness_class.instructor} "
                    f"on {current_date.strftime('%Y-%m-%d')} at {class_data['time']}"
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} fitness classes!")
        )
