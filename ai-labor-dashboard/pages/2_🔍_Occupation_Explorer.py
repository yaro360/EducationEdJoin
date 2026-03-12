import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Occupation Explorer", page_icon="🔍", layout="wide")

DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_occupations():
    return pd.read_csv(DATA_DIR / "occupations.csv")

df = load_occupations()

st.title("🔍 Occupation Explorer")
st.caption("AI Labor Market Signal Dashboard | Anthropic Economic Index + BLS Data")
st.markdown("---")

# ── Filters ────────────────────────────────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns([2, 1, 1])

with col_f1:
    search = st.text_input("Search occupations", placeholder="e.g. programmer, analyst, nurse…")

with col_f2:
    tier_filter = st.multiselect(
        "Exposure Tier",
        options=["High", "Medium", "Low"],
        default=["High", "Medium", "Low"],
    )

with col_f3:
    sector_options = sorted(df["sector"].unique())
    sector_filter = st.multiselect(
        "Sector",
        options=sector_options,
        default=sector_options,
    )

# Apply filters
mask = (
    df["exposure_tier"].isin(tier_filter)
    & df["sector"].isin(sector_filter)
)
if search:
    mask &= df["occupation"].str.contains(search, case=False, na=False)

filtered = df[mask].copy()

st.markdown(f"**{len(filtered)} occupation(s) matched**")

# ── Top-15 Exposure Bar Chart ──────────────────────────────────────────────────
st.subheader("Top 15 Occupations by Observed AI Exposure Score")

top15 = (
    df.nlargest(15, "exposure_score")
    .sort_values("exposure_score", ascending=True)
)

tier_colors = {"High": "#f38ba8", "Medium": "#fab387", "Low": "#a6e3a1"}

fig = px.bar(
    top15,
    x="exposure_score",
    y="occupation",
    orientation="h",
    color="exposure_tier",
    color_discrete_map=tier_colors,
    text=top15["exposure_score"].apply(lambda v: f"{v}%"),
    hover_data={"sector": True, "soc_code": True, "bls_growth_projection": True},
    template="plotly_dark",
    labels={
        "exposure_score": "Observed AI Exposure Score (%)",
        "occupation": "",
        "exposure_tier": "Tier",
    },
    title="Highest Observed AI Exposure — Top 15 Occupations",
)
fig.update_traces(textposition="outside")
fig.update_layout(
    height=520,
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font_color="#cdd6f4",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(range=[0, 100]),
)

st.plotly_chart(fig, use_container_width=True)
st.markdown(
    '<p class="footnote">Source: Anthropic Economic Index (March 2026). Observed exposure reflects real-world task '
    "augmentation/substitution by AI systems — distinct from theoretical task-overlap models.</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Scatter: Exposure vs Growth for filtered set ───────────────────────────────
if len(filtered) > 1:
    st.subheader("Exposure vs. Projected Growth — Filtered View")

    fig2 = px.scatter(
        filtered,
        x="exposure_score",
        y="bls_growth_projection",
        color="exposure_tier",
        color_discrete_map=tier_colors,
        hover_name="occupation",
        hover_data={"sector": True, "soc_code": True},
        template="plotly_dark",
        labels={
            "exposure_score": "Observed AI Exposure Score (%)",
            "bls_growth_projection": "BLS Projected Growth 2024–2034 (%)",
            "exposure_tier": "Tier",
        },
    )
    fig2.add_hline(y=0, line_dash="dot", line_color="#6c7086", annotation_text="0% growth")
    fig2.update_layout(
        height=380,
        plot_bgcolor="#1e1e2e",
        paper_bgcolor="#1e1e2e",
        font_color="#cdd6f4",
    )
    fig2.update_traces(marker=dict(size=10, opacity=0.85))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Searchable Dataframe ───────────────────────────────────────────────────────
st.subheader("Occupation Data Table")

display_df = filtered[[
    "occupation", "soc_code", "sector", "exposure_tier",
    "exposure_score", "bls_growth_projection",
]].rename(columns={
    "occupation": "Occupation",
    "soc_code": "SOC Code",
    "sector": "Sector",
    "exposure_tier": "Tier",
    "exposure_score": "Exposure Score (%)",
    "bls_growth_projection": "BLS Growth 2024–2034 (%)",
}).sort_values("Exposure Score (%)", ascending=False)

# Color-coded tier column
def style_tier(val):
    colors = {"High": "#f38ba840", "Medium": "#fab38740", "Low": "#a6e3a140"}
    return f"background-color: {colors.get(val, '')}; font-weight: 600"

st.dataframe(
    display_df.style.applymap(style_tier, subset=["Tier"]),
    use_container_width=True,
    height=420,
)

st.markdown(
    '<p class="footnote">Sources: Anthropic Economic Index (March 2026); BLS Standard Occupational Classification '
    "(SOC); BLS Employment Projections 2024–2034.</p>",
    unsafe_allow_html=True,
)
