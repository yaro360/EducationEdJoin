import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Hiring Trends", page_icon="📉", layout="wide")

DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_trends():
    df = pd.read_csv(DATA_DIR / "hiring_trends.csv")
    df["month"] = pd.to_datetime(df["month"])
    return df

df = load_trends()

st.title("📉 Hiring Trends — Ages 22–25")
st.caption("AI Labor Market Signal Dashboard | Anthropic Economic Index + BLS Data")
st.markdown("---")

# ── Interpretation callout ─────────────────────────────────────────────────────
with st.expander("Methodology: Difference-in-Differences (DiD)", expanded=False):
    st.markdown(
        """
        **Design**
        We compare the job-finding rate (share of unemployed workers who find employment
        each month) for two cohorts of workers aged 22–25:

        - **High-exposure occupations** — ≥50% observed AI exposure (e.g., computer
          programmers, customer service, data entry)
        - **No-exposure occupations** — <10% observed AI exposure (e.g., construction
          trades, personal care, food service)

        **Event window**
        The "treatment" event is the public release of ChatGPT (November 30, 2022),
        which proxies for the rapid mainstreaming of generative AI tools in the workplace.

        **Key finding (Anthropic Economic Index, March 2026)**
        Workers in high-AI-exposure occupations saw their job-finding rate fall by roughly
        **14 percentage points** relative to their no-exposure peers between November 2022
        and December 2025 — a statistically significant difference-in-differences estimate.
        This gap is not explained by pre-existing trends (parallel trends hold before Nov 2022).

        **Caveat**
        The data shown here are illustrative mock series seeded to match reported magnitudes.
        Replace with BLS CPS microdata for production use.
        """
    )

# ── Main line chart ────────────────────────────────────────────────────────────
st.subheader("Monthly Job-Finding Rate — High-Exposure vs. No-Exposure Occupations")

chatgpt_date = pd.Timestamp("2022-11-01")

# Compute DiD gap for latest period
post = df[df["month"] >= chatgpt_date]
did_gap = (
    post["no_exposure_rate"].mean() - post["high_exposure_rate"].mean()
).round(1)

fig = go.Figure()

# High-exposure line
fig.add_trace(
    go.Scatter(
        x=df["month"],
        y=df["high_exposure_rate"],
        mode="lines",
        name="High-Exposure Occupations",
        line=dict(color="#f38ba8", width=2.5),
        hovertemplate="%{x|%b %Y}<br>Rate: %{y:.1f}%<extra>High-Exposure</extra>",
    )
)

# No-exposure line
fig.add_trace(
    go.Scatter(
        x=df["month"],
        y=df["no_exposure_rate"],
        mode="lines",
        name="No-Exposure Occupations",
        line=dict(color="#a6e3a1", width=2.5),
        hovertemplate="%{x|%b %Y}<br>Rate: %{y:.1f}%<extra>No-Exposure</extra>",
    )
)

# Shaded divergence area
fig.add_trace(
    go.Scatter(
        x=pd.concat([df["month"], df["month"][::-1]]),
        y=pd.concat([df["no_exposure_rate"], df["high_exposure_rate"][::-1]]),
        fill="toself",
        fillcolor="rgba(243,139,168,0.10)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Divergence Gap",
        showlegend=True,
        hoverinfo="skip",
    )
)

# ChatGPT release vertical line
fig.add_vline(
    x=chatgpt_date.timestamp() * 1000,
    line_width=2,
    line_dash="dash",
    line_color="#cba6f7",
    annotation_text="ChatGPT Release<br>Nov 2022",
    annotation_position="top right",
    annotation_font_color="#cba6f7",
    annotation_font_size=11,
)

# COVID shock annotation
fig.add_vrect(
    x0=pd.Timestamp("2020-03-01").timestamp() * 1000,
    x1=pd.Timestamp("2020-09-01").timestamp() * 1000,
    fillcolor="rgba(137,180,250,0.08)",
    line_width=0,
    annotation_text="COVID-19<br>Shock",
    annotation_position="top left",
    annotation_font_color="#89b4fa",
    annotation_font_size=10,
)

fig.update_layout(
    template="plotly_dark",
    height=500,
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font_color="#cdd6f4",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(title="Month", showgrid=False),
    yaxis=dict(title="Job-Finding Rate (%)", showgrid=True, gridcolor="#313244"),
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    '<p class="footnote">Source: Anthropic Economic Index (March 2026); illustrative series seeded to reported '
    "DiD estimates. Production use requires BLS Current Population Survey (CPS) microdata.</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ── DiD Summary Panel ──────────────────────────────────────────────────────────
st.subheader("Difference-in-Differences Summary")

pre = df[df["month"] < chatgpt_date]

pre_high = pre["high_exposure_rate"].mean()
pre_no = pre["no_exposure_rate"].mean()
post_high = post["high_exposure_rate"].mean()
post_no = post["no_exposure_rate"].mean()

did_estimate = (post_high - pre_high) - (post_no - pre_no)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Pre-ChatGPT Gap (High vs. No)", f"{(pre_no - pre_high):.1f}pp")

with col2:
    st.metric("Post-ChatGPT Gap (High vs. No)", f"{(post_no - post_high):.1f}pp")

with col3:
    st.metric(
        "DiD Estimate",
        f"{did_estimate:.1f}pp",
        delta="Relative decline for high-exposure",
        delta_color="inverse",
    )

with col4:
    st.metric(
        "Reported in Paper",
        "−14pp",
        delta="Anthropic Economic Index, Mar 2026",
        delta_color="off",
    )

st.markdown("---")

# ── Before/After table ─────────────────────────────────────────────────────────
st.subheader("Period Averages")

summary = pd.DataFrame(
    {
        "Period": ["Pre-ChatGPT (Jan 2020 – Oct 2022)", "Post-ChatGPT (Nov 2022 – Dec 2025)"],
        "High-Exposure Rate (%)": [f"{pre_high:.1f}", f"{post_high:.1f}"],
        "No-Exposure Rate (%)": [f"{pre_no:.1f}", f"{post_no:.1f}"],
        "Gap (No − High) (pp)": [f"{(pre_no - pre_high):.1f}", f"{(post_no - post_high):.1f}"],
    }
)

st.dataframe(summary, use_container_width=True, hide_index=True)

st.info(
    "**Interpretation:** Before ChatGPT, workers in both cohorts found jobs at similar rates "
    f"(gap ≈ {(pre_no - pre_high):.1f}pp). After the AI shock, the gap widened to "
    f"≈ {(post_no - post_high):.1f}pp — the DiD estimate of **{did_estimate:.1f}pp** captures "
    "the causal effect of AI exposure on early-career hiring velocity, consistent with the "
    "Anthropic paper's reported −14pp finding."
)
