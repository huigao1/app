import streamlit as st
import pandas as pd
from utils import load_esg_zip

# ------------------------------------------------------------------
# Hero / Overview + Data preview in ONE page
# ------------------------------------------------------------------

st.title("🏠 Welcome to the ESG Analytics Suite – Corporate Margin Predictor")

st.markdown("""
This interactive dashboard helps you **explore**, **analyze**, and **model** how
Environmental‑Social‑Governance (**ESG**) performance and core financial ratios drive two profitability measures:

**• EBITDA Margin  • Operating Margin**

---
### 🔎 Why This Matters
* **Investor Insight** – Quantify how leverage, efficiency, and ESG improvements impact margins.
* **Strategic Planning** – Run “what‑if” scenarios on ESG pillars.
* **ESG Integration** – Bridge sustainability and valuation to spot mispriced stocks.

---
### 📚 Key Definitions
<details>
<summary><strong>EBITDA Margin</strong></summary>
EBITDA ÷ Revenue — operating profit before interest, taxes, depreciation & amortization.
</details>
<details>
<summary><strong>Operating Margin</strong></summary>
Operating Income ÷ Revenue — percentage of revenue left after operating expenses.
</details>

---
### 🗺️ What You Can Do Here
| Group | Page | Purpose |
|-------|------|---------|
| **Start** | Dataset Overview (this page) | Preview & download master dataset |
| **EDA** | Exploratory · Industry · Trends · Scatter Matrix | Interactive visuals & filters |
| **ML** | Regression Playground · K‑Means · Model Training · Predict by Ticker | Build models & forecast margins |
| **Docs** | Model & Ratios · About | Formulas, methodology, changelog |

---
### 🚀 Quick Start
1. Use sidebar filters on EDA pages.  
2. Head to **Predict by Ticker** to test real firms.  
3. Read **Model & Ratios** for formulas & pipeline.
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Dataset preview & download
# ------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    return load_esg_zip()

df = load_data()

st.subheader("📄 Dataset Preview")

