import streamlit as st

from src.api.client import APIClient


def show_home_page() -> None:
    """Display the home page."""
    st.markdown("# 🏠 Home")
    st.markdown("Welcome to the application!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", "1,234", "+5.2%")
    with col2:
        st.metric("Active Sessions", "456", "-2.1%")
    with col3:
        st.metric("API Calls", "12.5K", "+12.3%")

    st.markdown("---")
    st.markdown("## Recent Activity")

    # Fetch data from API
    client = APIClient(token=st.session_state.access_token)
    result = client.get("/health/")
    if result["success"]:
        st.json(result["data"])
    else:
        st.info("Connect to an API backend to see live data.")
