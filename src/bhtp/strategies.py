import pandas as pd
import numpy as np

def add_strategy_01(df):
    # Make sur indicators are available in dataset
    if ('SMA_Short' not in df.columns) or ('SMA_Medium' not in df.columns) or ('SMA_Long' not in df.columns):
        return pd.DataFrame()

    df['BodySize'] = (df['Close'] - df['Open']).abs()
    df['BodyAvg'] = df['BodySize'].rolling(window=20).mean()
    df['SMAAligned'] = np.where((df['SMA_Long'] > df['SMA_Medium'] ) & (df['SMA_Medium'] > df['SMA_Short']),True,False)    

    # Body is larger than 3 times the average & green candle
    df['Ignite'] = np.where((df['BodySize'] >= df['BodyAvg'] * 3) & (df['Close'] > df['Open']), True, False)
    df['IgniteBelowShortSMA'] = np.where((df['Ignite']) & (df['Close'] < df['SMA_Short']), True, False)
    df['Pullback'] = np.where(
        (df['Close'] < df['Open']) &
        df['Ignite'].shift(1) &
        (df['BodySize'] < (df['BodySize'].shift(1) * 1/3)) &
        (df['High'] > df['Close'].shift(1)) &
        (df['Low'] < df['Close'].shift(1)), True, False)
    df['Confirm'] = np.where(
        (df['Close'] > df['Open']) &
        (df['Pullback'].shift(1)) &
        (df['BodySize'] > (df['BodySize'].shift(2) * 1/3) ) &
        (df['Open'] > df['Close'].shift(1)),True,False)

    
    df['BuySignal'] = np.where(
        df['Ignite'].shift(2) & 
        df['Pullback'].shift(1) & 
        df['Confirm'] & 
        df['SMAAligned'].shift(2) & 
        df['IgniteBelowShortSMA'].shift(2), True, False)

    return df

def add_strategy_02(df):
    # Make sur indicators are available in dataset
    if ('SMA_Short' not in df.columns) or ('SMA_Medium' not in df.columns) or ('SMA_Long' not in df.columns):
        return pd.DataFrame()

    df['BodySize'] = (df['Close'] - df['Open']).abs()
    df['BodyAvg'] = df['BodySize'].rolling(window=20).mean()

    # Body is larger than 3 times the average & green candle
    df['Ignite'] = np.where((df['BodySize'] >= df['BodyAvg'] * 3) & (df['Close'] > df['Open']), True, False)
    df['Pullback'] = np.where(
        (df['Close'] < df['Open']) &
        df['Ignite'].shift(1) &
        (df['BodySize'] < (df['BodySize'].shift(1) * 1/3)) &
        (df['High'] > df['Close'].shift(1)) &
        (df['Low'] < df['Close'].shift(1)), True, False)
    df['Confirm'] = np.where(
        (df['Close'] > df['Open']) &
        (df['Pullback'].shift(1)) &
        (df['BodySize'] > (df['BodySize'].shift(2) * 1/3) ) &
        (df['Open'] > df['Close'].shift(1)),True,False)

    
    df['BuySignal'] = np.where(
        df['Ignite'].shift(2) & 
        df['Pullback'].shift(1) & 
        df['Confirm'], True, False)

    return df
