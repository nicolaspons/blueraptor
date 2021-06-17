import datetime
import os, sys, argparse
import pandas as pd
import backtrader as bt
from strategies.GoldenCross import GoldenCross
from strategies.BuyHold import BuyHold
from strategies.SuperTrendStrategy import SuperTrendStrategy
import backtrader as bt
from backtrader.plot import Plot_OldSync


class CustomPlotScheme(Plot_OldSync):
    def __init__(self):
        super().__init__()
        self.params.scheme.style = "candle"
        self.params.scheme.barup = "green"


cerebro = bt.Cerebro()
cerebro.broker.setcash(100000)

btc_usd_prices = pd.read_csv("../data/1d/BTCUSDT.csv", index_col=False)
btc_usd_prices["Open time"] = pd.to_datetime(btc_usd_prices["Open time"], unit="s")
# btc_usd_prices = btc_usd_prices.iloc[]

feed = bt.feeds.PandasData(
    dataname=btc_usd_prices,
    datetime="Open time",
    open=1,
    high=2,
    low=3,
    close=4,
    volume=5,
)

cerebro.adddata(feed)
# cerebro.addstrategy(SuperTrendStrategy)
# cerebro.addstrategy(BuyHold)
cerebro.addstrategy(GoldenCross)

cerebro.run()

cp = CustomPlotScheme()

cerebro.plot(plotter=cp)
