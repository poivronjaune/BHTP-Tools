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
    ============
    owner : str
        The GitHub username or organization that owns the repository.  
        
        Default: 'MapleFrogStudio'.
    repo : str
        The name of the GitHub repository.  
        
        Default: 'DATA-2023-04'.
    branch : str
        The branch of the repository to interact with.  
        
        Default: 'main'

    Usage:
    ======
    Instantiate a Github object, then call one of the load_funcion to fetch a bunch of stock data.

    Example:
    ========
    > from bhtp.github import Github
    >
    > g = Github()
    > print(g)
    > df = g.load_ohcvl_for_month(verbose=True) # Print each file download to see progress

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
        url = f'https://github.com/{self.owner}/{self.repo}/tree/{self.branch}'
        return url
    

    @property
    def api_content(self) -> str:
        """Builds a url link to the github api that retreives a json object of all items in the defined repository
        
        Returns:
        ========
            url : str
        """
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/'
        return url

    def repo_content(self, folder='/') -> list:
        """
        Retrieves the content of the specified folder in a GitHub repository.

        This function fetches and returns a list of file and/or folder information from the specified folder 
        in the repository. Each item in the list contains information such as file type, name, and download URL, formatted as json data.

        Parameters:
        ============
        folder : str, optional
            The path to the folder in the repository from which to retrieve contents. Defaults to the 
            root folder ('/').

            Default: '/'

        Returns:
        =========
        list
            A list of dictionaries where each item represents a file or folder in the 
            specified folder of the repository, including details like type, name, and download URL.

        """
        if folder == '/' or folder == '' or folder is None or not isinstance(folder, str):
            folder = ''
        url = self.api_content + folder
        content = requests.get(url, timeout=30)
        list_of_json_objects = content.json()
        return list_of_json_objects

    def select_files(self, repo_content, starts_with='') -> list:
        """
        Filters a list of GitHub file records for CSV files by file type and optional name prefix.

        This function takes a list of dictionaries (`repo_content`), each representing a GitHub file 
        record containing file metadata, and filters for CSV files. It returns a list of download 
        URLs for files where the type is 'file' and, optionally, the file name starts with a given prefix.

        Parameters:
        ----------
        repo_content : list of dict
            A list of dictionaries, where each dictionary represents a file record with keys 'type' 
            and 'download_url'. If `repo_content` is not a list or the items do not contain the required 
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
        if not isinstance(repo_content, list):
            raise ValueError('Invalid file list or start_with parameters to select files.')
        one_item = repo_content[0]
        if not isinstance(one_item, dict):
            raise ValueError('Invalid item in file list parameters to select files.')
        if not 'type' in one_item.keys() or not 'download_url' in one_item.keys():
            raise ValueError('Invalid keys in file list parameters to select files.')

        if starts_with == '' or starts_with is None:
            raw_urls = [record['download_url'] for record in repo_content if record['type'] == 'file']
        else:
            pattern = pattern = r"^" + starts_with + r".*\.csv$"
            raw_urls = [record['download_url'] for record in repo_content if record['type'] == 'file' and re.match(pattern, record['name'])]

        return raw_urls


    def load_ohlcv_from_raw_link(self, github_raw_link):
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
        
        try:
            df = pd.read_csv(github_raw_link)
        except Exception as e:
            raise RuntimeError(f'Unable to read target file, {e}')
        
        required_columns = ['Datetime','Open','High','Low','Close','Adj Close','Volume']
        all_columns_present = all(column in df.columns for column in required_columns)
        if not all_columns_present:
            raise RuntimeError(f'CSV file loaded is missing one or more of the following columns {required_columns}.')
        if not ('Symbol' in df.columns or 'Ticker' in df.columns):
            raise RuntimeError(f'CSV file loaded is missing one or more of the following columns Symbol or Ticker.')
        if 'Ticker' in df.columns:
            df = df.rename(columns={"Ticker": "Symbol"})

        df = df[['Datetime','Symbol', 'Open','High','Low','Close','Adj Close','Volume']]
        return df

    def load_ohlcv_for_month(self, verbose=False):
        """
        Load and aggregate OHLCV data from multiple CSV files for a given month (usually a DATA repo).

        This method retrieves OHLCV (Open, High, Low, Close, Volume) data for all files in the instantiated repo on init.
        The CSV files in the GitHub repository are concatenated into a single DataFrame.
        
        Parameters:
        ----------
        verbose : bool, optional
            If set to True, progress is printed as each file is processed. Default is False.
        
        Returns:
        -------
        pd.DataFrame
            A pandas DataFrame containing aggregated OHLCV data for the specified month and year. The DataFrame includes
            columns for 'Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Adj Close', and 'Volume'.
        
       
        Example:
        --------
        >>> github = Github(owner="MapleFrogStudio", repository="DATA-2023-04", branch="main")
        >>> df = github.load_ohlcv_for_month(verbose=True)
        >>> print(df.head())
        """
#        if year < 2023 or month < 1 or month > 12:
#            raise ValueError(f"{year}-{month}, year must be 2023 or higher, month must be between 1 and 12.")
#        file_name = f"DATA-{year:4}-{month:02}"
#        self.repo  = file_name
        json_content = self.repo_content()
        raw_urls = self.select_files(repo_content=json_content)
        total_files = len(raw_urls)
        month_df = pd.DataFrame()       # Initialize an empty Dataframe to append each file loaded in the month repo
        for i, raw_link in enumerate(raw_urls, start=1):
            data_df = self.load_ohlcv_from_raw_link(raw_link)
            month_df = pd.concat([month_df, data_df], ignore_index=True)
            if verbose:
                print(f'{i}/{total_files} : {raw_link}')
        
        return month_df

    def load_ohlcv_from_file(self, csv_file_name:str, verbose: bool = False) -> pd.DataFrame:
        """
        Load OHLCV data for a specific file from a GitHub repository.

        This method retrieves OHLCV (Open, High, Low, Close, Volume) data for a specified file (if available) 
        from the repository. The method searches for a CSV file matching the file name provided,
        and returns the data as a pandas DataFrame.

        Parameters:
        ----------
        csv_file_name : Name of the specific file to be loaded from the repo.
        
        Returns:
        -------
        pd.DataFrame
            A pandas DataFrame containing the OHLCV data for the specified file. The DataFrame includes
            columns for 'Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Adj Close', and 'Volume'.
        
        Example:
        --------
        >>> github = Github(owner="MapleFrogStudio", repository="DATA-2024-07", branch="main")
        >>> df = github.load_ohlcv_from_file(csv_file_name='NASDAQ-BM0-2024-07-15.csv', verbose=True)
        >>> print(df.head())
        """
        json_content = self.repo_content()
        index = next((i for i, d in enumerate(json_content) if d.get('name') == csv_file_name), None)

        if index is None:
            raise ValueError(f"Not Found - Unable to find {csv_file_name} in {self.repo}")         
        
        raw_urls = self.select_files(repo_content=json_content) 
        df = self.load_ohlcv_from_raw_link(raw_urls[index])

        return df

    def load_ohlcv_for_day(full_dt: str) -> pd.DataFrame:
        """
        Load OHLCV data for a specific day from a GitHub repository.

        This method retrieves all OHLCV (Open, High, Low, Close, Volume) data for a specified day (if available) 
        from the repository. The method searches for all CSV file containing the substring 'full_dt' provided,
        and returns the data as a pandas DataFrame.

        Parameters:
        ----------
        full_dt : A string formatted as 'yyyy-mm-dd' 
        
        Returns:
        -------
        pd.DataFrame
            A pandas DataFrame containing the OHLCV data for the specified day. The DataFrame includes
            columns for 'Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Adj Close', and 'Volume'.

        """
        if not isinstance(full_dt, 'str'):
            raise ValueError(f"{full_dt}, is not a string. Please provde a string formatted as yyyy-mm-dd")
        
        data = pd.DataFrame()
        return data

if __name__ == '__main__':                              # pragma: no cover
    # Example loading a small test file
    # ByPass Github Class config to load a fully qualified raw github url
    #url = ('https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/TESTING/OHLCV-valid01.csv')
    g1 = Github(repository='DATA-2023-04')
    print(g1)
    print(g1.api_content)
    print('======================================')
    repo_json = g1.repo_content() 
    print(repo_json[0:4])
    print('======================================')
    #data = g1.load_ohlcv_from_file(csv_file='NASDAQ-CC0-2023-04-03.csv', verbose=True)
    #print(data)

