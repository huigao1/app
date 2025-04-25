import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import load_esg_zip

@st.cache_data(show_spinner=False)
def load_data():
    return load_esg_zip()          # 默认读取根目录 zip

df = load_data()

st.title("⏳ ESG Trend Over Time")

esg_trend = df.groupby('year')['ESG_Combined_Score'].mean()
fig, ax = plt.subplots()
esg_trend.plot(marker='o', ax=ax)
ax.set_xlabel('Year')
ax.set_ylabel('Average ESG Combined Score')
ax.set_title('Average ESG Combined Score Over Time')
ax.grid(True)
st.pyplot(fig)
