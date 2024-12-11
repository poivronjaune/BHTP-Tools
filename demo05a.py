import os
import sys
import pandas as pd
import talib as ta
from talib import MA_Type

from bhtp.loader import Loader

def calculate_indicators(df):
    inputs = {}
    df['SMA5'] = ta.SMA(df['Close'], timeperiod=5)
    df['SMA9'] = ta.SMA(df['Close'], timeperiod=9)
    df['SMA25'] = ta.SMA(df['Close'], timeperiod=25)
    df['SMA50'] = ta.SMA(df['Close'], timeperiod=50)
    df['SMA100'] = ta.SMA(df['Close'], timeperiod=100)
    df['SMA200'] = ta.SMA(df['Close'], timeperiod=200)
    df['upper'], df['middle'], df['lower'] = ta.BBANDS(df['Close'], matype=MA_Type.T3)
    df['MSTAR'] = ta.CDLMORNINGSTAR(df['Open'], df['High'], df['Low'], df['Close'])
    return df

def add_indicators(df:pd.DataFrame):
    # Group data by symbol to apply the indicators calculation
    df = df.groupby('Symbol', group_keys=False).apply(calculate_indicators)     # include_groups=False      
    return df

def save_data_to_csv(df, last_date_saved, output):
    os.makedirs(output, exist_ok=True)
    save_file = os.path.join(output, 'saved_data.csv')
    write_header = not os.path.exists(save_file)
    if last_date_saved is None:
        df.to_csv(save_file, mode='a', header=write_header)  
    else:
        df[df.index >= last_date_saved].to_csv(save_file, mode='a', header=write_header)  
    last_date = df.index.max()
    return last_date_saved


def normalise_ohlcv_data(df:pd.DataFrame):
    print(f'Before normalisation: {df.columns}')
    #df = df.rename(columns={'Datetime': 'date', 'Symbol': 'symbol', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume' })
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.drop('Adj Close', axis=1)
    
    
    df.set_index('Datetime', inplace=True)
    try:
        df.index = df.index.tz_localize('UTC')
    except:
        df.index = df.index.tz_convert('UTC')
    print(f'After normalisation: {df.columns}')
    print('===========================================================')
    return df


def main2(params, verbose:bool = True):
    drive = params.get('input')
    folder = params.get('dataset')
    selected_files = params.get('files')
    selected_files_count = len(selected_files)
    output = params.get('output')
    min_data_required = params.get('chunks')

    # Choose files to load or all files
    l = Loader(root_path=drive)
    files_in_folder = l.list_files_in_folder(folder_path=folder)
    if selected_files_count < 1:
        selected_files = files_in_folder
        selected_files_count = len(selected_files)

    # Loop thourgh selected_files and handle data 
    data_df = pd.DataFrame()
    min_date_loaded = None
    for idx, file in enumerate(selected_files):
        if file in files_in_folder:
            loaded_df = l.load_one_file_from_folder(folder, file)
            if verbose:
                print(f'{idx+1:2} /{selected_files_count:2} -> Loaded "{file}" data file ({len(loaded_df)} records found)')  
            loaded_df = normalise_ohlcv_data(loaded_df)
            if min_date_loaded is None:
                min_date_loaded = loaded_df.index.min()
        else:
            if verbose:
                print(f'{idx+1:2} /{selected_files_count:2} -> Not found "{file}" in folder {params.get('data_folder')}')

        data_df = pd.concat([data_df, loaded_df])
        unique_dates = data_df.index.unique().sort_values(ascending=True)
        unique_symbols = data_df.Symbol.unique()
        print(f'Unique dates: {len(unique_dates)}, Unique symbols: {len(unique_symbols)}')
        if len(unique_dates) > min_data_required:
            print('----> Now we can add our indicators....')
            print(f'Smallest Datetime: {min(unique_dates)}, Largets Datetime: {max(unique_dates)} - Min loaded date: {min_date_loaded}')
            data_df = add_indicators(data_df, min_date_loaded, output)
            min_date_loaded = None
            # Purge older dates in our data_df  
        else:
            print('----> Oops we need add more data before our indicators can be added....')
            print(f'Smallest Datetime: {min(unique_dates)}, Largets Datetime: {max(unique_dates)} - Min loaded date: {min_date_loaded}')
        
        #input(f'min_date_loaded : {min_date_loaded}   ------ ENTER to continue...')

def main(params, verbose:bool = True):
    drive = params.get('input')
    folders = params.get('dataset')
    selected_files = params.get('files')
    selected_files_count = len(selected_files)
    output = params.get('output')
    min_data_required = params.get('chunks')

    # Choose files to load or all files
    l = Loader(root_path=drive)
    
    data_df = pd.DataFrame()
    min_date_loaded = None
    last_date_saved = None
    # Get the last date saved in the output if it exists and set it as last_date_saved, but load data_df with the min_data_required dates
    # Investigate how to load the x lines of a CSV file in a DataFrame
    for folder in folders:
        # Open dataset folder and select files to load
        files_in_folder = l.list_files_in_folder(folder_path=folder)
        if selected_files_count < 1:
            selected_files = files_in_folder
            selected_files_count = len(selected_files)

        # Loop through selected_files and handle data 
        for idx, file in enumerate(selected_files):
            if file in files_in_folder:
                loaded_df = l.load_one_file_from_folder(folder, file)
                if verbose:
                    print(f'{idx+1:2} /{selected_files_count:2} -> Loaded "{file}" data file ({len(loaded_df)} records found)')  
                loaded_df = normalise_ohlcv_data(loaded_df)
                if min_date_loaded is None:
                    min_date_loaded = loaded_df.index.min()
            else:
                if verbose:
                    print(f'{idx+1:2} /{selected_files_count:2} -> Not found "{file}" in folder {params.get('data_folder')}')

            # Data for one file was loaded, now append to our total data_df
            data_df = pd.concat([data_df, loaded_df])
            unique_dates = data_df.index.unique().sort_values(ascending=True)
            unique_symbols = data_df.Symbol.unique()
            print(f'Unique dates: {len(unique_dates)}, Unique symbols: {len(unique_symbols)}')
            
            # If total data_df has enough rows to calculate indicators do it, or loop to next file to load
            if len(unique_dates) > min_data_required:
                print('----> Now we can add our indicators....')
                print(f'Smallest Datetime: {min(unique_dates)}, Largets Datetime: {max(unique_dates)} - Min loaded date: {min_date_loaded}')
                data_df = add_indicators(data_df) # Add indicators, save to csv and purge old data
                last_date_saved = save_data_to_csv(data_df, last_date_saved, output)
                min_date_loaded = None
                min_date_required = unique_dates[-min_data_required]
                data_df = data_df[data_df.index >= min_date_required]
            else:
                print('----> Oops we need add more data before our indicators can be added....')
                print(f'Smallest Datetime: {min(unique_dates)}, Largets Datetime: {max(unique_dates)} - Min loaded date: {min_date_loaded}')
            
              

if __name__ == '__main__':
    # params = {
    #     #"input": "D:\\stockdata",
    #     "input": "D:\\stocks_tmp",
    #     "output": "D:\\stockdata_output\\minute",
    #     #"dataset": "DATA-2023-11",
    #     #"files": ["NASDAQ-BM0-2023-11-01.csv", "NASDAQ-BM0-2023-11-02.csv", "NASDAQ-BM0-2023-11-03.csv"],  # [] load all files
    #     #"dataset": "DATA-2023-03",
    #     #"files": ["NASDAQ-TE0-2023-03-06.csv", "NASDAQ-TE0-2023-03-07.csv", "NASDAQ-TE0-2023-03-08.csv"],  # [] load all files
    #     "dataset": "DATA-2024-08",
    #     "files": [],
    #     #"chunks": 500 # Number of unique Datetime values to load before processing dataset, make this big enough for lookback windows used in indicators
    #     "chunks": 220
    # }


    params = {
        "input": "D:\\stockdata",
        "output": "D:\\stockdata_output\\minute",
        "dataset": ["DATA-2024-08"],
        "files": [],
        "chunks": 220
    }
    main(params, verbose=False)

