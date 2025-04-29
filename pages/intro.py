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
By translating abstract ESG indicators into quantifiable margin projections, the model supports early-stage financial forecastingE, ESG scenario planning, as well as valuation analysis for investment and strategy teams

| Metric | What it measures | Why it matters |
|--------|------------------|----------------|
| **EBITDA Margin** | Core operational profitability before interest, taxes, depreciation, and amortization | Removes capital-structure noise → comparable across firms.|
| **Operating Margin** | Profitability after depreciation and amortization are deducted | Includes depreciation → full cost discipline.<br>Core KPI in DCF & management guidance. |

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

st.markdown("### 🧭 App Navigation Guide")
st.markdown(
    """
- **🏠 Welcome**  
  Overview of the project goal, model logic, and ESG-finance context.

- **🔍 About Our Data**  
  Summary of dataset source and basic visualization. 

- **📊 Industry ESG Distribution**  
  Explore ESG score distributions across industries.

- **⏳ Time-Series Trends**  
  Visualize ESG trends over time by industry.
  
- **📌 Features We Used**  
  Breakdown of financial + ESG features used in our models.

- **📈 Regression Model Comparison**  
  Compare Linear vs Gradient Boosting models performance interactively.

- **🎯 Predict by Ticker**  
  Input a stock ticker to simulate what-if analysis using real-time data.
    """
)


