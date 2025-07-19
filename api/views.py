from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, FitnessClass
from .serializers import BookingSerializer, FitnessClassSerializer


class ClassCreateView(APIView):
    """
    Create a new fitness class.
    """

    def post(self, request):
        try:
            serializer = FitnessClassSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClassListView(APIView):
    """
    List all fitness classes that are scheduled to start in the future.
    """

    def get(self, request):
        now = timezone.now()
        classes = FitnessClass.objects.filter(datetime_ist__gte=now).order_by(
            "datetime_ist"
        )
        serializer = FitnessClassSerializer(
            classes, many=True, context={"request": request}
        )
        return Response(serializer.data)


class BookClassView(APIView):
    """
    Book a fitness class.
    """

    @transaction.atomic
    def post(self, request):
        data = request.data
        required_fields = ["class_id", "client_name", "client_email"]
        for field in required_fields:
            if field not in data:
                return Response(
                    {"error": f"Missing field: {field}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        try:
            fitness_class = FitnessClass.objects.select_for_update().get(
                id=data["class_id"]
            )
        except ObjectDoesNotExist:
            return Response(
                {"error": "Class not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if fitness_class.available_slots <= 0:
            return Response(
                {"error": "No slots available for this class."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Create booking
        booking = Booking(
            fitness_class=fitness_class,
            client_name=data["client_name"],
            client_email=data["client_email"],
        )
        booking.save()
        fitness_class.available_slots -= 1
        fitness_class.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookingListView(APIView):
    """
    List all bookings for a client. Using the email query parameter.
    """

    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response(
                {"error": "Missing email query parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        bookings = Booking.objects.filter(client_email=email).order_by("-booking_time")
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
