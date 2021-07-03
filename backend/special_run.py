from datetime import datetime
import pandas as pd
import backtrader as bt
from pandas.core.indexes import interval
from strategies.SuperTrend import SuperTrend
from backtest import CommInfoFractional


cerebro = bt.Cerebro()

cerebro.broker.setcash(1000)

cerebro.broker.setcommission = 0.00075

cerebro.addstrategy(SuperTrend)

cerebro.addanalyzer(bt.analyzers.PyFolio, _name="pyfolio")

cerebro.broker.addcommissioninfo(CommInfoFractional(commission=0.00075))

for interval in ["1d"]:
    df = pd.read_csv(f"../data/{interval}/BTCUSDT.csv", index_col=False)
    df["Open time"] = pd.to_datetime(df["Open time"], unit="s")

    data = bt.feeds.PandasData(
        dataname=df, datetime="Open time", open=1, high=2, low=3, close=4, volume=5
    )

    cerebro.adddata(data)

cerebro.run()
cerebro.plot(iplot=False)
