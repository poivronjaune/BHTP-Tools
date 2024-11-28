import pandas as pd
import ta

class Indicators:
    def __init__(self):
        self.msg = 'Instantiaed'
        pass

    


# # Sample OHLCV DataFrame
# data = {
#     "timestamp": [
#         "2024-11-20 10:00:00", "2024-11-20 10:01:00", "2024-11-20 10:02:00",
#         "2024-11-20 10:03:00", "2024-11-20 10:04:00"
#     ],
#     "open": [100, 101, 102, 103, 104],
#     "high": [101, 102, 103, 104, 105],
#     "low": [99, 100, 101, 102, 103],
#     "close": [100.5, 101.5, 102.5, 103.5, 104.5],
#     "volume": [200, 210, 220, 230, 240]
# }

# df = pd.DataFrame(data)
# df["timestamp"] = pd.to_datetime(df["timestamp"])
# df.set_index("timestamp", inplace=True)

# # Calculate Indicators
# # Add a Simple Moving Average (SMA)
# df["SMA_3"] = ta.sma(df["close"], length=3)

# # Add Relative Strength Index (RSI)
# df["RSI_14"] = ta.rsi(df["close"], length=14)

# # Add Moving Average Convergence Divergence (MACD)
# macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
# df = pd.concat([df, macd], axis=1)

# # Display the DataFrame with indicators
# print(df)

if __name__ == '__main__':
    pass