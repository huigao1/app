import streamlit as st
import pandas as pd
from utils import load_esg_zip

st.title("📝 Model & Ratio Definitions")

st.markdown("""
### 1. Target Variable
| Symbol | Definition |
|--------|------------|
| **EBITDA_Margin** | EBITDA / Revenues_Total |

### 2. Feature Ratios
| Ratio | Formula | Intuition |
|-------|---------|-----------|
| **CapEx_Intensity** | Capital_Expenditures / Revenues_Total | How asset‑heavy the firm is |
| **Debt_Ratio** | Liabilities_Total / Assets_Total | Balance‑sheet leverage |
| **Log_Assets** | log(Assets_Total) | Firm size (scaled) |
| **Asset_Turnover** | Revenues_Total / Assets_Total | Efficiency of asset usage |
| **Market_Cap** | Price × Common_Equity_Total | Equity market valuation |
| **Earnings_Yield** | EPS_Basic / Price | Earnings relative to price |

---
### 3. Model Pipeline
```text
Input features (13) ─▶ StandardScaler ─▶
   └─ LinearRegression
   └─ RandomForestRegressor (n=300)
   └─ XGBRegressor (n=300)
```
Models are benchmarked by **Adjusted R²** and **MAE** on a 20% hold‑out test set.

---
### 4. Sample Calculation
""")

# Load one sample row for demo
df = load_esg_zip().dropna(subset=['Capital_Expenditures','Revenues_Total','Liabilities_Total','Assets_Total']).head(1).copy()
row = df.iloc[0]
calc = {
    'CapEx_Intensity': row['Capital_Expenditures']/row['Revenues_Total'],
    'Debt_Ratio': row['Liabilities_Total']/row['Assets_Total'],
    'Log_Assets': row['Assets_Total'].__float__(),
}
calc_df = pd.DataFrame(calc, index=[row['ticker']])
calc_df['Log_Assets'] = calc_df['Log_Assets'].apply(lambda x: pd.np.log(x))

st.dataframe(calc_df.style.format("{:.3f}"))

st.info("All ratios are recomputed in real time during model training (see **Model Training** page).")
