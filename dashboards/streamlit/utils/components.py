import streamlit as st

def render_insight(text: str):
    """Renders a standard self-explanatory business insight under a chart."""
    # Using a clean markdown block with an info icon and subdued styling
    st.markdown(f"> 💡 **Business Insight:** {text}")

def render_metric_card(title: str, value: str, icon: str = ""):
    """Renders a standard executive metric card."""
    # Since Streamlit columns manage layout, we just use st.metric, 
    # but we could also do custom HTML if needed for tighter control.
    # Streamlit's native st.metric matches the dark mode extremely well.
    st.metric(title, f"{icon} {value}")
