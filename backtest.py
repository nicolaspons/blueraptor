import backtrader as bt
import backtrader as bt

cerebro = bt.Cerebro()

data = bt.feeds.GenericCSVData(dataname="./data/daily_test.csv", dtformat=2)

cerebro.adddata(data)

cerebro.run()

cerebro.plot()
