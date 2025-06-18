from pydantic import BaseModel

class PayloadRequest(BaseModel):
    payload: str