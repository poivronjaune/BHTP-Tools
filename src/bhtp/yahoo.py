import yfinance as yf
import pandas as pd


def flatten_yahoo_data(data):
    """Flatten the multi-index DataFrame returned by yfinance to a single index DataFrame with ticker in column."""
    data = data.loc[(slice(None)),(slice(None),slice(None))].copy()
    data = data.stack()
    data = data.reset_index()
    data.rename(columns={'level_1': 'Symbol'}, inplace=True)
    data.rename(columns={'level_0': 'Datetime'}, inplace=True)
    data.set_index('Datetime', inplace=True)
    data.columns.name = None
    return data   


if __name__ == '__main__':
    symbols = ['AAPL', 'GOOGL']
    data = yf.download(symbols, period='1d', interval="1m", ignore_tz = True, prepost=False, threads=True, auto_adjust=True)
    data = flatten_yahoo_data(data)
    #data.to_csv('yahoo_data.csv')
    print(data)
    
