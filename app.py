from flask import Flask, render_template, jsonify
import config, csv
from binance.client import Client

app = Flask(__name__)

client = Client(config.API_KEY, config.SECRET_KEY)


@app.route("/")
def index():
    title = "CoinBot"

    info = client.get_account()
    return render_template("index.html", title=title, balances=info["balances"])


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
