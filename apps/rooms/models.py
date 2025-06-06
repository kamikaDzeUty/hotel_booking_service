from django.db import models

class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Room {self.number} ({self.room_type})"
