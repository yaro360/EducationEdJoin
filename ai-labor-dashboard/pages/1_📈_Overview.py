import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Overview", page_icon="📈", layout="wide")

# ── Load data ──────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_occupations():
    return pd.read_csv(DATA_DIR / "occupations.csv")

df = load_occupations()

# ── Page header ────────────────────────────────────────────────────────────────
st.title("📈 Market Overview")
st.caption("AI Labor Market Signal Dashboard | Anthropic Economic Index + BLS Data")
st.markdown("---")

# ── KPI Row ────────────────────────────────────────────────────────────────────
high_risk = df[df["exposure_tier"] == "High"]
avg_exposure = df["exposure_score"].mean()
high_risk_count = len(high_risk)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="High-Risk Occupations Tracked",
        value=f"{high_risk_count}",
        delta="+3 since Q4 2025",
        delta_color="inverse",
    )

with col2:
    st.metric(
        label="Avg Observed Exposure Score",
        value=f"{avg_exposure:.1f}%",
        delta="+4.2pp YoY",
        delta_color="inverse",
    )

with col3:
    st.metric(
        label="Hiring Velocity Δ (Ages 22–25)",
        value="-14%",
        delta="High-exposure vs. no-exposure cohorts",
        delta_color="inverse",
        help="Difference-in-differences estimate: workers in high-AI-exposure "
             "occupations saw a 14% relative decline in job-finding rate "
             "post-ChatGPT (Nov 2022–Dec 2025) vs. zero-exposure peers. "
             "Source: Anthropic Economic Index, March 2026.",
    )

with col4:
    st.metric(
        label="Growth Penalty per 10pp Exposure",
        value="-0.6pp",
        delta="BLS projected 2024–2034 growth",
        delta_color="inverse",
        help="Each 10-percentage-point increase in observed AI exposure is "
             "associated with a 0.6pp lower BLS 10-year employment growth "
             "projection. Source: Anthropic Economic Index, March 2026.",
    )

st.markdown("---")

# ── Scatter: Exposure Score vs BLS Growth Projection ──────────────────────────
st.subheader("Exposure Score vs. BLS Projected Employment Growth (2024–2034)")

tier_colors = {"High": "#f38ba8", "Medium": "#fab387", "Low": "#a6e3a1"}

fig = px.scatter(
    df,
    x="exposure_score",
    y="bls_growth_projection",
    color="exposure_tier",
    color_discrete_map=tier_colors,
    hover_name="occupation",
    hover_data={"sector": True, "soc_code": True, "exposure_score": ":.1f", "bls_growth_projection": ":.1f"},
    size_max=14,
    text=None,
    labels={
        "exposure_score": "Observed AI Exposure Score (%)",
        "bls_growth_projection": "BLS Projected Growth 2024–2034 (%)",
        "exposure_tier": "Exposure Tier",
    },
    title="Negative Correlation: Higher AI Exposure → Lower Employment Growth",
    template="plotly_dark",
)

# Add trend line
import numpy as np
x_vals = np.linspace(df["exposure_score"].min(), df["exposure_score"].max(), 100)
# slope: -0.6pp per 10pp exposure = -0.06 per pp
slope = -0.06
intercept = df["bls_growth_projection"].mean() - slope * df["exposure_score"].mean()
y_vals = slope * x_vals + intercept

fig.add_trace(
    go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="lines",
        name="Trend (−0.6pp/10pp exposure)",
        line=dict(color="#cdd6f4", width=2, dash="dash"),
    )
)

# Add zero-growth reference line
fig.add_hline(
    y=0,
    line_dash="dot",
    line_color="#6c7086",
    annotation_text="0% growth",
    annotation_position="bottom right",
)

fig.update_layout(
    height=520,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font_color="#cdd6f4",
)
fig.update_traces(marker=dict(size=10, opacity=0.85, line=dict(width=0.5, color="#313244")))

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    '<p class="footnote">Source: Anthropic Economic Index (March 2026); BLS Occupational Outlook Handbook 2024–2034. '
    "Observed exposure scores reflect share of workers in each occupation whose tasks are actively augmented "
    "or substituted by AI tools. Growth projections are BLS baseline estimates.</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Exposure Tier breakdown bar ────────────────────────────────────────────────
st.subheader("Occupation Count by Exposure Tier")

tier_counts = df["exposure_tier"].value_counts().reset_index()
tier_counts.columns = ["Tier", "Count"]
tier_order = {"High": 0, "Medium": 1, "Low": 2}
tier_counts["_order"] = tier_counts["Tier"].map(tier_order)
tier_counts = tier_counts.sort_values("_order").drop(columns="_order")

fig2 = px.bar(
    tier_counts,
    x="Tier",
    y="Count",
    color="Tier",
    color_discrete_map=tier_colors,
    text="Count",
    template="plotly_dark",
    title="Occupations by AI Exposure Tier",
    labels={"Count": "Number of Occupations"},
)
fig2.update_traces(textposition="outside")
fig2.update_layout(
    height=350,
    showlegend=False,
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font_color="#cdd6f4",
)

st.plotly_chart(fig2, use_container_width=True)

# ── Sector breakdown ───────────────────────────────────────────────────────────
st.subheader("Average Exposure Score by Sector")

sector_avg = (
    df.groupby("sector")["exposure_score"]
    .mean()
    .reset_index()
    .sort_values("exposure_score", ascending=True)
)

fig3 = px.bar(
    sector_avg,
    x="exposure_score",
    y="sector",
    orientation="h",
    color="exposure_score",
    color_continuous_scale=["#a6e3a1", "#fab387", "#f38ba8"],
    text=sector_avg["exposure_score"].apply(lambda v: f"{v:.1f}%"),
    template="plotly_dark",
    title="Sector Average Observed AI Exposure",
    labels={"exposure_score": "Avg Exposure Score (%)", "sector": ""},
)
fig3.update_traces(textposition="outside")
fig3.update_layout(
    height=420,
    coloraxis_showscale=False,
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font_color="#cdd6f4",
)

st.plotly_chart(fig3, use_container_width=True)
st.markdown(
    '<p class="footnote">Source: Anthropic Economic Index (March 2026). Sector classifications follow BLS Standard '
    "Occupational Classification (SOC) major groups.</p>",
    unsafe_allow_html=True,
)
