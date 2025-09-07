import streamlit as st

def get_user_input():
    with st.sidebar:
        st.header("⚙️ Controls")
        ticker = st.text_input("Ticker (e.g. RELIANCE.NS, AAPL)", value="RELIANCE.NS")
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"], index=2)
        interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
    return ticker, period, interval
