"""
utils.py ─ Shared helper functions used across the app.
"""

import os
import re
import uuid
from pathlib import Path

from flask import current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename


# ─── Slug ───────────────────────────────────────────────────────
def slugify(text: str) -> str:
    """Convert plain text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


# ─── File upload ────────────────────────────────────────────────
def allowed_file(filename: str) -> bool:
    allowed = current_app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


def save_image(file) -> str | None:
    """
    Persist an uploaded image to UPLOAD_FOLDER and return its URL path.
    Returns None if the file is empty or has a bad extension.
    """
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        return None

    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    upload_path = Path(current_app.config["UPLOAD_FOLDER"])
    upload_path.mkdir(parents=True, exist_ok=True)
    file.save(upload_path / unique_name)
    return f"/static/images/uploads/{unique_name}"


# ─── Flash helpers ──────────────────────────────────────────────
def flash_success(msg: str):
    flash(msg, "success")


def flash_error(msg: str):
    flash(msg, "error")


def flash_warning(msg: str):
    flash(msg, "warning")
