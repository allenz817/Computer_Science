"""
IEX Cloud data fetcher - Free tier available
"""
import requests
import pandas as pd
from datetime import datetime
from .base import DataFetcher, clean_price_data
from config import IEX_CLOUD_API_KEY


class IEXCloudFetcher(DataFetcher):
    """Fetches data from IEX Cloud API"""
    
    def __init__(self, api_key=None):
        super().__init__(name="IEX Cloud", rate_limit=None)
        self.api_key = api_key or IEX_CLOUD_API_KEY
        self.base_url = "https://cloud.iexapis.com/stable"
        
        # IEX Cloud free tier: 50,000 messages/month
        # We'll use it conservatively
    
    def fetch_prices(self, ticker, start_date, end_date=None):
        """
        Fetch historical price data from IEX Cloud
        
        Note: Free tier has limited history (5 years max)
        """
        if not self.api_key:
            print(f"Warning: No IEX Cloud API key configured. Get free key at https://iexcloud.io/console/")
            print(f"Skipping IEX Cloud fetch.")
            return pd.DataFrame()
        
        try:
            # Calculate date range
            if end_date is None:
                end_date = datetime.now()
            
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            
            # Determine range parameter
            days_diff = (end - start).days
            if days_diff <= 30:
                range_param = '1m'
            elif days_diff <= 90:
                range_param = '3m'
            elif days_diff <= 180:
                range_param = '6m'
            elif days_diff <= 365:
                range_param = '1y'
            elif days_diff <= 730:
                range_param = '2y'
            else:
                range_param = '5y'
            
            # Fetch data
            url = f"{self.base_url}/stock/{ticker}/chart/{range_param}"
            params = {
                'token': self.api_key,
                'chartCloseOnly': 'false'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 403:
                print(f"IEX Cloud: Invalid API key or quota exceeded")
                return pd.DataFrame()
            
            if response.status_code != 200:
                print(f"IEX Cloud API error: {response.status_code}")
                return pd.DataFrame()
            
            data = response.json()
            
            if not data:
                raise ValueError(f"No data returned for {ticker}")
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Convert date column
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            # Rename columns to standard format
            df = df.rename(columns={
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            })
            
            # Add Adj Close (IEX data is already adjusted)
            df['Adj Close'] = df['Close']
            
            # Filter by date range
            df = df[(df.index >= start) & (df.index <= end)]
            
            # Select relevant columns
            df = df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
            
            # Clean the data
            df = clean_price_data(df)
            
            return df
            
        except Exception as e:
            print(f"Error fetching {ticker} from IEX Cloud: {str(e)}")
            return pd.DataFrame()
    
    def fetch_info(self, ticker):
        """
        Fetch company/ETF information
        """
        if not self.api_key:
            return {'name': ticker, 'source': self.name}
        
        try:
            # Get company info
            url = f"{self.base_url}/stock/{ticker}/company"
            params = {'token': self.api_key}
            
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                return {'name': ticker, 'source': self.name}
            
            data = response.json()
            
            etf_info = {
                'name': data.get('companyName', ticker),
                'description': data.get('description', None),
                'sector': data.get('sector', None),
                'industry': data.get('industry', None),
                'website': data.get('website', None),
                'source': self.name
            }
            
            return etf_info
            
        except Exception as e:
            print(f"Error fetching info for {ticker}: {str(e)}")
            return {'name': ticker, 'source': self.name}
    
    def fetch_quote(self, ticker):
        """
        Fetch current quote
        """
        if not self.api_key:
            return {}
        
        try:
            url = f"{self.base_url}/stock/{ticker}/quote"
            params = {'token': self.api_key}
            
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                return {}
            
            return response.json()
            
        except Exception as e:
            print(f"Error fetching quote for {ticker}: {str(e)}")
            return {}
