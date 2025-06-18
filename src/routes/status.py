"""Status."""

from typing import Dict

from fastapi import APIRouter, HTTPException

from src.core.config import status_store

router = APIRouter()


@router.get("/status/{request_id}")
def check_status(request_id: str) -> Dict[str, str]:
    """Checks the status of a request based on its ID.

    Args:
        request_id (str): The unique identifier for the request.

    Returns:
        dict: A dictionary containing the current status.

    Raises:
        HTTPException:
            - 404 if the request ID is not found.
    """
    status: str | None = status_store.get(request_id)

    if not status:
        raise HTTPException(status_code=404, detail="Request ID not found.")

    return {"status": status}
