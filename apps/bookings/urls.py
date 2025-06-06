from django.urls import path
from .views import (
    BookingListCreateAPIView,
    BookingRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("bookings/", BookingListCreateAPIView.as_view(), name="booking-list-create"),
    path("bookings/<int:pk>/", BookingRetrieveUpdateDestroyAPIView.as_view(), name="booking-detail"),
]
