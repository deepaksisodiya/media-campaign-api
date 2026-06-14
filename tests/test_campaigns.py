from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.routers.campaigns import campaigns_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    campaigns_db.clear()
    yield


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_all_campaigns_empty():
    response = client.get("/campaigns/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_campaign():
    payload = {
        "name": "Nike Summer 2026",
        "budget": 50000.0,
        "channel": "Instagram"
    }
    response = client.post("/campaigns/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Nike Summer 2026"
    assert data["budget"] == 50000.0
    assert data["channel"] == "Instagram"
    assert data["is_active"] == True
    assert data["id"] is not None
    

def test_get_campaign():
    payload = {
        "name": "Nike Summer 2026",
        "budget": 50000.0,
        "channel": "Instagram"
    }
    create_response = client.post("/campaigns/", json=payload)
    assert create_response.status_code == 201
    campaign_id = create_response.json()["id"]

    get_response = client.get(f"/campaigns/{campaign_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Nike Summer 2026"


def test_get_campaign_not_found():
    get_response = client.get("/campaigns/999")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Campaign not found"


def test_update_campaign():
    payload = {
        "name": "Nike Summer 2026",
        "budget": 50000.0,
        "channel": "Instagram"
    }
    create_response = client.post("/campaigns/", json=payload)
    assert create_response.status_code == 201
    campaign_id = create_response.json()["id"]

    updated_payload = {
         "name": "Nike Summer 2026",
         "budget": 75000.0,
         "channel": "Facebook"
    }
    update_response = client.put(f"/campaigns/{campaign_id}", json=updated_payload)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Nike Summer 2026"
    assert data["budget"] == 75000.0
    assert data["channel"] == "Facebook"
    assert data["is_active"] == True
    assert data["id"] is not None


def test_delete_campaign():
    payload = {
        "name": "Nike Summer 2026",
        "budget": 50000.0,
        "channel": "Instagram"
    }
    create_response = client.post("/campaigns/", json=payload)
    assert create_response.status_code == 201
    campaign_id = create_response.json()["id"]

    delete_response = client.delete(f'/campaigns/{campaign_id}')
    assert delete_response.status_code == 204

    get_response = client.get(f"/campaigns/{campaign_id}")
    assert get_response.status_code == 404
    