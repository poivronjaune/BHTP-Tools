__version__ = "0.1.0"
version = __version__

import pandas as pd

def get_version():
    """
    Retrieve the current version of the package.

    This function returns the version string defined in the `__version__` variable of the package.
    
    Returns:
        str: The version string of the package, as specified by the `__version__` variable.
    
    Example:
        >>> import bhtp
        >>> bhtp.get_version()
        '1.0.0'
    
    Usage:
        This can be used to check the version of the package at runtime:
        
        >>> from bhtp import get_version
        >>> version = get_version()
        >>> print(f"Current package version: {version}")
        Current package version: 1.0.0    
    """
    return __version__


def load_prices_from_csv(file_link, source:bool = False):
    """
    Loads a CSV file containing OHLCV (Open, High, Low, Close, Volume) from a formatted csv file (github raw link or local file path).

    This function reads a CSV file from a specified location, validates the presence of required columns 
    for OHLCV data, and renames the 'Ticker' column to 'Symbol' if necessary. It returns a DataFrame containing 
    only the relevant columns: 'Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Adj Close', and 'Volume'.

    Parameters:
    ----------
    file_link : str
        The URL of the file location (online like GitHub raw link or local path) to the CSV file to be loaded.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing the OHLCV data with columns: 'Datetime', 'Symbol', 'Open', 'High', 'Low', 
        'Close', 'Adj Close', and 'Volume'.
    """
    
    try:
        df = pd.read_csv(file_link)
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
    if source:
        df['Source'] = file_link
    
    return df

