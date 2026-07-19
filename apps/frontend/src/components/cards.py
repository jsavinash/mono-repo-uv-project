import streamlit as st


def info_card(title: str, value: str, delta: str | None = None) -> None:
    """Display an info card with title, value, and optional delta."""
    with st.container(border=True):
        st.metric(label=title, value=value, delta=delta)


def status_badge(status: str) -> str:
    """Return an emoji badge for a given status."""
    badges = {
        "active": "🟢",
        "inactive": "🔴",
        "pending": "🟡",
        "completed": "✅",
        "failed": "❌",
    }
    return badges.get(status.lower(), "⚪")
