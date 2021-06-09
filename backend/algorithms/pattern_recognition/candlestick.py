import pandas as pd
from ..tools import is_top, is_black_candle, is_gap, is_lower_lows, is_white_candle


def three_line_strike(data: pd.DataFrame, index: int) -> bool:
    """Return True if the data match the three line strike pattern.

    The bullish three line strike reversal pattern carves out three black
    candles within a downtrend. Each bar posts a lower low and closes near the
    intrabar low. The fourth bar opens even lower but reverses in a wide-range
    outside bar that closes above the high of the first candle in the series.
    The opening print also marks the low of the fourth bar. According to
    Bulkowski, this reversal predicts higher prices with an 83% accuracy rate.
    """

    if index < 3:
        return False

    return (
        is_lower_lows(data, starting_index=index - 3, ending_index=index)
        and is_black_candle(data, index - 3)
        and is_black_candle(data, index - 2)
        and is_black_candle(data, index - 1)
        and is_white_candle(data, index)
        and data.iloc[index - 1]["Close"] > data.iloc[index]["Open"]
        and data.iloc[index]["Close"] > data.iloc[index - 3]["High"]
        and data.iloc[index]["Open"] == data.iloc[index]["Low"]
    )


def three_line_strike_simplified(data: pd.DataFrame, index: int) -> bool:
    """Return True if the data match the three line strike pattern.

    The bullish three line strike reversal pattern carves out three black
    candles within a downtrend. Each bar posts a lower low and closes near the
    intrabar low. The fourth bar opens even lower but reverses in a wide-range
    outside bar that closes above the high of the first candle in the series.
    The opening print also marks the low of the fourth bar. According to
    Bulkowski, this reversal predicts higher prices with an 83% accuracy rate.
    """

    if index < 3:
        return False

    return (
        is_lower_lows(data, starting_index=index - 3, ending_index=index)
        and is_black_candle(data, index - 3)
        and is_black_candle(data, index - 2)
        and is_black_candle(data, index - 1)
        and is_white_candle(data, index)
        and data.iloc[index]["Close"] > data.iloc[index - 3]["High"]
    )


def two_black_gapping(data: pd.DataFrame, index: int) -> bool:
    """Return True if the data match the three line strike pattern.

    The bearish two black gapping continuation pattern appears after a notable
    top in an uptrend, with a gap down that yields two black bars posting lower
    lows. This pattern predicts that the decline will continue to even lower
    lows, perhaps triggering a broader-scale downtrend. According to Bulkowski,
    this pattern predicts lower prices with a 68% accuracy rate.
    """

    if index < 3:
        return False

    return (
        is_top(data, index - 3, "Close", period=7)
        and is_black_candle(data, index - 2)
        and is_black_candle(data, index - 1)
        and is_black_candle(data, index)
        and is_gap(data, index - 1)
        and is_lower_lows(data, starting_index=index - 1, ending_index=index)
    )


def two_black_gapping_simplified(data: pd.DataFrame, index: int) -> bool:
    """Return True if the data match the three line strike pattern.

    The bearish two black gapping continuation pattern appears after a notable
    top in an uptrend, with a gap down that yields two black bars posting lower
    lows. This pattern predicts that the decline will continue to even lower
    lows, perhaps triggering a broader-scale downtrend. According to Bulkowski,
    this pattern predicts lower prices with a 68% accuracy rate.
    """

    if index < 3:
        return False

    return (
        is_top(data, index - 3, "Close", period=7)
        and is_black_candle(data, index - 2)
        and is_black_candle(data, index - 1)
        and is_black_candle(data, index)
        and is_lower_lows(data, starting_index=index - 1, ending_index=index)
    )
