from binance import Client
from binance.enums import (
    KLINE_INTERVAL_12HOUR,
    KLINE_INTERVAL_15MINUTE,
    KLINE_INTERVAL_1DAY,
    KLINE_INTERVAL_1HOUR,
    KLINE_INTERVAL_1MINUTE,
    KLINE_INTERVAL_1MONTH,
    KLINE_INTERVAL_1WEEK,
    KLINE_INTERVAL_2HOUR,
    KLINE_INTERVAL_30MINUTE,
    KLINE_INTERVAL_3DAY,
    KLINE_INTERVAL_3MINUTE,
    KLINE_INTERVAL_6HOUR,
)


def partition(l, low, high):
    i = low - 1
    pivot = l[high]["free"]

    for j in range(low, high):
        if l[j]["free"] > pivot:
            i += 1
            l[i], l[j] = l[j], l[i]
    i += 1
    l[i], l[high] = l[high], l[i]
    return i


def sort_balances(l):
    quicksort(l, 0, len(l) - 1)


def quicksort(l, low, high):
    if len(l) == 1:
        return l
    if low < high:
        p = partition(l, low, high)
        quicksort(l, low, p - 1)
        quicksort(l, p + 1, high)


intervals = {
    "1 min": Client.KLINE_INTERVAL_1MINUTE,
    "3 min": Client.KLINE_INTERVAL_3MINUTE,
    "5 min": Client.KLINE_INTERVAL_5MINUTE,
    "15 min": Client.KLINE_INTERVAL_15MINUTE,
    "30 min": Client.KLINE_INTERVAL_30MINUTE,
    "1 hour": Client.KLINE_INTERVAL_1HOUR,
    "2 hour": Client.KLINE_INTERVAL_2HOUR,
    "4 hour": Client.KLINE_INTERVAL_4HOUR,
    "6 hour": Client.KLINE_INTERVAL_6HOUR,
    "8 hour": Client.KLINE_INTERVAL_8HOUR,
    "12 hour": Client.KLINE_INTERVAL_12HOUR,
    "1 day": Client.KLINE_INTERVAL_1DAY,
    "3 day": Client.KLINE_INTERVAL_3DAY,
    "1 week": Client.KLINE_INTERVAL_1WEEK,
    "1 month": Client.KLINE_INTERVAL_1MONTH,
}
