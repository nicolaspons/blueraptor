import math
import backtrader as bt
from indicators.SuperTrend import SuperTrend


class SuperTrendStrategy(bt.Strategy):
    params = (
        ("time_period", 14),
        ("movav", bt.indicators.SmoothedMovingAverage),
        ("multiplier", 3),
        ("ticker", "BTCUSDT"),
    )

    def __init__(self) -> None:
        super().__init__()
        self.super_trend = SuperTrend(self.data)

    def next(self):
        if not self.position:
            if self.super_trend.lines.up_trend[0]:
                self.size = math.floor(self.broker.cash / self.data.close)
                print(
                    "Buy {} shares of {} at {}".format(
                        self.broker.cash, self.params.ticker, self.data.close[0]
                    )
                )
                self.buy(size=self.size)

        else:
            if (
                not self.super_trend.lines.up_trend[0]
                and self.super_trend.lines.up_trend[-1]
            ):
                print(
                    "Sell {} shares of {} at {}".format(
                        self.broker.cash, self.params.ticker, self.data.close[0]
                    )
                )
                self.close()
