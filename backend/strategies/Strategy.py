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

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            print("Order submitted or accepted")
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def is_crypto_market(self) -> bool:
        return self.params.market == "crypto"

    def compute_position_size(self) -> None:
        amount_to_invest = self.params.order_percentage * self.broker.cash
        if self.is_crypto_market():
            self.size = amount_to_invest / self.data.close
        else:
            # if we are dealing with the stock
            self.size = floor(amount_to_invest / self.data.close)
