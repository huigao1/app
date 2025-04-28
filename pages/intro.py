import streamlit as st
import pandas as pd
from utils import load_esg_zip

# -------------------------------------------------------------
# Hero / Landing ------------------------------------------------
# -------------------------------------------------------------

st.title("🔍 <span style='color:red'>WHAT?</span> Forecasting Profitability with Financial & ESG Signals", unsafe_allow_html=True)

st.markdown("""
Welcome to the **Corporate Margin Predictor**, a dashboard that blends core **financial ratios** with **ESG** scores to forecast two profitability metrics:

* **EBITDA Margin** – pre‑financing operating profitability  
* **Operating Margin** – efficiency after operating expenses & depreciation
""")

# ---------------- WHY ----------------
with st.expander("<span style='color:red'>WHY?</span> Importance", expanded=True):
    st.markdown("""
* **Investor Insight** – Understand how leverage, efficiency, and ESG improvements drive margins.  
* **Strategic Planning** – Run *what‑if* scenarios: “If Environmental Score ↑5 pts, EBITDA Margin ↑?”  
* **Valuation Edge** – Connect sustainability metrics with valuation to spot mispriced stocks.
""", unsafe_allow_html=True)

# ---------------- WHY Targets ----------------
with st.expander("🎯 Why predict these two margins?"):
    st.markdown("""
| Metric | Why it matters |
|--------|----------------|
| **EBITDA Margin** | \- Ignores capital structure & accounting noise → comparable across firms  <br>\- Anchors EV/EBITDA multiples in valuation |
| **Operating Margin** | \- Includes depreciation → captures full cost discipline  <br>\- Key KPI in DCF and management guidance |

> *Dual‑margin view* = one lens for **valuation** (EBITDA) + one for **operational health** (Operating).
""", unsafe_allow_html=True)

# ---------------- HOW ----------------
with st.expander("<span style='color:red'>HOW?</span> Methodology", expanded=True):
    st.markdown("""
1. **Data** – 5k firm‑years of cleaned accounting, market, and Refinitiv ESG scores  
2. **Feature Engineering** – Ratios (debt, turnover, ROA…), log assets, ESG pillars  
3. **Models** – Gradient Boosting & Linear Regression; cross‑validated hyper‑parameters  
4. **Evaluation** – Adjusted R² & MAE on 20 % hold‑out  
5. **What‑If** – Slider stress tests ESG risk and re‑predict margins
""", unsafe_allow_html=True)

# ---------------- Key Formulas ----------------
with st.expander("📚 Key Formulas", expanded=False):
    st.markdown("""
| Metric | Formula |
|--------|---------|
| **EBITDA Margin** | `EBITDA / Revenue` |
| **Operating Margin** | `Operating Income / Revenue` |

<details><summary><strong>EBITDA</strong></summary>
Earnings Before Interest, Taxes, Depreciation & Amortization – cash‑flow proxy.</details>

<details><summary><strong>Operating Income (EBIT)</strong></summary>
Profit after operating expenses but before interest & tax.</details>
""", unsafe_allow_html=True)

# ---------------- ESG Pillars ----------------
with st.expander("🌿 ESG Pillars & Key Sub‑Scores"):
    st.markdown("""
| Pillar | Sub‑score | Column | Captures |
|--------|-----------|--------|----------|
| **Environmental** | Emissions | `ESG_Emissions_Score` | CO₂e footprint, reduction targets |
|  | Environmental Overall | `ESG_Environmental_Score` | Resource use, biodiversity |
| **Social** | Human Rights | `ESG_Human_Rights_Score` | Supplier labor standards |
|  | Workforce | `ESG_Workforce_Score` | Diversity, safety, training |
| **Governance** | Governance Overall | `ESG_Governance_Score` | Board, pay, audit risk |
| – | Controversies | `ESG_Controversies_Score` | Litigation, scandals |
""")

# ---------------- Next Steps ----------------
with st.expander("🚀 Next Steps", expanded=True):
    st.markdown("""
1. Use sidebar filters (year, division) in EDA pages.  
2. Explore **Model Training** for feature importance & tuning.  
3. Try *Predict by Ticker* or *What‑If Simulator* to stress ESG risk.
""")

st.divider()

# -------------------------------------------------------------
# Dataset preview & download
# -------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    return load_esg_zip()

df = load_data()

st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

st.markdown("---\n*Use the **navigation bar** above to explore EDA or modeling pages.*")
