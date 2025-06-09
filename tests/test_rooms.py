# tests/test_rooms.py
import pytest


@pytest.mark.django_db
def test_list_rooms_empty(api_client):
    """GET /api/rooms/ пусто."""
    response = api_client.get("/api/rooms/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_create_retrieve_update_delete_room(api_client):
    """CRUD через POST, GET, PATCH, DELETE."""
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
    room_id = resp.json()["id"]

    # RETRIEVE
    resp = api_client.get(f"/api/rooms/{room_id}/")
    assert resp.status_code == 200
    assert resp.json()["room_type"] == "Suite"

    # UPDATE (PATCH)
    resp = api_client.patch(f"/api/rooms/{room_id}/", {"description": "Updated description"}, format="json")
    assert resp.status_code == 200
    assert resp.json()["description"] == "Updated description"

    # DELETE
    resp = api_client.delete(f"/api/rooms/{room_id}/")
    assert resp.status_code == 204
    resp = api_client.get(f"/api/rooms/{room_id}/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_put_room_full_update(api_client):
    """PUT полностью меняет все поля."""
    # создаём
    payload = {
        "number": "202",
        "room_type": "Double",
        "price_per_night": "120.00",
        "capacity": 3,
        "description": "Initial",
    }
    resp = api_client.post("/api/rooms/", payload, format="json")
    room_id = resp.json()["id"]

    # PUT (все поля)
    new_payload = {
        "number": "303",
        "room_type": "Deluxe",
        "price_per_night": "200.00",
        "capacity": 4,
        "description": "Full update",
    }
    resp = api_client.put(f"/api/rooms/{room_id}/", new_payload, format="json")
    assert resp.status_code == 200
    data = resp.json()
    assert data["number"] == "303"
    assert data["room_type"] == "Deluxe"
    assert data["capacity"] == 4


@pytest.mark.django_db
def test_create_room_missing_fields(api_client):
    """POST /api/rooms/ без обязательных полей → 400."""
    # пропускаем number
    payload = {
        "room_type": "Economy",
        "price_per_night": "30.00",
        "capacity": 1,
        "description": "No number",
    }
    resp = api_client.post("/api/rooms/", payload, format="json")
    assert resp.status_code == 400
    body = resp.json()
    assert "number" in body  # Django вернёт ошибку по полю number
