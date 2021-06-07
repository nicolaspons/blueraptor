import config
import csv
from binance.client import Client

client = Client(config.API_KEY, config.SECRET_KEY)

csvfile = open("15minutes.csv", "w", newline="")
candlestick_writer = csv.writer(csvfile, delimiter=",")

candlesticks = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 May, 2012", "6 Jun, 2021"
)

for candlestick in candlesticks:
    candlestick_writer.writerow(candlestick)

csvfile.close()
