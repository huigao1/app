import streamlit as st

# -------------------------------------------------------------
# Intro / Hero Page
# -------------------------------------------------------------

st.set_page_config(page_title="Corporate Margin Predictor", page_icon="📊", layout="wide")

st.title("🏠 Welcome to the ESG Analytics Suite – Corporate Margin Predictor")

st.markdown("""
This interactive dashboard helps you **explore**, **analyze**, and **model** how
Environmental-Social-Governance (**ESG**) performance and classic financial ratios
affect two critical profitability measures:

**1. EBITDA Margin**  **2. Operating Margin**

---
### 🔎 Why This Matters
* **Investor Insight** – Quantify how changes in asset efficiency, leverage, and ESG pillars translate into bottom-line profitability.
* **Strategic Planning** – Run “what-if” scenarios—e.g., *“If a company boosts its Environmental Score by 5 points, how much could its EBITDA margin improve?”*
* **ESG Integration** – Bridge sustainability performance with financial outcomes to identify mispriced stocks.

---
### 📚 Key Definitions
<details>
<summary><strong>EBITDA Margin</strong></summary>
EBITDA Margin = *EBITDA ÷ Revenue* – operating performance before interest, taxes, depreciation, and amortization.
</details>

<details>
<summary><strong>Operating Margin</strong></summary>
Operating Margin = *Operating Income ÷ Revenue* – percentage of revenue remaining after operating expenses.
</details>

---
### 🗺️ What You Can Do Here
| Group | Page | Purpose |
|-------|------|---------|
| **Start** | Dataset Overview | Quick preview & download of the master dataset |
| **EDA** | Exploratory · Industry · Trends · Scatter Matrix | Visual deep-dive with filters |
| **ML** | Regression Playground · K-Means · Model Training · Predict by Ticker | Build regressions, cluster companies, benchmark ML models, and forecast margins |
| **Docs** | Model & Ratios · About | Ratio formulas, methodology, and version info |

---
### 🚀 Getting Started
1. **Select a Year & Division** in the sidebar ﬁlters on relevant pages.
2. Explore **Feature Importance** and model outputs in ML tabs.
3. **Test Real Companies** on *Predict by Ticker* (e.g., AAPL, TSLA).

> **Tip:** Tables are interactive – click column headers to sort or use the search box.

Enjoy analyzing! If you have ideas for new features, [open an issue](https://github.com/your-repo).
""", unsafe_allow_html=True)
