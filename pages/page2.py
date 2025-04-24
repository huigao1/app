import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data(show_spinner=False)
def load_data(path="esg_cleaned_final.csv.zip"):
    return pd.read_csv(path, compression="zip")

df = load_data()

st.title("🏭 Average ESG by Industry Division")

industry_esg = df.groupby('Division')['ESG_Combined_Score'].mean().sort_values()
fig, ax = plt.subplots(figsize=(8, 6))
industry_esg.plot(kind='barh', ax=ax)
ax.set_xlabel('Average ESG Combined Score')
st.pyplot(fig)
