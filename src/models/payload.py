"""Payload model."""

from pydantic import BaseModel


class PayloadRequest(BaseModel):
    """Model for the payload used in the gateway endpoint.

    Attributes:
        payload (str): The encrypted payload represented as a hexadecimal string.
    """

    payload: str
