import backtrader as bt
import math


class GoldenCross(bt.Strategy):
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
      - ``order_percentage``: the percentage of our availabe cash that will be
      used to fill the order
      - ``ticker``: the ticker
    """

    params = (
        ("fast", 50),
        ("slow", 200),
        ("order_percentage", 0.95),
        ("ticker", "BTCUSDT"),
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
                amount_to_invest = self.params.order_percentage * self.broker.cash
                self.size = math.floor(amount_to_invest / self.data.close)

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
