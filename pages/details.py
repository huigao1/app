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
with st.expander("📊 Model Pipeline"):
    st.markdown("""
    ```
    ESG & Financial Features ─▶ StandardScaler ─▶
       ├─ LinearRegression
       ├─ RandomForestRegressor (n=300)
       └─ XGBRegressor (n=300)
    ```
    *Target predicted on main **Model Training** page: **EBITDA_Margin***
    """)

# ------------------------------------------------------------------
# 3. Sample calculation table
# ------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def sample_row():
    df = load_esg_zip()
    # pick first non‑null row with all fields
    req = ['Capital_Expenditures','Revenues_Total','Liabilities_Total','Assets_Total',
           'Net_Income','Common_Equity_Total','Price']
    row = df.dropna(subset=req).iloc[0]
    return row

row = sample_row()
calc = {
    'CapEx_Intensity': row['Capital_Expenditures']/row['Revenues_Total'],
    'Debt_Ratio': row['Liabilities_Total']/row['Assets_Total'],
    'Log_Assets': np.log(row['Assets_Total']),
    'ROA': row['Net_Income']/row['Assets_Total'],
    'ROE': row['Net_Income']/row['Common_Equity_Total'],
    'Net_Profit_Margin': row['Net_Income']/row['Revenues_Total'],
}
calc_df = pd.DataFrame(calc, index=[row['ticker']])

st.subheader("Example Ratio Calculation (single firm-year)")
st.dataframe(calc_df.style.format("{:.3f}"))

st.info("These ratios are recalculated on‑the‑fly during modeling and EDA pages.")
