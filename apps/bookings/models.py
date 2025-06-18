# apps/bookings/models.py
from django.db import models

from apps.rooms.models import Room


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("canceled", "Canceled"),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    guest_name = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_name} → Room {self.room.number} ({self.check_in} – {self.check_out})"
