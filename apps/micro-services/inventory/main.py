from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from typer import Typer
import uvicorn

from inventory.api.errors.http_error import http_error_handler
from inventory.api.errors.validation_error import http422_error_handler
from inventory.api.routes.api import router as api_router
from inventory.core.config import get_app_settings
from inventory.core.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()
    app = FastAPI(**settings.fastapi_kwargs)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_event_handler(
        "startup",
        create_start_app_handler(app, settings),
    )
    app.add_event_handler(
        "shutdown",
        create_stop_app_handler(app),
    )

    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.include_router(api_router, prefix=settings.api_prefix)

    return app


app_runner = get_application()
execute = Typer(add_completion=False)


@execute.command()
def main() -> None:
    uvicorn.run("inventory:main.app_runner", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    execute()
