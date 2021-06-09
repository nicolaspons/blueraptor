import backtrader as bt
import os

data_path = "../data"
data_file = "daily_test.csv"

cerebro = bt.Cerebro()

data = bt.feeds.GenericCSVData(dataname=os.path.join(data_path, data_file), dtformat=2)

cerebro.adddata(data)

cerebro.run()

cerebro.plot(style="candle", barup="green", bardown="red")
