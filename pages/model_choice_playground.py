import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from utils import load_esg_zip

st.title("⚙️ Model Playground – Linear vs HistGradientBoosting")

st.markdown(
    """
This page lets you **experiment with two machine learning models** — Linear Regression and HistGradientBoosting — to understand how different features influence financial outcomes like **EBITDA Margin** or **Operating Margin**.

You can:
- **Select any numerical target** and choose relevant **input features (X)**.
- **Compare model performance** using R² (fit quality) and MAE (error size).
- For boosting models, **adjust hyperparameters** (depth, learning rate, estimators) to observe overfitting or underfitting.
- Explore **feature importance or model coefficients** to learn which inputs drive predictions.

This tool helps reveal how ESG and financial metrics interact, and gives hands-on insight into model behavior — ideal for both learning and analysis.
"""
)

st.markdown("""
Choose between a **simple Linear Regression** or a **HistGradientBoostingRegressor** to see how different algorithms fit the data.

* **R²** – proportion of variance explained (closer to 1 ➜ better).
* **MAE** – average absolute error (closer to 0 ➜ better).
* For hist‑grad boosting you can tweak **n_estimators** (iterations), **learning_rate**, and **max_depth** to combat under/over‑fitting.
""")

@st.cache_data
def load_data():
    return load_esg_zip()

df = load_data()
num_cols = df.select_dtypes("number").columns.tolist()

# ────────────────────────────────────────────────────────────────
# Sidebar selectors
# ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Configuration")
    y_col = st.selectbox(
        "Target (y)",
        num_cols,
        index=num_cols.index("EBITDA_Margin") if "EBITDA_Margin" in num_cols else 0,
    )
    model_type = st.radio("Model", ["Linear Regression", "HistGradientBoosting"])
    default_feats = ["ESG_Combined_Score"]
    x_cols = st.multiselect(
        "Features (X)",
        [c for c in num_cols if c != y_col],
        default=default_feats,
    )
    if model_type == "HistGradientBoosting":
        n_estimators = st.slider("n_estimators", 100, 1000, 300, step=50)
        learning_rate = st.slider("learning_rate", 0.01, 1.0, 0.1, step=0.01)
        max_depth = st.slider("max_depth", 2, 10, 5)

# ────────────────────────────────────────────────────────────────
# Prepare data
# ────────────────────────────────────────────────────────────────
if not x_cols:
    st.info("Select at least one feature.")
    st.stop()

X = df[x_cols].dropna()
y = df.loc[X.index, y_col].dropna()
common = X.index.intersection(y.index)
X, y = X.loc[common], y.loc[common]

if len(common) < 30:
    st.warning("Not enough data points after dropping NA.")
    st.stop()

# ────────────────────────────────────────────────────────────────
# Build & fit model
# ────────────────────────────────────────────────────────────────
if model_type == "Linear Regression":
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("lr", LinearRegression())
    ])
else:
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("gb", HistGradientBoostingRegressor(
            max_iter=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=42
        ))
    ])

model.fit(X, y)
pred = model.predict(X)

# ────────────────────────────────────────────────────────────────
# Metrics
# ────────────────────────────────────────────────────────────────
r2 = r2_score(y, pred)
mae = mean_absolute_error(y, pred)
st.metric("R²", f"{r2:.3f}")
st.metric("MAE", f"{mae:.3f}")

# ────────────────────────────────────────────────────────────────
# Coefficients / Impurity-based feature importances
# ────────────────────────────────────────────────────────────────
st.subheader("Model Weights / Importances")
if model_type == "Linear Regression":
    coefs = model.named_steps["lr"].coef_
    fi_df = pd.DataFrame({"Feature": x_cols, "Weight": coefs})
else:
    fi = model.named_steps["gb"].feature_importances_
    fi_df = pd.DataFrame({"Feature": x_cols, "Importance": fi})

st.dataframe(fi_df.sort_values(fi_df.columns[-1], ascending=False)
             .set_index("Feature").style.format("{:.4f}"))

# ────────────────────────────────────────────────────────────────
# Permutation importances (robust)
# ────────────────────────────────────────────────────────────────
st.subheader("Permutation Importances")
perm = permutation_importance(
    model, X, y, n_repeats=10, random_state=42, n_jobs=-1
)
perm_df = (
    pd.DataFrame({
        "Feature": x_cols,
        "Importance": perm.importances_mean,
        "Std Dev": perm.importances_std
    })
    .sort_values("Importance", ascending=False)
    .set_index("Feature")
)
st.dataframe(perm_df.style.format("{:.4f}"))

# ────────────────────────────────────────────────────────────────
# Show source code
# ────────────────────────────────────────────────────────────────
with st.expander("👀 View full Streamlit code"):
    st.code(Path(__file__).read_text(), language="python")
