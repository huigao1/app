import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from utils import load_esg_zip

st.title("🎯 Predict EBITDA Margin by Ticker")

# ------------------------------------------------------------------
# 1. Load data & feature setup
# ------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_df():
    return load_esg_zip()

df = load_df()
features = [
    'ESG_Environmental_Score','ESG_Social_Score','ESG_Governance_Score',
    'ESG_Emissions_Score','ESG_Human_Rights_Score','ESG_Workforce_Score',
    'ESG_Controversies_Score','CapEx_Intensity','Debt_Ratio','Log_Assets',
    'Revenues_Total','Operating_Income_Before_Depreciation','Asset_Turnover'
]

target = 'EBITDA_Margin'

# ------------------------------------------------------------------
# 2. Train three models & choose best Adjusted R²
# ------------------------------------------------------------------
@st.cache_data(show_spinner=True)
def train_models():
    model_df = df[features + [target]].dropna()
    X, y = model_df[features], model_df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

    models = {
        'Linear': Pipeline([('sc',StandardScaler()),('m',LinearRegression())]),
        'RF':     Pipeline([('sc',StandardScaler()),('m',RandomForestRegressor(n_estimators=300,random_state=0))]),
        'XGB':    Pipeline([('sc',StandardScaler()),('m',XGBRegressor(n_estimators=300,random_state=0,verbosity=0))])
    }
    best_name,best_mod,best_adj=-1,None,-np.inf
    n,p = X_test.shape
    for name,mod in models.items():
        mod.fit(X_train,y_train)
        r2=r2_score(y_test,mod.predict(X_test))
        adj=1-(1-r2)*((n-1)/(n-p-1))
        if adj>best_adj:
            best_adj,best_name,best_mod=adj,name,mod
    return best_name,best_adj,best_mod

best_name,best_adj,best_model = train_models()

st.success(f"Best model: {best_name} (Adj R²={best_adj:.3f}) – model cached.")

# ------------------------------------------------------------------
# 3. User selects ticker/year to predict
# ------------------------------------------------------------------
all_tickers = sorted(df['ticker'].dropna().unique())
sel_ticker = st.selectbox('Select ticker', all_tickers)
rows = df[df['ticker']==sel_ticker]
sel_year = st.selectbox('Year', sorted(rows['year'].unique(), reverse=True))
row = rows[rows['year']==sel_year].iloc[0]

# ------------------------------------------------------------------
# 4. Predict & show output
# ------------------------------------------------------------------
X_single = row[features].values.reshape(1,-1)
pred = best_model.predict(X_single)[0]
actual = row[target] if not pd.isnull(row[target]) else None

st.subheader("Prediction")
st.metric("Predicted EBITDA Margin", f"{pred:.2%}")
if actual is not None:
    st.metric("Actual (reported)", f"{actual:.2%}")
else:
    st.info("Actual value missing in dataset.")
