import streamlit as st
import pandas as pd
from utils import load_esg_zip

# -------------------------------------------------------------
# Hero / Landing
# -------------------------------------------------------------

st.title("🔍 Forecasting Profitability with Financial & ESG Signals")

st.markdown("""
Welcome to the *Corporate Margin Predictor*, a proof‑of‑concept dashboard that uses core **financial ratios** plus **ESG (Environmental, Social, Governance)** scores to estimate two critical profitability measures:

1. **EBITDA Margin**  
2. **Operating Margin**

---
### 🔎 Why This Matters
* **Investor Insight** – Quantify how changes in asset efficiency, leverage, and ESG performance translate into bottom‑line profitability.  
* **Strategic Planning** – Run *what‑if* scenarios—e.g., “If a company boosts its Environmental Score by 5 points, how much could its EBITDA margin improve?”  
* **ESG Integration** – Bridge the gap between sustainability performance and financial outcomes, helping analysts identify under‑ or over‑priced stocks.

---
### 📚 Key Definitions
<details>
<summary><strong>What is EBITDA Margin?</strong></summary>
EBITDA ÷ Revenue — measures operating performance before interest, taxes, depreciation & amortization.
</details>

<details>
<summary><strong>What is Operating Margin?</strong></summary>
Operating Income ÷ Revenue — percentage of revenue left after covering operating expenses (incl. D&A).
</details>

---
### 🚀 Next Steps
1. **Select a Year & Sector** in the sidebar to focus your analysis.  
2. **Explore Feature Importance** to see which ratios and ESG pillars drive predictions.  
3. **Test Real Companies** on *Predict by Ticker* (e.g., Apple, Tesla) and see the model in action.

Scroll down to begin your exploration!
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Dataset preview & download
# -------------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    return load_esg_zip()

df = load_data()

st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

st.markdown("---\n*Tip: use the navigation bar above to explore EDA or modeling pages.*")
