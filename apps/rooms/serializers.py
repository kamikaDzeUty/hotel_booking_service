# apps/rooms/serializers.py
from rest_framework import serializers

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "number", "room_type", "price_per_night", "capacity", "description"]
