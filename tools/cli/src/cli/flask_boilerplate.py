#!/usr/bin/env python3

import os
from pathlib import Path

from typing import Annotated

from rich.console import Console
from typer import Argument, Typer, BadParameter
import re

app = Typer(add_completion=False)


def valid_service_folder_path(value: str) -> str:
    """Validates that the input service folder path format (###-####)."""
    pattern = r"^services/[\w-]+/[\w-]+/?$"
    if not re.match(pattern, value):
        raise BadParameter(
            f"'{value}' is not a valid service folder path format. Expected format: services/xxxx/."
        )
    return value


def regex_validator(value: str) -> str:
    """Validates the input string against a specific regex pattern."""
    # Example regex: starts with 'user_' followed by alphanumeric characters
    pattern = r"^user_[a-zA-Z0-9]+$"
    if not re.match(pattern, value):
        raise BadParameter(
            f"'{value}' is not a valid format. Expected format: user_[alphanumeric]"
        )
    return value


@app.command()
def main(n: Annotated[str, Argument(help="Path to service API folder")]) -> None:
    Console().print(f"********** Flask cli execution **********")
    create_flask_app_folder_structure(n)
    Console().print(f"********** Complete **********")


# Allow the script to be run standalone (useful during development).
if __name__ == "__main__":  # pragma: no cover
    app()


PROJECT_NAME = "src"  # add your project name here

LIST_FILES = [
    "Dockerfile",
    ".env",
    "README.md",
    "src/__init__.py",
    # config folder
    "src/config/__init__.py",
    "src/config/config.py",
    "src/config/dev_config.py",
    "src/config/production.py",
    # controllers
    "src/controllers/__init__.py",
    "src/controllers/user_controller.py",
    # middlewares
    "src/middlewares/__init__.py",
    # models
    "src/models/__init__.py",
    "src/models/user_model.py",
    # services
    "src/services/__init__.py",
    "src/services/user_service.py",
    # routes and utils
    "src/routes.py",
    "src/utils.py",
]


# "services/user/"
def create_flask_app_folder_structure(targetFolderPath):
    for file_path in LIST_FILES:
        file_path = Path(file_path)
        file_dir, file_name = os.path.split(file_path)

        # first make dir
        if file_dir != "":
            os.makedirs(targetFolderPath + file_dir, exist_ok=True)
            print(f"Creating Directory: {file_dir} for file: {file_name}")

        if (not os.path.exists(f"{targetFolderPath}{file_path}")) or (
            os.path.getsize(f"{targetFolderPath}{file_path}") == 0
        ):
            with open(f"{targetFolderPath}{file_path}", "w+") as f:
                pass
                print(f"Creating an empty file: {file_path}")
        else:
            print(f"File already exists {file_path}")
