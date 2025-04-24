import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data(show_spinner=False)
def load_data(path="esg_cleaned_final.csv"):
    return pd.read_csv(path)

df = load_data()

st.title("🔍 Exploratory Data Analysis")

st.subheader("Summary Statistics (Key Metrics)")
cols = [
    'ESG_Combined_Score', 'ROA', 'ROE', 'Net_Profit_Margin', 'Total_Return'
]
st.dataframe(df[cols].describe())

st.subheader("Distribution of ESG Combined Score")
fig, ax = plt.subplots()
sns.histplot(df['ESG_Combined_Score'].dropna(), kde=True, ax=ax)
ax.set_title('Distribution of ESG Combined Score')
st.pyplot(fig)

st.subheader("Correlation Heatmap (ESG & Financial Metrics)")
heat_cols = [
    'ESG_Combined_Score', 'ESG_Environmental_Score', 'ESG_Social_Score',
    'ESG_Governance_Score', 'ROA', 'ROE', 'Total_Return', 'Debt_Ratio'
]
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.heatmap(df[heat_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax2)
st.pyplot(fig2)
