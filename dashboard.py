import streamlit as st
import pandas as pd
import os

START_BALANCE = 10000

st.set_page_config(
    page_title="XAUUSD Paper Trader",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align:center;'>🚀 XAUUSD Paper Trading Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown("""
<style>

[data-testid="stMetric"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 12px;
}

/* Metric Label */
[data-testid="stMetricLabel"] {
    color: white !important;
    font-weight: bold !important;
    font-size: 18px !important;
}

/* Metric Value */
[data-testid="stMetricValue"] {
    color: white !important;
    font-weight: 900 !important;
    font-size: 32px !important;
}

</style>
""", unsafe_allow_html=True)
FILE = "trades/trades.csv"

if not os.path.exists(FILE):
    st.warning("No trade history found")
    st.stop()

df = pd.read_csv(FILE)

if df.empty:
    st.warning("No trades yet")
    st.stop()

total_trades = len(df)

wins = len(df[df["pnl"] > 0])

losses = len(df[df["pnl"] < 0])

win_rate = (wins / total_trades) * 100

total_profit = df["pnl"].sum()

avg_profit = df["pnl"].mean()

best_trade = df["pnl"].max()

worst_trade = df["pnl"].min()

current_balance = START_BALANCE + total_profit

st.subheader("Account Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Balance",
        f"{current_balance:.2f}"
    )

with col2:
    st.metric(
        "Profit",
        f"{total_profit:.2f}"
    )

with col3:
    st.metric(
        "Win Rate",
        f"{win_rate:.2f}%"
    )

with col4:
    st.metric(
        "Trades",
        total_trades
    )

st.subheader("Trading Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Wins",
        wins
    )

with col2:
    st.metric(
        "Losses",
        losses
    )

with col3:
    st.metric(
        "Best Trade",
        f"{best_trade:.2f}"
    )

with col4:
    st.metric(
        "Worst Trade",
        f"{worst_trade:.2f}"
    )

st.subheader("Strategy")

st.success(
    "Trend Breakout Strategy Active | GOLD.i# | Lot Size 0.02"
)

st.subheader("Equity Curve")

df["equity"] = (
    START_BALANCE
    + df["pnl"].cumsum()
)

st.line_chart(df["equity"])

st.subheader("Trade History")

st.dataframe(
    df,
    use_container_width=True
)

st.subheader("Last 10 Trades")

st.dataframe(
    df.tail(10),
    use_container_width=True
)