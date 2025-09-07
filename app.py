import streamlit as st
from src.data import get_stock_data
from src.helpers import format_number, compute_indicators
from src.ui import render_dashboard
from src.ui import show_ticker_bar


st.set_page_config(page_title="📊 Stock Market Dashboard", layout="wide")
tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "TATAMOTOR.NS" , "DMART.NS", "TITAN.NS", "BAJFINANCE.NS"]
show_ticker_bar(tickers)

st.title("📈 Stock Market Dashboard (yfinance)")

# Sidebar controls



with st.sidebar:
    st.header("⚙️ Controls")
    ticker = st.text_input("Ticker (e.g. RELIANCE.NS, TCS.NS, AAPL)", value="RELIANCE.NS")
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"], index=2)
    interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
    download_data = st.checkbox("Show download CSV button", value=True)

if ticker:
    try:
        df, info = get_stock_data(ticker.strip(), period, interval)

        if df is None or df.empty or "Close" not in df.columns:
            st.error("⚠️ No data found for this ticker/period/interval. Try another symbol or adjust the period.")
        else:
            # Compute indicators
            df_ind = compute_indicators(df)

            # Render everything (company header, tabs, charts, table, download)
            render_dashboard(df_ind, info, ticker, download_data)

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")