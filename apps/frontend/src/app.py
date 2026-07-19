"""
Frontend - Streamlit Frontend Application
"""

import streamlit as st

from src.config import settings


def initialize_app() -> None:
    """Initialize the Streamlit application."""
    st.set_page_config(
        page_title=settings.app_name,
        page_icon=settings.app_icon,
        layout=settings.app_layout,
        initial_sidebar_state=settings.app_sidebar_state,
    )


def main() -> None:
    """Main application entry point."""
    initialize_app()

    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    # Render sidebar
    from src.components.sidebar import render_sidebar

    render_sidebar()

    # Page routing
    if not st.session_state.authenticated:
        from src.pages.login import show_login_page

        show_login_page()
    else:
        page = st.session_state.get("page", "Home")
        if page == "Home":
            from src.pages.home import show_home_page

            show_home_page()
        elif page == "Dashboard":
            from src.pages.dashboard import show_dashboard_page

            show_dashboard_page()
        elif page == "Profile":
            from src.pages.profile import show_profile_page

            show_profile_page()


if __name__ == "__main__":
    main()
