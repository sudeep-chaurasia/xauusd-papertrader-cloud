from engine.paper_broker import PaperBroker

broker = PaperBroker(100000)

trade = broker.open_trade(
    "BUY",
    3300,
    0.1
)

print(
    broker.calculate_profit(
        trade,
        3305
    )
)