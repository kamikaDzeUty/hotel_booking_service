# apps/bookings/serializers.py
from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "room", "guest_name", "check_in", "check_out", "status", "created_at"]
        read_only_fields = ["id", "created_at"]
