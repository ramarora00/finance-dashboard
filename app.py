import streamlit as st
from src.data import get_stock_data
from src.helpers import format_number, compute_indicators
from src.ui import render_dashboard, show_ticker_bar

# Page config
st.set_page_config(page_title="📊 Stock Market Dashboard", layout="wide")

# Tickers list
tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", 
           "TATAMOTOR.NS", "DMART.NS", "TITAN.NS", "BAJFINANCE.NS"]

# Show horizontal ticker with smooth loop
show_ticker_bar(tickers)

# Title
st.markdown("""
<div style="font-size:28px; font-weight:bold; margin-bottom:5px;">📈 Finance Dashboard</div>
""", unsafe_allow_html=True)

# Hamburger menu below title
st.markdown("""
<style>
/* Sidebar style */
#mySidebar { 
    height:100%; width:0; position:fixed; z-index:1; top:0; left:0; 
    background-color:#111; overflow-x:hidden; transition:0.5s; padding-top:60px;
}
#mySidebar a { 
    padding:10px 20px; text-decoration:none; font-size:20px; color:white; display:block; transition:0.3s;
}
#mySidebar a:hover { color:#f1f1f1; }
#menuBtn { 
    font-size:28px; cursor:pointer; color:#111; margin-top:10px; display:inline-block; 
}
.ticker-wrapper { margin-top:10px; display:flex; align-items:center; }
</style>

<div class="ticker-wrapper">
    <span id="menuBtn" onclick="toggleSidebar()">&#9776;</span>
</div>

<div id="mySidebar">
  <a href="#">Home</a>
  <a href="#">Stocks</a>
  <a href="#">Portfolio</a>
  <a href="#">Settings</a>
</div>

<script>
function toggleSidebar() {
  var sidebar = document.getElementById("mySidebar");
  if (sidebar.style.width === "250px") { 
      sidebar.style.width = "0"; 
  } else { 
      sidebar.style.width = "250px"; 
  }
}
</script>
""", unsafe_allow_html=True)

# Streamlit sidebar controls
with st.sidebar:
    st.header("⚙️ Controls")
    ticker = st.text_input("Ticker (e.g. RELIANCE.NS, TCS.NS, AAPL)", value="RELIANCE.NS")
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"], index=2)
    interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
    download_data = st.checkbox("Show download CSV button", value=True)

# Fetch & display stock data
if ticker:
    try:
        df, info = get_stock_data(ticker.strip(), period, interval)

        if df is None or df.empty or "Close" not in df.columns:
            st.error("⚠️ No data found for this ticker/period/interval. Try another symbol or adjust the period.")
        else:
            # Compute indicators
            df_ind = compute_indicators(df)
            # Render dashboard
            render_dashboard(df_ind, info, ticker, download_data)

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
