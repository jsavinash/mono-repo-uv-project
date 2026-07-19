from pathlib import Path
import sys

from fastapi import FastAPI
from pydantic import BaseModel

sys.path.append(str(Path(__file__).resolve().parent))

from auth import router as auth_router
from plans import router as plans_router

app = FastAPI(title="Starter Kit API", version="0.1.0")
app.include_router(auth_router)
app.include_router(plans_router)


class HealthResponse(BaseModel):
    status: str
    service: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="api-gateway")


@app.get("/api/overview")
def overview() -> dict[str, str]:
    return {
        "message": "Welcome to the starter kit API",
        "mode": "monorepo-ready",
    }
