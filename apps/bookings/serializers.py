from rest_framework import serializers

from .models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        # 1) проверяем, что даты заезда/выезда корректны
        check_in = data["check_in"]
        check_out = data["check_out"]
        if check_in >= check_out:
            raise serializers.ValidationError("Дата выезда должна быть позже даты заезда.")

        # 2) нет ли уже подтверждённых броней, пересекающихся по датам
        overlapping = Booking.objects.filter(
            room=data["room"],
            status="confirmed",
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()
        if overlapping:
            raise serializers.ValidationError("На эти даты уже есть подтверждённая бронь.")

        return data


class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["status"]
