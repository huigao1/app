import streamlit as st

st.title("Page 3: Close Price data")

# Plot a Linbe Chart of the Stock Price of the stock
if 'data' in st.session_state:
   st.line_chart(st.session_state.data['Close'])

else:
   st.write("No stock data found. Please select stock on Main Page.")

