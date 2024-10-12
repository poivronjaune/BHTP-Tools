import sys
import requests
import re
import pandas as pd

class Github:
    """Utility class to retrieve github info and links"""
    def __init__(self, owner='MapleFrogStudio', repository='DATA-2023-04', branch='main') -> None:
        if owner is None or owner == '' or not isinstance(owner, str):
            raise ValueError('Invalid owner parameter.')
        if repository is None or repository == '' or not isinstance(repository, str):
            raise ValueError('Invalid repository parameter.')
        if branch is None or branch == '' or not isinstance(branch, str):
            raise ValueError('Invalid branch parameter.')   
             
        self.owner = owner
        self.repo  = repository
        self.branch = branch

    def __str__(self) -> str:
        #url = f'{self.owner} -> {self.repo} -> {self.branch}'
        url = f'https://github.com/{self.owner}/{self.repo}/tree/{self.branch}'
        return url
    

    @property
    def api_content(self) -> str:
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/'
        return url

    def repo_content(self, folder='/') -> list:
        ''' Return a list of files from  github repo that start_with a specifc string '''
        if folder == '/' or folder == '' or folder is None or not isinstance(folder, str):
            folder = ''
        url = self.api_content + folder
        content = requests.get(url, timeout=10)
        list_of_json_objects = content.json()
        return list_of_json_objects

    def select_files(self, file_list, starts_with='') -> list:
        """Filter the github list of json objects containing repo info for download url of CSV files and starts_with parameter"""
        if not isinstance(file_list, list):
            raise ValueError('Invalid file list or start_with parameters to select files.')
        one_item = file_list[0]
        if not isinstance(one_item, dict):
            raise ValueError('Invalid item in file list parameters to select files.')
        if not 'type' in one_item.keys() or not 'download_url' in one_item.keys():
            raise ValueError('Invalid keys in file list parameters to select files.')

        if starts_with == '' or starts_with is None:
            raw_urls = [record['download_url'] for record in file_list if record['type'] == 'file']
        else:
            pattern = pattern = r"^" + starts_with + r".*\.csv$"
            raw_urls = [record['download_url'] for record in file_list if record['type'] == 'file' and re.match(pattern, record['name'])]

        return raw_urls

    # Specialised loading function for Open, High, Low, Close, Volumne formatted csv files
    def load_ohlcv_csv(self, github_raw_link):
        #print(f'DEBUG: {github_raw_link}')
        df = pd.read_csv(github_raw_link)
        required_columns = ['Datetime','Open','High','Low','Close','Adj Close','Volume']
        all_columns_present = all(column in df.columns for column in required_columns)
        if not all_columns_present:
            raise RuntimeError(f'CSV file loaded is missing one or more of the following columns {required_columns}.')
        if not ('Symbol' in df.columns or 'Ticker' in df.columns):
            raise RuntimeError(f'CSV file loaded is missing one or more of the following columns Symbol or Ticker.')
        if 'Ticker' in df.columns:
            df = df.rename(columns={"Ticker": "Symbol"})

        df = df[['Datetime','Symbol', 'Open','High','Low','Close','Adj Close','Volume']]
        # print(df)
        return df

if __name__ == '__main__':                              # pragma: no cover
    # Example loading a small test file
    # ByPass Github Class config to load a fully qualified raw github url
    #url = ('https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/TESTING/OHLCV-valid01.csv')
    g1 = Github(repository='DATA-2024-02')
    print(g1)
    print(g1.api_content)
    raw_urls = g1.repo_content()
    data_df = pd.read_csv(g1.select_files(raw_urls)[0])
    print(data_df)
