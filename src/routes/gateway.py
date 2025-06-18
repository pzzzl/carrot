"""Gateway."""

import uuid
from typing import Dict

import jwt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from fastapi import APIRouter, Header, HTTPException

from src.core.config import SECRET_KEY, status_store
from src.models.payload import PayloadRequest
from src.utils.keys import private_key

router = APIRouter()


@router.post("/gateway")
def gateway(request: PayloadRequest, authorization: str = Header(None)) -> Dict[str, str]:
    """Validates the JWT token, decrypts the payload, and registers a request.

    Args:
        request (PayloadRequest): The request containing the encrypted payload (hex string).
        authorization (str): Authorization header in the format 'Bearer <jwt>'.

    Returns:
        dict: A dictionary containing the generated request ID.

    Raises:
        HTTPException:
            - 401 if the Authorization header is missing, malformed, or the JWT is invalid.
            - 400 if the payload is malformed or decryption fails.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")

    jwt_token: str = authorization.replace("Bearer ", "").strip()

    try:
        jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid JWT.")

    try:
        encrypted_data: bytes = bytes.fromhex(request.payload)
    except ValueError:
        raise HTTPException(status_code=400, detail="Malformed payload.")

    try:
        decrypted: bytes = private_key.decrypt(
            encrypted_data,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
        )
        print(f"Payload: {decrypted.decode()}")
    except Exception:
        raise HTTPException(status_code=400, detail="Decryption failed.")

    request_id: str = str(uuid.uuid4())
    status_store[request_id] = "processing"

    # Simulate immediate processing
    status_store[request_id] = "done"

    return {"request_id": request_id}
