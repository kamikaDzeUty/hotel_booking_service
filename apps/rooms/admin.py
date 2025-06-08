from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "room_type", "price_per_night", "capacity")
