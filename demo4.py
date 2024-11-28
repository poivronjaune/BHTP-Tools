import datetime
import pandas as pd
from bhtp.github import Github
from bhtp.universe import TradingUniverse


# Note when the execution was started to display run time at the end
runtime_start = datetime.datetime.now()


# Universe raw data - 1 minute multiple months
universe_df = pd.DataFrame()

# Load data to insert into Trading Universe
months = ['DATA-2024-08', 'DATA-2024-09', 'DATA-2024-10']
for repo in months:
    g = Github(owner='MapleFrogStudio', repository=repo, branch='main') 
    one_month_df = g.load_ohlcv_for_month(verbose=True)
    universe_df = pd.concat([universe_df, one_month_df], ignore_index=True)
    del(g)

tu = TradingUniverse()
tu.insert_data(universe_df, freq='all')
tu.calculate_indicators()
tu.save_universe()


# Display execution time for the download and aggregation of timeframes
runtime_end = datetime.datetime.now()
print(f'Starttime: {runtime_start}')
print(f'Endtime  : {runtime_end}')
print('==========================================================================================')
print(f'Full universe setup time: {runtime_end - runtime_start}')
