import pandas as pd


def is_top(data: pd.DataFrame, index: int, column_name: str, period: int = 10) -> bool:
    """Return True if the data at the index 'index' is the highest value in the
    last 'period' period.
    """

    if index <= 0 or index >= data.shape[0]:
        return False

    starting_index = max(0, index - period)

    return data.iloc[starting_index : index + 1][column_name].idxmax() == index


def is_black_candle(data: pd.DataFrame, index: int) -> bool:
    """Return True if the candle is a black candle.

    (e.g. the open price is higher than the close price)
    """

    return data.iloc[index]["Open"] > data.iloc[index]["Close"]


def is_white_candle(data: pd.DataFrame, index: int) -> bool:
    """Return True if the candle is a white candle.

    (e.g. the open price is lower than the close price)
    """

    return not is_black_candle(data, index)


def is_gap(data: pd.DataFrame, index: int) -> bool:
    """Return True if there is a gap between the candles at the index index and
    the previous one.
    """

    if index == 0:
        return False

    return (
        data.iloc[index - 1]["Low"] > data.iloc[index]["High"]
        or data.iloc[index - 1]["High"] < data.iloc[index]["Low"]
    )


def is_lower_lows(data: pd.DataFrame, starting_index: int, ending_index: int) -> bool:
    """Return True if the consecutive candles are posting lower lows."""

    if starting_index > ending_index:
        raise ValueError("starting_index must be lower than ending_index")

    if starting_index < 0 or ending_index < 0:
        raise ValueError(
            "starting_index and ending_index \
            must be greater than 0"
        )

    for i in range(starting_index, ending_index - 1):
        if data.iloc[i]["Low"] < data.iloc[i + 1]["Low"]:
            return False
    return True
