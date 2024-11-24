from bhtp.github import Github
from bhtp.universe import TradingUniverse
import pandas as pd

g = Github(owner='MapleFrogStudio', repository='DATA-2024-04', branch='main') 
data_df = g.load_ohlcv_for_month(verbose=True)
print(data_df)

tu = TradingUniverse()
tu.insert_data(data_df)
print(tu.df_1wk)