from typer import Typer
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from item.src.api.errors.http_error import http_error_handler
from item.src.api.errors.validation_error import http422_error_handler
from item.src.api.routes.api import router as api_router
from item.src.core.config import get_app_settings
from item.src.core.events import create_start_app_handler, create_stop_app_handler
import uvicorn


def get_application() -> FastAPI:
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler(
        "startup",
        create_start_app_handler(application, settings),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application),
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    #application.include_router(api_router, prefix=settings.api_prefix)

    return application



execute = Typer(add_completion=False)
@execute.command()
def main() -> None:
    """Run Flask App."""
    app = get_application()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, log_level="info") 

if __name__ == "__main__":
    execute()
