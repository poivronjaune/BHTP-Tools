import pandas as pd
from bhtp.github import Github

class TradingUniverse:
    """Trading Universe Class contains all trading information to simulate a trading environnement 
       with price data including multiple timeframes.
    """

    def __init__(self):
        self.df_1min = None
        self.df_5min = None
        self.df_15min = None
        self.df_1hr = None
        self.df_4hr = None
        self.df_1day = None
        self.df_1wk = None
        self.df_1month = None

    def timeframe(self, timeframe: str) -> pd.DataFrame:
        """
        If data for 1 minute time frame exists, aggregate data to another timeframe.
        requires self.df_1min to contain valid data

        Parameters:
        ============
        timeframe : str
            Target timeframe ['5min', '15min', '1h','4h', '1D', '1W', '1ME'] # ME = Month End

        """
        if self.df_1min is None:
            raise ValueError('No minute data available to aggregate.')
        if timeframe not in ['5min', '15min', '1h', '4h', '1D', '1W', '1ME']:
            raise ValueError("Invalid timeframe target, Use : ['5min', '15min', '1h','4h', '1D', '1W', '1ME']")
        
        new_timeframe = (
            self.df_1min.groupby('Symbol')
            .resample(timeframe)      # new timeframe frequency
            .agg({
                'Open': 'first',      # First open in the interval
                'High': 'max',        # Maximum high in the interval
                'Low': 'min',         # Minimum low in the interval
                'Close': 'last',      # Last close in the interval
                'Volume': 'sum'       # Total volume in the interval
            })
            #.drop(columns='Symbol')   # Remove Symbol from multi-level index
            .reset_index()            # Reset index to make it a standard DataFrame
        )
        new_timeframe = new_timeframe[['Datetime','Symbol','Open','High','Low','Close','Volume']]
        new_timeframe.set_index('Datetime', inplace=True)
        return new_timeframe  

    def insert_data(self, df_ohlcv: pd.DataFrame, freq='all') -> None:
        """
        Inserts minute price data in the trading universe. Dataframe should contain the following columns
        [Datetime, Symbol, Open, High, Low, Close, Volume]. 
        Use the Github class to load online data from Github repositories. 

        Parameters:
        ============
        df_ohlcv : Pandas Dataframe
            Dataframe containing minute price data [Datetime, Symbol, Open, High, Low, Close, Volume]

        """
        valid_freq = ['5min', '15min', '1h', '4h', '1D', '1W', '1ME', 'all']
        # Reorganise minute data for Trading Universe structure, sorted, index and columns
        self.df_1min = df_ohlcv
        self.df_1min = self.df_1min.sort_values(by=['Symbol', 'Datetime'])
        self.df_1min['Datetime'] = pd.to_datetime(self.df_1min['Datetime'])
        self.df_1min = self.df_1min[['Datetime','Symbol','Open','High','Low','Close','Volume']]
        self.df_1min.set_index('Datetime', inplace=True)

        if freq not in valid_freq:
            raise ValueError(f"Invalid 'freq' parameter, use of {valid_freq}")
        
        match freq:
            case '5min' : self.df_5min = self.timeframe('5min')
            case '15min' : self.df_15min = self.timeframe('15min')
            case '1h' : self.df_1hr = self.timeframe('1h')
            case '4h' : self.df_4hr = self.timeframe('4h')
            case '1D' : self.df_1day = self.timeframe('1D')
            case '1W' : self.df_1wk = self.timeframe('1W')
            case '1ME' : self.df_1month = self.timeframe('1ME')      
            case 'all' :
                self.df_5min = self.timeframe('5min')
                self.df_15min = self.timeframe('15min')
                self.df_1hr = self.timeframe('1h')
                self.df_4hr = self.timeframe('4h')
                self.df_1day = self.timeframe('1D')
                self.df_1wk = self.timeframe('1W')
                self.df_1month = self.timeframe('1ME')      


    def calculate_indicators(self, indicators: list) -> None:
        """Using data loaded in Universe (1min, 5min, 15min, 1h, 4h, 1d, 1w, 1month) calculate a bunch of indicators.
        Append all indicators in Universe data as new DataFrame columns.
        """
        if not isinstance(indicators, list):
            raise ValueError('TradingUnivers.calculate_indicators: bad parameter. use a list of strings.')
        
        ## TODO: Implement some indicators



