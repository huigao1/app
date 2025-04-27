import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from utils import load_esg_zip

st.title("⚙️ Model Playground – Linear vs Random Forest")

df = load_esg_zip()
num_cols = df.select_dtypes("number").columns.tolist()

# ---------------- UI ----------------
colA, colB = st.columns(2)
with colA:
    y_col = st.selectbox("Target (y)", num_cols, index=num_cols.index('EBITDA_Margin') if 'EBITDA_Margin' in num_cols else 0)
with colB:
    model_type = st.radio("Model", ["Linear Regression", "Random Forest"], horizontal=True)

x_cols = st.multiselect("Features (X)", [c for c in num_cols if c != y_col], default=['ESG_Combined_Score'])

if not x_cols:
    st.info("Select at least one feature.")
    st.stop()

# ---------------- Data prep ----------------
X = df[x_cols].dropna()
y = df.loc[X.index, y_col].dropna()
common = X.index.intersection(y.index)
X, y = X.loc[common], y.loc[common]

if len(common) < 30:
    st.warning("Not enough rows after dropping NA.")
    st.stop()

# ---------------- Model training ----------------
if model_type == "Linear Regression":
    model = Pipeline([('sc', StandardScaler()), ('lr', LinearRegression())])
else:
    n_estimators = st.slider("n_estimators", 100, 500, 300, step=50)
    max_depth = st.slider("max_depth", 3, 20, 10)
    model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=0)

model.fit(X, y)
pred = model.predict(X)

r2 = r2_score(y, pred)
mae = mean_absolute_error(y, pred)

st.metric("R²", f"{r2:.3f}")
st.metric("MAE", f"{mae:.3f}")

# ---------------- Coefficients / Feature importance --------------
st.subheader("Feature Importance" if model_type=="Random Forest" else "Coefficients")
if model_type == "Linear Regression":
    coef_df = pd.DataFrame({"Feature": x_cols, "Weight": model.named_steps['lr'].coef_})
else:
    coef_df = pd.DataFrame({"Feature": x_cols, "Weight": model.feature_importances_})
coef_df = coef_df.sort_values("Weight", ascending=False).set_index("Feature")
st.dataframe(coef_df.style.format("{:.4f}"))
