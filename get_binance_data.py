import config
import csv
import os
import json
import argparse
import pandas as pd
from itertools import product
from datetime import datetime
from binance.client import Client

DIR_PATH = "./data"
STARTING_DATE = "1 Jan, 2010"
TIKERS_PATH = "./resources/tickers.json"

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

intervals = [
    Client.KLINE_INTERVAL_1WEEK,
    Client.KLINE_INTERVAL_1DAY,
    Client.KLINE_INTERVAL_4HOUR,
    Client.KLINE_INTERVAL_1HOUR,
]

# Creating client
client = Client(config.API_KEY, config.SECRET_KEY)


def create_directories(intervals):
    """Creates directories for each interval if it doesn't exist."""
    if not os.path.exists(DIR_PATH):
        os.mkdir(DIR_PATH)
    for interval in intervals:
        path_to_interval = os.path.join(DIR_PATH, interval)
        if not os.path.exists(path_to_interval):
            os.mkdir(path_to_interval)


def request_binance_data(tickers_intervals, starting_date, ending_date):
    """Requests the data from the binance API and save them into a csv file."""
    for ticker, interval in tickers_intervals:
        print(
            "Getting historical data for the ticker {} with {} interval".format(
                ticker, interval
            )
        )
        try:
            csvfile = open(
                os.path.join(DIR_PATH, interval, "{}.csv".format(ticker)),
                "w",
                newline="",
            )
            candlestick_writer = csv.writer(csvfile, delimiter=",")

            candlesticks = client.get_historical_klines(
                ticker, interval, starting_date, ending_date
            )

            candlestick_writer.writerow(headers)

            for candlestick in candlesticks:
                candlestick[0] = candlestick[0] / 1000
                candlestick_writer.writerow(candlestick)

            csvfile.close()
        except Exception as e:
            print(e)


def update_binance_data(tickers_intervals):
    """Requests the data from the binance API and updates the corresponding csv file."""
    for ticker, interval in tickers_intervals:
        try:
            csvfile = open(
                os.path.join(DIR_PATH, interval, "{}.csv".format(ticker)),
                "w",
                newline="",
            )
            path_to_file = os.path.join(DIR_PATH, interval, f"{ticker}.csv")
            csvfile = pd.read_csv(path_to_file, index_col=False)
            starting_date = datetime.utcfromtimestamp(
                csvfile.iloc[-1]["Open time"]
            ).strftime("%d %b, %Y")
            print(
                "Getting historical data for the ticker {} with {} interval starting from {}".format(
                    ticker, interval, starting_date
                )
            )

            candlesticks = client.get_historical_klines(
                ticker, interval, starting_date, datetime.now().strftime("%d %b, %Y")
            )

            # overriding the last row.
            candlesticks[0][0] = candlesticks[0][0] / 1000
            csvfile.loc[len(csvfile) - 1] = candlesticks[0][:-1]
            for candlestick in candlesticks[1:]:
                candlestick[0] = candlestick[0] / 1000
                csvfile.loc[len(csvfile)] = candlestick[:-1]

            csvfile.to_csv(path_to_file, index=False)
        except Exception as e:
            print(e)


def main(args=None):
    args = parse_args(args)

    tickers = args.tickers
    if len(tickers) == 0:
        # Tickers loading
        with open(TIKERS_PATH, "r") as f:
            tickers = json.load(f)
        f.close()

    create_directories(args.intervals)

    tickers_intervals = list(product(tickers, intervals))

    if args.update:
        # Update the data
        update_binance_data(tickers_intervals)
    else:
        request_binance_data(
            tickers_intervals, starting_date=args.fromdate, ending_date=args.todate
        )


def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=("Binance Data"),
    )

    parser.add_argument(
        "--dirpath", default=DIR_PATH, required=False, help="Directory data path"
    )

    # Defaults for dates
    parser.add_argument(
        "--fromdate",
        required=False,
        default=STARTING_DATE,
        help="Date[time] in d b, Y format",
    )

    parser.add_argument(
        "--todate",
        required=False,
        default=datetime.now().strftime("%d %b, %Y"),
        help="Date[time] in d b, Y format",
    )

    parser.add_argument(
        "--tickers",
        required=False,
        default=[],
        nargs="+",
        help="list of tikers format",
    )

    parser.add_argument(
        "--intervals",
        required=False,
        default=intervals,
        nargs="+",
        help="kwargs in key=value format",
    )

    parser.add_argument(
        "--update",
        required=False,
        default=False,
        help="Boolean used to update the existing data in bool format",
    )

    return parser.parse_args(pargs)


main()
