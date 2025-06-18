"""Test gateway."""

from typing import Tuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from fastapi.testclient import TestClient

from src.carrot import app

client = TestClient(app)


def get_auth_and_key() -> Tuple[str, rsa.RSAPublicKey]:
    """Authenticate and retrieve JWT token and RSA public key.

    Returns:
        Tuple[str, rsa.RSAPublicKey]: JWT token string and RSA public key object.
    """
    auth_response = client.post("/auth", headers={"Authorization": "PAT valid_pat"})
    data = auth_response.json()
    jwt_token: str = data["jwt"]
    public_key_pem: str = data["rsa_public_key"]

    public_key = serialization.load_pem_public_key(public_key_pem.encode())

    return jwt_token, public_key


def encrypt_payload(public_key: rsa.RSAPublicKey, payload: bytes) -> str:
    """Encrypt the payload using the given RSA public key with OAEP padding.

    Args:
        public_key (rsa.RSAPublicKey): The RSA public key for encryption.
        payload (bytes): The data to encrypt.

    Returns:
        str: The encrypted payload as a hex string.
    """
    encrypted = public_key.encrypt(
        payload,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    return encrypted.hex()


def test_gateway_success() -> None:
    """Test successful request to the gateway endpoint."""
    jwt_token, public_key = get_auth_and_key()
    payload = encrypt_payload(public_key, b'{"teste": "ok"}')

    response = client.post(
        "/gateway",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"payload": payload},
    )
    assert response.status_code == 200
    assert "request_id" in response.json()


def test_gateway_invalid_jwt() -> None:
    """Test gateway endpoint response with invalid JWT token."""
    response = client.post("/gateway", headers={"Authorization": "Bearer invalid_jwt"}, json={"payload": "abcd"})
    assert response.status_code == 401


def test_gateway_invalid_payload_format() -> None:
    """Test gateway endpoint response with invalid payload hex string format."""
    jwt_token, _ = get_auth_and_key()
    response = client.post(
        "/gateway",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"payload": "invalid_hex_string"},
    )
    assert response.status_code == 400
