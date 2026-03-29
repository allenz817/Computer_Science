"""
Configuration settings for ETF Analytics application
"""

# API Keys (set these as environment variables or update here)
ALPHA_VANTAGE_API_KEY = "demo"  # Get free key at alphavantage.co
IEX_CLOUD_API_KEY = None  # Get free key at iexcloud.io (50k messages/month free)

# Data Source Configuration
DATA_SOURCES = {
    'alpha_vantage': {
        'enabled': True,
        'priority': 1,  # Primary source
        'rate_limit': 25  # calls per day (500 for premium)
    },
    'iex_cloud': {
        'enabled': True,
        'priority': 2,  # Secondary/validation source
        'rate_limit': None  # 50k messages/month free tier
    },
    'fred': {
        'enabled': True,
        'priority': 1,  # For benchmarks and risk-free rates
        'rate_limit': None
    }
}

# Data Quality Thresholds
QUALITY_THRESHOLDS = {
    'min_data_points': 20,  # Minimum trading days required
    'max_missing_pct': 0.05,  # Maximum 5% missing data
    'price_change_threshold': 0.25,  # Flag >25% daily changes
    'volume_spike_threshold': 5.0,  # Flag 5x average volume
    'correlation_threshold': 0.95  # Min correlation between sources
}

# Analysis Parameters
RISK_FREE_RATE = 0.03  # 3% annual
TRADING_DAYS_PER_YEAR = 252
MONTHS_PER_YEAR = 12

# Cache Settings
CACHE_DIRECTORY = './data_cache'
CACHE_EXPIRY_DAYS = 1  # Refresh cache daily
