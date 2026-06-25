import streamlit as st
import plotly.express as px
import pandas as pd
from dashboards.streamlit.utils.theme import apply_theme, BLUE, ORANGE, GREEN, RED
from dashboards.streamlit.utils.components import render_insight

def render(df: pd.DataFrame):
    st.header("Demand Analysis")
    
    chart1, chart2 = st.columns(2)
    
    with chart1:
        st.subheader("Monthly Booking Trend")
        monthly_data = df.groupby("arrival_date_month", observed=False).size().reset_index(name="bookings")
        fig = px.line(monthly_data, x="arrival_date_month", y="bookings", markers=True, color_discrete_sequence=[BLUE])
        fig.update_traces(line=dict(width=4, shape="spline"), marker=dict(size=10))
        fig = apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
        render_insight("Summer months (July, August) observe peak booking volume, indicating high seasonality.")

    with chart2:
        st.subheader("Seasonality Heatmap")
        heatmap_data = df.groupby(["arrival_date_month", "hotel"], observed=False).size().reset_index(name="bookings")
        heatmap_pivot = heatmap_data.pivot(index="hotel", columns="arrival_date_month", values="bookings")
        fig_heat = px.imshow(heatmap_pivot, color_continuous_scale="Blues", aspect="auto")
        fig_heat = apply_theme(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)
        render_insight("Resort hotels see a sharper spike in August compared to the consistent demand for City hotels.")
        
    # Bottom charts removed to keep dashboard minimal
