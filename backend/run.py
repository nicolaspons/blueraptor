import json

from strategies.SuperTrend import SuperTrend
from backtest import Backtest

CASH = 100000
PATH_TO_DATA = "../data"
PATH_TO_SAVE = "./statistics"
STRATEGIES = [("Super Trend", SuperTrend)]


bt = Backtest(
    cash=CASH,
    tikers=["BTCUSDT"],
    intervals=["1d"],
    path_to_data=PATH_TO_DATA,
    path_to_save=PATH_TO_SAVE,
    strategies=STRATEGIES,
)

bt.run()
