"""Main application entry point.

This module initializes the FastAPI app and includes
all the API routers responsible for authentication,
gateway handling, and status checking.

Run this module to start the API server.

Example:
    uvicorn src.carrot:app --reload

"""

from fastapi import FastAPI

from src.routes import auth, gateway, status

app: FastAPI = FastAPI()


app.include_router(auth.router)
app.include_router(gateway.router)
app.include_router(status.router)
