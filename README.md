# BHTP-Tools
**Brothers Hobby Trading Package Tools** – A set of tools to code and backtest automated stock trading strategies.

> **⚠️ Work in Progress:** This project is currently under development. Features, functionality, and documentation may change frequently. Thank you for your patience!

[![Work in Progress](https://img.shields.io/badge/status-in_progress-yellow)](https://github.com/poivronjaune/BHTP-Tools)
![Last Commit](https://img.shields.io/github/last-commit/poivronjaune/BHTP-Tools)
[![Documentation Status](https://readthedocs.org/projects/bhtp/badge/?version=latest)](https://bhtp.readthedocs.io/en/latest/?badge=latest)

---

## Overview

**BHTP-Tools** is a Python package designed for building and backtesting automated trading strategies. This package offers a range of tools to support working with market data, performing backtests, and handling data from sources like GitHub repositories.

## Installation  
*We recommend using a virtual environment for this package as it is a development version*
This package is not published to PyPi yet.  
Use pip install from the github repository to install locally.  
This should create a script command to display the version installed.  

```bash
pip install git+https://github.com/poivronjaune/BHTP-Tools.git
bhtp
```

## Modules  
### Downloading minute price data  
***github.py*** : Contains a Github class methods to download data from a github repo.  

***Example 1***:  
To retrieve a full month of data from [Github repository DATA-2024-08](https://github.com/MapleFrogStudio/DATA-2024-08). Set the verbose parameter to True to see the loading progress.  
  
<span style="color:red">**Warning**</span>: this repo contains **431** csv files that load 2.6 millions lines of data. It may take several minutes to run (a standard google colab execution takes around 10 minutes).   
```bash
from bhtp.github import Github
import pandas as pd

g = Github(owner='MapleFrogStudio', repository='DATA-2024-04', branch='main') 
data_df = g.load_ohlcv_for_month(verbose=True)
print(data_df)
```
***Example 2***:  
To retreive OHLC Data from a [Github repository DATA-2024-08](https://github.com/MapleFrogStudio/DATA-2024-08) containing files that start with "nasdaq1" 
```bash
from bhtp.github import Github
import pandas as pd

# Create an instance of the Github class
g = Github(owner='MapleFrogStudio', repository='DATA-2024-04', branch='main')

# Fetch the list of files in the root folder
content = g.repo_content()

# Filter files that start with a specific prefix
csv_files = g.select_files(content, starts_with='nasdaq1')

# Initialize an empty master DataFrame
master_df = pd.DataFrame()

# Loop through each CSV file and load the data into master_df
for file in csv_files:
    data_df = g.load_ohlcv_csv(file)  # Load the OHLCV data
    master_df = pd.concat([master_df, data_df], ignore_index=True)  # Concatenate the new DataFrame

# Display the concatenated master DataFrame
print(master_df.head())
```

### Creating a trading universe  
***universe.py*** : Class and methods to build a trading universe.  Load data from local csv files or using the Github class to load directly from Github repositories.  

***Example 3***  
To create a bunch of timeframes from our 1 minute price data, load some prices from a month and run the following code.  
Data source is the same as example 1 above.    
```bash
# examples/demo03.py
from bhtp.github import Github
from bhtp.universe import TradingUniverse
import pandas as pd

# Load data to insert into Trading Universe
g = Github(owner='MapleFrogStudio', repository='DATA-2024-04', branch='main') 
data_df = g.load_ohlcv_for_month(verbose=True)

# Insert Data into Universe and generate all timeframes
tu = TradingUniverse()
tu.insert_data(data_df)
print(f'1 min timeframe: {len(tu.df_1min)} records')
print(f'5 min timeframe: {len(tu.df_5min)} records')
print(f'1 day timeframe: {len(tu.df_1day)} records')  
```  
 
## External links  
[TA-Lib details](https://ta-lib.github.io/ta-lib-python/index.html) : C Library called by TA-Lib python wrapper.   
[TA-Lib Wheels](https://github.com/cgohlke/talib-build) : Download a binary version based on your python version.  
- Python 3.13 : adjust requirements.txt to install -> ./wheels/ta_lib-0.5.1-cp**313**-cp**313**-win_amd64.whl  
- Python 3.12 : adjust requirements.txt to install -> ./wheels/ta_lib-0.5.1-cp**312**-cp**312**-win_amd64.whl  
  
[QuestDB](https://questdb.io/) Timeseries Database for high performance data analysis instead of using raw cvs Files   
[QuestDB Python package](https://py-questdb-client.readthedocs.io/en/latest/index.html) Python package to ingest (load into DB) data.  
- This package usually does not work with the latest version of python  
- Use "py" launcher to setup a specific version of python and the associated environment.  
- py -v3.12 -m venv env for example.  