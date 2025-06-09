# tests/test_bookings.py
import pytest


@pytest.mark.django_db
def test_booking_crud_and_overlap(api_client):
    """Базовый CRUD и overlap-валидация (как было)."""
    # создаём комнату
    room = api_client.post(
        "/api/rooms/",
        {
            "number": "301",
            "room_type": "Deluxe",
            "price_per_night": "200.00",
            "capacity": 3,
            "description": "Test room",
        },
        format="json",
    ).json()
    room_id = room["id"]

    # пусто
    resp = api_client.get("/api/bookings/")
    assert resp.status_code == 200
    assert resp.json() == []

    # корректная бронь
    booking = api_client.post(
        "/api/bookings/",
        {
            "room": room_id,
            "guest_name": "Alice",
            "check_in": "2025-07-01",
            "check_out": "2025-07-05",
            "status": "confirmed",
        },
        format="json",
    ).json()
    booking_id = booking["id"]

    # overlap должен падать
    resp = api_client.post(
        "/api/bookings/",
        {
            "room": room_id,
            "guest_name": "Bob",
            "check_in": "2025-07-03",
            "check_out": "2025-07-06",
            "status": "confirmed",
        },
        format="json",
    )
    assert resp.status_code == 400

    # retrieve, patch status, delete (как было)
    assert api_client.get(f"/api/bookings/{booking_id}/").status_code == 200
    assert (
        api_client.patch(f"/api/bookings/{booking_id}/", {"status": "canceled"}, format="json").status_code == 200
    )
    assert api_client.delete(f"/api/bookings/{booking_id}/").status_code == 204


@pytest.mark.django_db
def test_create_booking_invalid_dates(api_client):
    """POST /api/bookings/ с check_in >= check_out → 400."""
    # комната
    room_id = api_client.post(
        "/api/rooms/",
        {
            "number": "302",
            "room_type": "Standard",
            "price_per_night": "100.00",
            "capacity": 2,
            "description": "Test room 2",
        },
        format="json",
    ).json()["id"]

    # неверные даты
    resp = api_client.post(
        "/api/bookings/",
        {
            "room": room_id,
            "guest_name": "Charlie",
            "check_in": "2025-08-10",
            "check_out": "2025-08-05",
            "status": "confirmed",
        },
        format="json",
    )
    assert resp.status_code == 400
    errors = resp.json().get("non_field_errors", [])
    assert "Дата выезда должна быть позже даты заезда." in errors


@pytest.mark.django_db
def test_put_booking_full_update_and_overlap(api_client):
    """PUT обновляет даты, и overlap при подтверждении блокируется."""
    # создаём комнату
    room_id = api_client.post(
        "/api/rooms/",
        {
            "number": "303",
            "room_type": "Economy",
            "price_per_night": "80.00",
            "capacity": 2,
            "description": "Test room 3",
        },
        format="json",
    ).json()["id"]

    # базовая бронь
    api_client.post(
        "/api/bookings/",
        {
            "room": room_id,
            "guest_name": "Dana",
            "check_in": "2025-09-01",
            "check_out": "2025-09-05",
            "status": "confirmed",
        },
        format="json",
    ).json()

    # создаём вторую бронь в режиме pending
    b2 = api_client.post(
        "/api/bookings/",
        {
            "room": room_id,
            "guest_name": "Eve",
            "check_in": "2025-09-06",
            "check_out": "2025-09-10",
            "status": "pending",
        },
        format="json",
    ).json()
    b2_id = b2["id"]

    # PUT переводит pending → confirmed на пересекающиеся даты → 400
    resp = api_client.put(
        f"/api/bookings/{b2_id}/",
        {
            "room": room_id,
            "guest_name": "Eve",
            "check_in": "2025-09-03",
            "check_out": "2025-09-07",
            "status": "confirmed",
        },
        format="json",
    )
    assert resp.status_code == 400

    # но если даты не пересекаются и статус confirmed → 200
    resp = api_client.put(
        f"/api/bookings/{b2_id}/",
        {
            "room": room_id,
            "guest_name": "Eve",
            "check_in": "2025-09-10",
            "check_out": "2025-09-12",
            "status": "confirmed",
        },
        format="json",
    )
    assert resp.status_code == 200
    assert resp.json()["check_in"] == "2025-09-10"


@pytest.mark.django_db
def test_create_pending_booking_allows_overlap(api_client):
    """pending-бронь может пересекаться с confirmed."""
    room_id = api_client.post(
        "/api/rooms/",
        {
            "number": "304",
            "room_type": "Suite",
            "price_per_night": "300.00",
            "capacity": 4,
            "description": "Suite room",
        },
        format="json",
    ).json()["id"]

    # confirmed
    api_client.post(
        "/api/bookings/",
        {
            "room": room_id,
            "guest_name": "Frank",
            "check_in": "2025-10-01",
            "check_out": "2025-10-05",
            "status": "confirmed",
        },
        format="json",
    )

    # pending на пересекающиеся даты
    resp = api_client.post(
        "/api/bookings/",
        {
            "room": room_id,
            "guest_name": "Grace",
            "check_in": "2025-10-03",
            "check_out": "2025-10-06",
            "status": "pending",
        },
        format="json",
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_delete_nonexistent_booking_and_room(api_client):
    """DELETE /nonexistent → 404."""
    assert api_client.delete("/api/bookings/9999/").status_code == 404
    assert api_client.delete("/api/rooms/9999/").status_code == 404


@pytest.mark.django_db
def test_bookings_filter_and_order(api_client):
    # создаём комнату
    room = api_client.post(
        "/api/rooms/",
        {"number": "701", "room_type": "X", "price_per_night": "70.00", "capacity": 1, "description": ""},
        format="json",
    ).json()
    room_id = room["id"]

    # три бронирования с разными датами
    dates = ["2025-10-15", "2025-09-01", "2025-11-05"]
    for d in dates:
        api_client.post(
            "/api/bookings/",
            {"room": room_id, "guest_name": "A", "check_in": d, "check_out": "2025-12-01", "status": "confirmed"},
            format="json",
        )

    # фильтр по комнате и сортировка по check_in (по умолчанию)
    resp = api_client.get(f"/api/bookings/?room={room_id}")
    ci_list = [b["check_in"] for b in resp.json()]
    assert ci_list == sorted(ci_list)
