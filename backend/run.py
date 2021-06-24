import json

from strategies.SuperTrendStrategy import SuperTrendStrategy
from backtest import Backtest

CASH = 1000
PATH_TO_DATA = "../data"
PATH_TO_SAVE = "./statistics"
STRATEGIES = [("Super Trend", SuperTrendStrategy)]


bt = Backtest(
    cash=CASH,
    tikers=["BTCUSDT"],
    intervals=["1D"],
    path_to_data=PATH_TO_DATA,
    path_to_save=PATH_TO_SAVE,
    strategies=STRATEGIES,
)

bt.run()
