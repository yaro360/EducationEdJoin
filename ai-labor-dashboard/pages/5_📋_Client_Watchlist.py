import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Client Watchlist", page_icon="📋", layout="wide")

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "watchlist.db"

# ── Exposure tier assignment map (by occupation category keyword) ──────────────
TIER_MAP = {
    "software": "High", "developer": "High", "programmer": "High",
    "data entry": "High", "data analyst": "High", "analyst": "High",
    "customer service": "High", "call center": "High",
    "accounting": "High", "bookkeeping": "High", "tax": "High",
    "legal secretary": "High", "paralegal": "High", "transcription": "High",
    "underwriter": "High", "loan": "High",
    "hr": "Medium", "human resources": "Medium", "compliance": "Medium",
    "graphic design": "Medium", "purchasing": "Medium",
    "network admin": "Medium", "database admin": "Medium",
    "manager": "Medium", "operations": "Medium",
    "nurse": "Low", "physician": "Low", "therapist": "Low",
    "teacher": "Low", "social worker": "Low",
    "construction": "Low", "electrician": "Low", "plumber": "Low",
    "carpenter": "Low", "retail": "Low", "chef": "Low",
    "security": "Low", "childcare": "Low",
}

RECOMMENDED_ACTIONS = {
    "High": "🔴 Immediate AI readiness audit; reskilling roadmap Q1",
    "Medium": "🟡 Pilot AI tools; monitor automation risk quarterly",
    "Low": "🟢 Low urgency; track coverage gap trends annually",
}

TREND_ICONS = {"High": "↓ Declining", "Medium": "→ Stable", "Low": "↑ Growing"}


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            industry TEXT NOT NULL,
            occupation_category TEXT NOT NULL,
            exposure_tier TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            trend_direction TEXT NOT NULL,
            recommended_action TEXT NOT NULL,
            added_date TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def assign_tier(occupation_category: str) -> str:
    occ_lower = occupation_category.lower()
    for keyword, tier in TIER_MAP.items():
        if keyword in occ_lower:
            return tier
    return "Medium"  # default


def tier_to_risk_score(tier: str) -> int:
    return {"High": 85, "Medium": 55, "Low": 20}.get(tier, 50)


# ── Init DB ────────────────────────────────────────────────────────────────────
conn = get_connection()

st.title("📋 Client Watchlist")
st.caption("AI Labor Market Signal Dashboard | Anthropic Economic Index + BLS Data")
st.markdown("---")

# ── Add Client Form ────────────────────────────────────────────────────────────
st.subheader("Add New Client")

with st.form("add_client_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        client_name = st.text_input(
            "Client / Company Name *",
            placeholder="e.g. Acme Financial Corp",
        )
        industry = st.selectbox(
            "Industry *",
            options=[
                "Financial Services",
                "Technology",
                "Healthcare",
                "Legal & Professional Services",
                "Insurance",
                "Retail & E-Commerce",
                "Media & Publishing",
                "Manufacturing",
                "Government & Public Sector",
                "Education",
                "Real Estate",
                "Consulting",
                "Other",
            ],
        )

    with col2:
        occupation_category = st.text_input(
            "Primary Occupation Category *",
            placeholder="e.g. Software Developer, Customer Service, Accounting",
        )
        notes = st.text_area(
            "Notes (optional)",
            placeholder="Context, engagement stage, key contacts…",
            height=100,
        )

    submitted = st.form_submit_button("Add to Watchlist", use_container_width=True)

    if submitted:
        if not client_name or not occupation_category:
            st.error("Client name and occupation category are required.")
        else:
            tier = assign_tier(occupation_category)
            risk_score = tier_to_risk_score(tier)
            action = RECOMMENDED_ACTIONS[tier]
            trend = TREND_ICONS[tier]

            conn.execute(
                """
                INSERT INTO watchlist
                (client_name, industry, occupation_category, exposure_tier,
                 risk_score, trend_direction, recommended_action, added_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    client_name, industry, occupation_category, tier,
                    risk_score, trend, action, datetime.now().strftime("%Y-%m-%d"),
                ),
            )
            conn.commit()
            st.success(
                f"Added **{client_name}** — Tier: **{tier}** | Risk Score: **{risk_score}/100**"
            )

st.markdown("---")

# ── Watchlist Table ────────────────────────────────────────────────────────────
st.subheader("Watchlist")

watchlist_df = pd.read_sql("SELECT * FROM watchlist ORDER BY risk_score DESC, added_date DESC", conn)

if watchlist_df.empty:
    st.info("No clients yet. Use the form above to add your first client.")
else:
    # ── Summary KPIs ───────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Clients", len(watchlist_df))
    with k2:
        high_count = (watchlist_df["exposure_tier"] == "High").sum()
        st.metric("High-Risk Clients", high_count)
    with k3:
        avg_risk = watchlist_df["risk_score"].mean()
        st.metric("Avg Risk Score", f"{avg_risk:.0f}/100")
    with k4:
        industries = watchlist_df["industry"].nunique()
        st.metric("Industries Covered", industries)

    st.markdown("")

    # ── Filterable display ─────────────────────────────────────────────────────
    tier_filter = st.multiselect(
        "Filter by Tier",
        options=["High", "Medium", "Low"],
        default=["High", "Medium", "Low"],
        key="wl_tier_filter",
    )
    display = watchlist_df[watchlist_df["exposure_tier"].isin(tier_filter)].copy()

    display_cols = display[[
        "client_name", "industry", "occupation_category",
        "exposure_tier", "risk_score", "trend_direction",
        "recommended_action", "added_date",
    ]].rename(columns={
        "client_name": "Client",
        "industry": "Industry",
        "occupation_category": "Occupation Focus",
        "exposure_tier": "Tier",
        "risk_score": "Risk Score",
        "trend_direction": "Trend",
        "recommended_action": "Recommended Action",
        "added_date": "Added",
    })

    def style_tier(val):
        c = {"High": "#f38ba840", "Medium": "#fab38740", "Low": "#a6e3a140"}
        return f"background-color: {c.get(val, '')}; font-weight:600"

    def style_risk(val):
        if val >= 75:
            return "color: #f38ba8; font-weight:700"
        elif val >= 45:
            return "color: #fab387; font-weight:600"
        return "color: #a6e3a1"

    st.dataframe(
        display_cols.style
        .applymap(style_tier, subset=["Tier"])
        .applymap(style_risk, subset=["Risk Score"]),
        use_container_width=True,
        height=400,
    )

    # ── Delete controls ────────────────────────────────────────────────────────
    with st.expander("Remove a client"):
        client_options = watchlist_df["client_name"].tolist()
        to_delete = st.selectbox("Select client to remove", options=["— select —"] + client_options)
        if st.button("Remove", type="secondary") and to_delete != "— select —":
            conn.execute("DELETE FROM watchlist WHERE client_name = ?", (to_delete,))
            conn.commit()
            st.success(f"Removed {to_delete}")
            st.rerun()

    # ── Risk distribution chart ────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Client Risk Distribution")

    import plotly.express as px

    tier_colors = {"High": "#f38ba8", "Medium": "#fab387", "Low": "#a6e3a1"}
    tier_counts = (
        watchlist_df["exposure_tier"]
        .value_counts()
        .reindex(["High", "Medium", "Low"], fill_value=0)
        .reset_index()
    )
    tier_counts.columns = ["Tier", "Count"]

    fig = px.pie(
        tier_counts,
        names="Tier",
        values="Count",
        color="Tier",
        color_discrete_map=tier_colors,
        template="plotly_dark",
        title="Clients by AI Exposure Risk Tier",
        hole=0.45,
    )
    fig.update_layout(
        height=360,
        plot_bgcolor="#1e1e2e",
        paper_bgcolor="#1e1e2e",
        font_color="#cdd6f4",
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown(
    '<p class="footnote">Risk scores are auto-assigned based on occupation keyword matching against the '
    "Anthropic Economic Index exposure tier classifications. Refine by editing the TIER_MAP in this page.</p>",
    unsafe_allow_html=True,
)
