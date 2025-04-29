import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_esg_zip

sns.set_style("whitegrid")

@st.cache_data(show_spinner=False)
def load_data():
    return load_esg_zip()

df = load_data()


st.markdown("<h2 style='margin-bottom:0.2em'>🧾 What Data Powers This Model?</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Year span", f"{df['year'].min()}–{df['year'].max()}")
c3.metric("Unique tickers", df['ticker_ann'].nunique())

st.divider()

st.markdown(
    """
This dataset is sourced from Wharton Research Data Services (WRDS) and includes both active and delisted U.S.-listed firms.
It merges structured financial statement data with annual, company-level ESG (Environmental, Social, and Governance) scores.

The dataset enables longitudinal analysis of how financial performance and sustainability indicators evolve across industries and market cycles.
""",
    unsafe_allow_html=True,
)

st.markdown("### 📊 ESG Score Distributions")
plot_cols = ['ESG_Combined_Score','ESG_Environmental_Score','ESG_Social_Score','ESG_Governance_Score']
tabs = st.tabs([f"Dist • {c.split('_')[1]}" if c!='ESG_Combined_Score' else "Dist • Combined" for c in plot_cols])
for tab, col in zip(tabs, plot_cols):
    with tab:
        fig, ax = plt.subplots(figsize=(6,3))
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(col.replace('_',' '))
        st.pyplot(fig)

st.markdown("### 🔗 Correlation Matrix (ESG & Financial Metrics)")
heat_cols = plot_cols + ['ROA','ROE','Total_Return','Debt_Ratio']
fig2, ax2 = plt.subplots(figsize=(8,5))
mask = None
sns.heatmap(df[heat_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax2, mask=mask)
ax2.set_title('Pearson correlations')
st.pyplot(fig2)
