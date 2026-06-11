import streamlit as st

st.set_page_config(
    page_title="Hotel Demand Analytics Dashboard",
    layout="wide"
)

st.title("Hotel Demand Analytics Dashboard")

st.sidebar.header("Filters")

hotel = st.sidebar.selectbox(
    "Hotel Type",
    ["All", "City Hotel", "Resort Hotel"]
)

st.metric("Total Bookings", "Coming Soon")
st.metric("Cancellation Rate", "Coming Soon")
st.metric("Average ADR", "Coming Soon")

st.write("Dashboard under Development")