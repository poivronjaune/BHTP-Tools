import pandas as pd
import numpy as np

from bhtp.symbols import nasdaq1_symbols
from bhtp.data import get_github_file_links, get_github_data, get_yahoo_data, get_local_data
from bhtp.indicators import add_indicators
from bhtp.strategies import add_strategy_02

def detect_signals_pattern_01(data):
    '''Extract all unique symbols from Dataset and loop through each symbol to add indicators and buy signals.
    add_strategy_xx will add condition columns to produce a buySignal column that will True.
    Output:
    data_extended.csv: contains all pandas column added to analyse the strategy
    signals.csv: contains all buy signals detected by strategy code
    '''
    buy_signal = pd.DataFrame()
    data_extended = pd.DataFrame()

    symbols = data['Symbol'].unique()
    for idx, symbol in enumerate(symbols):
      df = data[data['Symbol'] == symbol].copy()
      print(f'{idx+1:3}/{len(symbols):3} : {symbol:9} {df.index.min()} to {df.index.max()} {len(df):6} rows of data')
      df = add_indicators(df)
      df = add_strategy_02(df)
      if df.empty:
        continue
      signals = df[df['BuySignal']]
      buy_signal = pd.concat([buy_signal, signals])
      buy_signal.sort_index(inplace=True)
      data_extended = pd.concat([data_extended, df])
      del(df)
      del(signals)

    data_extended.sort_index(inplace=True)
    return buy_signal, data_extended

if __name__ == '__main__':
    '''Load all available daily data available on a local disk for analysis'''
    #symbols = nasdaq1_symbols
    #data = get_yahoo_data(symbols)
    #data.to_csv('nasdaq1.csv', sep=',', encoding='utf-8')

    files = [
      'D:/stockdata_daily/daily_tsx.csv',
      'D:/stockdata_daily/daily_nasdaq1.csv',
      'D:/stockdata_daily/daily_nasdaq2.csv',
      'D:/stockdata_daily/daily_nasdaq3.csv',
      'D:/stockdata_daily/daily_nasdaq4.csv',
      'D:/stockdata_daily/daily_nasdaq5.csv'
    ]
    much_data = pd.DataFrame()

    for file_name in files:
      print(f'******* LOADING FILE : {file_name} *************')
      data = get_local_data(file_name)
      much_data = pd.concat([much_data, data])


    signals, ext_data = detect_signals_pattern_01(much_data)
    signals.to_csv('signals.csv')
    ext_data.to_csv('data_extented.csv')


