from django.db import models
from django.utils import timezone


class FitnessClass(models.Model):
    CLASS_CHOICES = [
        ("Yoga", "Yoga"),
        ("Zumba", "Zumba"),
        ("HIIT", "HIIT"),
    ]
    name = models.CharField(max_length=50, choices=CLASS_CHOICES)
    datetime_ist = models.DateTimeField(help_text="Class time in IST")
    instructor = models.CharField(max_length=100)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} with {self.instructor} at {self.datetime_ist}"


class Booking(models.Model):
    fitness_class = models.ForeignKey(
        FitnessClass, on_delete=models.CASCADE, related_name="bookings"
    )
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booking_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name} ({self.client_email})"
