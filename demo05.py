from genericpath import isdir
import pandas as pd
import talib
import os
from glob import glob

def calculate_indicators(df):
    """Calculate indicators for a single DataFrame."""
    df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)  # 20-period SMA
    df['RSI_14'] = talib.RSI(df['Close'], timeperiod=14)  # 14-period RSI
    df['BB_upper'], df['BB_middle'], df['BB_lower'] = talib.BBANDS(
        df['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
    )
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(
        df['Close'], fastperiod=12, slowperiod=26, signalperiod=9
    )
    return df

#def calculate_indicators(group):
#    min_len = 100
#    if len(group) >= min_len:  # Check if the group has enough data (e.g., 5 rows)
#        return ta.add_all_ta_features(group, 
#                                      open="Open", 
#                                      high="High", 
#                                      low="Low", 
#                                      close="Close", 
#                                      volume="Volume", 
#                                      fillna=True)
#    else:
#        # If the group is too small, return the group unchanged
#        return group

def process_month(folder_path, buffer=None):
    """Process all files in a folder and return the processed data."""
    all_files = sorted(glob(os.path.join(folder_path, "*.csv")))  # Ensure files are processed in order
    dfs = []

    # Load and concatenate files for the month
    for idx, file in enumerate(all_files):
        print(f"Processing file ({idx+1:2}/{len(all_files):2})  : {file}")
        df = pd.read_csv(file)
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df.set_index('Datetime', inplace=True)
        dfs.append(df)
    
    month_data = pd.concat(dfs)
    
    # Include the buffer from the previous month
    if buffer is not None:
        month_data = pd.concat([buffer, month_data])

    # Group by Symbol and calculate indicators
    month_data = month_data.groupby('Symbol', group_keys=False).apply(calculate_indicators)

    # Extract the new buffer (last 30 days of data)
    buffer = month_data[month_data.index >= (month_data.index.max() - pd.Timedelta(days=30))]
    
    return month_data, buffer

def process_year(base_folder, output_folder):
    """Process all months in a year, ensuring continuity between months."""
    months = sorted(glob(os.path.join(base_folder, "DATA-2023-*")))
    buffer = None

    for idx, month_folder in enumerate(months[0:1]):
        if os.path.isdir(os.path.join(base_folder, month_folder)):
            print(f"Processing ({idx+1:2}/{len(months):2}) : {month_folder}...")
            
            # Process the month
            processed_data, buffer = process_month(month_folder, buffer)
    
            # Save the processed data excluding the buffer rows
            save_path = os.path.join(output_folder, os.path.basename(month_folder) + ".csv")
            processed_data_to_save = processed_data.loc[processed_data.index < buffer.index.min()]
            processed_data_to_save.to_csv(save_path)
    
            print(f"Saved processed data to {save_path}")
        else:
            print(f"Processing ({idx:2}/{len(months):2}) : {month_folder}...")

# Example usage
base_folder = "D:\\stockdata"  # Folder containing DATA-2023-03, etc.
output_folder = "D:\\stockdata_output"
os.makedirs(output_folder, exist_ok=True)

process_year(base_folder, output_folder)
