from flask import Flask, render_template, jsonify, request
import config, csv
from binance.client import Client
import numpy as np
import tools
import json
import pandas as pd
import os
import talib


app = Flask(__name__)

client = Client(config.API_KEY, config.SECRET_KEY)


@app.route("/")
def index():
    title = "CoinBot"

    account = client.get_account()
    balances = account["balances"]
    tools.sort_balances(balances)
    exchange_info = client.get_exchange_info()

    return render_template(
        "index.html",
        title=title,
        balances=balances[:10],
        symbols=exchange_info["symbols"],
    )


@app.route("/buy")
def buy():
    return "buy"


@app.route("/sell")
def sell():
    return "sell"


@app.route("/settings")
def settings():
    return "settings"


@app.route("/history")
def hisory():
    candlesticks = client.get_historical_klines(
        "BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "3 days ago UTC "
    )

    processed_candlesticks = []
    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4],
        }
        processed_candlesticks.append(candlestick)
    return jsonify(processed_candlesticks)


@app.route("/screener")
def screener():
    pattern = request.args.get("pattern", None)
    interval = request.args.get("interval", None)

    with open("./tickers.json", "r") as f:
        ticker_names = json.load(f)
    f.close()

    tickers = {}

    if pattern and interval:
        for ticker_name in ticker_names:
            df = pd.read_csv(
                os.path.join("./data", interval, ticker_name + ".csv"), index_col=False
            )
            pattern_function = getattr(talib, pattern)
            result = pattern_function(df["Open"], df["High"], df["Low"], df["Close"])
            last = result.tail(1).values[0]
            tickers[ticker_name] = last

    with open("./patterns.json", "r") as f:
        patterns = json.load(f)
    f.close()
    return render_template(
        "screener.html", patterns=patterns, intervals=tools.intervals, tickers=tickers
    )


@app.route("/snapshot")
def snapshot():
    with open("./tickers.json", "r") as f:
        tickers = json.load(f)
    f.close()
    tickers = tickers[:10]


@app.route("/scan")
def scan():
    return render_template("scan.html")
