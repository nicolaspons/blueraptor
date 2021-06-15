import ccxt
import ta
import pandas as pd
import config
from ta.volatility import BollingerBands

exchange = ccxt.binance({"apiKey": config.API_KEY, "secret": config.SECRET_KEY})

markets = exchange.load_markets()

bars = exchange.fetch_ohlcv("ETH/USDT", limit=20)

df = pd.DataFrame(bars, columns=["Open time", "Open", "High", "Low", "Close", "Volume"])

bb_indicator = BollingerBands(df["Close"])

upper_band = bb_indicator.bollinger_hband()
lower_band = bb_indicator.bollinger_lband()
moving_average = bb_indicator.bollinger_mavg()
