"""
Frontend - Streamlit Frontend Application
Implements a page registry pattern for clean routing.
"""

from collections.abc import Callable

import streamlit as st

# Page registry: maps page names to their render functions
# Using eager imports for better performance and traceability
from src.components.sidebar import render_sidebar
from src.config import settings
from src.pages.dashboard import show_dashboard_page
from src.pages.home import show_home_page
from src.pages.login import show_login_page
from src.pages.profile import show_profile_page

PAGE_REGISTRY: dict[str, Callable[[], None]] = {
    "Home": show_home_page,
    "Dashboard": show_dashboard_page,
    "Profile": show_profile_page,
}

LOGIN_PAGE = "Login"
HOME_PAGE = "Home"


def initialize_app() -> None:
    """Initialize the Streamlit application."""
    st.set_page_config(
        page_title=settings.app_name,
        page_icon=settings.app_icon,
        layout=settings.app_layout,
        initial_sidebar_state=settings.app_sidebar_state,
    )


def initialize_session_state() -> None:
    """Initialize or reset session state variables."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "page" not in st.session_state:
        st.session_state.page = HOME_PAGE


def main() -> None:
    """Main application entry point."""
    initialize_app()
    initialize_session_state()

    # Render sidebar (shared navigation)
    render_sidebar()

    # Page routing
    if not st.session_state.authenticated:
        show_login_page()
        return

    page = st.session_state.get("page", HOME_PAGE)
    page_handler = PAGE_REGISTRY.get(page)

    if page_handler:
        page_handler()
    else:
        # Fallback to home if page not found
        st.session_state.page = HOME_PAGE
        show_home_page()


if __name__ == "__main__":
    main()
