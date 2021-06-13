import config
import csv
import os
import json
from datetime import datetime
from binance.client import Client

DIR_PATH = "./data"
STARTING_DATE = "1 Jan, 2010"

intervals = {"1DAY": Client.KLINE_INTERVAL_1DAY}

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

# Tickers loading
with open("tickers.json", "r") as f:
    tickers = json.load(f)
f.close()

# Creating client
client = Client(config.API_KEY, config.SECRET_KEY)

for ticker in tickers:
    for k, v in intervals.items():
        print(
            "Getting historical data for the ticker {} with {} interval".format(
                ticker, k
            )
        )
        filename = ticker + ".csv"
        csvfile = open(os.path.join(DIR_PATH, v, filename), "w", newline="")
        candlestick_writer = csv.writer(csvfile, delimiter=",")

        candlesticks = client.get_historical_klines(
            ticker, v, STARTING_DATE, datetime.now().strftime("%d %b, %Y")
        )

        candlestick_writer.writerow(headers)

        for candlestick in candlesticks:
            candlestick[0] = candlestick[0] / 1000
            candlestick_writer.writerow(candlestick)

        csvfile.close()
