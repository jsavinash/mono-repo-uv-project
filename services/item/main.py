"""
E-Commerce Platform - Main Application
FastAPI-based microservices architecture
"""
from typer import Typer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_client import make_asgi_app
import logging

from item.app.api.v1.api import api_router
from item.app.core.config.settings import settings
#from item.app.db.database import engine, Base
from item.app.middleware.logging import LoggingMiddleware
from item.app.middleware.rate_limit import RateLimitMiddleware
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
#Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Complete E-Commerce Platform API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Mount static files
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include API router
#app.include_router(api_router, prefix=settings.API_V1_STR)

# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting E-Commerce Platform API...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database: {settings.DATABASE_URL}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down E-Commerce Platform API...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "E-Commerce Platform API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ecommerce-api",
        "version": settings.VERSION
    }

execute = Typer(add_completion=False)
@execute.command()
def main() -> None:
    """Run Flask App."""
    import uvicorn
    uvicorn.run(
        "item.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=4,
        log_level="info"
    )

if __name__ == "__main__":
    execute()
