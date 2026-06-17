import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Hotel Demand Analytics Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/hotel_bookings_cleaned.csv")
    return df

df = load_data()

# --------------------------------------------------
# Basic Setup
# --------------------------------------------------
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

df["arrival_date_month"] = pd.Categorical(
    df["arrival_date_month"],
    categories=month_order,
    ordered=True
)

# Single-color dashboard palette
BAR_COLOR = "#4C78A8"
LINE_COLOR = "#4C78A8"
RISK_COLOR = "#E45756"

# --------------------------------------------------
# Dashboard Title
# --------------------------------------------------
st.title("Hotel Demand Analytics Dashboard")
st.markdown(
    "Interactive business dashboard for analyzing hotel booking demand, cancellations, ADR, lead time, and customer behavior."
)

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("Dashboard Filters")

hotel_filter = st.sidebar.selectbox(
    "Hotel Type",
    options=["All Hotels"] + sorted(df["hotel"].dropna().unique().tolist())
)

month_filter = st.sidebar.multiselect(
    "Arrival Month",
    options=month_order,
    default=[],
    placeholder="Select arrival month(s)"
)

market_filter = st.sidebar.selectbox(
    "Market Segment",
    options=["All Segments"] + sorted(df["market_segment"].dropna().unique().tolist())
)

customer_filter = st.sidebar.selectbox(
    "Customer Type",
    options=["All Customers"] + sorted(df["customer_type"].dropna().unique().tolist())
)

deposit_filter = st.sidebar.selectbox(
    "Deposit Type",
    options=["All Deposit Types"] + sorted(df["deposit_type"].dropna().unique().tolist())
)

booking_status_filter = st.sidebar.selectbox(
    "Booking Status",
    options=["All Bookings", "Not Cancelled", "Cancelled"]
)

lead_time_range = st.sidebar.slider(
    "Lead Time Range",
    min_value=int(df["lead_time"].min()),
    max_value=int(df["lead_time"].max()),
    value=(int(df["lead_time"].min()), int(df["lead_time"].max()))
)

adr_range = st.sidebar.slider(
    "ADR Range",
    min_value=0,
    max_value=300,
    value=(0, 300)
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------
filtered_df = df.copy()

if hotel_filter != "All Hotels":
    filtered_df = filtered_df[filtered_df["hotel"] == hotel_filter]

if month_filter:
    filtered_df = filtered_df[filtered_df["arrival_date_month"].isin(month_filter)]

if market_filter != "All Segments":
    filtered_df = filtered_df[filtered_df["market_segment"] == market_filter]

if customer_filter != "All Customers":
    filtered_df = filtered_df[filtered_df["customer_type"] == customer_filter]

if deposit_filter != "All Deposit Types":
    filtered_df = filtered_df[filtered_df["deposit_type"] == deposit_filter]

if booking_status_filter == "Cancelled":
    filtered_df = filtered_df[filtered_df["is_canceled"] == 1]
elif booking_status_filter == "Not Cancelled":
    filtered_df = filtered_df[filtered_df["is_canceled"] == 0]

filtered_df = filtered_df[
    (filtered_df["lead_time"] >= lead_time_range[0]) &
    (filtered_df["lead_time"] <= lead_time_range[1]) &
    (filtered_df["adr"] >= adr_range[0]) &
    (filtered_df["adr"] <= adr_range[1])
]

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please change the filter values.")
    st.stop()

# --------------------------------------------------
# KPI Calculations
# --------------------------------------------------
total_bookings = len(filtered_df)
cancelled_bookings = filtered_df["is_canceled"].sum()
cancellation_rate = filtered_df["is_canceled"].mean() * 100
avg_adr = filtered_df["adr"].mean()
room_nights = filtered_df["total_nights"].sum()
avg_lead_time = filtered_df["lead_time"].mean()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
st.subheader("Executive KPI Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Bookings", f"{total_bookings:,}")
col2.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")
col3.metric("Average ADR", f"{avg_adr:.2f}")
col4.metric("Room Nights", f"{room_nights:,.0f}")
col5.metric("Avg Lead Time", f"{avg_lead_time:.1f} days")

st.divider()

# --------------------------------------------------
# Row 1: Monthly Trend and Cancellation Split
# --------------------------------------------------
chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("Monthly Booking Trend")

    monthly_data = (
        filtered_df.groupby("arrival_date_month", observed=False)
        .size()
        .reset_index(name="bookings")
        .sort_values("arrival_date_month")
    )

    fig_monthly = px.line(
        monthly_data,
        x="arrival_date_month",
        y="bookings",
        markers=True,
        title="Bookings by Arrival Month"
    )

    fig_monthly.update_traces(
        line=dict(color=LINE_COLOR, width=3),
        marker=dict(size=8, color=LINE_COLOR)
    )

    fig_monthly.update_layout(
        xaxis_title="Arrival Month",
        yaxis_title="Bookings",
        showlegend=False
    )

    st.plotly_chart(fig_monthly, use_container_width=True)

with chart2:
    st.subheader("Cancellation Split")

    status_data = filtered_df["is_canceled"].map({
        0: "Not Cancelled",
        1: "Cancelled"
    }).value_counts().reset_index()

    status_data.columns = ["booking_status", "bookings"]

    fig_status = px.bar(
        status_data,
        x="booking_status",
        y="bookings",
        text="bookings",
        title="Cancelled vs Not Cancelled Bookings"
    )

    fig_status.update_traces(
        marker_color=BAR_COLOR,
        textposition="outside"
    )

    fig_status.update_layout(
        xaxis_title="Booking Status",
        yaxis_title="Bookings",
        showlegend=False
    )

    st.plotly_chart(fig_status, use_container_width=True)

# --------------------------------------------------
# Row 2: Cancellation Risk Analysis
# --------------------------------------------------
chart3, chart4 = st.columns(2)

with chart3:
    st.subheader("Cancellation by Customer Type")

    customer_data = (
        filtered_df.groupby("customer_type")
        .agg(
            bookings=("is_canceled", "count"),
            cancellation_rate=("is_canceled", "mean")
        )
        .reset_index()
    )

    customer_data["cancellation_rate"] *= 100
    customer_data = customer_data.sort_values("cancellation_rate", ascending=False)

    fig_customer = px.bar(
        customer_data,
        x="customer_type",
        y="cancellation_rate",
        text=customer_data["cancellation_rate"].round(2),
        title="Cancellation Rate by Customer Type"
    )

    fig_customer.update_traces(
        marker_color=RISK_COLOR,
        textposition="outside"
    )

    fig_customer.update_layout(
        xaxis_title="Customer Type",
        yaxis_title="Cancellation Rate (%)",
        showlegend=False
    )

    st.plotly_chart(fig_customer, use_container_width=True)

with chart4:
    st.subheader("Cancellation by Market Segment")

    segment_data = (
        filtered_df.groupby("market_segment")
        .agg(
            bookings=("is_canceled", "count"),
            cancellation_rate=("is_canceled", "mean")
        )
        .reset_index()
    )

    segment_data["cancellation_rate"] *= 100
    segment_data = segment_data.sort_values("cancellation_rate", ascending=False)

    fig_segment = px.bar(
        segment_data,
        x="market_segment",
        y="cancellation_rate",
        text=segment_data["cancellation_rate"].round(2),
        title="Cancellation Rate by Market Segment"
    )

    fig_segment.update_traces(
        marker_color=RISK_COLOR,
        textposition="outside"
    )

    fig_segment.update_layout(
        xaxis_title="Market Segment",
        yaxis_title="Cancellation Rate (%)",
        showlegend=False
    )

    st.plotly_chart(fig_segment, use_container_width=True)

# --------------------------------------------------
# Row 3: ADR and Lead Time
# --------------------------------------------------
chart5, chart6 = st.columns(2)

with chart5:
    st.subheader("ADR Distribution")

    fig_adr = px.histogram(
        filtered_df,
        x="adr",
        nbins=40,
        title="ADR Distribution"
    )

    fig_adr.update_traces(marker_color=BAR_COLOR)

    fig_adr.update_layout(
        xaxis_title="Average Daily Rate",
        yaxis_title="Number of Bookings",
        showlegend=False
    )

    st.plotly_chart(fig_adr, use_container_width=True)

with chart6:
    st.subheader("Lead Time Impact")

    lead_data = (
        filtered_df.groupby("is_canceled")
        .agg(avg_lead_time=("lead_time", "mean"))
        .reset_index()
    )

    lead_data["booking_status"] = lead_data["is_canceled"].map({
        0: "Not Cancelled",
        1: "Cancelled"
    })

    fig_lead = px.bar(
        lead_data,
        x="booking_status",
        y="avg_lead_time",
        text=lead_data["avg_lead_time"].round(1),
        title="Average Lead Time by Booking Status"
    )

    fig_lead.update_traces(
        marker_color=BAR_COLOR,
        textposition="outside"
    )

    fig_lead.update_layout(
        xaxis_title="Booking Status",
        yaxis_title="Average Lead Time",
        showlegend=False
    )

    st.plotly_chart(fig_lead, use_container_width=True)

# --------------------------------------------------
# Row 4: Country and Deposit Analysis
# --------------------------------------------------
chart7, chart8 = st.columns(2)

with chart7:
    st.subheader("Top Source Countries")

    country_data = (
        filtered_df["country"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    country_data.columns = ["country", "bookings"]

    fig_country = px.bar(
        country_data,
        x="bookings",
        y="country",
        orientation="h",
        text="bookings",
        title="Top 10 Countries by Bookings"
    )

    fig_country.update_traces(
        marker_color=BAR_COLOR,
        textposition="outside"
    )

    fig_country.update_layout(
        xaxis_title="Bookings",
        yaxis_title="Country",
        showlegend=False
    )

    st.plotly_chart(fig_country, use_container_width=True)

with chart8:
    st.subheader("Deposit Type Analysis")

    deposit_data = (
        filtered_df["deposit_type"]
        .value_counts()
        .reset_index()
    )

    deposit_data.columns = ["deposit_type", "bookings"]

    fig_deposit = px.bar(
        deposit_data,
        x="deposit_type",
        y="bookings",
        text="bookings",
        title="Bookings by Deposit Type"
    )

    fig_deposit.update_traces(
        marker_color=BAR_COLOR,
        textposition="outside"
    )

    fig_deposit.update_layout(
        xaxis_title="Deposit Type",
        yaxis_title="Bookings",
        showlegend=False
    )

    st.plotly_chart(fig_deposit, use_container_width=True)

