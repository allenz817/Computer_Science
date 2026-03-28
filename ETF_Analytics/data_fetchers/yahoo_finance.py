"""
Yahoo Finance data fetcher using yfinance library
"""
import yfinance as yf
import pandas as pd
from datetime import datetime
from .base import DataFetcher, clean_price_data


class YahooFinanceFetcher(DataFetcher):
    """Fetches data from Yahoo Finance"""
    
    def __init__(self):
        super().__init__(name="Yahoo Finance", rate_limit=None)
    
    def fetch_prices(self, ticker, start_date, end_date=None):
        """
        Fetch historical price data
        
        Parameters:
        -----------
        ticker : str
            ETF ticker symbol
        start_date : str or datetime
            Start date for data
        end_date : str or datetime, optional
            End date for data (defaults to today)
        
        Returns:
        --------
        pd.DataFrame with OHLCV data
        """
        try:
            if end_date is None:
                end_date = datetime.now()
            
            # Download data
            data = yf.download(ticker, start=start_date, end=end_date, 
                             progress=False, auto_adjust=False)
            
            if data.empty:
                raise ValueError(f"No data returned for {ticker}")
            
            # Standardize column names
            data.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            
            # Clean the data
            data = clean_price_data(data)
            
            return data
            
        except Exception as e:
            print(f"Error fetching {ticker} from Yahoo Finance: {str(e)}")
            return pd.DataFrame()
    
    def fetch_info(self, ticker):
        """
        Fetch ETF metadata and information
        
        Returns:
        --------
        dict with ETF information
        """
        try:
            etf = yf.Ticker(ticker)
            info = etf.info
            
            # Extract relevant ETF information
            etf_info = {
                'name': info.get('longName', ticker),
                'category': info.get('category', 'Unknown'),
                'expense_ratio': info.get('annualReportExpenseRatio', None),
                'aum': info.get('totalAssets', None),
                'inception_date': info.get('fundInceptionDate', None),
                'ytd_return': info.get('ytdReturn', None),
                'beta': info.get('beta3Year', None),
                'holdings_count': info.get('holdings', None),
                'top_holdings': self._get_top_holdings(etf),
                'source': self.name
            }
            
            return etf_info
            
        except Exception as e:
            print(f"Error fetching info for {ticker}: {str(e)}")
            return {'name': ticker, 'source': self.name}
    
    def _get_top_holdings(self, ticker_obj, top_n=10):
        """Extract top N holdings if available"""
        try:
            holdings = ticker_obj.get_holdings()
            if holdings is not None and not holdings.empty:
                return holdings.head(top_n).to_dict('records')
        except:
            pass
        return None
    
    def fetch_dividends(self, ticker, start_date=None):
        """Fetch dividend history"""
        try:
            etf = yf.Ticker(ticker)
            dividends = etf.dividends
            
            if start_date:
                dividends = dividends[dividends.index >= start_date]
            
            return dividends
            
        except Exception as e:
            print(f"Error fetching dividends for {ticker}: {str(e)}")
            return pd.Series()
