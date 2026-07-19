import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def show_dashboard_page() -> None:
    """Display the dashboard page with charts and analytics."""
    st.markdown("# 📊 Dashboard")
    st.markdown("Analytics and insights.")

    # Sample data
    df = pd.DataFrame(
        {
            "Date": pd.date_range(start="2024-01-01", periods=30, freq="D"),
            "Users": [100 + i * 5 + (i % 7) * 10 for i in range(30)],
            "Revenue": [1000 + i * 50 + (i % 5) * 200 for i in range(30)],
        }
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(df, x="Date", y="Users", title="User Growth")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(df, x="Date", y="Revenue", title="Revenue")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("## Data Table")
    st.dataframe(df, use_container_width=True)
