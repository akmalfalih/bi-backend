"""
Test file untuk autentikasi (JWT)
Letakkan di folder: tests/test_auth.py
Jalankan: pytest -q
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Ganti dengan user valid dari database kamu
VALID_USERNAME = "admin"
VALID_PASSWORD = "secret123"


def test_login_success():
    """Pastikan login dengan kredensial valid menghasilkan token JWT"""
    response = client.post(
        "/auth/token",
        data={"username": VALID_USERNAME, "password": VALID_PASSWORD},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_fail_invalid_user():
    """Pastikan login gagal untuk user yang tidak ada"""
    response = client.post(
        "/auth/token",
        data={"username": "unknown_user", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_me_endpoint_after_login():
    """Pastikan /auth/me bisa diakses setelah login dan token valid"""
    login_res = client.post(
        "/auth/token",
        data={"username": VALID_USERNAME, "password": VALID_PASSWORD},
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/auth/me", headers=headers)
    assert me_res.status_code == 200
    data = me_res.json()
    assert "username" in data
    assert data["username"] == VALID_USERNAME
