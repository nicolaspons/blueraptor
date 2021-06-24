from backtrader import Strategy
from math import floor


class Strategy(Strategy):
    """
    Strategy template use to specify the market type.

    Params

      - ``name``: the strategy name
      - ``market``: the market type
      - ``order_percentage``: the percentage of our availabe cash that will be
      used to fill the order
      - ``ticker``: the ticker
    """

    params = (
        ("name", ""),
        ("market", "crypto"),
        ("order_percentage", 1),
        ("ticker", "")
    )

    def is_crypto_market(self) -> bool:
        return self.params.market == "crypto"

    def compute_position_size(self) -> None:
        amount_to_invest = self.params.order_percentage * self.broker.cash
        if self.is_crypto_market():
            self.size = amount_to_invest / self.data.close
        else:
            # if we are dealing with the stock
            self.size = floor(amount_to_invest / self.data.close)
