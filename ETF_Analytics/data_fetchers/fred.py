"""
FRED (Federal Reserve Economic Data) fetcher for benchmark data
"""
import pandas as pd
import requests
from datetime import datetime
from .base import DataFetcher


class FREDFetcher(DataFetcher):
    """Fetches benchmark and economic data from FRED"""
    
    def __init__(self):
        super().__init__(name="FRED", rate_limit=None)
        self.base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
    
    def fetch_risk_free_rate(self, start_date, end_date=None):
        """
        Fetch 3-Month Treasury Bill rate as risk-free rate proxy
        
        Returns:
        --------
        pd.Series with daily risk-free rates
        """
        return self._fetch_series('DGS3MO', start_date, end_date)
    
    def fetch_treasury_10y(self, start_date, end_date=None):
        """Fetch 10-Year Treasury Constant Maturity Rate"""
        return self._fetch_series('DGS10', start_date, end_date)
    
    def fetch_sp500(self, start_date, end_date=None):
        """Fetch S&P 500 index level"""
        return self._fetch_series('SP500', start_date, end_date)
    
    def _fetch_series(self, series_id, start_date, end_date=None):
        """
        Generic function to fetch FRED series
        
        Parameters:
        -----------
        series_id : str
            FRED series identifier
        start_date : str or datetime
            Start date
        end_date : str or datetime, optional
            End date
        """
        try:
            if end_date is None:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            params = {
                'id': series_id,
                'cosd': pd.to_datetime(start_date).strftime('%Y-%m-%d'),
                'coed': pd.to_datetime(end_date).strftime('%Y-%m-%d')
            }
            
            # Fetch CSV data
            df = pd.read_csv(self.base_url, params=params, index_col=0, parse_dates=True)
            
            # Return as Series
            series = df.iloc[:, 0]
            series.name = series_id
            
            # Convert to numeric, handle '.' as NaN
            series = pd.to_numeric(series, errors='coerce')
            
            # Forward fill missing values
            series = series.fillna(method='ffill')
            
            return series
            
        except Exception as e:
            print(f"Error fetching {series_id} from FRED: {str(e)}")
            return pd.Series()
    
    def fetch_prices(self, ticker, start_date, end_date=None):
        """Not applicable for FRED (only economic indicators)"""
        raise NotImplementedError("FRED does not provide individual ETF prices")
    
    def fetch_info(self, ticker):
        """Not applicable for FRED"""
        raise NotImplementedError("FRED does not provide ETF information")
