import backtrader as bt
from indicators.SuperTrend import ST
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
        self.super_trend = ST(self.data)

    def next(self):
        if not self.position:
            if self.super_trend.lines.up_trend[0]:
                self.buy()

        elif (
                not self.super_trend.lines.up_trend[0]
                and self.super_trend.lines.up_trend[-1]
        ):
            self.close()
