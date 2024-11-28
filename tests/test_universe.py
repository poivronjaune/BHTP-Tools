import time
from tkinter import N
import pandas as pd
from numpy import true_divide
import pytest
from bhtp.github import Github
from bhtp.universe import TradingUniverse

@pytest.fixture(scope="session")
def tu1():
    # Default trading universe
    return TradingUniverse()

# To prevent connection not established errors when testing, use a local csv file to load price data
@pytest.fixture(scope="session")
def g_data():
    data_df = pd.read_csv('tests/test_data.csv')

    ####
    # Remove comments to test directly from github repo.
    ######
    #g1 = Github()
    #data_df = pd.DataFrame()
    #files = ['NASDAQ-CC0-2023-04-03.csv', 'NASDAQ-BM0-2023-04-22.csv', 'NASDAQ-TE0-2023-04-20.csv'] 
    #max_retries = 5
    #for csv_file in files:
    #    try_to_load = True
    #    loading_attempt = 1
    #    while try_to_load:
    #        try:
    #            data = g1.load_ohlcv_from_file(csv_file)
    #            try_to_load = False
    #        except ConnectionError as e:
    #            if loading_attempt > max_retries:
    #                try_to_load = False
    #                raise ConnectionError(f'{max_retries} retries in test to load github\n{e}')
    #            loading_attempt += 1
    #            time.sleep(2)
    #
    #    data_df = pd.concat([data_df, data], ignore_index=True)
    ##    data_df.to_csv('test_data.csv', index=False)
    return data_df


def test_init_setup(tu1):
    tu = tu1
    assert tu.df_1min is None
    assert tu.df_5min is None
    assert tu.df_15min is None
    assert tu.df_1hr is None
    assert tu.df_4hr is None
    assert tu.df_1day is None
    assert tu.df_1wk is None
    assert tu.df_1month is None


@pytest.mark.parametrize("freq, a1, a2, a3, a4, a5, a6, a7", [
    ('5min', False, True, True, True, True, True, True),
    ('15min', True, False, True, True, True, True, True),
    ('1h', True, True, False, True, True, True, True),
    ('4h', True, True, True, False, True, True, True),
    ('1D', True, True, True, True, False, True, True),
    ('1W', True, True, True, True, True, False, True),
    ('1ME', True, True, True, True, True, True, False),
])
def test_insert_data_specific_timeframe(g_data, freq, a1, a2, a3, a4, a5, a6, a7):
    tu = TradingUniverse()
    assert tu is not None
    assert g_data is not None
    tu.insert_data(g_data, freq=freq)
    assert (tu.df_5min is None) == a1
    assert (tu.df_15min is None) == a2
    assert (tu.df_1hr is None) == a3
    assert (tu.df_4hr is None) == a4
    assert (tu.df_1day is None) == a5
    assert (tu.df_1wk is None) == a6
    assert (tu.df_1month is None) == a7
    del(tu)

def test_insert_data_all_timeframes(tu1, g_data):
    print(f'\n*********\n Loading test data may take 30-60 seconds\n*********\n')
    assert tu1 is not None
    assert tu1.df_1min is None
    assert g_data is not None
    print(g_data)
    tu1.insert_data(g_data)
    assert tu1.df_1min is not None
    assert tu1.df_5min is not None
    assert tu1.df_15min is not None
    assert tu1.df_1hr is not None
    assert tu1.df_4hr is not None
    assert tu1.df_1day is not None
    assert tu1.df_1wk is not None
    assert tu1.df_1month is not None
    
    