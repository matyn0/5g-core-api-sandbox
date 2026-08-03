import pytest
from fastapi.testclient import TestClient

from app.data import fake_subscriptions
from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_subscriptions():
    fake_subscriptions.clear()
    yield
    fake_subscriptions.clear()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_ues():
    response = client.get("/nef/ue")

    assert response.status_code == 200

    body = response.json()
    assert body["count"] == 3
    assert [ue["ue_id"] for ue in body["ues"]] == ["001", "002", "003"]


def test_get_ue_status():
    response = client.get("/nef/ue/001/status")

    assert response.status_code == 200
    assert response.json() == {
        "ue_id": "001",
        "status": "connected",
        "slice_id": "slice-embb",
        "cell_id": "cell-01",
    }


def test_get_unknown_ue_status():
    response = client.get("/nef/ue/999/status")

    assert response.status_code == 404
    assert response.json() == {"detail": "UE not found"}


def test_list_subscriptions_is_empty():
    response = client.get("/nef/subscriptions")

    assert response.status_code == 200
    assert response.json() == {
        "count": 0,
        "subscriptions": [],
    }


def test_subscription_lifecycle():
    subscription = {
        "ue_id": "001",
        "event_type": "ue-status-change",
        "callback_url": "https://example.com/callback",
    }

    create_response = client.post("/nef/subscriptions", json=subscription)

    assert create_response.status_code == 200

    created = create_response.json()
    assert created == {
        "subscription_id": "sub-001",
        **subscription,
        "status": "active",
    }

    list_response = client.get("/nef/subscriptions")

    assert list_response.status_code == 200
    assert list_response.json() == {
        "count": 1,
        "subscriptions": [created],
    }

    get_response = client.get("/nef/subscriptions/sub-001")

    assert get_response.status_code == 200
    assert get_response.json() == created

    delete_response = client.delete("/nef/subscriptions/sub-001")

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Subscription deleted",
        "subscription": created,
    }

    missing_response = client.get("/nef/subscriptions/sub-001")

    assert missing_response.status_code == 404
    assert missing_response.json() == {"detail": "Subscription not found"}


def test_create_subscription_for_unknown_ue():
    response = client.post(
        "/nef/subscriptions",
        json={
            "ue_id": "999",
            "event_type": "ue-status-change",
            "callback_url": "https://example.com/callback",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "UE not found"}


def test_create_subscription_with_missing_fields():
    response = client.post(
        "/nef/subscriptions",
        json={"ue_id": "001"},
    )

    assert response.status_code == 422

    missing_fields = {
        error["loc"][-1] for error in response.json()["detail"]
    }
    assert missing_fields == {"event_type", "callback_url"}


def test_delete_unknown_subscription():
    response = client.delete("/nef/subscriptions/sub-999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Subscription not found"}


def test_subscription_ids_do_not_overwrite_active_subscriptions():
    first = client.post(
        "/nef/subscriptions",
        json={
            "ue_id": "001",
            "event_type": "ue-status-change",
            "callback_url": "https://example.com/first",
        },
    ).json()
    second = client.post(
        "/nef/subscriptions",
        json={
            "ue_id": "002",
            "event_type": "ue-status-change",
            "callback_url": "https://example.com/second",
        },
    ).json()

    client.delete(f"/nef/subscriptions/{first['subscription_id']}")

    third = client.post(
        "/nef/subscriptions",
        json={
            "ue_id": "003",
            "event_type": "ue-status-change",
            "callback_url": "https://example.com/third",
        },
    ).json()
    response = client.get("/nef/subscriptions")

    assert second["subscription_id"] == "sub-002"
    assert third["subscription_id"] == "sub-003"
    assert response.json()["count"] == 2


def test_list_slice_load_analytics():
    response = client.get("/nwdaf/analytics/slice-load")

    assert response.status_code == 200

    body = response.json()
    assert body["analytics_type"] == "slice-load"
    assert [item["slice_id"] for item in body["slices"]] == [
        "slice-embb",
        "slice-urllc",
        "slice-mmtc",
    ]


def test_get_slice_load_analytics():
    response = client.get("/nwdaf/analytics/slice-load/slice-embb")

    assert response.status_code == 200
    assert response.json() == {
        "analytics_type": "slice-load",
        "slice": {
            "slice_id": "slice-embb",
            "name": "Enhanced Mobile Broadband",
            "load_percent": 72,
            "active_ues": 128,
            "status": "high",
        },
    }


def test_get_unknown_slice_load_analytics():
    response = client.get("/nwdaf/analytics/slice-load/unknown")

    assert response.status_code == 404
    assert response.json() == {"detail": "Slice not found"}
