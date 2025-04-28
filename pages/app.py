import streamlit as st
import pandas as pd
import numpy as np
import joblib, yfinance as yf
from pathlib import Path
import matplotlib.pyplot as plt

st.title("🧪 ESG Risk What‑If Simulator – EBITDA vs Operating Margin")

# -------------------------------------------------------------
# Helper: load model (search repo root then same dir)
# -------------------------------------------------------------

import joblib
from pathlib import Path

# Try repo root first, then same dir as this file
candidates = [
    Path(__file__).resolve().parent.parent / 'ebitda_margin_model.pkl',
    Path(__file__).resolve().with_name('ebitda_margin_model.pkl')
]

for p in candidates:
    if p.exists():
        ebitda_model = joblib.load(p)
        break
else:
    raise FileNotFoundError("❌ Model file `ebitda_margin_model.pkl` not found. "
                            "Place it in repo root or pages/ and push again.")

def load_or_train_operating(df):
    try:
        return load_model('operating_margin_predictor.pkl')
    except FileNotFoundError:
        # 👉 训练代码，得到 model
        joblib.dump(model, 'operating_margin_predictor.pkl')
        return model

ebitda_model   = load_model('ebitda_margin_model.pkl')
operating_model = load_model('operating_margin_predictor.pkl')

# -------------------------------------------------------------
# User input
# -------------------------------------------------------------

ticker = st.text_input("Enter a stock ticker (example: AAPL, TSLA):").strip().upper()

if not ticker:
    st.stop()

# -------------------------------------------------------------
# Fetch data via yfinance
# -------------------------------------------------------------

try:
    stock = yf.Ticker(ticker)

    sustainability = stock.sustainability
    if sustainability is None or sustainability.empty:
        st.error("No ESG data available for this ticker."); st.stop()

    environment_risk = sustainability.loc["environmentScore"].iloc[0]
    social_risk      = sustainability.loc["socialScore"].iloc[0]
    governance_risk  = sustainability.loc["governanceScore"].iloc[0]

    # Normalize to 0‑1 scores
    env_score = 1 - environment_risk/100
    soc_score = 1 - social_risk/100
    gov_score = 1 - governance_risk/100

    balance_sheet = stock.balance_sheet
    financials    = stock.financials
    cashflow      = stock.cashflow

    total_assets  = balance_sheet.loc["Total Assets"].iloc[0]
    total_liab    = balance_sheet.loc["Total Liabilities Net Minority Interest"].iloc[0]
    revenue       = financials.loc["Total Revenue"].iloc[0]
    net_income    = financials.loc["Net Income"].iloc[0]
    cash_ops      = cashflow.loc["Operating Cash Flow"].iloc[0]
    capex         = cashflow.loc["Capital Expenditure"].iloc[0]

    # Ratios shared by both models
    debt_ratio    = total_liab / total_assets
    asset_turnover= revenue / total_assets
    log_assets    = np.log10(total_assets)
    roa           = net_income / total_assets
    net_margin    = net_income / revenue
    cashflow_margin = cash_ops / revenue
    capex_intensity = abs(capex) / revenue

except Exception as e:
    st.error(f"Data fetch error: {e}")
    st.stop()

st.success("✅ Data fetched & ratios calculated")

# -------------------------------------------------------------
# What‑If simulation
# -------------------------------------------------------------

risk_increases = st.slider("Increase ESG Risk by (%)", 0, 100, (0, 100), step=20)
incs = [x/100 for x in range(risk_increases[0], risk_increases[1]+1, 20)]

results = []
for inc in incs:
    new_env_risk = min(environment_risk * (1+inc), 100)
    new_soc_risk = min(social_risk      * (1+inc), 100)
    new_gov_risk = min(governance_risk  * (1+inc), 100)

    ne, ns, ng = [1 - x/100 for x in (new_env_risk, new_soc_risk, new_gov_risk)]

    ebt_input = pd.DataFrame([{  # input columns for EBITDA model
        "Asset_Turnover": asset_turnover, "Debt_Ratio": debt_ratio,
        "Log_Assets": log_assets, "ROA": roa,
        "Net_Profit_Margin": net_margin, "CashFlow_Margin": cashflow_margin,
        "ESG_Environmental_Score": ne, "ESG_Social_Score": ns, "ESG_Governance_Score": ng
    }])

    op_input = pd.DataFrame([{  # input for Operating margin model
        "Asset_Turnover": asset_turnover, "Debt_Ratio": debt_ratio,
        "Log_Assets": log_assets, "CapEx_Intensity": capex_intensity,
        "ESG_Environmental_Score": ne, "ESG_Social_Score": ns, "ESG_Governance_Score": ng
    }])

    ebt_pred = float(ebitda_model.predict(ebt_input)[0])
    op_pred  = float(operating_model.predict(op_input)[0])

    results.append({
        "Risk +%": int(inc*100),
        "EBITDA Margin": round(ebt_pred,4),
        "Operating Margin": round(op_pred,4)
    })

results_df = pd.DataFrame(results)

# -------------------------------------------------------------
# Tabs: table & plots
# -------------------------------------------------------------

tab_table, tab_plot = st.tabs(["Results Table","Plots"])

with tab_table:
    st.dataframe(results_df)

with tab_plot:
    fig, ax = plt.subplots()
    ax.plot(results_df['Risk +%'], results_df['EBITDA Margin'], marker='o', label='EBITDA')
    ax.plot(results_df['Risk +%'], results_df['Operating Margin'], marker='s', label='Operating')
    ax.set_xlabel('Increase in ESG Risk (%)'); ax.set_ylabel('Predicted Margin')
    ax.set_title(f'Impact of ESG Risk Increase on Margins – {ticker}')
    ax.legend(); ax.grid(True)
    st.pyplot(fig)

st.success("🧹 Scenario simulation complete!")
