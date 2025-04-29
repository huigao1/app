import streamlit as st
import pandas as pd
from utils import load_esg_zip

st.markdown(
    "<h2 style='color:#d62728'>🔍 Corporate Margin Predictor</h2>"
    "<h4>Forecasting Profitability with Financial &amp; ESG Signals</h4>",
    unsafe_allow_html=True,
)

st.markdown("Team members: Hui Gao, Phunsok Norboo, Zehui Wang")

st.markdown("### 🧠 What Our Model Does — and Why It Matters")
st.markdown(
    """
This model estimates **EBITDA Margin** and **Operating Margin** using a combination of ESG scores and traditional financial metrics.  

It applies a **regression-based approach** to uncover patterns between a firm’s sustainability profile and its financial outcomes.  
By translating abstract ESG indicators into quantifiable margin projections, the model supports:
- Early-stage **financial forecasting**
- ESG **scenario planning**
- **Valuation analysis** for investment and strategy teams

| Metric | What it measures | Why it matters |
|--------|------------------|----------------|
| **EBITDA Margin** | Core operational profitability before interest, taxes, depreciation, and amortization | Removes capital-structure noise → comparable across firms.<br>Anchors EV/EBITDA multiples. |
| **Operating Margin** | Profitability after depreciation and amortization are deducted | Includes depreciation → full cost discipline.<br>Core KPI in DCF & management guidance. |

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

### 🔎 Why This Matters

- **Investor Insight** · Link asset efficiency, leverage & ESG to bottom-line margins  
- **Strategic Planning** · Run *what-if* ESG scenarios (e.g. +5pts Environmental → Δ EBITDA)  
- **Valuation Edge** · Converts abstract ESG ratings into forecastable financial outcomes.
""",
    unsafe_allow_html=True,
)

st.markdown("### 🌿 What is an ESG Score?")

st.markdown(
    """
- **ESG (Environmental, Social, and Governance)** scores assess how well a company manages non-financial risks.
- **Environmental**: Tracks climate impact, emissions, waste, and resource usage.
- **Social**: Measures labor practices, diversity, community impact, and human rights.
- **Governance**: Evaluates board structure, transparency, audit practices, and ethics.

ESG scores translate complex qualitative factors into measurable data, helping investors and analysts  
incorporate long-term sustainability and reputational risk into financial decision-making.
    """
)

st.markdown("### 🌿 ESG Pillars at a Glance")
st.markdown(
    """
| Pillar | ESG Score | Column | What it Measures |
|--------|-----------|--------|------------------|
| **E** | Environmental Score | `ESG_Environmental_Score` | Assesses a company's resource use, emissions, and environmental risk management. Reflects exposure to climate-related issues such as carbon footprint and energy efficiency. High scores indicate proactive sustainability practices and lower environmental liabilities. |
| **S** | Social Score | `ESG_Social_Score` | Evaluates labor practices, employee welfare, and community impact. Includes factors like diversity, training, safety, and supply chain ethics. Strong social performance can enhance reputation and reduce operational risks. |
| **G** | Governance Score | `ESG_Governance_Score` | Measures oversight quality, executive accountability, and internal controls. Covers board composition, shareholder rights, and audit transparency. Sound governance underpins long-term strategy and regulatory compliance. |
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
