import pandas as pd
import ta
# possible migration to : https://github.com/TA-Lib/ta-lib-python

class Indicators:
    def __init__(self):
        pass
   


def test():
    # Sample OHLCV DataFrame
    data = {
        "open": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        "high": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        "low": [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
        "close": [100.5, 101.5, 102.5, 103.5, 104.5, 105.5, 106.5, 107.5, 108.5, 109.5],
        "volume": [200, 210, 220, 230, 240, 250, 260, 270, 280, 290]
    }

    df = pd.DataFrame(data)

    # Calculate technical indicators with adjusted periods
    df['macd'] = ta.trend.macd(df['close'], window_slow=5, window_fast=3)  # Adjust MACD lookback to 5 and 3
    df['rsi'] = ta.momentum.rsi(df['close'], window=5)  # Adjust RSI lookback to 5
    df['ema'] = ta.trend.ema_indicator(df['close'], window=5)  # Adjust EMA lookback to 5
    df['bollinger_hband'] = ta.volatility.bollinger_hband(df['close'], window=5)  # Adjust Bollinger Bands to 5
    df['bollinger_lband'] = ta.volatility.bollinger_lband(df['close'], window=5)  # Adjust Bollinger Bands to 5

    # Print the DataFrame with indicators
    print(df)

def test2():
    # Load your CSV file into a pandas DataFrame
    df = pd.read_csv('tests/test_data.csv')

    # Ensure the datetime column is parsed as datetime
    df['Datetime'] = pd.to_datetime(df['Datetime'])

    # Sort by datetime to ensure correct order for SMA calculation
    df = df.sort_values(by=['Symbol', 'Datetime'])

    # Calculate SMA50 for each symbol group
    df['SMA50'] = df.groupby('Symbol')['Close'].transform(lambda x: ta.trend.sma_indicator(x, window=50))

    # Show the resulting DataFrame
    print(df.tail(50))

def apply_ta_to_group(group):
    min_len = 100
    if len(group) >= min_len:  # Check if the group has enough data (e.g., 5 rows)
        return ta.add_all_ta_features(group, 
                                      open="Open", 
                                      high="High", 
                                      low="Low", 
                                      close="Close", 
                                      volume="Volume", 
                                      fillna=True)
    else:
        # If the group is too small, return the group unchanged
        return group


def test3():
    # Load your CSV file into a pandas DataFrame
    df = pd.read_csv('tests/test_data.csv')

    # Ensure the datetime column is parsed as datetime
    df['Datetime'] = pd.to_datetime(df['Datetime'])

    # Sort by datetime to ensure correct order for indicators calculation
    df = df.sort_values(by=['Symbol', 'Datetime'])

    # Calculate multiple indicators (e.g., SMA50, EMA, RSI, etc.) for each symbol
    # Use `add_all_ta_features` to calculate multiple indicators at once

    df = df.groupby('Symbol').apply(apply_ta_to_group)

    # Show the resulting DataFrame with multiple indicators
    print(df)
    print('==============================================')
    print(df.columns.to_list())
    

if __name__ == '__main__':
    test3()