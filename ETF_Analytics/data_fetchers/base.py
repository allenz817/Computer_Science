"""
Base data fetcher class and common utilities
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import time


class DataFetcher(ABC):
    """Abstract base class for data fetchers"""
    
    def __init__(self, name, rate_limit=None):
        self.name = name
        self.rate_limit = rate_limit
        self.last_call_time = None
        
    def _enforce_rate_limit(self):
        """Enforce rate limiting between API calls"""
        if self.rate_limit and self.last_call_time:
            time_since_last = time.time() - self.last_call_time
            min_interval = 3600 / self.rate_limit  # seconds per call
            if time_since_last < min_interval:
                time.sleep(min_interval - time_since_last)
        self.last_call_time = time.time()
    
    @abstractmethod
    def fetch_prices(self, ticker, start_date, end_date):
        """Fetch price data for a ticker"""
        pass
    
    @abstractmethod
    def fetch_info(self, ticker):
        """Fetch ETF information and metadata"""
        pass


def clean_price_data(df):
    """Standardize price data format"""
    # Ensure datetime index
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    
    # Sort by date
    df = df.sort_index()
    
    # Remove duplicates
    df = df[~df.index.duplicated(keep='first')]
    
    # Forward fill missing values (max 5 days)
    df = df.fillna(method='ffill', limit=5)
    
    return df


def validate_price_data(df):
    """Basic validation of price data"""
    issues = []
    
    # Check for negative prices
    if (df[['Open', 'High', 'Low', 'Close']] < 0).any().any():
        issues.append("Negative prices detected")
    
    # Check for zero volume
    if (df['Volume'] == 0).sum() > len(df) * 0.1:  # More than 10%
        issues.append("Excessive zero volume days")
    
    # Check OHLC consistency
    if ((df['High'] < df['Low']) | 
        (df['Close'] > df['High']) | 
        (df['Close'] < df['Low'])).any():
        issues.append("OHLC inconsistency detected")
    
    return issues
