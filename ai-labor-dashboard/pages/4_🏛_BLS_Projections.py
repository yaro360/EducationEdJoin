import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="BLS Projections", page_icon="🏛", layout="wide")

DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_occupations():
    return pd.read_csv(DATA_DIR / "occupations.csv")

df = load_occupations()

st.title("🏛 BLS Employment Projections 2024–2034")
st.caption("AI Labor Market Signal Dashboard | Anthropic Economic Index + BLS Data")
st.markdown("---")

# ── BLS CSV upload / fallback ──────────────────────────────────────────────────
bls_path = DATA_DIR / "bls_ep_table1.csv"

st.info(
    "**Optional:** Download the BLS Employment Projections table from "
    "[bls.gov/emp](https://www.bls.gov/emp/tables/emp-by-detailed-occupation.htm) "
    "and place it at `data/bls_ep_table1.csv` to use real BLS data. "
    "The dashboard currently shows **seeded mock data** that matches reported paper findings."
)

if bls_path.exists():
    try:
        bls_raw = pd.read_csv(bls_path)
        st.success(f"BLS file loaded: {len(bls_raw)} rows")
        st.dataframe(bls_raw.head(), use_container_width=True)
    except Exception as e:
        st.warning(f"Could not parse BLS file: {e}. Falling back to seed data.")

st.markdown("---")

# ── Chart 1: Projected growth by exposure tier (box plot) ─────────────────────
st.subheader("Projected 2024–2034 Employment Growth by AI Exposure Tier")

tier_colors = {"High": "#f38ba8", "Medium": "#fab387", "Low": "#a6e3a1"}
tier_order = ["High", "Medium", "Low"]

fig = px.box(
    df,
    x="exposure_tier",
    y="bls_growth_projection",
    color="exposure_tier",
    color_discrete_map=tier_colors,
    category_orders={"exposure_tier": tier_order},
    points="all",
    hover_name="occupation",
    template="plotly_dark",
    labels={
        "exposure_tier": "AI Exposure Tier",
        "bls_growth_projection": "BLS Projected Growth 2024–2034 (%)",
    },
    title="Higher Exposure Tiers Show Weaker Employment Growth Projections",
)
fig.add_hline(
    y=0,
    line_dash="dot",
    line_color="#6c7086",
    annotation_text="0% growth",
    annotation_position="top right",
)
fig.update_layout(
    height=480,
    showlegend=False,
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font_color="#cdd6f4",
)
st.plotly_chart(fig, use_container_width=True)

# ── Summary stats table ────────────────────────────────────────────────────────
tier_stats = (
    df.groupby("exposure_tier")["bls_growth_projection"]
    .agg(["mean", "median", "min", "max", "count"])
    .reindex(tier_order)
    .round(1)
    .reset_index()
    .rename(columns={
        "exposure_tier": "Tier",
        "mean": "Mean Growth (%)",
        "median": "Median Growth (%)",
        "min": "Min (%)",
        "max": "Max (%)",
        "count": "# Occupations",
    })
)

st.dataframe(tier_stats, use_container_width=True, hide_index=True)

st.markdown(
    '<p class="footnote">Source: BLS Employment Projections 2024–2034 (baseline); Anthropic Economic Index '
    "(March 2026) for exposure tier classifications. Mock data seeded to match reported correlations.</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Chart 2: Waterfall — absolute job change by tier ──────────────────────────
st.subheader("Illustrative Absolute Employment Change by Exposure Tier (2024–2034)")

# Approximate: scale growth % by representative employment base
tier_employment_base = {"High": 8_500_000, "Medium": 6_200_000, "Low": 12_000_000}

waterfall_data = []
for tier in tier_order:
    avg_growth = df[df["exposure_tier"] == tier]["bls_growth_projection"].mean() / 100
    base = tier_employment_base[tier]
    change = int(base * avg_growth)
    waterfall_data.append({"Tier": tier, "Base (2024, M)": base / 1e6, "Change": change})

wf_df = pd.DataFrame(waterfall_data)

fig2 = go.Figure(
    go.Waterfall(
        name="Job Change",
        orientation="v",
        x=wf_df["Tier"].tolist() + ["Net Total"],
        y=wf_df["Change"].tolist() + [int(wf_df["Change"].sum())],
        connector=dict(line=dict(color="#313244")),
        increasing=dict(marker_color="#a6e3a1"),
        decreasing=dict(marker_color="#f38ba8"),
        totals=dict(marker_color="#89b4fa"),
        text=[
            f"{v:+,.0f}" for v in wf_df["Change"].tolist()
        ] + [f"{wf_df['Change'].sum():+,.0f}"],
        textposition="outside",
    )
)
fig2.update_layout(
    template="plotly_dark",
    height=420,
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font_color="#cdd6f4",
    title="Net Job Change by Exposure Tier — Illustrative Estimate",
    yaxis=dict(title="Jobs Added / Lost", showgrid=True, gridcolor="#313244"),
    xaxis=dict(title="AI Exposure Tier"),
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    '<p class="footnote">Illustrative only. Employment base figures are approximations of current BLS employment '
    "levels. Actual projections require full BLS EP table data.</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Chart 3: Scatter per sector ───────────────────────────────────────────────
st.subheader("Exposure Score vs. Growth — By Sector")

sector_agg = (
    df.groupby("sector")
    .agg(
        avg_exposure=("exposure_score", "mean"),
        avg_growth=("bls_growth_projection", "mean"),
        count=("occupation", "count"),
    )
    .reset_index()
)

fig3 = px.scatter(
    sector_agg,
    x="avg_exposure",
    y="avg_growth",
    size="count",
    color="avg_exposure",
    color_continuous_scale=["#a6e3a1", "#fab387", "#f38ba8"],
    hover_name="sector",
    hover_data={"avg_exposure": ":.1f", "avg_growth": ":.1f", "count": True},
    text="sector",
    template="plotly_dark",
    labels={
        "avg_exposure": "Avg Observed Exposure Score (%)",
        "avg_growth": "Avg BLS Projected Growth (%)",
        "count": "# Occupations",
    },
    title="Sector-Level: AI Exposure vs. Growth Projection",
)
fig3.update_traces(textposition="top center", textfont_size=9)
fig3.add_hline(y=0, line_dash="dot", line_color="#6c7086")
fig3.update_layout(
    height=500,
    coloraxis_showscale=False,
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font_color="#cdd6f4",
)
st.plotly_chart(fig3, use_container_width=True)
