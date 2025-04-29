import streamlit as st
import pandas as pd
import numpy as np
from utils import load_esg_zip

st.title("📝 Model Pipeline & Ratio Definitions")

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


with st.subtitle("📊 Model Pipeline"):
    st.markdown("""
    ```
    ESG & Financial Features ─▶ StandardScaler ─▶
       ├─ LinearRegression
       ├─ HistGradientBoostingRegressor
    ```
    *Target predicted on main **Model Training** page: **EBITDA_Margin**, **Operating_Margin**
    """)


CODE = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.inspection import permutation_importance

# 1. Load your cleaned dataset (update filename as needed)
df = pd.read_csv('esg_cleaned_final.csv')

# 2. Define financial controls + extra margins
features = [
    'Asset_Turnover','Debt_Ratio','Log_Assets','ROA','Net_Profit_Margin',
    'CashFlow_Margin','ESG_Environmental_Score','ESG_Social_Score','ESG_Governance_Score'
]

target = 'EBITDA_Margin'

# 3. Prepare data
data = df.dropna(subset=features+[target]).reset_index(drop=True)
X, y = data[features], data[target]

# 4. Train/test split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

# 5. Build pipeline
gb_pipe = Pipeline([
    ('imputer',SimpleImputer(strategy='median')),
    ('gb',HistGradientBoostingRegressor(max_iter=200,max_depth=5,learning_rate=0.05,random_state=42))
])

# 6. Fit model
gb_pipe.fit(X_train,y_train)

# 7‑8. Evaluate
for label,X_,y_ in [('Train',X_train,y_train),('Test',X_test,y_test)]:
    pred = gb_pipe.predict(X_)
    r2  = r2_score(y_,pred)
    rmse= np.sqrt(mean_squared_error(y_,pred))
    mae = mean_absolute_error(y_,pred)
    print(f"{label}: R²={r2:.3f}  RMSE={rmse:.3f}  MAE={mae:.3f}")

# 9. Permutation importances
perm = permutation_importance(gb_pipe,X_test,y_test,n_repeats=10,random_state=42,n_jobs=-1)
fi = pd.DataFrame({'Feature':features,'Importance':perm.importances_mean}).sort_values('Importance',ascending=False)
print(fi)

# 10. Plot importances
plt.figure(figsize=(8,5))
plt.barh(fi['Feature'],fi['Importance'])
plt.gca().invert_yaxis(); plt.tight_layout(); plt.show()

# 11. Save model
import joblib
joblib.dump(gb_pipe,'ebitda_margin_predictor.pkl')"""

st.title("📑 Original Code – EBITDA Gradient Boosting Training")

st.code(CODE, language="python")

CODE2 = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.inspection import permutation_importance

# 1. Load your cleaned dataset
df = pd.read_csv('esg_cleaned_final.csv')

# 2. Define financial controls + extra margins
features = [
    "Asset_Turnover",
    "Debt_Ratio",
    "Log_Assets",
    "CapEx_Intensity",
    "ESG_Environmental_Score",
    "ESG_Social_Score",
    "ESG_Governance_Score"
]
target = "Operating_Margin"

# 3. Prepare data: drop any rows missing features or target
data = df.dropna(subset=features + [target]).reset_index(drop=True)
X = data[features]
y = data[target]

# 4. Train/Test split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# 5. Build Gradient Boosting pipeline
gb_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("gb",      HistGradientBoostingRegressor(
        max_iter=200,
        max_depth=5,
        learning_rate=0.05,
        random_state=42
    ))
])

# 6. Fit the model on training set
gb_pipe.fit(X_train, y_train)

# 7. Predict on train & test
y_train_pred = gb_pipe.predict(X_train)
y_test_pred  = gb_pipe.predict(X_test)

# 8. Compute performance metrics
train_r2   = r2_score(y_train, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_mae  = mean_absolute_error(y_train, y_train_pred)

test_r2    = r2_score(y_test, y_test_pred)
test_rmse  = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_mae   = mean_absolute_error(y_test, y_test_pred)

# 9. Print detailed performance
print(f"\n=== Gradient Boosting Performance for {target} ===")
print("Dataset      |    R²    |   RMSE   |   MAE")
print("-" * 47)
print(f"Train        | {train_r2:8.4f} | {train_rmse:8.4f} | {train_mae:8.4f}")
print(f"Test         | {test_r2:8.4f} | {test_rmse:8.4f} | {test_mae:8.4f}")

# 10. Permutation-based feature importance (on test set)
perm = permutation_importance(
    gb_pipe, X_test, y_test,
    n_repeats=20, random_state=42, n_jobs=-1
)
importances = perm.importances_mean
stds        = perm.importances_std

# 11. Create a DataFrame of importances and print it
fi_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances,
    "Std": stds
}).sort_values(by="Importance", ascending=False).reset_index(drop=True)

print("\nFeature importances (permutation-based):")
print(fi_df.to_string(index=False))

# 12. Plot feature importances
plt.figure(figsize=(8, 5))
plt.barh(fi_df["Feature"], fi_df["Importance"], xerr=fi_df["Std"])
plt.title(f"Permutation Importances for {target} (GB)")
plt.xlabel("Mean decrease in R² when permuted")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
import joblib

# assuming gb_pipe is already trained
joblib.dump(gb_pipe, "operating_margin_predictor.pkl")"""

st.title("📑 Original Code – Operating Gradient Boosting Training")

st.code(CODE2, language="python")
