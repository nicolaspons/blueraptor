import backtrader as bt
from backtrader.indicators import MACD, CrossOver
from indicators.SuperTrend import ST
from .Strategy import Strategy


class SuperTrend(Strategy):
    params = (
        ("name", "Super Trend"),
        ("time_period", 14),
        ("movav", bt.indicators.SmoothedMovingAverage),
        ("multiplier", 3),
        ("target", 0.99),
        ("notifytrade", "True"),
    )

    def __init__(self) -> None:
        super().__init__()
        self.super_trend = ST(self.data)
        self.macd = MACD(self.data)
        self.crossover = CrossOver(self.macd.signal, self.macd.macd)

    def next(self):
        if not self.position:
            if self.super_trend.lines.up_trend[0]:
                self.order_target_percent(target=self.p.target)

        else:
            if (
                not self.super_trend.lines.up_trend[0]
                and self.super_trend.lines.up_trend[-1]
            ):
                self.close()
                # If you go short
                # self.order_target_percent(target=-self.p.target)
            elif self.crossover > 0:
                self.close()
