import backtrader as bt
from indicators.SuperTrend import SuperTrend
from .Strategy import Strategy


class SuperTrend(Strategy):
    params = (
        ("name", "Super Trend"),
        ("time_period", 14),
        ("movav", bt.indicators.SmoothedMovingAverage),
        ("multiplier", 3),
    )

    def __init__(self) -> None:
        super().__init__()
        self.super_trend = SuperTrend(self.data)

    def next(self):
        if not self.position:
            if self.super_trend.lines.up_trend[0]:
                self.compute_position_size()
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
