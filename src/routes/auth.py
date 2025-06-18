"""Auth."""

import datetime
from typing import Dict

import jwt
from fastapi import APIRouter, Header, HTTPException

from src.core.config import PAT_DB, SECRET_KEY
from src.utils.keys import public_pem

router = APIRouter()


@router.post("/auth")
def auth(authorization: str = Header(None)) -> Dict[str, str]:
    """Generates a JWT token based on a valid PAT and returns the RSA public key.

    Args:
        authorization (str): Authorization header in the format 'PAT <token>'.

    Returns:
        dict: A dictionary containing the JWT token and the RSA public key.

    Raises:
        HTTPException: 401 if the authorization header is missing, malformed, or the PAT is invalid.
    """
    if not authorization or not authorization.startswith("PAT "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")

    pat: str = authorization.replace("PAT ", "").strip()

    if pat not in PAT_DB:
        raise HTTPException(status_code=401, detail="Invalid PAT.")

    payload: dict = {"user": PAT_DB[pat], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}

    token: str = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"jwt": token, "rsa_public_key": public_pem}
