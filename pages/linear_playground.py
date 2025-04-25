import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from utils import load_esg_zip

df = load_esg_zip()
num_cols = df.select_dtypes("number").columns.tolist()

st.title("📈 Regression Playground")

y_col = st.selectbox("Target (y)", num_cols, index=num_cols.index('EBITDA_Margin') if 'EBITDA_Margin' in num_cols else 0)
x_cols = st.multiselect("Features (X)", [c for c in num_cols if c != y_col], default=['ESG_Combined_Score'])

if x_cols:
    X, y = df[x_cols].dropna(), df[y_col].dropna()
    common = X.index.intersection(y.index)
    X, y = X.loc[common], y.loc[common]
    if len(common) < 30:
        st.warning("Not enough rows for regression."); st.stop()
    model = LinearRegression().fit(X, y)
    pred = model.predict(X)
    r2 = r2_score(y, pred)
    st.write(f"**R² = {r2:.3f}**")

    st.write("### Coefficients")
    st.dataframe(pd.DataFrame({"Feature": x_cols, "β": model.coef_}).set_index("Feature"))
else:
    st.info("Select at least one feature.")
