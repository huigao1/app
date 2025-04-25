import streamlit as st
import pandas as pd
from utils import load_esg_zip

@st.cache_data(show_spinner=False)
def load_data():
    return load_esg_zip()          # 默认读取根目录 zip

df = load_data()
st.title("📊 Dataset Overview")
st.write("Preview of the cleaned ESG & financial dataset (loaded from ZIP).")
st.dataframe(df.head())
st.markdown("---\n*Tip: use the navigation bar above to explore EDA or modeling pages.*")
