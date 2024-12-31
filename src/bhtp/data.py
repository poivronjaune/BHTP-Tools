import re
import requests
import pandas as pd
import yfinance as yf

def get_github_data(github_raw_link):
    try:
        data = pd.read_csv(github_raw_link)
    except Exception as e:
        raise RuntimeError(f'Unable to read target file, {e}')
    
    required_columns = ['Datetime','Open','High','Low','Close','Adj Close','Volume']
    all_columns_present = all(column in data.columns for column in required_columns)
    if not all_columns_present:
        raise RuntimeError(f'CSV file loaded is missing one or more of the following columns {required_columns}.')
    if not ('Symbol' in data.columns or 'Ticker' in data.columns):
        raise RuntimeError(f'CSV file loaded is missing one or more of the following columns Symbol or Ticker.')
    if 'Ticker' in data.columns:
        data = data.rename(columns={"Ticker": "Symbol"})

    #data = data[['Datetime','Symbol', 'Open','High','Low','Close','Adj Close','Volume']]
    data = data[['Datetime','Symbol', 'Open','High','Low','Close','Volume']]
    data.set_index('Datetime', inplace=True)
    return data

def get_github_file_links(owner, repo, folder, starts_with=''):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/'

    if folder == '/' or folder == '' or folder is None or not isinstance(folder, str):
        folder = ''
    url = url + folder
    content = requests.get(url, timeout=30)
    list_of_json_objects = content.json()

    if starts_with == '' or starts_with is None:
        raw_urls = [record['download_url'] for record in list_of_json_objects if record['type'] == 'file']
    else:
        pattern = pattern = r"^" + starts_with + r".*\.csv$"
        raw_urls = [record['download_url'] for record in list_of_json_objects if record['type'] == 'file' and re.match(pattern, record['name'])]

    return raw_urls

def get_yahoo_data(symbols):
    try:
        data = yf.download(symbols, period='max', interval="1d", ignore_tz = True, prepost=False)
    except:
        raise ValueError('DEBIG: Unable to load data...')
    data = data.loc[(slice(None)),(slice(None),slice(None))].copy()
    data = data.stack()
    data = data.reset_index()
    data.rename(columns={'Date':'Datetime', 'Ticker':'Symbol'}, inplace=True)
    data = data[['Datetime','Symbol', 'Open','High','Low','Close','Volume']]
    data.set_index('Datetime', inplace=True)

    return data

def get_local_data(file_name):
    try:
        data = pd.read_csv(file_name)
    except Exception as e:
        raise ValueError(f'DEBUG: Unable to open file : {e}')
    
    data = data.reset_index()
    data.rename(columns={'Date':'Datetime', 'Ticker':'Symbol'}, inplace=True)
    data = data[['Datetime','Symbol', 'Open','High','Low','Close','Volume']]
    data.set_index('Datetime', inplace=True)

    return data






