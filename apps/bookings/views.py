# apps/bookings/views.py
from rest_framework import filters, generics
from rest_framework.exceptions import ValidationError

from .models import Booking
from .serializers import BookingSerializer


class BookingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["check_in"]
    ordering = ["check_in"]

    def get_queryset(self):
        qs = super().get_queryset()
        room_id = self.request.query_params.get("room")
        if room_id:
            qs = qs.filter(room_id=room_id)
        return qs

    def perform_create(self, serializer):
        data = serializer.validated_data
        check_in = data["check_in"]
        check_out = data["check_out"]
        room = data["room"]
        status = data["status"]

        # 1) порядок дат
        if check_in >= check_out:
            raise ValidationError({"non_field_errors": ["Дата выезда должна быть позже даты заезда."]})

        # 2) overlap только для confirmed
        if status == "confirmed":
            conflict = Booking.objects.filter(
                room=room,
                status="confirmed",
                check_in__lt=check_out,
                check_out__gt=check_in,
            ).exists()
            if conflict:
                raise ValidationError({"non_field_errors": ["На эти даты уже есть подтверждённая бронь."]})

        serializer.save()


class BookingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_update(self, serializer):
        instance = self.get_object()
        data = serializer.validated_data

        # новые или старые значения
        check_in = data.get("check_in", instance.check_in)
        check_out = data.get("check_out", instance.check_out)
        room = data.get("room", instance.room)
        status = data.get("status", instance.status)

        # 1) порядок дат
        if check_in >= check_out:
            raise ValidationError({"non_field_errors": ["Дата выезда должна быть позже даты заезда."]})

        # 2) overlap только для confirmed
        if status == "confirmed":
            qs = Booking.objects.filter(
                room=room,
                status="confirmed",
                check_in__lt=check_out,
                check_out__gt=check_in,
            ).exclude(pk=instance.pk)
            if qs.exists():
                raise ValidationError({"non_field_errors": ["На эти даты уже есть подтверждённая бронь."]})

        serializer.save()
