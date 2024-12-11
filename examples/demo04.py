# BAD IMPLEMENTATION - Out of Memory Error because too much data is loaded at once

import datetime
import os
import pandas as pd
import ta
from bhtp.github import Github
from bhtp.universe import TradingUniverse

def apply_ta_to_group(group):
    min_len = 100
    if len(group) >= min_len:  # Check if the group has enough data (e.g., 5 rows)
        return ta.add_all_ta_features(group, 
                                      open="Open", 
                                      high="High", 
                                      low="Low", 
                                      close="Close", 
                                      volume="Volume", 
                                      fillna=True)
    else:
        # If the group is too small, return the group unchanged
        return group
    
def tmp_out_of_memory():
    g1 = Github()

    universe = pd.DataFrame()
    #for i in ['03','04','05','06','07','08','09','10','11','12']:
    for i in ['03']:
        folder_path = os.path.join("D:\\", "stockdata", f"DATA-2023-{i}")
        print(f'Loading : {folder_path}')
        data_df = g1.load_ohlcv_from_local_files(folder_path)
        universe = pd.concat([universe, data_df], ignore_index=True)

    # Ensure the datetime column is parsed as datetime
    print(f'Datime indexing... ')
    universe['Datetime'] = pd.to_datetime(universe['Datetime'])

    # Sort by datetime to ensure correct order for indicators calculation
    print(f'Sorting on [Symbol, Datetime]... ')
    universe = universe.sort_values(by=['Symbol', 'Datetime'])

    # Calculate multiple indicators (e.g., SMA50, EMA, RSI, etc.) for each symbol
    # Use `add_all_ta_features` to calculate multiple indicators at once
    print(f'Adding all indicators...')
    universe = universe.groupby('Symbol').apply(apply_ta_to_group)
    print(f'Saving to csv file D:\\csv\\all_data.csv')
    universe.to_csv('D:\\csv\\all_data.csv', header=True, index=False)
    print(universe)    



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
