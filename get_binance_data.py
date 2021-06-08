import config
import csv
from binance.client import Client

client = Client(config.API_KEY, config.SECRET_KEY)

csvfile = open("15minutes_test.csv", "w", newline="")
candlestick_writer = csv.writer(csvfile, delimiter=",")

candlesticks = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "7 May, 2021", "7 Jun, 2021"
)

for candlestick in candlesticks:
    candlestick_writer.writerow(candlestick)

csvfile.close()
