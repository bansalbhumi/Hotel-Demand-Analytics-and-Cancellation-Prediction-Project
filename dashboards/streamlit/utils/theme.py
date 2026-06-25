import plotly.graph_objects as go

# -------------------------------------------------------------------
# Theme Constants
# -------------------------------------------------------------------
BG_COLOR = "#0E1117"
CARD_COLOR = "#161B22"
GRID_COLOR = "#2D333B"
TEXT_COLOR = "#FFFFFF"

# Accent Colors
BLUE = "#4C9AFF"
ORANGE = "#FFB347"
GREEN = "#52C41A"
RED = "#FF4D4F"

COLOR_SEQUENCE = [BLUE, ORANGE, GREEN, RED]

# -------------------------------------------------------------------
# Plotly Standardized Template
# -------------------------------------------------------------------
def apply_theme(fig: go.Figure) -> go.Figure:
    """Applies the FAANG executive dashboard theme to a Plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        margin=dict(l=25, r=25, t=50, b=25), # 25px margin around charts
        height=420, # Uniform height
        autosize=True,
        font=dict(color=TEXT_COLOR, size=14),
        title="", # Explicitly suppress default titles (using empty string, not None)
        xaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=False
        ),
        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=False
        ),
        legend=dict(
            font=dict(size=14),
            bgcolor="rgba(0,0,0,0)"
        ),
        uniformtext_mode='hide'
    )
    return fig
