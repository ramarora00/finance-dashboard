import yfinance as yf
import pandas as pd

def get_stock_data(ticker: str, period="6mo", interval="1d") -> pd.DataFrame:
    """Fetch stock data safely from Yahoo Finance and clean columns"""
    df = yf.download(ticker, period=period, interval=interval)

    # Handle MultiIndex or non-string columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip().title() for col in df.columns.values]
    else:
        df.columns = df.columns.map(str).str.strip().str.title()

    return df
