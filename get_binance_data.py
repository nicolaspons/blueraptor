import config
import csv
import os
from binance.client import Client

dir_path = "./data"

client = Client(config.API_KEY, config.SECRET_KEY)

csvfile = open(os.path.join(dir_path, "daily_test.csv"), "w", newline="")
candlestick_writer = csv.writer(csvfile, delimiter=",")

candlesticks = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2021", "7 Jun, 2021"
)

for candlestick in candlesticks:
    candlestick[0] = candlestick[0] / 1000
    candlestick_writer.writerow(candlestick)

csvfile.close()
