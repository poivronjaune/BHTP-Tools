import pandas as pd
import datetime
from bhtp.github import Github
from bhtp.universe import TradingUniverse

# Note when the execution was started to display run time at the end
runtime_start = datetime.datetime.now()

# Load data to insert into Trading Universe
g = Github(owner='MapleFrogStudio', repository='DATA-2024-04', branch='main') 
data_df = g.load_ohlcv_for_month(verbose=True)

# Insert Data into Universe and generate all timeframes
tu = TradingUniverse()
print(f'\nLaunching timeframe aggregation for {len(data_df)} records\n')
tu.insert_data(data_df)
print(f'1 min timeframe: {len(tu.df_1min)} records')
print(f'5 min timeframe: {len(tu.df_5min)} records')
print(f'1 hour timeframe: {len(tu.df_1hr)} records')
print(f'4 hours timeframe: {len(tu.df_4hr)} records')
print(f'1 day timeframe: {len(tu.df_1day)} records')
print(f'1 week timeframe: {len(tu.df_1wk)} records')
print(f'1 month timeframe: {len(tu.df_1month)} records')


# Display execution time for the download and aggregation of timeframes
runtime_end = datetime.datetime.now()
print(f'Starttime: {runtime_start}')
print(f'Endtime  : {runtime_end}')
print('==========================================================================================')
print(f'Full universe setup time: {runtime_end - runtime_start}')