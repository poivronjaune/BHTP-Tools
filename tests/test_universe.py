import time
from tkinter import N
import pandas as pd
from numpy import true_divide
import pytest
from bhtp.github import Github
from bhtp.universe import TradingUniverse

# To prevent connection not established errors when testing, use a local csv file to load price data
@pytest.fixture(scope="session")
def g_data():
    data_df = pd.read_csv('tests/test_data.csv')
    return data_df

@pytest.fixture(scope="session")
def tu_empty():
    # Default trading universe
    return TradingUniverse()

@pytest.fixture(scope="session")
def tu_loaded(g_data):
    # Default trading universe
    tu = TradingUniverse()
    tu.insert_data(g_data, freq='all')
    return tu

def test_init_setup(tu_empty):
    tu = tu_empty
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
    ('all', False, False, False, False, False, False, False),
])
def test_insert_data_for_many_timeframes(g_data, freq, a1, a2, a3, a4, a5, a6, a7):
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

def test_fail_insert_data(g_data):
    tu = TradingUniverse()
    with pytest.raises(Exception) as exc_info:
        tu.insert_data(g_data, freq='Invalid')
    print(f"Pytest Message: {exc_info.value}")

@pytest.mark.parametrize("param1", [
    10,
    'Hello',
    None,
])
def test_fail_calculate_indicators(g_data, param1):
    tu = TradingUniverse()
    with pytest.raises(Exception) as exc_info:
        tu.calculate_indicators(param1)
    print(f"Pytest Message: {exc_info.value}")

@pytest.mark.parametrize("indicator, params, columns", [
    ('sma', [50], ['sma50']),
    ('rsi', [14], ['gain', 'loss', 'rsi']),
])
def test_calculate_indicators(tu_loaded, indicator, params, columns):
    # Add indicators tests here
    print(f'\n{indicator}: {len(tu_loaded.df_1min)}, {tu_loaded.df_1min.columns.to_list()}')
    print(f'\n{indicator}: {len(tu_loaded.df_1day)}, {tu_loaded.df_1day.columns.to_list()}')

