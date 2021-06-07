import talib
from numpy import genfromtxt

data = genfromtxt("15minutes.csv", delimiter=",")

close = data[:, 4]

rsi = talib.RSI(close)

print(rsi)
