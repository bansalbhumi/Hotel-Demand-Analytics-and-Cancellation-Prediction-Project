import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dashboards.streamlit.utils.theme import apply_theme, BLUE, ORANGE, GREEN, RED, COLOR_SEQUENCE
from dashboards.streamlit.utils.components import render_insight

def render(df: pd.DataFrame):
    st.header("Cancellation Analytics")
    
    chart1, chart2 = st.columns(2)
    
    with chart1:
        st.subheader("Cancellation Rate by Market Segment")
        segment_data = df.groupby("market_segment", observed=False).agg(rate=("is_canceled", "mean")).reset_index()
        segment_data["rate"] = segment_data["rate"] * 100
        segment_data = segment_data.sort_values("rate", ascending=True)
        
        # Color by severity: >40% Red, >20% Orange, else Green
        colors = []
        for val in segment_data["rate"]:
            if val > 40: colors.append(RED)
            elif val > 20: colors.append(ORANGE)
            else: colors.append(GREEN)
            
        fig_segment = go.Figure(go.Bar(
            x=segment_data["rate"], y=segment_data["market_segment"], orientation="h",
            marker_color=colors, text=segment_data["rate"], texttemplate="%{text:.1f}%", textposition="outside"
        ))
        
        fig_segment = apply_theme(fig_segment)
        fig_segment.update_layout(xaxis_title="Cancellation Rate (%)", yaxis_title="")
        st.plotly_chart(fig_segment, use_container_width=True)
        render_insight("Groups and Online TA segments exhibit the highest cancellation risk.")

    with chart2:
        st.subheader("Cancellation by Customer Type")
        cust_data = df.groupby("customer_type", observed=False).agg(rate=("is_canceled", "mean")).reset_index()
        cust_data["rate"] = cust_data["rate"] * 100
        cust_data = cust_data.sort_values("rate", ascending=True)
        
        fig_cust = px.bar(cust_data, x="rate", y="customer_type", orientation="h", color_discrete_sequence=[BLUE])
        fig_cust.update_traces(texttemplate="%{x:.1f}%", textposition="outside")
        fig_cust = apply_theme(fig_cust)
        fig_cust.update_layout(xaxis_title="Cancellation Rate (%)", yaxis_title="")
        st.plotly_chart(fig_cust, use_container_width=True)
        render_insight("Transient customers have significantly higher cancellation rates than Contract or Group customers.")
        
    # Additional charts removed to keep dashboard minimal
