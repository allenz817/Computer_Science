# ETF Analytics Platform

A prototype application for analyzing ETF data with focus on data quality and reliability.

## Features

- **Multi-Source Data Fetching**: Aggregates data from multiple free sources (yfinance, Alpha Vantage, FRED)
- **Data Quality Validation**: Cross-validates prices and detects anomalies
- **ETF-Specific Metrics**: Tracking error, expense ratios, holdings analysis
- **Portfolio Analytics**: Risk metrics, correlation analysis, efficient frontier
- **Quality Scoring**: Assigns reliability scores based on data completeness and consistency

## Data Sources

1. **Alpha Vantage** (primary) - Historical prices, fundamentals
2. **IEX Cloud** (secondary) - Validation, current quotes  
3. **FRED** - Risk-free rates and benchmark indices

## Installation

```bash
pip install -r requirements.txt
```

**Get Free API Keys:**
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key (required)
- **IEX Cloud**: https://iexcloud.io/console/ (optional, 50k messages/month free)

Add keys to [config.py](config.py):
```python
ALPHA_VANTAGE_API_KEY = "your_key_here"
IEX_CLOUD_API_KEY = "your_key_here"  # optional
```

## Quick Start

```python
from etf_app import ETFAnalyzer

# Initialize analyzer
analyzer = ETFAnalyzer()

# Analyze single ETF
etf_data = analyzer.analyze_etf('SPY', start_date='2020-01-01')

# Compare multiple ETFs
comparison = analyzer.compare_etfs(['SPY', 'QQQ', 'IWM'], start_date='2020-01-01')

# Portfolio optimization
optimal_weights = analyzer.optimize_portfolio(['SPY', 'AGG', 'GLD'])
```

## Project Structure

```
ETF_Analytics/
├── data_fetchers/      # Data collection from various sources
├─**API Rate Limits**: Alpha Vantage free tier = 25 calls/day (500 for premium)
- **Data History**: Free tiers may have limited historical data
- **Holdings Data**: Requires manual SEC filing downloads (not yet implemented) risk analysis
├── utils/              # Helper functions
├── etf_app.py          # Main application
└── example.py          # Usage examples
```

## Current Limitations

- Free tier API rate limits (Alpha Vantage: 25/day)
- yfinance is unofficial and may break
- Holdings data requires manual SEC filing downloads
