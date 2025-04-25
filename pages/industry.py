import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import load_esg_zip

@st.cache_data(show_spinner=False)
def load_data():
    return load_esg_zip()          # 默认读取根目录 zip

df = load_data()

st.title("🏭 Average ESG by Industry Division")

industry_esg = df.groupby('Division')['ESG_Combined_Score'].mean().sort_values()
fig, ax = plt.subplots(figsize=(8, 6))
industry_esg.plot(kind='barh', ax=ax)
ax.set_xlabel('Average ESG Combined Score')
st.pyplot(fig)
