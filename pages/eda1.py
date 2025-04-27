import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils import load_esg_zip

# ------------------------------------------------------------------
# Load data and optional filters
# ------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    return load_esg_zip()

df = load_data()

st.title("🔍 Exploratory Data Analysis")

# Sidebar industry filter
divisions = sorted(df['Division'].dropna().unique())
sel_divs = st.sidebar.multiselect("Filter by Division", divisions, default=divisions)
filtered = df[df['Division'].isin(sel_divs)]

# ------------------------------------------------------------------
# KPI cards
# ------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Rows", f"{len(filtered):,}")
col2.metric("Years", f"{filtered['year'].min()}–{filtered['year'].max()}")
col3.metric("Divisions", filtered['Division'].nunique())

# ------------------------------------------------------------------
# Summary statistics
# ------------------------------------------------------------------
with st.expander("📊 Numeric Summary"):
    st.dataframe(filtered.select_dtypes("number").describe().T)

# ------------------------------------------------------------------
# Distribution tabs
# ------------------------------------------------------------------
metrics = ['ESG_Combined_Score','ROA','ROE','Total_Return']
for m in metrics:
    if m not in filtered.columns:
        metrics.remove(m)

tabs = st.tabs(metrics)
for t, m in zip(tabs, metrics):
    with t:
        fig, ax = plt.subplots()
        sns.histplot(filtered[m].dropna(), kde=True, ax=ax)
        ax.set_title(f'Distribution of {m}')
        st.pyplot(fig)

# ------------------------------------------------------------------
# Correlation heatmap
# ------------------------------------------------------------------
heat_cols = ['ESG_Combined_Score','ESG_Environmental_Score','ESG_Social_Score',
             'ESG_Governance_Score','ROA','ROE','Total_Return','Debt_Ratio']
valid = [c for c in heat_cols if c in filtered.columns]
if len(valid) >= 2:
    st.subheader("Correlation Matrix")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(filtered[valid].corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    st.pyplot(fig)

# ------------------------------------------------------------------
# ESG vs Market Cap scatter
# ------------------------------------------------------------------
if {'ESG_Combined_Score','Market_Cap'}.issubset(filtered.columns):
    st.subheader("ESG vs Market Cap (log scale)")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered, x='ESG_Combined_Score', y='Market_Cap', hue='Division', alpha=.7, ax=ax)
    ax.set_yscale('log')
    st.pyplot(fig)

# ------------------------------------------------------------------
# Merge insights from accounting & stock (from code.py logic)
# ------------------------------------------------------------------
with st.expander("🔗 Data Merge Insights – ESG vs Accounting vs Stock"):
    try:
        acct = pd.read_csv("acct.csv")
        stock = pd.read_csv("stock.csv")

        # standardize
        for d in (acct,):
            d.columns = d.columns.str.strip().str.lower()
        if 'fyear' in acct.columns:
            acct = acct.rename(columns={'fyear':'year'})
        if 'tic' in acct.columns:
            acct = acct.rename(columns={'tic':'ticker'})
        stock.columns = stock.columns.str.strip().str.lower()
        stock['date'] = pd.to_datetime(stock['date'])
        stock['year']  = stock['date'].dt.year

        esg_pairs   = set(zip(df['cusip'].astype(str).str[:8], df['year']))
        acct_pairs  = set(zip(acct['cusip'].astype(str).str[:8], acct['year']))
        stock_pairs = set(zip(stock['cusip'].astype(str).str[:8], stock['year']))

        st.write(f"**ESG pairs**: {len(esg_pairs):,}")
        st.write(f"**Accounting pairs**: {len(acct_pairs):,}")
        st.write(f"**Stock pairs**: {len(stock_pairs):,}")
        st.write(f"**Intersection (all three)**: {len(esg_pairs & acct_pairs & stock_pairs):,}")
    except FileNotFoundError:
        st.info("Upload **acct.csv** and **stock.csv** to project root to see merge insights.")
