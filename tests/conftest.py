import pytest
import pandas as pd
from bhtp.universe import TradingUniverse

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
