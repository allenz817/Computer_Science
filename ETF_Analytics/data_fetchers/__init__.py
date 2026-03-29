"""
Data fetchers package - aggregates multiple data sources
"""
from .base import DataFetcher, clean_price_data, validate_price_data
from .alpha_vantage import AlphaVantageFetcher
from .iex_cloud import IEXCloudFetcher
from .fred import FREDFetcher

__all__ = [
    'DataFetcher',
    'AlphaVantageFetcher',
    'IEXCloudFetcher',
    'FREDFetcher',
    'clean_price_data',
    'validate_price_data'
]
