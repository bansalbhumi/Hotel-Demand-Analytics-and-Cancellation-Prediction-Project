import streamlit as st
import plotly.express as px
import pandas as pd
from dashboards.streamlit.utils.theme import apply_theme, BLUE, ORANGE, GREEN, RED, COLOR_SEQUENCE
from dashboards.streamlit.utils.components import render_insight

def render(df: pd.DataFrame):
    st.header("Executive Overview")
    
    # --------------------------------------------------
    # KPIs
    # --------------------------------------------------
    total_bookings = len(df)
    cancellation_rate = df["is_canceled"].mean() * 100 if total_bookings > 0 else 0.0
    avg_adr = df["adr"].mean() if total_bookings > 0 else 0.0
    room_nights = int(df["total_nights"].sum())
    avg_lead_time = df["lead_time"].mean() if total_bookings > 0 else 0.0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Bookings", f"{total_bookings:,}")
    col2.metric("Cancellation Rate", f"{cancellation_rate:.1f}%")
    col3.metric("Average ADR", f"${avg_adr:.2f}")
    col4.metric("Avg Lead Time", f"{int(avg_lead_time)} days")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --------------------------------------------------
    # Charts Row 1
    # --------------------------------------------------
    chart1, chart2 = st.columns(2)
    
    with chart1:
        st.subheader("Monthly Booking Trend")
        monthly_data = (
            df.groupby(["arrival_date_month", "hotel"], observed=False)
            .size()
            .reset_index(name="bookings")
            .sort_values("arrival_date_month")
        )
        
        fig_monthly = px.line(
            monthly_data,
            x="arrival_date_month",
            y="bookings",
            color="hotel",
            markers=True,
            color_discrete_sequence=[BLUE, ORANGE]
        )
        
        fig_monthly.update_traces(
            line=dict(width=4, shape="spline"),
            marker=dict(size=10),
            hovertemplate="<b>%{x}</b><br>Bookings: %{y:,}<extra></extra>"
        )
        
        fig_monthly = apply_theme(fig_monthly)
        fig_monthly.update_layout(xaxis_title="", yaxis_title="Bookings", showlegend=True, legend_title="")
        st.plotly_chart(fig_monthly, use_container_width=True)
        render_insight("City Hotels consistently drive higher booking volumes across all months compared to Resort Hotels.")

    with chart2:
        st.subheader("Cancellation Split")
        cancel_counts = df["is_canceled"].value_counts()
        
        status_data = pd.DataFrame({
            "status": ["Not Cancelled", "Cancelled"],
            "count": [
                int(cancel_counts.get(0, 0)),
                int(cancel_counts.get(1, 0))
            ]
        })
        
        fig_status = px.pie(
            status_data,
            names="status",
            values="count",
            hole=0.6,
            color="status",
            color_discrete_map={"Cancelled": RED, "Not Cancelled": BLUE}
        )
        
        # Add center text
        fig_status.add_annotation(
            text=f"{cancellation_rate:.1f}%<br>Cancelled",
            x=0.5, y=0.5,
            font=dict(size=24, color="#FFFFFF"),
            showarrow=False
        )
        
        fig_status.update_traces(
            textinfo="percent",
            hovertemplate="%{label}: %{value:,}<extra></extra>"
        )
        
        fig_status = apply_theme(fig_status)
        st.plotly_chart(fig_status, use_container_width=True)
        render_insight("A massive 37% of overall bookings are cancelled, indicating a significant revenue leakage point.")

    # Removed duplicate country chart to keep dashboard minimal
