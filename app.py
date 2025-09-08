import streamlit as st
from src.data import get_stock_data
from src.helpers import format_number, compute_indicators
from src.ui import render_dashboard, show_ticker_bar

# Page config (PRESERVED)
st.set_page_config(page_title="📊 Stock Market Dashboard", layout="wide")

# Tickers list (PRESERVED) 
tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "TATAMOTOR.NS", "DMART.NS", "TITAN.NS", "BAJFINANCE.NS"]

# Show horizontal ticker with smooth loop (PRESERVED)
show_ticker_bar(tickers)

# Title (PRESERVED)
st.markdown("""
<h1 style='text-align: center; color: #1f77b4; margin-bottom: 30px;'>
📊 Stock Market Dashboard
</h1>
""", unsafe_allow_html=True)

# ========== PERPLEXITY-STYLE LONG HORIZONTAL SEARCH BAR ==========
st.markdown("""
<style>
.big-search-bar input {
    height: 60px !important;
    font-size: 18px !important;
    border-radius: 30px !important;
    padding: 0 25px !important;
    border: 2px solid #e1e5e9 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}
.big-search-bar input:focus {
    border-color: #1f77b4 !important;
    box-shadow: 0 4px 20px rgba(31,119,180,0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# Long horizontal search bar
st.markdown('<div class="big-search-bar">', unsafe_allow_html=True)
search_ticker = st.text_input(
    "",
    value="RELIANCE.NS",
    placeholder="🔍 Search stocks (e.g., AAPL, RELIANCE.NS, GOOGL, TSLA, MSFT)...",
    label_visibility="collapsed",
    key="main_search"
).upper()
st.markdown('</div>', unsafe_allow_html=True)

# Controls row below search bar
st.markdown("<br>", unsafe_allow_html=True)
control_col1, control_col2, control_col3, control_col4, control_col5 = st.columns([2, 2, 2, 1, 1])

with control_col1:
    # Period selection
    period_options = {
        "1mo": "1 Month",
        "3mo": "3 Months", 
        "6mo": "6 Months",  # DEFAULT
        "1y": "1 Year",
        "2y": "2 Years",
        "5y": "5 Years"
    }
    
    selected_period = st.selectbox(
        "📅 **Time Period**",
        options=list(period_options.keys()),
        format_func=lambda x: period_options[x],
        index=2  # Default to 6mo
    )

with control_col2:
    # Interval selection
    interval_options = {
        "1d": "Daily",
        "1wk": "Weekly", 
        "1mo": "Monthly"
    }
    
    selected_interval = st.selectbox(
        "⏱️ **Data Interval**",
        options=list(interval_options.keys()),
        format_func=lambda x: interval_options[x],
        index=0  # Default to daily
    )

with control_col3:
    # Quick stock suggestions
    popular_stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "AAPL", "GOOGL", "MSFT", "TSLA"]
    
    quick_pick = st.selectbox(
        "⚡ **Quick Pick**",
        options=["Custom"] + popular_stocks,
        index=0
    )

with control_col4:
    st.markdown("<br>", unsafe_allow_html=True)
    refresh_btn = st.button("🔄 **Refresh**", use_container_width=True)

with control_col5:
    st.markdown("<br>", unsafe_allow_html=True)
    download_data = st.checkbox("📥 **Download**", value=True)

# Use quick pick if selected
final_ticker = quick_pick if quick_pick != "Custom" else search_ticker

# Refresh functionality
if refresh_btn:
    st.cache_data.clear()
    st.rerun()

st.markdown("---")  # Clean separator

# ========== MAIN DASHBOARD (ALL EXISTING FEATURES PRESERVED) ==========

try:
    # Show loading spinner
    with st.spinner(f"📊 Loading {final_ticker} data for {period_options[selected_period]}..."):
        # Get stock data (PRESERVED FUNCTIONALITY)
        df, info = get_stock_data(final_ticker, selected_period, selected_interval)
    
    if df.empty:
        st.error(f"❌ No data found for ticker: **{final_ticker}**")
        
        # Show popular suggestions
        st.info("💡 **Try these popular stocks:**")
        suggestion_cols = st.columns(4)
        suggestions = ["RELIANCE.NS", "TCS.NS", "AAPL", "GOOGL", "MSFT", "TSLA", "INFY.NS", "HDFCBANK.NS"]
        
        for i, stock in enumerate(suggestions):
            with suggestion_cols[i % 4]:
                if st.button(f"📈 {stock}", key=f"suggest_{i}"):
                    st.session_state.main_search = stock
                    st.rerun()
    
    else:
        # Show quick stats
        current_price = df['Close'].iloc[-1]
        price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100)
        
        st.success(f"✅ **{final_ticker}** loaded • ₹{current_price:.2f} • {price_change:+.2f}% ({period_options[selected_period]}) • {len(df)} data points")
        
        # Compute indicators (PRESERVED FUNCTIONALITY)
        df_with_indicators = compute_indicators(df)
        
        # Render the complete dashboard (ALL EXISTING FEATURES PRESERVED)
        render_dashboard(df_with_indicators, info, final_ticker, download_data)

except Exception as e:
    st.error(f"❌ **Error loading data:** {str(e)}")
    st.info("💡 **Tips:** Check ticker format (RELIANCE.NS for Indian stocks, AAPL for US stocks)")
