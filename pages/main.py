import streamlit as st, pandas as pd
from utils import load_esg_zip

@st.cache_data(show_spinner=False)
def load():
    return load_esg_zip()
df = load()

# KPI 卡
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rows", f"{len(df):,}")
col2.metric("Years", f"{df['year'].min()}–{df['year'].max()}")
col3.metric("Divisions", df['Division'].nunique())
col4.metric("Tickers", df['ticker'].nunique())

st.divider()
st.write("### Quick preview")
st.dataframe(df.head())

# 下载按钮
csv_bytes = df.to_csv(index=False).encode()
st.download_button("⬇️ Download filtered CSV", csv_bytes, "esg_subset.csv", "text/csv")
