import yfinance as yf
import pandas as pd

def download_minute_data(symbols):
    data = yf.download(symbols, period='1d', interval="1m", ignore_tz=True, prepost=False, threads=True, auto_adjust=True)
    return data

def download_daily_data(symbols, start_dt='2020-01-01', end_dt=None):
    """Download daily data for the given symbols."""
    if end_dt is None:
        data = yf.download(symbols, start=start_dt, interval="1d", ignore_tz=True, prepost=False, threads=True, auto_adjust=True)
    else:
        data = yf.download(symbols, start=start_dt, end=end_dt, interval="1d", ignore_tz=True, prepost=False, threads=True, auto_adjust=True)
    return data
    data = yf.download(symbols, start='2020-01-01', interval="1d", ignore_tz=True, prepost=False, threads=True, auto_adjust=True)


def flatten_dataframe(data):
    """Flatten the multi-index DataFrame returned by yfinance to a single index DataFrame with ticker in column."""
    if data.index.name != 'Datetime':
        data.index.name = 'Datetime'
    data = data.loc[(slice(None)),(slice(None),slice(None))].copy()
    data = data.stack(future_stack=True)
    data = data.reset_index()
    data.rename(columns={'level_1': 'Symbol'}, inplace=True)
    data.rename(columns={'level_0': 'Datetime'}, inplace=True)
    data.set_index('Datetime', inplace=True)
    data.columns.name = None
    return data   


if __name__ == '__main__':
    symbols = ['AAPL', 'GOOGL']
    data = download_minute_data(symbols)
    data = flatten_dataframe(data)
    #data.to_csv('yahoo_data.csv')
    print(data)
    
