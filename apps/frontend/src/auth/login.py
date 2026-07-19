"""
Authentication utilities.
"""

import streamlit as st


def require_authentication() -> bool:
    """Check if user is authenticated, redirect if not."""
    if not st.session_state.get("authenticated", False):
        st.warning("Please log in to access this page.")
        st.session_state.page = "Login"
        st.rerun()
        return False
    return True


def logout() -> None:
    """Clear session state and log out."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.access_token = None
    st.rerun()
