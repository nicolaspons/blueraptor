import config
import csv
import os
from binance.client import Client

dir_path = "./data"

client = Client(config.API_KEY, config.SECRET_KEY)

csvfile = open(os.path.join(dir_path, "XRPUSDT_4H.csv"), "w", newline="")
candlestick_writer = csv.writer(csvfile, delimiter=",")

candlesticks = client.get_historical_klines(
    "XRPUSDT", Client.KLINE_INTERVAL_4HOUR, "1 Jan, 2012", "8 Jun, 2021"
)

headers = [
    "Open time",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "Close time",
    "Quote asset volume",
    "Number of trades",
    "Taker buy base asset volume",
    "Taker buy quote asset volume",
]

candlestick_writer.writerow(headers)

for candlestick in candlesticks:
    candlestick[0] = candlestick[0] / 1000
    candlestick_writer.writerow(candlestick)

csvfile.close()
