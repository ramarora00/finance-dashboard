import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def get_stock_data(ticker: str, period: str, interval: str):
    """Fetch stock history and info from yfinance and return a cleaned DataFrame + info dict."""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    info = {}
    try:
        info = stock.info or {}
    except Exception:
        info = {}
    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    return df, info