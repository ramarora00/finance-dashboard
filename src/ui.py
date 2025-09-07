import streamlit as st
import plotly.graph_objects as go
from src.helpers import format_number
import streamlit as st
import yfinance as yf
import time



def show_ticker_bar(tickers):
    def get_live_prices(ticker):
        try:
            data = yf.download(ticker, period="1d", interval="1m", progress=False)
            if data.empty or len(data) < 2:
                return None, None  # agar data insufficient ho
            last = float(data["Close"].iloc[-1])
            prev = float(data["Close"].iloc[-2])
            change = float((last - prev) / prev * 100)

            return last, change
        except Exception as e:
            return None, None

    ticker_items = []
    for t in tickers:
        last, change = get_live_prices(t)
        if last is not None:
            color = "limegreen" if change > 0 else "red"
            arrow = "▲" if change > 0 else "▼"
            ticker_items.append(
                f"<span style='margin-right:40px; color:{color}; font-weight:600;'>{t} ₹{last:.2f} {arrow}{change:.2f}%</span>"
            )
            time.sleep(1.5)
        time.sleep(.5)  # API rate limit ke liye thoda wait karna

    if ticker_items:
        ticker_html = " ".join(ticker_items)
        st.markdown(
            f"""
            <div style="overflow:hidden; white-space:nowrap; box-sizing:border-box;">
                <div style="display:inline-block; padding-left:100%; animation: ticker 20s linear infinite; font-size:16px;">
                    {ticker_html}
                </div>
            </div>
            <style>
            @keyframes ticker {{
                0%   {{ transform: translateX(0%); }}
                100% {{ transform: translateX(-100%); }}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("Ticker data unavailable.")




def render_dashboard(df_ind, info, ticker, download_data: bool):
    """Render the company header, tabs, charts and raw data exactly like original app.py."""
    short_name = info.get("shortName") or info.get("longName") or ticker
    st.subheader(f"🏢 {short_name} — {ticker}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Market Cap", format_number(info.get("marketCap")))
    col2.metric("Sector", info.get("sector", "N/A"))
    col3.metric("Industry", info.get("industry", "N/A"))

    # Tabs: Overview / Candlestick / Indicators / Data
    tabs = st.tabs(["Overview", "Candlestick", "Indicators", "Raw Data"])

    with tabs[0]:
        st.markdown("#### Closing Price & Moving Averages")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind["Close"], mode="lines", name="Close"))
        if "MA50" in df_ind.columns:
            fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind["MA50"], mode="lines", name="MA50"))
        if "MA200" in df_ind.columns:
            fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind["MA200"], mode="lines", name="MA200"))
        fig.update_layout(xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Volume")
        vol_fig = go.Figure()
        vol_fig.add_trace(go.Bar(x=df_ind.index, y=df_ind["Volume"], name="Volume"))
        vol_fig.update_layout(xaxis_title="Date", yaxis_title="Volume")
        st.plotly_chart(vol_fig, use_container_width=True)

    with tabs[1]:
        st.markdown("#### Candlestick Chart")
        candle = go.Figure(data=[go.Candlestick(
            x=df_ind.index,
            open=df_ind["Open"], high=df_ind["High"], low=df_ind["Low"], close=df_ind["Close"]
        )])
        candle.update_layout(xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(candle, use_container_width=True)

    with tabs[2]:
        st.markdown("#### RSI (14)")
        if "RSI14" in df_ind.columns:
            rsi_fig = go.Figure()
            rsi_fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind["RSI14"], mode="lines", name="RSI14"))
            rsi_fig.update_layout(yaxis=dict(range=[0, 100]), xaxis_title="Date")
            st.plotly_chart(rsi_fig, use_container_width=True)
        else:
            st.info("RSI not available for this timeframe.")

        st.markdown("#### MACD")
        if "MACD" in df_ind.columns:
            macd_fig = go.Figure()
            macd_fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind["MACD"], name="MACD"))
            macd_fig.add_trace(go.Scatter(x=df_ind.index, y=df_ind["MACD_Signal"], name="Signal"))
            st.plotly_chart(macd_fig, use_container_width=True)
        else:
            st.info("MACD not available for this timeframe.")

    with tabs[3]:
        st.markdown("#### Raw Data (last rows)")
        st.dataframe(df_ind.tail(10))

        if download_data:
            csv = df_ind.to_csv(index=True).encode('utf-8')
            st.download_button(label="⬇️ Download CSV", data=csv, file_name=f"{ticker}_data.csv", mime="text/csv")