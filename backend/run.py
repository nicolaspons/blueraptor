import json

from strategies.SuperTrendStrategy import SuperTrendStrategy
from .backtest import Backtest
from .utils import INTERVALS

CASH = 1000
with open("../ticker.txt", "r") as f:
    TICKERS = json.load(f)
PATH_TO_DATA = "../data"
PATH_TO_SAVE = "../backtesting"
STRATEGIES = [("Super Trend", SuperTrendStrategy)]


bt = Backtest(
    cash=CASH,
    tikers=["BTCUSDT"],
    intervals=INTERVALS,
    path_to_data=PATH_TO_DATA,
    path_to_save=PATH_TO_SAVE,
    strategies=STRATEGIES,
)

bt.run()
