import pandas as pd

# --------- Helpers ----------
def format_number(x):
    try:
        if x is None or (isinstance(x, float) and pd.isna(x)):
            return "N/A"
        return f"{int(x):,}"
    except Exception:
        return str(x)


def compute_indicators(df: pd.DataFrame):
    """Compute MA50, MA200, RSI(14), MACD for given df in-place and return df."""
    if "Close" not in df.columns:
        return df
    df = df.copy()
    df["MA50"] = df["Close"].rolling(window=50, min_periods=1).mean()
    df["MA200"] = df["Close"].rolling(window=200, min_periods=1).mean()

    # RSI (14)
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14, min_periods=14).mean()
    avg_loss = loss.rolling(window=14, min_periods=14).mean()
    rs = avg_gain / avg_loss
    df["RSI14"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df