import streamlit as st

st.set_page_config(
    page_title="AI Labor Market Signal Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global dark-theme CSS tweaks ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Sidebar nav label */
    [data-testid="stSidebarNav"] { padding-top: 1rem; }

    /* KPI metric cards */
    [data-testid="metric-container"] {
        background: #1e1e2e;
        border: 1px solid #313244;
        border-radius: 8px;
        padding: 1rem 1.2rem;
    }

    /* Footnote style */
    .footnote {
        font-size: 0.72rem;
        color: #6c7086;
        margin-top: 0.4rem;
    }

    /* Risk tier badges */
    .badge-high   { background:#f38ba8; color:#1e1e2e; padding:2px 8px; border-radius:4px; font-weight:600; }
    .badge-medium { background:#fab387; color:#1e1e2e; padding:2px 8px; border-radius:4px; font-weight:600; }
    .badge-low    { background:#a6e3a1; color:#1e1e2e; padding:2px 8px; border-radius:4px; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar header ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        ## 📊 AI Labor Market
        ### Signal Dashboard
        ---
        **Data Sources**
        • Anthropic Economic Index (Mar 2026)
        • BLS Occupational Outlook Handbook
        • BLS Employment Projections 2024–2034
        ---
        """,
        unsafe_allow_html=False,
    )

# ── Main landing splash (shown only on app.py itself, not sub-pages) ──────────
st.title("AI Labor Market Signal Dashboard")
st.caption("Powered by Anthropic Economic Index + BLS Data | Updated March 2026")

st.markdown(
    """
    Welcome. Use the **sidebar** to navigate between pages.

    | Page | What you'll find |
    |---|---|
    | 📈 Overview | KPIs, headline stats, exposure vs. growth scatter |
    | 🔍 Occupation Explorer | Searchable table + top-15 exposure bar chart |
    | 📉 Hiring Trends | Job-finding rate divergence since ChatGPT (Nov 2022) |
    | 🏛 BLS Projections | 2024–2034 projected growth by AI exposure tier |
    | 📋 Client Watchlist | Add clients, auto-assign risk tier, store in SQLite |
    | 🧩 Coverage Gap | Theoretical vs. observed AI coverage by sector |

    ---
    > **Methodology note:** "Observed exposure" measures the share of workers in an
    > occupation whose tasks are actively augmented or substituted by AI tools *today*,
    > as opposed to theoretical task-level overlap. Source: Anthropic Economic Index,
    > March 2026.
    """,
    unsafe_allow_html=False,
)
