# tests/test_bookings.py
import pytest


@pytest.mark.django_db
def test_booking_crud_and_overlap(api_client):
    """CRUD и валидация перекры тия броней."""
    # создаём комнату для брони
    room_payload = {
        "number": "301",
        "room_type": "Deluxe",
        "price_per_night": "200.00",
        "capacity": 3,
        "description": "Test booking room",
    }
    room_resp = api_client.post("/api/rooms/", room_payload, format="json")
    room_id = room_resp.json()["id"]

    # пустой список броней
    resp = api_client.get("/api/bookings/")
    assert resp.status_code == 200
    assert resp.json() == []

    # создаём валидную бронь
    booking_payload = {
        "room": room_id,
        "guest_name": "Alice",
        "check_in": "2025-07-01",
        "check_out": "2025-07-05",
        "status": "confirmed",
    }
    resp = api_client.post("/api/bookings/", booking_payload, format="json")
    assert resp.status_code == 201
    booking_id = resp.json()["id"]

    # пересекающаяся бронь должна упасть
    overlap_payload = {
        "room": room_id,
        "guest_name": "Bob",
        "check_in": "2025-07-03",
        "check_out": "2025-07-06",
        "status": "confirmed",
    }
    resp = api_client.post("/api/bookings/", overlap_payload, format="json")
    assert resp.status_code == 400
    assert "На эти даты уже есть подтверждённая бронь." in resp.json().get("non_field_errors", [])

    # читаем бронь
    resp = api_client.get(f"/api/bookings/{booking_id}/")
    assert resp.status_code == 200
    assert resp.json()["guest_name"] == "Alice"

    # обновляем статус
    resp = api_client.patch(f"/api/bookings/{booking_id}/", {"status": "canceled"}, format="json")
    assert resp.status_code == 200
    assert resp.json()["status"] == "canceled"

    # удаляем бронь
    resp = api_client.delete(f"/api/bookings/{booking_id}/")
    assert resp.status_code == 204

    # проверяем, что бронь удалена
    resp = api_client.get(f"/api/bookings/{booking_id}/")
    assert resp.status_code == 404
