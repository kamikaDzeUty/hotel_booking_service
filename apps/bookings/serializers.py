from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "room",
            "guest_name",
            "check_in",
            "check_out",
            "status",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate(self, data):
        check_in = data.get("check_in")
        check_out = data.get("check_out")
        room = data.get("room")

        # 1) check_in < check_out
        if check_in >= check_out:
            raise serializers.ValidationError(
                "Дата выезда должна быть позже даты заезда."
            )

        # 2) проверка на пересечение с уже подтверждёнными бронями
        overlapping = Booking.objects.filter(
            room=room,
            status="confirmed",
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()

        if overlapping:
            raise serializers.ValidationError(
                "На эти даты уже есть подтверждённая бронь."
            )

        return data
