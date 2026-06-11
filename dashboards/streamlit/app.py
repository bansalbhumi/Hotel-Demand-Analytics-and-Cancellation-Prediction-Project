import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Hotel Demand Analytics Dashboard",
    layout="wide"
)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/hotel_bookings_cleaned.csv")
    return df

df = load_data()

# Title
st.title("Hotel Demand Analytics Dashboard")
st.write("Interactive dashboard for hotel booking demand, cancellations, ADR, and customer segments.")

# Sidebar Filters
st.sidebar.header("Dashboard Filters")

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

hotel_filter = st.sidebar.multiselect(
    "Select Hotel Type",
    options=sorted(df["hotel"].dropna().unique()),
    default=sorted(df["hotel"].dropna().unique())
)

month_filter = st.sidebar.multiselect(
    "Select Arrival Month",
    options=month_order,
    default=month_order
)

market_filter = st.sidebar.multiselect(
    "Select Market Segment",
    options=sorted(df["market_segment"].dropna().unique()),
    default=sorted(df["market_segment"].dropna().unique())
)

customer_filter = st.sidebar.multiselect(
    "Select Customer Type",
    options=sorted(df["customer_type"].dropna().unique()),
    default=sorted(df["customer_type"].dropna().unique())
)

deposit_filter = st.sidebar.multiselect(
    "Select Deposit Type",
    options=sorted(df["deposit_type"].dropna().unique()),
    default=sorted(df["deposit_type"].dropna().unique())
)

country_options = sorted(df["country"].dropna().unique())

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=country_options,
    default=country_options
)

# Apply Filters
filtered_df = df[
    (df["hotel"].isin(hotel_filter)) &
    (df["arrival_date_month"].isin(month_filter)) &
    (df["market_segment"].isin(market_filter)) &
    (df["customer_type"].isin(customer_filter)) &
    (df["country"].isin(country_filter)) &
    (df["deposit_type"].isin(deposit_filter))
]

# KPI Calculations
total_bookings = len(filtered_df)
cancelled_bookings = filtered_df["is_canceled"].sum()
cancellation_rate = ((cancelled_bookings / total_bookings) * 100) if total_bookings > 0 else 0
avg_adr = filtered_df["adr"].mean() if total_bookings > 0 else 0
total_room_nights = filtered_df["total_nights"].sum() if total_bookings > 0 else 0
avg_lead_time = filtered_df["lead_time"].mean() if total_bookings > 0 else 0

# KPI Cards
st.subheader("Executive KPI Cards")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Bookings", f"{total_bookings:,}")
col2.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")
col3.metric("Average ADR", f"{avg_adr:.2f}")
col4.metric("Room Nights", f"{total_room_nights:,.0f}")
col5.metric("Avg Lead Time", f"{avg_lead_time:.1f} days")

st.divider()

# Empty data handling
if filtered_df.empty:
    st.warning("No data available for the selected filters. Please change the filter selection.")
    st.stop()

# Monthly Booking Trend
st.subheader("Monthly Booking Trend by Hotel Type")

monthly_bookings = (
    filtered_df.groupby(["arrival_date_month", "hotel"])
    .size()
    .reset_index(name="bookings")
)

monthly_bookings["arrival_date_month"] = pd.Categorical(
    monthly_bookings["arrival_date_month"],
    categories=month_order,
    ordered=True
)

monthly_bookings = monthly_bookings.sort_values("arrival_date_month")

fig_monthly = px.line(
    monthly_bookings,
    x="arrival_date_month",
    y="bookings",
    color="hotel",
    markers=True,
    title="Monthly Booking Trend by Hotel Type"
)

fig_monthly.update_layout(
    xaxis_title="Arrival Month",
    yaxis_title="Number of Bookings"
)

st.plotly_chart(fig_monthly, width="stretch")

st.markdown(
    "Business Insight: Booking demand shows seasonal movement, and City Hotel usually receives higher booking volume than Resort Hotel."
)

# Hotel type comparison
st.subheader("Hotel Type Comparison")

hotel_comparison = (
    filtered_df.groupby("hotel")
    .agg(
        total_bookings=("hotel", "count"),
        avg_adr=("adr", "mean"),
        avg_nights=("total_nights", "mean"),
        cancellation_rate=("is_canceled", "mean")
    )
    .reset_index()
)

hotel_comparison["cancellation_rate"] = hotel_comparison["cancellation_rate"] * 100

fig_hotel = px.bar(
    hotel_comparison,
    x="hotel",
    y="total_bookings",
    text="total_bookings",
    title="Total Bookings by Hotel Type"
)

fig_hotel.update_layout(
    xaxis_title="Hotel Type",
    yaxis_title="Total Bookings"
)

st.plotly_chart(fig_hotel, width="stretch")

# Cancellation rate by customer type
st.subheader("Cancellation Rate by Customer Type")

cancel_customer = (
    filtered_df.groupby("customer_type")
    .agg(
        total_bookings=("is_canceled", "count"),
        cancelled_bookings=("is_canceled", "sum"),
        cancellation_rate=("is_canceled", "mean")
    )
    .reset_index()
)

cancel_customer["cancellation_rate"] = cancel_customer["cancellation_rate"] * 100
cancel_customer = cancel_customer.sort_values("cancellation_rate", ascending=False)

fig_cancel = px.bar(
    cancel_customer,
    x="customer_type",
    y="cancellation_rate",
    text=cancel_customer["cancellation_rate"].round(2),
    title="Cancellation Rate by Customer Type"
)

fig_cancel.update_layout(
    xaxis_title="Customer Type",
    yaxis_title="Cancellation Rate (%)"
)

st.plotly_chart(fig_cancel, width="stretch")

st.markdown(
    "Business Insight: Customer types with higher cancellation rates should be monitored for stronger booking confirmation and retention strategies."
)

# Cancellation rate by market segment
st.subheader("Cancellation Rate by Market Segment")

segment_cancel = (
    filtered_df.groupby("market_segment")
    .agg(
        total_bookings=("is_canceled", "count"),
        cancellation_rate=("is_canceled", "mean")
    )
    .reset_index()
)

segment_cancel["cancellation_rate"] *= 100
segment_cancel = segment_cancel.sort_values("cancellation_rate", ascending=False)

fig_segment_cancel = px.bar(
    segment_cancel,
    x="market_segment",
    y="cancellation_rate",
    text=segment_cancel["cancellation_rate"].round(2),
    title="Cancellation Rate by Market Segment"
)

fig_segment_cancel.update_layout(
    xaxis_title="Market Segment",
    yaxis_title="Cancellation Rate (%)"
)

st.plotly_chart(fig_segment_cancel, width="stretch")

st.markdown(
    "Business Insight: Market segments with higher cancellation rates may require stronger confirmation policies, advance payment checks, or targeted follow-up."
)

# ADR distribution
st.subheader("ADR Distribution")

adr_filtered = filtered_df[filtered_df["adr"] <= 300]

fig_adr = px.histogram(
    adr_filtered,
    x="adr",
    nbins=50,
    title="ADR Distribution Without Extreme Outliers"
)

fig_adr.update_layout(
    xaxis_title="Average Daily Rate",
    yaxis_title="Number of Bookings"
)

st.plotly_chart(fig_adr, width="stretch")

st.markdown(
    "Business Insight: Most bookings fall within a moderate ADR range, while extreme ADR values should be reviewed before model development."
)

# Market Segment Breakdown
st.subheader("Bookings by Market Segment")

segment_bookings = (
    filtered_df["market_segment"]
    .value_counts()
    .reset_index()
)

segment_bookings.columns = ["market_segment", "bookings"]

fig_segment = px.bar(
    segment_bookings,
    x="market_segment",
    y="bookings",
    text="bookings",
    title="Bookings by Market Segment"
)

fig_segment.update_layout(
    xaxis_title="Market Segment",
    yaxis_title="Number of Bookings"
)

st.plotly_chart(fig_segment, width="stretch")

st.markdown(
    "Business Insight: Market segment analysis helps identify the strongest booking channels and customer acquisition sources."
)

# Dashboard Summary
st.divider()

st.subheader("Dashboard Summary")

st.markdown("""
This dashboard provides an interactive prototype for analyzing hotel booking demand, cancellations, ADR, and customer segments.

Key capabilities:
- Filter bookings by hotel, month, market segment, customer type, country, and deposit type.
- Track executive KPIs such as total bookings, cancellation rate, ADR, room nights, and lead time.
- Analyze booking trends, customer cancellation behavior, ADR distribution, and market segment performance.
""")