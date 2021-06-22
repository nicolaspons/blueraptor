import datetime
import os, sys, argparse
import pandas as pd
import backtrader as bt
from pyfolio import pos
from strategies.GoldenCross import GoldenCross
from strategies.BuyHold import BuyHold
from strategies.SuperTrendStrategy import SuperTrendStrategy
import backtrader as bt
from backtrader.plot import Plot_OldSync
import pyfolio as pf


class CustomPlotScheme(Plot_OldSync):
    def __init__(self):
        super().__init__()
        self.params.scheme.style = "candle"
        self.params.scheme.barup = "green"

    def plot(
        self, strategy, figid=0, numfigs=1, iplot=True, start=None, end=None, **kwargs
    ):
        figs = super().plot(strategy, figid, numfigs, iplot, start, end, **kwargs)

        for i, fig in enumerate(figs):
            width = 100
            height = 16
            dpi = 300
            fig.set_size_inches(width, height)
            filename = "/Users/pons_n/Desktop/" + "test" + str(i) + ".png"
            print("Trying to save the plot")
            fig.savefig(filename, dpi=dpi)

    def show(self):
        print("skip the display")
        return


cerebro = bt.Cerebro()
cerebro.broker.setcash(100000)

btc_usd_prices = pd.read_csv("../data/1d/BTCUSDT.csv", index_col=False)
btc_usd_prices["Open time"] = pd.to_datetime(btc_usd_prices["Open time"], unit="s")
btc_usd_prices = btc_usd_prices.iloc[100:800]

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
cerebro.addstrategy(SuperTrendStrategy)
# cerebro.addstrategy(BuyHold)
# cerebro.addstrategy(GoldenCross)


cerebro.broker.setcommission(commission=0.00075, margin=False)

cerebro.addanalyzer(bt.analyzers.PyFolio, _name="pyfolio")

results = cerebro.run()

strat = results[0]

pyfoliozer = strat.analyzers.getbyname("pyfolio")

returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()

print(returns)

print(":::")

print(positions)

print("mmm")
print(transactions)

print("lll")
print(gross_lev)

pf.create_simple_tear_sheet(returns, positions=positions, transactions=transactions)

cp = CustomPlotScheme()

figs = cerebro.plot(plotter=cp, iplot=False)
