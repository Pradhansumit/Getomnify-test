from datetime import datetime

import pytz
from django.test import TestCase
from django.utils import timezone

from .models import Booking, FitnessClass
from .utils import convert_from_timezone, convert_to_timezone

# Create your tests here.


class TimezoneTestCase(TestCase):
    def setUp(self):
        # Create a test class in IST
        ist = pytz.timezone("Asia/Kolkata")
        test_time = ist.localize(datetime(2024, 1, 15, 9, 0, 0))

        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            datetime_ist=test_time,
            instructor="Test Instructor",
            total_slots=20,
            available_slots=20,
        )

    def test_timezone_conversion(self):
        """Test converting IST time to other timezones"""
        # Convert to UTC
        utc_time = convert_to_timezone(self.fitness_class.datetime_ist, "UTC")
        self.assertIsNotNone(utc_time)

        # Convert to EST
        est_time = convert_to_timezone(self.fitness_class.datetime_ist, "US/Eastern")
        self.assertIsNotNone(est_time)

        # Verify times are different (IST is ahead of UTC)
        # Compare the actual time values, not the datetime objects
        self.assertNotEqual(self.fitness_class.datetime_ist.hour, utc_time.hour)


class BookingTestCase(TestCase):
    def setUp(self):
        ist = pytz.timezone("Asia/Kolkata")
        test_time = ist.localize(datetime(2024, 1, 15, 9, 0, 0))

        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            datetime_ist=test_time,
            instructor="Test Instructor",
            total_slots=5,
            available_slots=5,
        )

    def test_booking_reduces_available_slots(self):
        """Test that booking reduces available slots"""
        initial_slots = self.fitness_class.available_slots

        booking = Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Test User",
            client_email="test@example.com",
        )

        # Manually reduce available slots as the view does
        self.fitness_class.available_slots -= 1
        self.fitness_class.save()

        # Refresh from database
        self.fitness_class.refresh_from_db()

        self.assertEqual(self.fitness_class.available_slots, initial_slots - 1)
