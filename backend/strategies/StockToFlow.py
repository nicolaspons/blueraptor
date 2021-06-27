import backtrader as bt
from .Strategy import Strategy

# Set percent of trailing stop
PERC_TRAIL = 0.40

class StockToFlow(Strategy):
    params = (
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('trailpercent', PERC_TRAIL),
        ('smaperiod', 30),
        ('dirperiod', 10),
    )

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None # No pending orders

    def __init__(self) -> None:
        super().__init__()
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.params.macd1,
                                       period_me2=self.params.macd2,
                                       period_signal=self.params.macdsig)
        
        # Cross of macd.macd and macd.signal
        self.mcoss = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=self.params.smaperiod)
        self.smadir = self.sma - self.sma(-self.params.dirperiod)

    def start(self):
        self.order = None # Avoid operations on pending order

    def next(self):
        if self.order:
            return # Pending order execution

        if not self.position: # Not in the market
            if self.mcross[0] > 0.0 and self.smadir < 0.0 and self.data.close < self.data.stf:
                self.order = self.buy()
                self.order = 'none'
        
        elif self.order is None: # Position in the Market
            self.order = self.sell(exectype=bt.Order.StopTrail,trailpercent=self.params.trailpercent)
            tcheck = self.data.close * (1.0 - self.params.trailpercent)