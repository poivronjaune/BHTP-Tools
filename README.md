# BHTP-Tools
**Brothers Hobby Trading Package Tools** – A set of tools to code and backtest automated stock trading strategies.

> **⚠️ Work in Progress:** This project is currently under development. Features, functionality, and documentation may change frequently. Thank you for your patience!

[![Work in Progress](https://img.shields.io/badge/status-in_progress-yellow)](https://github.com/poivronjaune/BHTP-Tools)
![Last Commit](https://img.shields.io/github/last-commit/poivronjaune/BHTP-Tools)

---

## Overview

**BHTP-Tools** is a Python package designed for building and backtesting automated trading strategies. This package offers a range of tools to support working with market data, performing backtests, and handling data from sources like GitHub repositories.

### Downloading minute price data  
***github.py*** : Contains a Github class methods to download data from a github repo.  

***Example*** to retreive OHLC Data from a (Github repository)[https://github.com/MapleFrogStudio/DATA-2024-08] containing files that start with "nasdaq1" 
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

