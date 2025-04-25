import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error

from utils import load_esg_zip

@st.cache_data(show_spinner=False)
def load_data():
    return load_esg_zip()          # 默认读取根目录 zip

df = load_data()

st.title("🤖 Modeling EBITDA Margin")

features = [
    'ESG_Environmental_Score', 'ESG_Social_Score', 'ESG_Governance_Score',
    'ESG_Emissions_Score', 'ESG_Human_Rights_Score', 'ESG_Workforce_Score',
    'ESG_Controversies_Score', 'CapEx_Intensity', 'Debt_Ratio', 'Log_Assets',
    'Revenues_Total', 'Operating_Income_Before_Depreciation', 'Asset_Turnover'
]
target = 'EBITDA_Margin'

model_df = df[features + [target]].dropna()
X, y = model_df[features], model_df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Linear Regression": Pipeline([
        ('scaler', StandardScaler()),
        ('lr', LinearRegression())
    ]),
    "Random Forest": Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestRegressor(n_estimators=300, random_state=42))
    ]),
    "XGBoost": Pipeline([
        ('scaler', StandardScaler()),
        ('xgb', XGBRegressor(n_estimators=300, random_state=42, verbosity=0))
    ])
}

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    n, p = X_test.shape
    adj_r2 = 1 - (1 - r2) * ((n - 1)/(n - p - 1))
    results.append({"Model": name, "R2": r2, "Adj R2": adj_r2, "MAE": mae})

st.subheader("Model Performance (Test Set)")
st.dataframe(
    pd.DataFrame(results)
      .sort_values('Adj R2', ascending=False)
      .reset_index(drop=True)
      .style.format({"R2": "{:.3f}", "Adj R2": "{:.3f}", "MAE": "{:.3f}"})
)
