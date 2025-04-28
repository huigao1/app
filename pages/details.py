import streamlit as st
import pandas as pd
import numpy as np
from utils import load_esg_zip

st.title("📝 Model Pipeline & Ratio Definitions")

# ------------------------------------------------------------------
# 1. Ratio dictionary
# ------------------------------------------------------------------
ratio_info = pd.DataFrame([
    ["CapEx_Intensity", "Capital_Expenditures / Revenues_Total", "Asset‑intensity"],
    ["Debt_Ratio", "Liabilities_Total / Assets_Total", "Balance‑sheet leverage"],
    ["Log_Assets", "ln(Assets_Total)", "Firm size"],
    ["Asset_Turnover", "Revenues_Total / Assets_Total", "Efficiency"],
    ["ROA", "Net_Income / Assets_Total", "Return on assets"],
    ["ROE", "Net_Income / Common_Equity_Total", "Return on equity"],
    ["Net_Profit_Margin", "Net_Income / Revenues_Total", "Income share of sales"],
    ["Total_Return", "(Price_t − Price_{t−1}) / Price_{t−1}", "Annual stock return"],
], columns=["Ratio", "Formula", "Intuition"]).set_index("Ratio")

st.subheader("Key Features & Targets")
st.dataframe(ratio_info)

# ------------------------------------------------------------------
# 2. Model overview diagram
# ------------------------------------------------------------------
with st.subheader("📊 Model Pipeline"):
    st.markdown("""
    ```
    ESG & Financial Features ─▶ StandardScaler ─▶
       ├─ LinearRegression
       ├─ HistGradientBoostingRegressor
    ```
    *Target predicted on main **Model Training** page: **EBITDA_Margin**, **Operating_Margin**
    """)

