from rest_framework import serializers

from .models import Booking, FitnessClass
from .utils import convert_from_timezone, convert_to_timezone


class FitnessClassSerializer(serializers.ModelSerializer):
    datetime_local = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = [
            "id",
            "name",
            "datetime_ist",
            "datetime_local",
            "instructor",
            "total_slots",
            "available_slots",
        ]

    def get_datetime_local(self, obj):
        """Convert IST datetime to user's timezone or default to UTC"""
        request = self.context.get("request")
        if request and hasattr(request, "query_params"):
            timezone_param = request.query_params.get("timezone", "UTC")
            try:
                return convert_to_timezone(obj.datetime_ist, timezone_param)
            except:
                return convert_to_timezone(obj.datetime_ist, "UTC")
        return convert_to_timezone(obj.datetime_ist, "UTC")


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "fitness_class", "client_name", "client_email", "booking_time"]
        read_only_fields = ["booking_time"]
