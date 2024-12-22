import requests
import pandas as pd
from bhtp import load_data_from_questdb

host = "http://localhost:9000"
query = "SELECT * FROM prices WHERE Datetime > '2024-10-01' AND Symbol = 'AMZN';"
url = f"{host}/exec"
params = {"query": query}

response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()
print(data.keys())
print(f'Number of rows: {data.get('count')}')
print(f'SQL Query: {data.get('query')}')
print(f'List of columns: {data.get('columns')}')
column_names = [row['name'] for row in data.get('columns')]
print(column_names)
#print(data["dataset"])
df = pd.DataFrame(data["dataset"], columns=column_names)
print(f'Number of rows{len(df)}')
print(df.tail(10))

