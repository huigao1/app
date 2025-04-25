import streamlit as st, matplotlib.pyplot as plt, seaborn as sns
from utils import load_esg_zip

df = load_esg_zip()
divs = sorted(df['Division'].dropna().unique())
sel = st.sidebar.multiselect("Filter Division", divs, default=divs)
filtered = df[df['Division'].isin(sel)]

st.title("🔍 Exploratory Analysis")

with st.expander("Numeric summary"):
    st.dataframe(filtered.select_dtypes("number").describe().T)

# 多指标分布
metrics = ['ESG_Combined_Score', 'ROA', 'ROE', 'Total_Return']
tabs = st.tabs(metrics)
for t, m in zip(tabs, metrics):
    with t:
        fig, ax = plt.subplots()
        sns.histplot(filtered[m].dropna(), kde=True, ax=ax)
        ax.set_title(f'Distribution of {m}')
        st.pyplot(fig)

# 相关热图
heat_cols = ['ESG_Combined_Score','ESG_Environmental_Score','ESG_Social_Score',
             'ESG_Governance_Score','ROA','ROE','Total_Return','Debt_Ratio']
fig2, ax2 = plt.subplots(figsize=(10,6))
sns.heatmap(filtered[heat_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax2)
st.subheader("Correlation Matrix")
st.pyplot(fig2)

# 散点 ESG vs Market Cap
if {'Market_Cap','ESG_Combined_Score'}.issubset(filtered.columns):
    fig3, ax3 = plt.subplots()
    sns.scatterplot(data=filtered, x='ESG_Combined_Score', y='Market_Cap',
                    hue='Division', alpha=.7, ax=ax3)
    ax3.set_yscale('log'); ax3.set_title("ESG vs Market-Cap (log scale)")
    st.pyplot(fig3)
