from fastapi import FastAPI
from src.routes import auth, gateway, status

app = FastAPI()

app.include_router(auth.router)
app.include_router(gateway.router)
app.include_router(status.router)
