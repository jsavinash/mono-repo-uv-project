import streamlit as st

from src.api.client import APIClient


def show_login_page() -> None:
    """Display the login/registration page."""
    st.markdown("# 🔐 Welcome")
    st.markdown("Please login or create an account.")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1, st.form("login_form"):
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                client = APIClient()
                result = client.post(
                    "/auth/login/", {"email": email, "password": password}
                )
                if result["success"]:
                    data = result["data"]
                    st.session_state.authenticated = True
                    st.session_state.user = data.get("user", {})
                    st.session_state.access_token = data.get("access_token", "")
                    st.success("Login successful!")
                    st.rerun()

    with tab2, st.form("register_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        reg_email = st.text_input("Email", placeholder="your@email.com")
        reg_password = st.text_input("Password", type="password")
        reg_password_confirm = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register", use_container_width=True)

        if submitted:
            if not all([username, reg_email, reg_password, reg_password_confirm]):
                st.error("Please fill in all fields.")
            elif reg_password != reg_password_confirm:
                st.error("Passwords do not match.")
            elif len(reg_password) < 8:
                st.error("Password must be at least 8 characters.")
            else:
                client = APIClient()
                result = client.post(
                    "/auth/register/",
                    {
                        "username": username,
                        "email": reg_email,
                        "password": reg_password,
                        "password_confirm": reg_password_confirm,
                    },
                )
                if result["success"]:
                    data = result["data"]
                    st.session_state.authenticated = True
                    st.session_state.user = data.get("user", {})
                    st.session_state.access_token = data.get("access_token", "")
                    st.success("Registration successful!")
                    st.rerun()
