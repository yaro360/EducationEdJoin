import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Coverage Gap", page_icon="🧩", layout="wide")

st.title("🧩 AI Coverage Gap Analysis")
st.caption("AI Labor Market Signal Dashboard | Anthropic Economic Index + BLS Data")
st.markdown("---")

# ── Explanation ────────────────────────────────────────────────────────────────
with st.expander("What is the Coverage Gap?", expanded=True):
    st.markdown(
        """
        **Theoretical coverage** (task-overlap models like O*NET + GPT-4 task matching) predicts
        that the majority of white-collar occupations are exposed to AI automation. But
        **observed coverage** — measured by what workers are *actually using* AI for in their day-to-day
        tasks — is dramatically lower.

        The gap represents the difference between:
        - What AI *could* do based on task descriptions
        - What AI is *actually doing* in real workplaces today

        This gap reflects adoption friction: change management, regulation, trust, workflow
        integration, and tacit knowledge that resists automation. Tracking its size over time
        reveals the pace of real-world AI diffusion. Source: Anthropic Economic Index, March 2026.
        """
    )

# ── Data ───────────────────────────────────────────────────────────────────────
coverage_data = pd.DataFrame(
    {
        "Sector": [
            "Computer & Mathematical",
            "Office & Administrative Support",
            "Business & Financial Operations",
            "Legal",
            "Arts, Design & Media",
            "Healthcare Support",
            "Healthcare Practitioners",
            "Education & Library",
            "Management",
            "Sales & Related",
        ],
        "Theoretical Coverage (%)": [94, 90, 75, 55, 60, 35, 40, 30, 50, 45],
        "Observed Coverage (%)": [33, 28, 22, 15, 18, 9, 8, 7, 14, 10],
    }
).sort_values("Theoretical Coverage (%)", ascending=True)

coverage_data["Gap (pp)"] = (
    coverage_data["Theoretical Coverage (%)"] - coverage_data["Observed Coverage (%)"]
)
coverage_data["Adoption Rate (%)"] = (
    (coverage_data["Observed Coverage (%)"] / coverage_data["Theoretical Coverage (%)"]) * 100
).round(1)

# ── Main horizontal grouped bar chart ─────────────────────────────────────────
st.subheader("Theoretical vs. Observed AI Coverage by Sector")

fig = go.Figure()

fig.add_trace(
    go.Bar(
        y=coverage_data["Sector"],
        x=coverage_data["Theoretical Coverage (%)"],
        name="Theoretical Coverage",
        orientation="h",
        marker_color="#89b4fa",
        opacity=0.55,
        text=[f"{v}%" for v in coverage_data["Theoretical Coverage (%)"]],
        textposition="outside",
        hovertemplate="%{y}<br>Theoretical: %{x}%<extra></extra>",
    )
)

fig.add_trace(
    go.Bar(
        y=coverage_data["Sector"],
        x=coverage_data["Observed Coverage (%)"],
        name="Observed Coverage",
        orientation="h",
        marker_color="#f38ba8",
        text=[f"{v}%" for v in coverage_data["Observed Coverage (%)"]],
        textposition="outside",
        hovertemplate="%{y}<br>Observed: %{x}%<extra></extra>",
    )
)

fig.update_layout(
    barmode="overlay",
    template="plotly_dark",
    height=520,
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font_color="#cdd6f4",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(title="Coverage (%)", range=[0, 115], showgrid=True, gridcolor="#313244"),
    yaxis=dict(title=""),
    title="The Coverage Gap: AI Potential vs. Workplace Reality",
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    '<p class="footnote">Source: Anthropic Economic Index (March 2026). Theoretical coverage uses task-overlap '
    "methodology (O*NET + GPT-4 capability matching). Observed coverage derived from AI usage patterns "
    "in actual workplace tasks across sectors.</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Gap magnitude chart ────────────────────────────────────────────────────────
st.subheader("Coverage Gap Magnitude (Theoretical − Observed)")

gap_sorted = coverage_data.sort_values("Gap (pp)", ascending=True)

fig2 = px.bar(
    gap_sorted,
    x="Gap (pp)",
    y="Sector",
    orientation="h",
    color="Gap (pp)",
    color_continuous_scale=["#a6e3a1", "#fab387", "#f38ba8"],
    text=gap_sorted["Gap (pp)"].apply(lambda v: f"{v}pp"),
    template="plotly_dark",
    labels={"Gap (pp)": "Gap (percentage points)", "Sector": ""},
    title="Largest Gaps = Highest Adoption Friction",
)
fig2.update_traces(textposition="outside")
fig2.update_layout(
    height=420,
    coloraxis_showscale=False,
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font_color="#cdd6f4",
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Adoption rate scatter ──────────────────────────────────────────────────────
st.subheader("Adoption Rate (Observed / Theoretical)")

fig3 = px.scatter(
    coverage_data,
    x="Theoretical Coverage (%)",
    y="Adoption Rate (%)",
    size="Observed Coverage (%)",
    color="Adoption Rate (%)",
    color_continuous_scale=["#f38ba8", "#fab387", "#a6e3a1"],
    hover_name="Sector",
    hover_data={"Observed Coverage (%)": True, "Gap (pp)": True},
    text="Sector",
    template="plotly_dark",
    labels={
        "Theoretical Coverage (%)": "Theoretical AI Coverage (%)",
        "Adoption Rate (%)": "Observed / Theoretical (%)",
    },
    title="Sectors with High Theoretical Exposure Have Lowest Adoption Rates",
)
fig3.update_traces(textposition="top center", textfont_size=9)
fig3.update_layout(
    height=480,
    coloraxis_showscale=False,
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font_color="#cdd6f4",
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── Data table ─────────────────────────────────────────────────────────────────
st.subheader("Coverage Gap Data Table")

table_df = coverage_data[[
    "Sector", "Theoretical Coverage (%)", "Observed Coverage (%)",
    "Gap (pp)", "Adoption Rate (%)",
]].sort_values("Gap (pp)", ascending=False)

def style_gap(val):
    if val >= 60:
        return "color: #f38ba8; font-weight:700"
    elif val >= 40:
        return "color: #fab387"
    return "color: #a6e3a1"

st.dataframe(
    table_df.style.applymap(style_gap, subset=["Gap (pp)"]),
    use_container_width=True,
    hide_index=True,
)

# ── Strategic implications ─────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Strategic Implications for CTOs & Consultants")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        **High-Gap Sectors (>50pp gap)**
        Massive unrealized automation potential. These sectors face the sharpest
        future disruption risk as adoption friction reduces over time. Clients here
        should begin AI readiness audits **now** to get ahead of the curve.

        *Sectors: Computer & Math, Office & Admin, Business & Finance*
        """
    )

with col2:
    st.markdown(
        """
        **Low-Gap Sectors (<30pp gap)**
        Either lower theoretical exposure or slower adoption pathways (regulatory,
        physical-world constraints). Lower urgency but continued monitoring warranted
        as AI capabilities expand into embodied and domain-specific tasks.

        *Sectors: Healthcare, Education, Sales*
        """
    )
