from rest_framework import viewsets

from .models import Booking
from .serializers import BookingCreateSerializer, BookingStatusSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()

    def get_serializer_class(self):
        # при создании используем проверяющий даты сериализатор
        if self.action == "create":
            return BookingCreateSerializer
        # при обновлении статуса — лёгкий сериализатор только с полем status
        if self.action in ("update", "partial_update"):
            return BookingStatusSerializer
        # для list и retrieve можно снова вернуть полный сериализатор
        return BookingCreateSerializer
