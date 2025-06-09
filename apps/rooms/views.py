# apps/rooms/views.py
from rest_framework import filters, generics

from .models import Room
from .serializers import RoomSerializer


class RoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price_per_night"]
    ordering = ["price_per_night"]


class RoomRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
