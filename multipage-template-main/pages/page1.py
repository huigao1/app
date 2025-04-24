import streamlit as st
import pandas as pd

# Print out the title for Page 1: View stock info dataframe
st.title("Page 1: View Stock Data")

# Display the Pandas dataframe of the stock data from yfinance
#  Note: The stock info dataframe is stored in a StreamLit "session state" that allows the data to be shared across
#        the mutiple pages (ie, main.py, page1.py, page2.py and page4.py)

st.dataframe(st.session_state.data, use_container_width=True)

# The dataframe can also be displayed as an editable interactive dataframe using the StreamLit data_editor function 
#st.session_state.data = st.data_editor(st.session_state.data)
