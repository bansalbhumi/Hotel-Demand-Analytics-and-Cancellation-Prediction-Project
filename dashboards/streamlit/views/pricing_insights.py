import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dashboards.streamlit.utils.theme import apply_theme, BLUE, ORANGE, GREEN, RED
from dashboards.streamlit.utils.components import render_insight
import plotly.figure_factory as ff
import numpy as np

def get_season(month):
    if month in ['December', 'January', 'February']: return 'Winter'
    elif month in ['March', 'April', 'May']: return 'Spring'
    elif month in ['June', 'July', 'August']: return 'Summer'
    else: return 'Autumn'

def render(df: pd.DataFrame):
    st.header("Pricing & Revenue Insights")
    
    df_season = df.copy()
    df_season['season'] = df_season['arrival_date_month'].apply(get_season)
    
    # Sample down to 10,000 rows for rendering speed while maintaining distribution
    df_plot = df_season.sample(n=min(10000, len(df_season)), random_state=42)
    
    chart1, chart2 = st.columns(2)
    
    with chart1:
        st.subheader("ADR Distribution")
        pricing_df = df_plot[df_plot['adr'] <= 300]
        mean_adr = df_season[df_season['adr'] <= 300]['adr'].mean() # Calculate true mean
        median_adr = df_season[df_season['adr'] <= 300]['adr'].median() # Calculate true median
        
        fig_adr = px.histogram(
            pricing_df, x="adr", nbins=50, 
            color_discrete_sequence=[BLUE]
        )
        
        fig_adr.add_vline(x=mean_adr, line_dash="dash", line_color=RED, annotation_text=f"Mean: ${mean_adr:.2f}", annotation_position="top right")
        fig_adr.add_vline(x=median_adr, line_dash="dot", line_color=GREEN, annotation_text=f"Median: ${median_adr:.2f}", annotation_position="bottom right")
        
        fig_adr = apply_theme(fig_adr)
        fig_adr.update_layout(xaxis_title="Average Daily Rate ($)", yaxis_title="Bookings")
        st.plotly_chart(fig_adr, use_container_width=True)
        render_insight(f"ADR is right-skewed with a median of ${median_adr:.2f}. The mean is pulled slightly higher to ${mean_adr:.2f}.")

    with chart2:
        st.subheader("ADR by Hotel Type")
        fig_hotel = px.box(
            df_plot, x="hotel", y="adr", color="hotel",
            color_discrete_sequence=[BLUE, ORANGE]
        )
        fig_hotel.update_traces(boxpoints=False)
        fig_hotel.update_yaxes(range=[0, 300]) # Hide extreme y-axis distortion
        fig_hotel = apply_theme(fig_hotel)
        fig_hotel.update_layout(xaxis_title="", yaxis_title="ADR ($)", showlegend=False)
        st.plotly_chart(fig_hotel, use_container_width=True)
        render_insight("City Hotels command a higher and tighter median ADR range compared to Resort Hotels.")
        
    # Additional charts removed to keep dashboard minimal
