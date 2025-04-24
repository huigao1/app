import streamlit as st
import pandas as pd

# ---------------------------
# Data loader (cached)
# ---------------------------
@st.cache_data(show_spinner=False)
def load_data(path: str = "esg_cleaned_final.csv") -> pd.DataFrame:
    return pd.read_csv(path)

df = load_data()

# ---------------------------
# Page content
# ---------------------------
st.title("📊 Dataset Overview")

st.write("Preview of the cleaned ESG & financial dataset used throughout the dashboard.")

st.dataframe(df.head())

st.markdown(
    "---\n"
    "*Tip: use the navigation bar at the top to dive into EDA or modeling pages.*"
)
