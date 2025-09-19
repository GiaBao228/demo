import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app({"DATABASE": ":memory:", "ENV": "testing"})
    app.testing = True
    with app.test_client() as client:
        yield client

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json["status"] == "ok"

def test_user_safe_no_id(client):
    r = client.get("/user_safe")
    assert r.status_code == 400

def test_user_safe_valid(client):
    r = client.get("/user_safe?id=1")
    assert r.status_code == 200
    assert "safe_result" in r.json

def test_search_safe_escapes(client):
    r = client.get("/search_safe?q=<script>alert(1)</script>")
    assert "<script>" not in r.get_data(as_text=True)
