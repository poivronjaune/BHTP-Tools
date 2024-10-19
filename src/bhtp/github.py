import sys
import requests
import re
import pandas as pd

class Github:
    """
    A utility class for retrieving information and links from a specified GitHub repository.

    This class allows users to interact with a GitHub repository by providing methods to:
    - Retrieve the content of a specific folder within the repository.
    - Filter files in the repository by type and name prefix.
    - Load and validate OHLCV (Open, High, Low, Close, Volume) formatted CSV files.

    Attributes:
    ----------
    owner : str
        The GitHub username or organization that owns the repository.
    repo : str
        The name of the GitHub repository.
    branch : str
        The branch of the repository to interact with.

    """
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
        """
            A python __dunder__ method that assembles the class parameters in a URL String for printingé

        Returns:
        -------
        str
            a URL link to the defined github repository.

        """
        url = f'https://github.com/{self.owner}/{self.repo}/tree/{self.branch}'
        return url
    

    @property
    def api_content(self) -> str:
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/'
        return url

    def repo_content(self, folder='/') -> list:
        """
        Retrieves the content of a specified folder in a GitHub repository.

        This function fetches and returns a list of file and folder metadata from the specified folder 
        in the repository. Each item in the list contains information such as file type, name, and download URL.

        Parameters:
        ----------
        folder : str, optional
            The path to the folder in the repository from which to retrieve contents. Defaults to the 
            root folder ('/').

        Returns:
        -------
        list
            A list of dictionaries where each dictionary represents an item (file or folder) in the 
            specified folder, including details like type, name, and download URL.

        """
        if folder == '/' or folder == '' or folder is None or not isinstance(folder, str):
            folder = ''
        url = self.api_content + folder
        content = requests.get(url, timeout=10)
        list_of_json_objects = content.json()
        return list_of_json_objects

    def select_files(self, file_list, starts_with='') -> list:
        """
        Filters a list of GitHub file records for CSV files by file type and optional name prefix.

        This function takes a list of dictionaries (`file_list`), each representing a GitHub file 
        record containing file metadata, and filters for CSV files. It returns a list of download 
        URLs for files where the type is 'file' and, optionally, the file name starts with a given prefix.

        Parameters:
        ----------
        file_list : list of dict
            A list of dictionaries, where each dictionary represents a file record with keys 'type' 
            and 'download_url'. If `file_list` is not a list or the items do not contain the required 
            keys, a `ValueError` is raised.
        starts_with : str, optional
            A string prefix for filtering file names. If provided, only files with names starting 
            with this prefix and ending in '.csv' are included. If empty or None, all CSV files are 
            included regardless of name.

        Returns:
        -------
        list
            A list of download URLs (strings) for files matching the criteria.

        """
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
        """
        Loads a CSV file containing OHLCV (Open, High, Low, Close, Volume) formatted data from a GitHub link.

        This function reads a CSV file from the specified GitHub raw URL, validates the presence of required columns 
        for OHLCV data, and renames the 'Ticker' column to 'Symbol' if necessary. It returns a DataFrame containing 
        only the relevant columns: 'Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Adj Close', and 'Volume'.

        Parameters:
        ----------
        github_raw_link : str
            The URL of the GitHub raw link pointing to the CSV file to be loaded.

        Returns:
        -------
        pd.DataFrame
            A DataFrame containing the OHLCV data with columns: 'Datetime', 'Symbol', 'Open', 'High', 'Low', 
            'Close', 'Adj Close', and 'Volume'.
        """
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
