import streamlit as st
import pandas as pd
import os
import sys

# Add project root to sys.path so modules can be resolved
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Page Configuration
st.set_page_config(
    page_title="Executive Hotel Demand Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Import Views
from dashboards.streamlit.views import (
    executive_overview,
    demand_analysis,
    cancellation_analytics,
    pricing_insights,
    customer_intelligence,
    ml_risk_prediction
)
from agent_ui import render_ai_analyst_page


# Load Data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "..", "data", "raw", "hotel_bookings.csv")
    df = pd.read_csv(data_path)
    
    df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    df["country"] = df["country"].fillna("Unknown")
    df["children"] = df["children"].fillna(0)
    df["agent"] = df["agent"].fillna(0)
    df["company"] = df["company"].fillna(0)
    
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    df["arrival_date_month"] = pd.Categorical(df["arrival_date_month"], categories=month_order, ordered=True)
    
    return df

df = load_data()

def render_ml(df):
    ml_risk_prediction.render()
    
def render_ai(df):
    render_ai_analyst_page()

st.sidebar.title('Navigation')

PAGES = {
    "1. Executive Overview": executive_overview.render,
    "2. Demand Analysis": demand_analysis.render,
    "3. Cancellation Analytics": cancellation_analytics.render,
    "4. Pricing & ADR Insights": pricing_insights.render,
    "5. Customer Intelligence": customer_intelligence.render,
    "6. ML Risk Prediction": render_ml,
    "7. AI Analyst": render_ai
}

selection = st.sidebar.radio("Go to", list(PAGES.keys()))


# Global Filters (Only applied to analytic views)
if selection not in ["6. ML Risk Prediction", "7. AI Analyst"]:
    st.sidebar.markdown("---")
    st.sidebar.header("Global Filters")

    hotel_options = ["All"] + sorted(df["hotel"].dropna().unique().tolist())
    hotel_filter = st.sidebar.selectbox("Hotel Type", options=hotel_options, index=0)

    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    month_filter = st.sidebar.multiselect("Arrival Month", options=month_order, default=[])

    market_options = ["All"] + sorted(df["market_segment"].dropna().unique().tolist())
    market_filter = st.sidebar.selectbox("Market Segment", options=market_options, index=0)

    customer_options = ["All"] + sorted(df["customer_type"].dropna().unique().tolist())
    customer_filter = st.sidebar.selectbox("Customer Type", options=customer_options, index=0)

    # Advanced Filters Expander (Empty as requested to remove others, but kept for future-proofing)
    with st.sidebar.expander("Advanced Filters"):
        st.caption("No advanced filters currently active.")


    # Apply Filters
    filtered_df = df.copy()

    if hotel_filter != "All":
        filtered_df = filtered_df[filtered_df["hotel"] == hotel_filter]

    if month_filter:
        filtered_df = filtered_df[filtered_df["arrival_date_month"].isin(month_filter)]

    if market_filter != "All":
        filtered_df = filtered_df[filtered_df["market_segment"] == market_filter]

    if customer_filter != "All":
        filtered_df = filtered_df[filtered_df["customer_type"] == customer_filter]

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    # Route to Analytic Page
    PAGES[selection](filtered_df)
else:
    # Route to standalone pages (no global filters applied)
    PAGES[selection](df)
