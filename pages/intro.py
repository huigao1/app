import streamlit as st
import pandas as pd
from utils import load_esg_zip

# -------------------------------------------------------------
# Hero / Landing
# -------------------------------------------------------------

st.title("🔍 Forecasting Profitability with Financial & ESG Signals")

st.markdown("""
Welcome to the **Corporate Margin Predictor**, a proof‑of‑concept dashboard that blends core **financial ratios** with **ESG (Environmental, Social, Governance)** scores to estimate two critical profitability measures:

1. **EBITDA Margin**  2. **Operating Margin**
""")

# ---------------- Why This Matters ----------------
with st.expander("🔎 Why This Matters", expanded=True):
    st.markdown("""
* **Investor Insight** – Quantify how changes in asset efficiency, leverage, and ESG performance translate into bottom‑line profitability.  
* **Strategic Planning** – Run *what‑if* scenarios—e.g., “If a firm boosts its Environmental Score by 5 points, how much could its EBITDA margin improve?”  
* **ESG Integration** – Bridge sustainability metrics with valuation to uncover mispriced stocks.
""")

# ---------------- Key Definitions ----------------
with st.expander("📚 Key Formulas & Definitions", expanded=True):
    st.markdown("""
| Metric | Formula | Insight |
|--------|---------|---------|
| **EBITDA Margin** | `EBITDA / Revenue` | Strips away capital structure & accounting charges; enables cross‑company comparison. |
| **Operating Margin** | `Operating Income / Revenue` | Shows core efficiency after operating costs and depreciation. |

<details>
<summary><strong>EBITDA</strong></summary>
**E**arnings **B**efore **I**nterest, **T**axes, **D**epreciation & **A**mortization – cash‑flow proxy.
</details>

<details>
<summary><strong>Operating Income</strong></summary>
Also called **EBIT** – profit after operating expenses but before interest & tax.
</details>
""", unsafe_allow_html=True)


# ---------------- ESG Pillars ----------------
with st.expander("🌿 ESG Pillars & Key Sub‑Scores", expanded=False):
    st.markdown("""
| Pillar | Sub‑score | Dataset column | What it captures |
|--------|-----------|----------------|------------------|
| **Environmental** | Emissions | `ESG_Emissions_Score` | CO₂e footprint, reduction initiatives |
| | Environmental Overall | `ESG_Environmental_Score` | Resource use, waste, biodiversity |
| **Social** | Human Rights | `ESG_Human_Rights_Score` | Supply‑chain labor standards |
| | Workforce | `ESG_Workforce_Score` | Diversity, safety, training |
| **Governance** | Governance Overall | `ESG_Governance_Score` | Board structure, pay, audit quality |
| ‑ | Controversies | `ESG_Controversies_Score` | Litigation, scandals, regulatory fines |
""")

# ---------------- Next Steps ----------------
with st.expander("🚀 Next Steps", expanded=True):
    st.markdown("""
1. **Select a Year & Division** with sidebar filters in EDA pages.  
2. **Explore Feature Importance** under *Model Training* to see which ratios and ESG pillars drive predictions.  
3. **Predict Real Companies** on *Predict by Ticker* (AAPL, TSLA, etc.).
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

st.markdown("---\n*Use the **navigation bar** at the top to explore EDA or modeling pages.*")
