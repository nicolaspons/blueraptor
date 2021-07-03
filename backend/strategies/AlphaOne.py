import backtrader as bt
from backtrader.indicators import ExponentialMovingAverage, MACD, CrossOver
from .Strategy import Strategy


class AlphaOne(Strategy):
    params = (("name", "AlphaOne"), ("target", 0.99))

    def __init__(self) -> None:
        super().__init__()
        self.sma_15m = ExponentialMovingAverage(self.data1, period=50)
        self.sma_1h = ExponentialMovingAverage(self.data2, period=50)
        self.macd = MACD(self.data)

        self.crossover = CrossOver(self.sma_15m, self.sma_1h)

    def next(self):
        if not self.position:
            if self.crossover > 0 and self.macd > 0:
                self.order_target_percent(target=self.p.target)
