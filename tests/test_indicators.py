import pytest
import pandas as pd
from bhtp.indicators import Indicators as I

# tu_empty, tu_loaded, g_data are defined as session scope fixtures in conftest.py
def test_indciators_init_class(tu_loaded):
    i = I()
    print(i.msg)
    assert i is not None
