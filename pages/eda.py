import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_esg_zip

@st.cache_data(show_spinner=False)
def load_data():
    return load_esg_zip()

df = load_data()

st.title("🔍 Exploratory Data Analysis")

st.subheader("The Colab Notebook can be found here:")

st.subheader("Summary Statistics (Key Metrics)")
cols = ['ESG_Combined_Score','ESG_Environmental_Score','ESG_Social_Score',
        'ESG_Governance_Score','ROA','ROE','Net_Profit_Margin','Total_Return']
st.dataframe(df[cols].describe())

plot_cols = ['ESG_Combined_Score','ESG_Environmental_Score','ESG_Social_Score','ESG_Governance_Score']
for col in plot_cols:
    st.subheader(f"Distribution of {col}")
    fig, ax = plt.subplots()
    sns.histplot(df[col].dropna(), kde=True, ax=ax)
    ax.set_title(f'Distribution of {col}')
    st.pyplot(fig)

st.subheader("Correlation Heatmap (ESG & Financial Metrics)")
heat_cols = ['ESG_Combined_Score','ESG_Environmental_Score','ESG_Social_Score',
             'ESG_Governance_Score','ROA','ROE','Total_Return','Debt_Ratio']
fig2, ax2 = plt.subplots(figsize=(10,6))
sns.heatmap(df[heat_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax2)
st.pyplot(fig2)

with st.subheader("📈 Yearly Correlation: ESG Combined vs Total Return"):
    corr = (df.dropna(subset=['ESG_Combined_Score','Total_Return'])
              .groupby('year')
              .apply(lambda g: g['ESG_Combined_Score'].corr(g['Total_Return'])))
    fig3, ax3 = plt.subplots(figsize=(8,4))
    ax3.plot(corr.index, corr.values, marker='o')
    ax3.axhline(0, color='gray', linewidth=.8)
    ax3.set_title('Yearly Correlation: ESG Combined vs Total Return')
    ax3.set_xlabel('Year'); ax3.set_ylabel('Pearson r'); ax3.grid(alpha=.3)
    st.pyplot(fig3)
    st.dataframe(corr.rename('Correlation').reset_index())
