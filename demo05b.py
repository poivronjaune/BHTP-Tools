import os
import sys
import datetime
import pandas as pd
from bhtp.loader import Loader
import talib as ta
from talib import MA_Type

from bhtp import load_prices_from_csv
from bhtp.loader import Loader

from questdb.ingress import Sender, IngressError

# CREATE QUESTDB TABLE with SYMBOL Datatypes for performance rather than Strings, CAPACITY 256 CACHE is optional
create_table_sql = """
CREATE TABLE prices (
    Symbol SYMBOL CAPACITY 256 CACHE,
    Close DOUBLE,
    High DOUBLE,
    Low DOUBLE,
    Open DOUBLE,
    Volume DOUBLE,
    Datetime TIMESTAMP,
    sourcefile SYMBOL CAPACITY 256 CACHE
) 
TIMESTAMP (Datetime) 
PARTITION BY DAY 
WAL 
DEDUP UPSERT KEYS(Datetime, Symbol);
"""

def normalise_ohlcv_data(df:pd.DataFrame):
    print(f'Before normalisation: {df.columns}')
    #df = df.rename(columns={'Datetime': 'date', 'Symbol': 'symbol', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume' })
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.drop('Adj Close', axis=1)
    
    return df

def insert_data(df):
    conf = f'http::addr=localhost:9000;'

    try:
        with Sender.from_conf(conf) as sender:
            sender.dataframe(
                df,
                table_name='prices',  # Table name to insert into.
                symbols=['Symbol'],  # Columns to be inserted as SYMBOL types.
                at='Datetime')  # Column containing the designated timestamps.
            #sender.flush_and_keep(&mut buffer)
    except IngressError as e:
        print(f'Got error: {e}\n')

def load_multiple_datasets(DRIVE_PATH, DATASETS):
    l = Loader(DRIVE_PATH)
    for folder in DATASETS:
        df = l.load_files_from_folder(folder, verbose=True, source=True)
        #df['Datetime'] = pd.to_datetime(df['Datetime'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
        df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
        if df['Datetime'].dt.tz is None:
            # Localize naive datetime to UTC
            df['Datetime'] = df['Datetime'].dt.tz_localize('UTC')
        else:
            # Convert timezone-aware datetime to UTC
            df['Datetime'] = df['Datetime'].dt.tz_convert('UTC')    

        df.drop('Adj Close', axis=1, inplace=True)

        print(df)
        insert_data(df)

if __name__ == '__main__':
    DRIVE_PATH = os.path.abspath('D:\\stockdata')
    DATASET_FOLDER =  'DATA-2023-03'
    
    # LOAD PRICES FROM A SINGLE FILE
    #SINGLE_FILE = 'amex1-2024-01-04.csv'
    #file1 = os.path.join(DRIVE_PATH, DATASET_FOLDER, SINGLE_FILE)
    #df = load_prices_from_csv(file1)

    # LOAD PRICCES FOR ONLY ONE FOLDER
    #DATASETS = [DATASET_FOLDER]
    #load_multiple_datasets(DRIVE_PATH, DATASETS)

    # LOAD PRICES FOR MULTIPLE DATASETS
    DATASETS = [
                                      'DATA-2023-03','DATA-2023-04','DATA-2023-05','DATA-2023-06',
        'DATA-2023-07','DATA-2023-08','DATA-2023-09','DATA-2023-10','DATA-2023-11','DATA-2023-12',
        'DATA-2024-01','DATA-2024-02','DATA-2024-03','DATA-2024-04','DATA-2024-05','DATA-2024-06',
        'DATA-2024-07','DATA-2024-08','DATA-2024-09','DATA-2024-10','DATA-2024-11','DATA-2024-12']
    load_multiple_datasets(DRIVE_PATH, DATASETS)


