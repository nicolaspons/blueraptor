import backtrader as bt
import math

from .Strategy import Strategy


class GoldenCross(Strategy):
    """
    The golden cross is a chart pattern that is a bullish signal in which a
    relatively short-term moving average crosses above a long-term moving
    average. The golden cross is a bullish breakout pattern formed from a
    crossover involving a security's short-term moving average (such as the
    15-day moving average) breaking above its long-term moving average
    such as the 50-day moving average) or resistance level. As long-term
    indicators carry more weight, the golden cross indicates a bull market on
    the horizon and is reinforced by high trading volumes.

    See:
        https://www.investopedia.com/terms/g/goldencross.asp

    Params

      - ``fast``, ``slow``: for the MovingAverages
    """

    params = (
        ("name", "Golden Cross"),
        ("fast", 50),
        ("slow", 200),
    )

    def __init__(self) -> None:
        super().__init__()
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close,
            period=self.params.fast,
            plotname="{} day moving average".format(self.params.fast),
        )

        self.slow_moving_average = bt.indicators.SMA(
            self.data.close,
            period=self.params.slow,
            plotname="{} day moving average".format(self.params.slow),
        )

        self.crossover = bt.indicators.CrossOver(
            self.fast_moving_average, self.slow_moving_average
        )

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                self.compute_position_size()
                print(
                    "Buy {} shares of {} at {}".format(
                        self.size, self.params.ticker, self.data.close[0]
                    )
                )
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossover < 0:
                print(
                    "Sell {} shares of {} at {}".format(
                        self.size, self.params.ticker, self.data.close[0]
                    )
                )
                self.close()
