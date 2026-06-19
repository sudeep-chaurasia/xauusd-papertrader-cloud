import time

from config import LOT_SIZE
from data.twelvedata_feed import (
    get_price,
    get_candles
)

from engine.paper_broker import PaperBroker
from engine.trade_logger import initialize
from strategies.trend_breakout import signal


MAX_OPEN_TRADES = 10


def main():

    initialize()

    broker = PaperBroker(100000)

    last_signal = None

    print("CLOUD AUTO TRADER STARTED")

    while True:

        try:

            df = get_candles()

            # Dashboard / Debug ke liye
            df["ema20"] = df["close"].ewm(
                span=20,
                adjust=False
            ).mean()

            df["ema50"] = df["close"].ewm(
                span=50,
                adjust=False
            ).mean()

            current_signal = signal(df)

            print(
                f"Signal={current_signal} | "
                f"EMA20={df['ema20'].iloc[-1]:.2f} | "
                f"EMA50={df['ema50'].iloc[-1]:.2f} | "
                f"OpenTrades={len(broker.open_positions)} | "
                f"Balance={broker.balance:.2f}"
            )

            # New Trade Entry
            if (
                current_signal is not None
                and current_signal != last_signal
                and len(broker.open_positions) < MAX_OPEN_TRADES
            ):

                tick = get_price()

                if current_signal == "BUY":

                    broker.open_trade(
                        side="BUY",
                        price=tick["ask"],
                        lot=LOT_SIZE
                    )

                elif current_signal == "SELL":

                    broker.open_trade(
                        side="SELL",
                        price=tick["bid"],
                        lot=LOT_SIZE
                    )

                last_signal = current_signal

            # Open Trades Monitoring
            tick = get_price()

            for trade in broker.open_positions.copy():

                current_price = (
                    tick["bid"]
                    if trade["side"] == "BUY"
                    else tick["ask"]
                )

                pnl = broker.calculate_profit(
                    trade,
                    current_price
                )

                print(
                    f"Trade #{trade['id']} "
                    f"PNL={pnl:.2f}"
                )

                if pnl >= trade["tp_usd"]:

                    broker.close_trade(
                        trade,
                        current_price
                    )

                elif pnl <= -trade["sl_usd"]:

                    broker.close_trade(
                        trade,
                        current_price
                    )

            # 5 minute polling
            time.sleep(300)

        except Exception as e:

            print(
                "ERROR:",
                str(e)
            )

            time.sleep(60)


if __name__ == "__main__":

    main()