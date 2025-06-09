# tests/test_rooms.py
import pytest


@pytest.mark.django_db
def test_list_rooms_empty(api_client):
    """GET /api/rooms/ должен вернуть пустой список, если комнат нет."""
    response = api_client.get("/api/rooms/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_create_retrieve_update_delete_room(api_client):
    """Проверяем полный CRUD для Room."""
    # CREATE
    payload = {
        "number": "201",
        "room_type": "Suite",
        "price_per_night": "150.00",
        "capacity": 2,
        "description": "Test suite",
    }
    resp = api_client.post("/api/rooms/", payload, format="json")
    assert resp.status_code == 201
    data = resp.json()
    room_id = data["id"]
    assert data["number"] == "201"

    # RETRIEVE
    resp = api_client.get(f"/api/rooms/{room_id}/")
    assert resp.status_code == 200
    assert resp.json()["room_type"] == "Suite"

    # UPDATE (PATCH)
    update_payload = {"description": "Updated description"}
    resp = api_client.patch(f"/api/rooms/{room_id}/", update_payload, format="json")
    assert resp.status_code == 200
    assert resp.json()["description"] == "Updated description"

    # DELETE
    resp = api_client.delete(f"/api/rooms/{room_id}/")
    assert resp.status_code == 204

    # ENSURE GONE
    resp = api_client.get(f"/api/rooms/{room_id}/")
    assert resp.status_code == 404
