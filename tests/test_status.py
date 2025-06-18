"""Test status."""

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from fastapi.testclient import TestClient

from src.carrot import app

client = TestClient(app)


def test_status_success() -> None:
    """Test status endpoint returns 'done' for a valid request."""
    auth_response = client.post("/auth", headers={"Authorization": "PAT valid_pat"})
    jwt_token: str = auth_response.json()["jwt"]
    public_key_pem: str = auth_response.json()["rsa_public_key"]

    public_key: rsa.RSAPublicKey = serialization.load_pem_public_key(public_key_pem.encode())

    encrypted: bytes = public_key.encrypt(
        b'{"test": "status"}',
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )

    payload_hex: str = encrypted.hex()

    gateway_response = client.post(
        "/gateway",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"payload": payload_hex},
    )

    request_id: str = gateway_response.json()["request_id"]

    status_response = client.get(f"/status/{request_id}")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "done"


def test_status_not_found() -> None:
    """Test status endpoint returns 404 for a nonexistent request ID."""
    response = client.get("/status/nonexistent_id")
    assert response.status_code == 404
