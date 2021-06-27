import backtrader as bt


class ST(bt.Indicator):
    """
    SuperTrend indicator
    """

    lines = (
        "upper_band",
        "lower_band",
        "up_trend",
        "basic_upper_band",
        "basic_lower_band",
    )
    plotlines = dict(
        upper_band=dict(_name="Upper band", color="red"),
        basic_upper_band=dict(_name="Upper band", color="grey"),
        basic_lower_band=dict(_name="Lower band", color="grey"),
        lower_band=dict(_name="Lower band", color="green"),
    )
    plotinfo = dict(plot=True, subplot=False)
    params = (
        ("time_period", 14),
        ("movav", bt.indicators.SmoothedMovingAverage),
        ("multiplier", 3),
        ("plot_basic_bands", False),
    )

    def __init__(self) -> None:
        super().__init__()
        self.lines.atr = bt.indicators.ATR(
            self.data, period=self.params.time_period, movav=self.params.movav
        )

        hl2 = (self.data.high + self.data.low) / 2

        self.lines.basic_upper_band = hl2 + (self.params.multiplier * self.lines.atr)
        self.lines.upper_band = hl2 + (self.params.multiplier * self.lines.atr)
        self.lines.basic_lower_band = hl2 - (self.params.multiplier * self.lines.atr)
        self.lines.lower_band = hl2 - (self.params.multiplier * self.lines.atr)

        if not self.params.plot_basic_bands:
            self.plotlines.basic_upper_band._plotskip = True
            self.plotlines.basic_lower_band._plotskip = True

    def next(self):
        if self.data.close[0] > self.lines.upper_band[-1]:
            self.lines.up_trend[0] = True
        elif self.data.close[0] < self.lines.lower_band[-1]:
            self.lines.up_trend[0] = False
        else:
            self.lines.up_trend[0] = self.lines.up_trend[-1]
            if (
                self.lines.up_trend[0]
                and self.lines.lower_band[0] < self.lines.lower_band[-1]
            ):
                self.lines.lower_band[0] = self.lines.lower_band[-1]

            if (
                not self.lines.up_trend[0]
                and self.lines.upper_band[0] > self.lines.upper_band[-1]
            ):
                self.lines.upper_band[0] = self.lines.upper_band[-1]

    def _plotlabel(self):
        plabels = [self.p.time_period, self.p.movav]

        return plabels
