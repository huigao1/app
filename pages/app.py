import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import joblib, matplotlib.pyplot as plt
from pathlib import Path

st.title("🧪 ESG Risk What‑If Simulator – EBITDA & Operating Margins")

# ------------------------------------------------------------------
# Helper: load model from repo root or same dir
# ------------------------------------------------------------------

def load_model(fname: str):
    for p in [Path(__file__).resolve().parent.parent / fname,
              Path(__file__).resolve().with_name(fname)]:
        if p.exists():
            return joblib.load(p)
    st.error(f"❌ Model file '{fname}' not found. Upload it to repo root or pages/.")
    st.stop()

# Load both models
ebitda_model   = load_model('ebitda_margin_model.pkl')
operating_model= load_model('operating_margin_model.pkl')

# ------------------------------------------------------------------
# User Input (ticker)
# ------------------------------------------------------------------

ticker = st.text_input("Enter a stock ticker (example: AAPL, TSLA):").strip().upper()
if not ticker:
    st.stop()

# ------------------------------------------------------------------
# Fetch ESG + Financial data via yfinance
# ------------------------------------------------------------------

try:
    stock = yf.Ticker(ticker)
    sustainability = stock.sustainability
    if sustainability is None or sustainability.empty:
        st.error("No ESG data for this ticker."); st.stop()

    # Raw ESG risk scores (0‑100, lower better)
    env_risk = sustainability.loc['environmentScore'].iloc[0]
    soc_risk = sustainability.loc['socialScore'].iloc[0]
    gov_risk = sustainability.loc['governanceScore'].iloc[0]

    # Financial statements
    bs   = stock.balance_sheet
    fin  = stock.financials
    cf   = stock.cashflow

    total_assets  = bs.loc['Total Assets'].iloc[0]
    total_liab    = bs.loc['Total Liabilities Net Minority Interest'].iloc[0]
    revenue       = fin.loc['Total Revenue'].iloc[0]
    net_income    = fin.loc['Net Income'].iloc[0]
    cash_ops      = cf.loc['Operating Cash Flow'].iloc[0]
    capex         = cf.loc['Capital Expenditure'].iloc[0]

except Exception as e:
    st.error(f"Data fetch error: {e}"); st.stop()

# Derived ratios
asset_turnover   = revenue / total_assets
log_assets       = np.log10(total_assets)
debt_ratio       = total_liab / total_assets
roa              = net_income / total_assets
net_margin       = net_income / revenue
cashflow_margin  = cash_ops / revenue
capex_intensity  = abs(capex) / revenue

st.success("✅ ESG & financial data fetched for " + ticker)

# ------------------------------------------------------------------
# Risk range slider
# ------------------------------------------------------------------
range_pct = st.slider("Increase ESG risk by (%)", 0, 100, (0, 100), step=10)
incs = list(range(range_pct[0], range_pct[1]+1, 10))  # e.g., [0,10,20,...]

results = []
for pct in incs:
    factor = 1 + pct/100
    new_env = min(env_risk*factor, 100)
    new_soc = min(soc_risk*factor, 100)
    new_gov = min(gov_risk*factor, 100)

    # Normalized ESG scores (0‑1, higher better)
    NE, NS, NG = [1 - x/100 for x in (new_env,new_soc,new_gov)]

    # Build input rows for each model
    ebt_row = pd.DataFrame([{ 'Asset_Turnover': asset_turnover, 'Debt_Ratio': debt_ratio, 'Log_Assets': log_assets,
                              'ROA': roa, 'Net_Profit_Margin': net_margin, 'CashFlow_Margin': cashflow_margin,
                              'ESG_Environmental_Score': NE, 'ESG_Social_Score': NS, 'ESG_Governance_Score': NG }])

    op_row  = pd.DataFrame([{ 'Asset_Turnover': asset_turnover, 'Debt_Ratio': debt_ratio, 'Log_Assets': log_assets,
                              'CapEx_Intensity': capex_intensity,
                              'ESG_Environmental_Score': NE, 'ESG_Social_Score': NS, 'ESG_Governance_Score': NG }])

    ebt_pred = float(ebitda_model.predict(ebt_row)[0])
    op_pred  = float(operating_model.predict(op_row)[0])

    results.append({ 'Risk +%': pct, 'EBITDA Margin': round(ebt_pred,4), 'Operating Margin': round(op_pred,4) })

results_df = pd.DataFrame(results)

# ------------------------------------------------------------------
# Display tabs
# ------------------------------------------------------------------

tab1, tab2 = st.tabs(["Results Table", "Margin Curves"])

with tab1:
    st.dataframe(results_df)

with tab2:
    fig, ax = plt.subplots()
    ax.plot(results_df['Risk +%'], results_df['EBITDA Margin'], marker='o', label='EBITDA')
    ax.plot(results_df['Risk +%'], results_df['Operating Margin'], marker='s', label='Operating')
    ax.set_xlabel('Increase in ESG Risk (%)'); ax.set_ylabel('Predicted Margin'); ax.grid(True)
    ax.set_title(f'ESG Risk vs Margins – {ticker}')
    ax.legend()
    st.pyplot(fig)

st.success("🧹 Scenario simulation complete!")

with st.markdown("👀 Full Streamlit Code for this App"):
    st.code(Path(__file__).read_text(), language="python")
