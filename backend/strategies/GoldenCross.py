import datetime
import os, sys, argparse
import pandas as pd
import backtrader as bt

cerebro = bt.Cerebro()
cerebro.broker.setcash(100000)

btc_usd_prices = pd.read_csv("../../data/1d/BTCUSDT.csv", index_col=False)
btc_usd_prices["Open time"] = pd.to_datetime(btc_usd_prices["Open time"], unit="s")

feed = bt.feeds.PandasData(dataname=btc_usd_prices, datetime="Open time")

cerebro.adddata(feed)

cerebro.run()

cerebro.plot()
