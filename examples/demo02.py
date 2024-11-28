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
