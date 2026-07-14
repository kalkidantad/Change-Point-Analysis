"""Tests for Flask dashboard API."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_summary(client):
    response = client.get("/api/summary")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total_observations"] > 8000


def test_prices_with_date_filter(client):
    response = client.get("/api/prices?start=2020-01-01&end=2020-12-31")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] > 200
    assert data["data"][0]["date"] >= "2020-01-01"


def test_events(client):
    response = client.get("/api/events")
    assert response.status_code == 200
    assert response.get_json()["count"] >= 10


def test_change_points(client):
    response = client.get("/api/change-points")
    assert response.status_code == 200
    assert response.get_json()["count"] >= 1


def test_event_associations(client):
    response = client.get("/api/event-associations")
    assert response.status_code == 200
    assert response.get_json()["count"] >= 1


def test_event_metrics(client):
    response = client.get("/api/events/12/metrics?window_days=30")
    assert response.status_code == 200
    data = response.get_json()
    assert "pre_mean_price" in data
    assert "pct_change" in data


def test_event_metrics_not_found(client):
    response = client.get("/api/events/999/metrics")
    assert response.status_code == 404
