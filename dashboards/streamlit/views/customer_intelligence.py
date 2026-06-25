import streamlit as st
import plotly.express as px
import pandas as pd
from dashboards.streamlit.utils.theme import apply_theme, BLUE
from dashboards.streamlit.utils.components import render_insight

def render(df: pd.DataFrame):
    st.header("Customer Intelligence")
    
    chart1, chart2 = st.columns(2)
    
    with chart1:
        st.subheader("Market Segment Treemap")
        seg_data = df.groupby("market_segment", observed=False).size().reset_index(name="bookings")
        fig_seg = px.treemap(seg_data, path=["market_segment"], values="bookings", color_discrete_sequence=[BLUE])
        fig_seg.update_traces(textinfo="label+value+percent root", hovertemplate="%{label}<br>Bookings: %{value:,}<extra></extra>")
        fig_seg.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=420, paper_bgcolor="#0E1117", font=dict(color="#FFFFFF"))
        st.plotly_chart(fig_seg, use_container_width=True)
        render_insight("Online Travel Agents completely dominate the market segment mix.")

    with chart2:
        st.subheader("Top 15 Country Contribution")
        country_data = df.groupby("country").size().reset_index(name="bookings").sort_values("bookings").tail(15)
        fig_country = px.bar(country_data, x="bookings", y="country", orientation="h", color_discrete_sequence=[BLUE])
        fig_country.update_traces(texttemplate="%{x:,}", textposition="outside")
        fig_country = apply_theme(fig_country)
        fig_country.update_layout(xaxis_title="Bookings", yaxis_title="")
        st.plotly_chart(fig_country, use_container_width=True)
        render_insight("Portugal remains the primary customer base, followed closely by Western Europe.")
