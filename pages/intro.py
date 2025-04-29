import streamlit as st
import pandas as pd
from utils import load_esg_zip

st.markdown(
    "<h2 style='color:#d62728'>🔍 Corporate Margin Predictor</h2>"
    "<h4>Forecasting Profitability with Financial &amp; ESG Signals</h4>",
    unsafe_allow_html=True,
)

st.markdown("Team members: Hui Gao, Zehui Wang, Phunsok Norboo")
st.markdown("### 🔎 Why This Matters")
st.markdown(
    """
- **Investor Insight** · Link asset efficiency, leverage & ESG to bottom-line margins  
- **Strategic Planning** · Run *what-if* ESG scenarios (e.g.\ +5pts Environmental → Δ EBITDA)  
- **Valuation Edge** · Bridge sustainability metrics with pricing to detect mis-valued stocks
"""
)

st.markdown("### 🎯 Why Predict *EBITDA* & *Operating* Margins")
st.markdown(
    """
| &nbsp;Metric&nbsp; | Why it matters |
|-------------------|----------------|
| **EBITDA Margin** | Removes capital-structure noise → comparable across firms.<br>Anchors EV/EBITDA multiples. |
| **Operating Margin** | Includes depreciation → full cost discipline.<br>Core KPI in DCF & management guidance. |
""",
    unsafe_allow_html=True,
)

st.markdown("### 📚 Key Formulas")
st.markdown(
    """
| Metric | Formula |
|--------|---------|
| **EBITDA Margin** | `EBITDA / Revenue` |
| **Operating Margin** | `Operating Income / Revenue` |

<small><strong>EBITDA</strong> = Earnings Before Interest · Taxes · Depreciation · Amortization.  
<strong>Operating Income</strong> (EBIT) = profit after operating costs but before interest & tax.</small>
""",
    unsafe_allow_html=True,
)


st.markdown("### 🌿 ESG Pillars at a Glance")
st.markdown(
    """
| Pillar | Key Sub-score | Column | Captures |
|--------|---------------|--------|----------|
| **E** | Emissions | `ESG_Emissions_Score` | CO₂e footprint, reduction targets |
|  | Environmental Overall | `ESG_Environmental_Score` | Resource use, waste, biodiversity |
| **S** | Human Rights | `ESG_Human_Rights_Score` | Supplier labor standards |
|  | Workforce | `ESG_Workforce_Score` | Diversity, safety, training |
| **G** | Governance | `ESG_Governance_Score` | Board quality, exec pay, audit risk |
| – | Controversies | `ESG_Controversies_Score` | Litigation, scandals, fines |
""",
    unsafe_allow_html=True,
)


st.markdown("### 🚀 Get Started")
st.markdown(
    """
1. Use sidebar filters (year, division) on **EDA** pages  
2. Check **Model Training** for feature importance & tuning  
3. Try **Predict by Ticker** or **What-If Simulator** to stress ESG risk
"""
)

st.markdown("---")

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    return load_esg_zip()


df = load_data()

st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

st.caption("Use the navigation bar at the top to explore · download · model.")
