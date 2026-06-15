from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.routers.campaigns import campaigns_db
from unittest.mock import MagicMock, patch

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

def test_create_campaign_validation():
    invalid_budget_payload = {
        "name": "Nike Summer 2026",
        "budget": -50000.0,
        "channel": "Instagram"
    }
    invalid_budget_response = client.post("/campaigns/", json=invalid_budget_payload)
    assert invalid_budget_response.status_code == 422

    invalid_channel_payload = {
        "name": "Nike Summer 2026",
        "budget": 50000.0,
        "channel": "Snapchat"
    }
    invalid_channel_response = client.post("/campaigns/", json=invalid_channel_payload)
    assert invalid_channel_response.status_code == 422

    invalid_name_payload = {
        "name": "Ni",
        "budget": 50000.0,
        "channel": "YouTube"
    }
    invalid_name_response = client.post("/campaigns/", json=invalid_name_payload)
    assert invalid_name_response.status_code == 422


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


def test_filter_by_channel():
    client.post("/campaigns/", json={"name": "Nike Summer", "budget": 50000, "channel": "Instagram"})
    client.post("/campaigns/", json={"name": "Adidas Launch", "budget": 30000, "channel": "Youtube"})

    response = client.get("/campaigns/?channel=Instagram")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["channel"] == "Instagram"

def test_filter_by_is_active():
     client.post("/campaigns/", json={"name": "Nike Summer", "budget": 50000, "channel": "Instagram", "is_active": True})
     client.post("/campaigns/", json={"name": "Puma Winter", "budget": 20000, "channel": "Instagram", "is_active": False})

     response = client.get("/campaigns/?is_active=True")
     assert response.status_code == 200
     results = response.json()
     assert len(results) == 1
     assert results[0]["name"] == "Nike Summer"



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


def test_analyse_campaign():
    payload = {
        "name": "Nike Summer 2026",
        "budget": 50000.0,
        "channel": "Instagram"
    }
    create_response = client.post("/campaigns/", json=payload)
    assert create_response.status_code == 201
    campaign_id = create_response.json()["id"]

    mock_message = MagicMock()
    mock_message.content[0].text = "Great campaign with strong potential."
    with patch("app.routers.analyse.client.messages.create", return_value=mock_message):
        response = client.post(f"/campaigns/{campaign_id}/analyse")
    assert response.status_code == 200
    data = response.json()
    assert data["campaign_id"] == campaign_id
    assert data["analyse"] == "Great campaign with strong potential."


    