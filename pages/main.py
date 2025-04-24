import streamlit as st
import pandas as pd

@st.cache_data(show_spinner=False)
def load_data(path: str = "esg_cleaned_final.csv.zip") -> pd.DataFrame:
    # 直接读取 zip 内部的 CSV
    return pd.read_csv(path, compression="zip")

df = load_data()

st.title("📊 Dataset Overview")
st.write("Preview of the cleaned ESG & financial dataset (loaded from ZIP).")
st.dataframe(df.head())
st.markdown("---\n*Tip: use the navigation bar above to explore EDA or modeling pages.*")
