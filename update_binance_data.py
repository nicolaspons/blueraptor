import config
import os
import json
import pandas as pd
from datetime import datetime
from binance.client import Client

DIR_PATH = "./data"

intervals = {"1DAY": Client.KLINE_INTERVAL_1DAY, "4HOUR": Client.KLINE_INTERVAL_4HOUR}

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
        filename = ticker + ".csv"
        path_to_file = os.path.join(DIR_PATH, v, filename)
        df = pd.read_csv(path_to_file, index_col=False)
        ts = df.iloc[-1]["Open time"]
        starting_date = datetime.utcfromtimestamp(ts).strftime("%d %b, %Y")
        print(
            "Getting historical data for the ticker {} with {} interval starting from {}".format(
                ticker, k, starting_date
            )
        )

        candlesticks = client.get_historical_klines(
            ticker, v, starting_date, datetime.now().strftime("%d %b, %Y")
        )

        # overriding the last row.
        candlesticks[0][0] = candlesticks[0][0] / 1000
        df.loc[len(df) - 1] = candlesticks[0][:-1]
        for candlestick in candlesticks[1:]:
            candlestick[0] = candlestick[0] / 1000
            df.loc[len(df)] = candlestick[:-1]

        df.to_csv(path_to_file, index=False)
