"""Test auth."""

from fastapi.testclient import TestClient

from src.carrot import app

client = TestClient(app)


def test_auth_success() -> None:
    """Test successful authentication with a valid PAT."""
    response = client.post("/auth", headers={"Authorization": "PAT valid_pat"})
    assert response.status_code == 200
    data = response.json()
    assert "jwt" in data
    assert "rsa_public_key" in data


def test_auth_missing_header() -> None:
    """Test authentication failure when Authorization header is missing."""
    response = client.post("/auth")
    assert response.status_code == 401


def test_auth_invalid_pat() -> None:
    """Test authentication failure with an invalid PAT."""
    response = client.post("/auth", headers={"Authorization": "PAT wrong_pat"})
    assert response.status_code == 401
