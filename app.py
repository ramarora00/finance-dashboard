import streamlit as st
import pandas as pd
import plotly.express as px
from features.data_fetcher import get_stock_data

st.title("📊 Stock Market Dashboard")

# --- Input ---
ticker = st.text_input("Enter Stock Symbol", "RELIANCE.NS")

if ticker:
    # --- Get Data ---
    df = get_stock_data(ticker)
    
    # --- Show Table ---
    st.subheader(f"{ticker} - Latest Data")
    st.write(df.tail())

    # --- Plot Close Price ---
    if "Close" in df.columns:
        fig = px.line(df, x=df.index, y="Close", title=f"{ticker} Stock Price")
        st.plotly_chart(fig)
    else:
        st.warning("No 'Close' column found in data.")

    # --- CSV Download ---
    csv = df.to_csv(index=True)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{ticker}_data.csv",
        mime="text/csv"
    )
