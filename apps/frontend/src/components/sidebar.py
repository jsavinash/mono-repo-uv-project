import streamlit as st
from streamlit_option_menu import option_menu


def render_sidebar() -> None:
    """Render the sidebar navigation menu."""
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=Logo", use_column_width=True)
        st.markdown("---")

        if st.session_state.authenticated:
            # Show navigation for authenticated users
            selected = option_menu(
                menu_title="Navigation",
                options=["Home", "Dashboard", "Profile"],
                icons=["house", "bar-chart", "person"],
                menu_icon="cast",
                default_index=0,
            )
            st.session_state.page = selected

            st.markdown("---")
            st.markdown(f"**User:** {st.session_state.user.get('username', 'N/A')}")

            if st.button("Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.access_token = None
                st.rerun()
        else:
            st.markdown("### Welcome!")
            st.markdown("Please log in to continue.")
