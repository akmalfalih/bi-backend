from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_USERNAME = "admin"
VALID_PASSWORD = "secret123"


def get_token():
    res = client.post(
        "/auth/token",
        data={"username": VALID_USERNAME, "password": VALID_PASSWORD},
    )
    assert res.status_code == 200
    return res.json()["access_token"]


def test_summary_endpoint():
    """Pastikan /dashboard/summary mengembalikan struktur data baru (wrapper JSON)"""
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/dashboard/summary", headers=headers)
    assert res.status_code == 200

    body = res.json()
    assert "data" in body
    assert "message" in body
    assert "period" in body

    data = body["data"]
    assert "tbs" in data
    assert "cpo" in data
    assert "total_panen" in data["tbs"]
    assert "total_terjual" in data["cpo"]
    assert "rata_rata_ffa" in data["cpo"]


def test_trend_endpoint():
    """Pastikan /dashboard/production/trend mengembalikan data list di dalam wrapper JSON"""
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/dashboard/production/trend", headers=headers)
    assert res.status_code == 200

    body = res.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0
    assert "tanggal" in body["data"][0]
    assert "total" in body["data"][0]


def test_by_location_endpoint():
    """Pastikan /dashboard/production/by-location mengembalikan list di dalam key 'data'"""
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/dashboard/production/by-location", headers=headers)
    assert res.status_code == 200

    body = res.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    if body["data"]:
        first_item = body["data"][0]
        assert "kode_kebun" in first_item
        assert "total" in first_item
