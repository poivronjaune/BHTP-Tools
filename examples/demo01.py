from bhtp.github import Github
import pandas as pd

g = Github(owner='MapleFrogStudio', repository='DATA-2024-04', branch='main') 
data_df = g.load_ohlcv_for_month(verbose=True)
print(data_df)
