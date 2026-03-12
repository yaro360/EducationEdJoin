# AI Labor Market Signal Dashboard

A local Streamlit dashboard for CTOs and tech consultants to track AI-driven
labor market disruption signals, based on Anthropic's **"observed exposure"**
framework from their March 2026 Economic Index research paper.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the dashboard

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
ai-labor-dashboard/
├── app.py                          # Main entry point (Streamlit multi-page)
├── requirements.txt
├── README.md
├── data/
│   ├── occupations.csv             # Seed occupation data (50 occupations)
│   ├── hiring_trends.csv           # Monthly time series 2020–2025
│   ├── watchlist.db                # Auto-created SQLite on first run
│   └── bls_ep_table1.csv           # Optional — place BLS EP CSV here
└── pages/
    ├── 1_📈_Overview.py
    ├── 2_🔍_Occupation_Explorer.py
    ├── 3_📉_Hiring_Trends.py
    ├── 4_🏛_BLS_Projections.py
    ├── 5_📋_Client_Watchlist.py
    └── 6_🧩_Coverage_Gap.py
```

---

## Pages

| Page | Description |
|---|---|
| **Overview** | KPI cards, exposure vs. BLS growth scatter, sector averages |
| **Occupation Explorer** | Searchable/filterable table, top-15 bar chart |
| **Hiring Trends** | Job-finding rate DiD chart with ChatGPT event line |
| **BLS Projections** | Growth by exposure tier, waterfall, sector scatter |
| **Client Watchlist** | Add clients → auto-assign risk tier → SQLite storage |
| **Coverage Gap** | Theoretical vs. observed coverage grouped bar chart |

---

## Replacing Mock Data with Real BLS Data

### Option A: BLS Public Data API v2

The BLS Public API v2 (no registration required for <500 requests/day) can pull
employment projections and CPS data programmatically.

**Endpoint:**
```
https://api.bls.gov/publicAPI/v2/timeseries/data/
```

**Example request (Python/requests):**

```python
import requests, json

headers = {"Content-type": "application/json"}
payload = json.dumps({
    "seriesid": ["OEUN000000000000000000001"],  # Replace with target series ID
    "startyear": "2020",
    "endyear": "2025",
    "registrationkey": "YOUR_API_KEY",  # Register free at data.bls.gov/registrationEngine
})

response = requests.post(
    "https://api.bls.gov/publicAPI/v2/timeseries/data/",
    data=payload,
    headers=headers,
)
data = response.json()
```

**Useful BLS series prefixes:**
- `OES` — Occupational Employment and Wage Statistics
- `EP` — Employment Projections (pull `ep-table1.csv` directly from bls.gov/emp)
- `LN` — Labor Force Statistics from the CPS

**BLS Employment Projections CSV:**
Download directly from:
```
https://www.bls.gov/emp/tables/emp-by-detailed-occupation.htm
```
Save as `data/bls_ep_table1.csv` — the BLS Projections page will auto-load it.

### Option B: BLS Data Viewer
Browse and export series at [beta.bls.gov/dataViewer/](https://beta.bls.gov/dataViewer/).

---

## Connecting to Lightcast (Burning Glass) API

Lightcast provides real-time job posting data useful for measuring hiring velocity.

```python
import requests

# Step 1: Get OAuth2 token
token_response = requests.post(
    "https://auth.emsicloud.com/connect/token",
    data={
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "grant_type": "client_credentials",
        "scope": "postings:us",
    },
)
access_token = token_response.json()["access_token"]

# Step 2: Query job postings by SOC code
headers = {"Authorization": f"Bearer {access_token}"}
postings = requests.post(
    "https://emsiservices.com/jpa/postings/us/timeseries",
    headers=headers,
    json={
        "filter": {
            "when": {"start": "2023-01", "end": "2025-12"},
            "occupation": {"soc5": ["15-1252"]},  # Software Developers
        },
        "metrics": ["unique_postings"],
        "timeseries_resolution": "month",
    },
)
print(postings.json())
```

Contact [lightcast.io](https://lightcast.io) for API access (paid).

---

## Data Sources & Methodology

- **Anthropic Economic Index (March 2026)** — Observed AI exposure scores and
  hiring velocity estimates. "Observed exposure" measures real-world task
  augmentation/substitution by AI tools, not theoretical task overlap.
- **BLS Occupational Outlook Handbook** — Employment projections 2024–2034
- **BLS Current Population Survey (CPS)** — Job-finding rate microdata

All charts currently use **seeded mock data** calibrated to match reported
paper magnitudes. Replace with live API calls for production use.

---

## Enabling Dark Theme

Add to `.streamlit/config.toml`:

```toml
[theme]
base = "dark"
primaryColor = "#cba6f7"
backgroundColor = "#1e1e2e"
secondaryBackgroundColor = "#181825"
textColor = "#cdd6f4"
```

---

## License

MIT — for internal/client use. Data sources subject to BLS public use terms
and Anthropic Economic Index citation requirements.
