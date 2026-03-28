"""
Alpha Vantage data fetcher for validation and additional data
"""
import requests
import pandas as pd
from datetime import datetime
from .base import DataFetcher, clean_price_data
from config import ALPHA_VANTAGE_API_KEY


class AlphaVantageFetcher(DataFetcher):
    """Fetches data from Alpha Vantage API"""
    
    def __init__(self, api_key=None):
        super().__init__(name="Alpha Vantage", rate_limit=25)
        self.api_key = api_key or ALPHA_VANTAGE_API_KEY
        self.base_url = "https://www.alphavantage.co/query"
    
    def fetch_prices(self, ticker, start_date, end_date=None):
        """
        Fetch daily price data
        
        Note: Alpha Vantage returns full history regardless of dates
        """
        if not self.api_key or self.api_key == "demo":
            print(f"Warning: Using demo API key for Alpha Vantage. Get your free key at alphavantage.co")
        
        self._enforce_rate_limit()
        
        try:
            params = {
                'function': 'TIME_SERIES_DAILY_ADJUSTED',
                'symbol': ticker,
                'outputsize': 'full',
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if 'Error Message' in data:
                raise ValueError(f"API Error: {data['Error Message']}")
            
            if 'Note' in data:
                raise ValueError(f"API Rate Limit: {data['Note']}")
            
            # Parse time series data
            time_series = data.get('Time Series (Daily)', {})
            
            if not time_series:
                raise ValueError(f"No data returned for {ticker}")
            
            # Convert to DataFrame
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            
            # Rename columns
            df.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 
                         'Dividend', 'Split']
            
            # Convert to numeric
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Filter by date range
            if start_date:
                df = df[df.index >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df.index <= pd.to_datetime(end_date)]
            
            # Clean data
            df = clean_price_data(df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']])
            
            return df
            
        except Exception as e:
            print(f"Error fetching {ticker} from Alpha Vantage: {str(e)}")
            return pd.DataFrame()
    
    def fetch_info(self, ticker):
        """
        Fetch company overview (limited for ETFs)
        """
        self._enforce_rate_limit()
        
        try:
            params = {
                'function': 'OVERVIEW',
                'symbol': ticker,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            etf_info = {
                'name': data.get('Name', ticker),
                'sector': data.get('Sector', None),
                'description': data.get('Description', None),
                'source': self.name
            }
            
            return etf_info
            
        except Exception as e:
            print(f"Error fetching info for {ticker}: {str(e)}")
            return {'name': ticker, 'source': self.name}
