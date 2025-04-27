import streamlit as st
import pandas as pd
from utils import load_esg_zip

# -------------------------------------------------------------
# Hero / Landing section
# -------------------------------------------------------------

st.set_page_config(page_title="Corporate Margin Predictor", page_icon="📊", layout="wide")

st.title("🔍 Forecasting Profitability with Financial & ESG Signals")

st.markdown("""
Welcome to the *Corporate Margin Predictor*, a proof‑of‑concept dashboard that blends core **financial ratios** with **ESG (Environmental, Social, Governance) scores** to estimate two critical profitability measures:

1. **EBITDA Margin**  
2. **Operating Margin**

---
### 🔎 Why This Matters
* **Investor Insight** – Quantify how changes in asset efficiency, leverage, and ESG pillars translate into bottom‑line profitability.  
* **Strategic Planning** – Run *what‑if* scenarios—e.g., “If a company boosts its Environmental Score by 5 points, how much could its EBITDA margin improve?”  
* **ESG Integration** – Bridge sustainability performance with financial outcomes to spot under‑ or over‑priced stocks.

---
### 📚 Key Definitions
<details>
<summary><strong>EBITDA Margin</strong></summary>
EBITDA ÷ Revenue – measures operating performance before interest, taxes, depreciation, and amortization.
</details>

<details>
<summary><strong>Operating Margin</strong></summary>
Operating Income ÷ Revenue – percentage of revenue left after operating expenses (incl. D&A), indicating core efficiency.
</details>

---
### 🚀 Next Steps
1. **Select a Year & Division** via sidebar filters on EDA pages.  
2. **Explore Feature Importance** in the ML section to see which ratios and ESG pillars drive predictions.  
3. **Test Real Companies** on *Predict by Ticker* (e.g., AAPL, TSLA) to see the model in action.

Scroll down to begin your exploration!
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Dataset preview & download
# -------------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    return load_esg_zip()

df = load_data()

