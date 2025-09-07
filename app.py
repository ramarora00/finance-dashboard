import streamlit as st
import yfinance as yf
import plotly.express as px

from features.sidebar import get_user_input

st.title("📊 Stock Market Dashboard")

# Get sidebar inputs
ticker, period, interval = get_user_input()

# Fetch data
if ticker:
    df = yf.download(ticker, period=period, interval=interval)
    
    if df.empty:
        st.error(f"No data found for ticker {ticker} with period={period} and interval={interval}")
    else:
        df.columns = df.columns.str.strip().str.title()  # Strip & fix column names
        st.write(df.tail())
        fig = px.line(df, x=df.index, y="Close", title=f"{ticker} Stock Price")
        st.plotly_chart(fig)
