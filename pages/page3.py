import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data(show_spinner=False)
def load_data(path="esg_cleaned_final.csv"):
    return pd.read_csv(path)

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
