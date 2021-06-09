import pandas as pd


def three_line_strike(data: pd.DataFrame, index: int) -> bool:
    """Return True if the data match the three line strike pattern."""

    if index < 3:
        return False

    candles = data.iloc[index - 3 : index + 1]

    return (
        candles.iloc[0]["Close"] > candles.iloc[1]["Close"]
        and candles.iloc[1]["Close"] > candles.iloc[2]["Close"]
        and candles.iloc[2]["Close"] > candles.iloc[3]["Open"]
        and candles.iloc[3]["Close"] > candles.iloc[0]["High"]
    )
