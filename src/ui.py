import streamlit as st
import plotly.graph_objects as go

from src.helpers import format_number


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