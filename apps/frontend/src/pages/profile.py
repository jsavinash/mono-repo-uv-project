import streamlit as st

from src.api.client import APIClient


def show_profile_page() -> None:
    """Display the user profile page."""
    st.markdown("# 👤 Profile")
    st.markdown("Manage your account settings.")

    client = APIClient(token=st.session_state.access_token)
    result = client.get("/users/me/")

    if result["success"]:
        user_data = result["data"].get("data", result["data"])

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://via.placeholder.com/150", width=150)
            st.markdown(f"**{user_data.get('username', 'N/A')}**")
            st.markdown(f"*{user_data.get('email', 'N/A')}*")

        with col2:
            with st.form("profile_form"):
                phone = st.text_input("Phone", value=user_data.get("phone_number", ""))
                bio = st.text_area("Bio", value=user_data.get("bio", ""))
                theme = st.selectbox(
                    "Theme",
                    options=["light", "dark"],
                    index=0 if user_data.get("theme", "light") == "light" else 1,
                )
                email_notifications = st.checkbox(
                    "Email Notifications",
                    value=user_data.get("email_notifications", True),
                )
                submitted = st.form_submit_button(
                    "Update Profile", use_container_width=True
                )

                if submitted:
                    update_result = client.patch(
                        "/users/me/",
                        {
                            "phone_number": phone,
                            "bio": bio,
                            "theme": theme,
                            "email_notifications": email_notifications,
                        },
                    )
                    if update_result["success"]:
                        st.success("Profile updated!")
                        st.rerun()
    else:
        st.warning("Could not load profile. Make sure the API is running.")
