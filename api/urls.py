from django.urls import path

from api.views import BookClassView, BookingListView, ClassCreateView, ClassListView

urlpatterns = [
    path("create-class/", ClassCreateView.as_view(), name="create-class"),
    path("classes/", ClassListView.as_view(), name="class-list"),
    path("book/", BookClassView.as_view(), name="book-class"),
    path("bookings/", BookingListView.as_view(), name="booking-list"),
]
