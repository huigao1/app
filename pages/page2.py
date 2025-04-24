import streamlit as st
import pandas as pd

st.title("Page 2: Stock Price Statistics")


if 'data' in st.session_state:
   st.write("Statistics of the DataFrame:")
   st.write(st.session_state.data.describe())
else:
   st.write("No stock data found. Please select stock on Main Page.")
