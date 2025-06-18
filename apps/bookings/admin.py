# apps/bookings/admin.py
from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "guest_name", "check_in", "check_out", "status")
