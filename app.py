import streamlit as st
import yfinance as yf
import plotly.express as px

st.title("📊 Stock Market Dashboard")

ticker = st.text_input("Enter Stock Symbol", "RELIANCE.NS")

if ticker:
    df = yf.download(ticker, period="6mo", interval="1d")
    st.write(df.tail())

    fig = px.line(df, x=df.index, y="Close", title=f"{ticker} Stock Price")
    st.plotly_chart(fig)
