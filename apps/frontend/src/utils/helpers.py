from datetime import datetime
import json
from typing import Any

import streamlit as st


def format_date(date_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a date string."""
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime(fmt)
    except (ValueError, TypeError):
        return date_str


def display_json(data: dict[str, Any]) -> None:
    """Display JSON data in a formatted way."""
    st.code(json.dumps(data, indent=2, default=str), language="json")


def show_toast(message: str, icon: str = "ℹ️") -> None:
    """Show a toast notification."""
    st.toast(f"{icon} {message}")
