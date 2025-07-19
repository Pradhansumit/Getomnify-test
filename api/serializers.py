from rest_framework import serializers

from .models import Booking, FitnessClass


class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = [
            "id",
            "name",
            "datetime_ist",
            "instructor",
            "total_slots",
            "available_slots",
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "fitness_class", "client_name", "client_email", "booking_time"]
        read_only_fields = ["booking_time"]
