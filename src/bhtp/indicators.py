import talib
from talib import abstract
from talib.abstract import *

#sma = abstract.Function('sma')

def add_indicators(df, short=20, medium=50, long=200):
    df['SMA_Short'] = talib.SMA(df['Close'], timeperiod=short)
    df['SMA_Medium'] = talib.SMA(df['Close'], timeperiod=medium)
    df['SMA_Long'] = talib.SMA(df['Close'], timeperiod=long)
    df['RSI'] = talib.RSI(df['Close'])
    

    return df