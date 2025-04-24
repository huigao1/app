import streamlit as st
import pandas as pd
import yfinance as yf

# Print out info for the Main page:
st.title("Main Page: Please select a stock")
st.header("<---- Enter ticker & dates in Sidebar Prompts.")

# Sidebar inputs for ticker symbol and dates
ticker_symbol = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, MSFT)", value="MSFT")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-31"))

# Print update onb which ticker and dates
st.write(f"You have selected **{ticker_symbol}** from {start_date} to {end_date}.")
st.markdown(''':red[Now click on] :blue-background[Page 1, 2 or 3] to the left to view analyses.''')

# Access the stock data for the given tocker using the yfinance "download" function
# Temporarily store data in "df" dataframe
df = yf.download(ticker_symbol, start=start_date, end=end_date)
if df.empty:
   st.error("No data found. Please check the ticker symbol or date range.")
   st.stop()


#  Note: The stock info dataframe (df) is stored in a StreamLit "session state" that allows the data to be shared across
#        the mutiple pages (ie, main.py, page1.py, page2.py and page4.py)
st.session_state.data = df
